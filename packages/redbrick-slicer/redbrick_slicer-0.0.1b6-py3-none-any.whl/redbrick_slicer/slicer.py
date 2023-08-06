"""Main object for RedBrick SDK."""
import os
import json
import re
import gzip
import random
from typing import Dict, List, Tuple, no_type_check
from uuid import uuid4
import asyncio

import qt  # type: ignore
import slicer  # type: ignore
from DICOMLib import DICOMUtils  # type: ignore

from redbrick_slicer.common.context import RBContext
from redbrick_slicer.project import RBProject
from redbrick_slicer.utils.files import download_files
from redbrick_slicer.utils.url import generate_task_url, tool_url_parse


# pylint: skip-file


class RBSlicer:
    """Interact with a RedBrick task in 3D Slicer application."""

    def __init__(self, context: RBContext, url: str) -> None:
        """Construct RBProject."""
        self.context = context
        self.url = url

        self.org_id, self.project_id, self.task_id, self.stage_name = tool_url_parse(
            self.url
        )
        self.project = RBProject(self.context, self.org_id, self.project_id)

        self.segments: List[str] = []
        self.segment_color_map: Dict[str, List[int]] = {}

        self.root = os.path.join(os.path.expanduser("~"), ".redbrick-slicer")
        self.org_dir = os.path.join(self.root, str(self.org_id))
        self.project_dir = os.path.join(self.org_dir, str(self.project_id))
        self.task_dir = os.path.join(self.project_dir, str(self.task_id))

        self.data_dir = os.path.join(self.task_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)

    @staticmethod
    def _get_categories(category: Dict) -> List[str]:
        category_names = [category["name"]]
        for child in category.get("children", []):
            category_names += [
                category_names[0] + "::" + name
                for name in RBSlicer._get_categories(child)
            ]
        return category_names

    def _cat2cat(self, cat_name: str, cat_id: int, colormap: List[Dict]) -> Dict:
        for val in colormap:
            if val["trail"] and "::".join(val["trail"][1:]) == cat_name:
                self.segment_color_map[cat_name] = [
                    int(val["color"][i : i + 2], 16) for i in (1, 3, 5)
                ]
                break
        else:
            self.segment_color_map[cat_name] = [
                random.randint(0, 255) for _ in range(3)
            ]

        return {
            "recommendedDisplayRGBValue": self.segment_color_map[cat_name],
            "CodeMeaning": cat_name,
            "CodingSchemeDesignator": "SCT",
            "3dSlicerLabel": cat_name,
            "3dSlicerIntegerLabel": cat_id,
            "cid": str(cat_id),
            "UMLSConceptUID": "C0344335",
            "CodeValue": str(cat_id),
            "contextGroupName": "CommonTissueSegmentationTypes",
            "SNOMEDCTConceptID": str(cat_id),
        }

    @no_type_check
    def get_task(self) -> None:
        """Get task for labeling."""
        task, taxonomy = self.project.export.get_raw_data_single(self.task_id)

        parent_cat = taxonomy.get("categories", [])
        if len(parent_cat) == 1 and parent_cat[0]["name"] == "object":
            for child in parent_cat[0]["children"]:
                self.segments += RBSlicer._get_categories(child)

        if not self.segments:
            print("Unsupported taxonomy")
            return

        print("Available categories:", self.segments)

        slicer.mrmlScene.Clear(0)

        term_json_file = os.path.join(self.project_dir, "terminologies.json")
        term_json = {
            "SegmentationCategoryTypeContextName": taxonomy["name"],
            "@schema": "https://raw.githubusercontent.com/qiicr/dcmqi/master/doc/segment-context-schema.json#",
            "SegmentationCodes": {
                "Category": [
                    {
                        "CodeMeaning": "Categories",
                        "CodingSchemeDesignator": "SCT",
                        "showAnatomy": True,
                        "cid": "7150",
                        "CodeValue": "85756007",
                        "contextGroupName": "SegmentationPropertyCategories",
                        "Type": [
                            self._cat2cat(cat, idx + 1, taxonomy["colorMap"])
                            for idx, cat in enumerate(self.segments)
                        ],
                    }
                ],
            },
        }

        with open(term_json_file, "w", encoding="utf-8") as file_:
            json.dump(term_json, file_, indent=2)

        termLogic = slicer.util.getModuleLogic("Terminologies")
        termLogic.LoadTerminologyFromFile(term_json_file)

        taxName = re.sub(r"[^a-zA-Z]", "", taxonomy["name"])
        slicer.app.settings().setValue("Terminology/LastTerminologyContext", taxName)
        defaultCat = f"{taxName}~SCT^85756007^Categories~^^~^^~Anatomic codes - DICOM master list~^^~^^"
        slicer.app.settings().setValue(
            "Segmentations/DefaultTerminologyEntry", defaultCat
        )

        files = []
        for idx, item in enumerate(task["itemsPresigned"]):
            path = os.path.join(self.data_dir, f"{idx}.dcm")
            if not os.path.isfile(path):
                files.append((item, path))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_files(files))

        with DICOMUtils.TemporaryDICOMDatabase() as db:
            DICOMUtils.importDicom(self.data_dir, db)
            patientUIDs = db.patients()
            assert len(patientUIDs) == 1, "Failed to load data"
            DICOMUtils.loadPatientByUID(patientUIDs[0])

        if task["labelsPath"]:
            labels_path = os.path.join(self.task_dir, "labels.nii")
            if os.path.isfile(labels_path):
                os.remove(labels_path)
            loop.run_until_complete(download_files([(task["labelsPath"], labels_path)]))

            slicer.util.loadSegmentation(labels_path)
            segmentationNode = slicer.mrmlScene.GetFirstNodeByClass(
                "vtkMRMLSegmentationNode"
            )

        else:
            segmentationNode = slicer.vtkMRMLSegmentationNode()
            slicer.mrmlScene.AddNode(segmentationNode)

        slicer.util.selectModule("SegmentEditor")
        segmentationNode = slicer.mrmlScene.GetFirstNodeByClass(
            "vtkMRMLSegmentationNode"
        )

        rb_segmentation = segmentationNode.GetSegmentation()
        labels = task["labels"]
        label_rb_map = {}
        for label in labels:
            label_rb_map[label["dicom"]["instanceid"]] = "::".join(
                label["category"][0][1:]
            )

        display = segmentationNode.GetDisplayNode()
        for num in range(rb_segmentation.GetNumberOfSegments()):
            seg = rb_segmentation.GetNthSegment(num)
            display.SetSegmentVisibility(rb_segmentation.GetNthSegmentID(num), True)
            val = seg.GetLabelValue()
            if val in label_rb_map:
                seg.SetName(label_rb_map[val])
                if label_rb_map[val] in self.segment_color_map:
                    seg.SetColor(
                        tuple(
                            map(
                                lambda color: color / 255,
                                self.segment_color_map[label_rb_map[val]],
                            )
                        )
                    )

        sliceController = (
            slicer.app.layoutManager().sliceWidget("Red").sliceController()
        )
        save_btn = qt.QPushButton("Save")
        submit_btn = qt.QPushButton("Submit")
        exit_btn = qt.QPushButton("Exit")

        save_btn.clicked.connect(self.handle_save)
        submit_btn.clicked.connect(self.handle_submit)
        exit_btn.clicked.connect(self.handle_exit)

        barLayout = sliceController.barLayout()
        child = 0
        while True:
            if barLayout.itemAt(child) is None:
                break
            widget = barLayout.itemAt(child).widget()
            if isinstance(widget, qt.QPushButton) and widget.text in (
                "Save",
                "Submit",
                "Exit",
            ):
                barLayout.removeWidget(widget)
            else:
                child += 1

        barLayout.addWidget(save_btn)
        barLayout.addWidget(submit_btn)
        barLayout.addWidget(exit_btn)

    def handle_save(self) -> None:
        """Save button handler."""
        print("Saving...")
        self.save_data(False)

    def handle_submit(self) -> None:
        """Submit button handler."""
        print("Submitting...")
        self.save_data(True)
        print(generate_task_url(self.url))

    def handle_exit(self) -> None:
        """Reset button handler."""
        print("Exiting...")
        slicer.mrmlScene.Clear(0)

    @no_type_check
    def save_data(self, finished: bool) -> None:
        """Save data for task."""
        import numpy as np
        import nibabel as nb  # type: ignore

        scene = slicer.mrmlScene

        segmentationNode = scene.GetFirstNodeByClass("vtkMRMLSegmentationNode")
        rb_segmentation = segmentationNode.GetSegmentation()
        labels = []
        for num in range(rb_segmentation.GetNumberOfSegments()):
            seg = rb_segmentation.GetNthSegment(num)
            name = seg.GetName()
            if name not in self.segments:
                print(f"Category: `{name}` not found. Skipping")
                return
            labels.append(
                {
                    "category": [["object"] + name.split("::")],
                    "attributes": [],
                    "labelid": str(uuid4()),
                    "dicom": {"instanceid": seg.GetLabelValue()},
                }
            )

        segmentationNode = scene.GetFirstNodeByClass("vtkMRMLSegmentationNode")
        referenceVolumeNode = scene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
        labelmapVolumeNode = scene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")
        slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(
            segmentationNode, labelmapVolumeNode, referenceVolumeNode
        )
        new_labels = os.path.join(self.task_dir, "new_labels.nii")
        slicer.util.saveNode(labelmapVolumeNode, new_labels)
        scene.RemoveNode(labelmapVolumeNode.GetDisplayNode().GetColorNode())
        scene.RemoveNode(labelmapVolumeNode)

        img = nb.load(new_labels)
        img.set_data_dtype(np.ubyte)
        data = np.round(img.get_fdata()).astype(np.ubyte)
        means = nb.Nifti1Image(data, header=img.header, affine=img.affine)
        new_labels = os.path.join(self.task_dir, "new_labels_converted.nii")
        nb.save(means, new_labels)
        with open(new_labels, "rb") as file_:
            compressed = gzip.compress(file_.read())

        # self.project.labeling.assign_task(self.stage_name, self.task_id, self.user_id)
        task = {
            "taskId": self.task_id,
            "labelBlob": compressed,
            "draft": not finished,
            "labels": labels,
        }
        self.project.labeling.put_task(self.stage_name, task)

        if finished:
            scene.Clear(0)
