"""Abstract interface to Labeling APIs."""
from typing import Optional, Dict

from redbrick_slicer.common.client import RBClient
from redbrick_slicer.common.labeling import LabelingControllerInterface


class LabelingRepo(LabelingControllerInterface):
    """Implementation of manual labeling apis."""

    def __init__(self, client: RBClient) -> None:
        """Construct ExportRepo."""
        self.client = client

    def presign_labels_path(
        self,
        org_id: str,
        project_id: str,
        task_id: str,
        file_type: str,
    ) -> Dict:
        """Presign labels path."""
        query = """
        query slicer_presignLabelsPath(
            $orgId: UUID!
            $projectId: UUID!
            $taskId: UUID!
            $fileType: String!
        ) {
            presignLabelsPath(
                orgId: $orgId
                projectId: $projectId
                taskId: $taskId
                fileType: $fileType
            ) {
                fileName
                filePath
                presignedUrl
            }
        }
        """
        variables = {
            "orgId": org_id,
            "projectId": project_id,
            "taskId": task_id,
            "fileType": file_type,
        }
        response = self.client.execute_query(query, variables)
        presigned: Dict = response["presignLabelsPath"]
        return presigned

    def put_labeling_results(
        self,
        org_id: str,
        project_id: str,
        stage_name: str,
        task_id: str,
        labels_data: str,
        labels_path: Optional[str] = None,
        finished: bool = True,
    ) -> None:
        """Put Labeling results."""
        query = """
        mutation slicer_putManualLabelingTaskAndLabels(
            $orgId: UUID!
            $projectId: UUID!
            $stageName: String!
            $taskId: UUID!
            $elapsedTimeMs: Int!
            $finished: Boolean!
            $labelsData: String
            $labelsPath: String
        ) {
            putManualLabelingTaskAndLabels(
                orgId: $orgId
                projectId: $projectId
                stageName: $stageName
                taskId: $taskId
                elapsedTimeMs: $elapsedTimeMs
                finished: $finished
                labelsData: $labelsData
                labelsPath: $labelsPath
            ) {
                ok
            }
        }
        """

        variables = {
            "orgId": org_id,
            "projectId": project_id,
            "stageName": stage_name,
            "taskId": task_id,
            "labelsData": labels_data,
            "labelsPath": labels_path,
            "finished": finished,
            "elapsedTimeMs": 0,
        }
        self.client.execute_query(query, variables)

    def assign_task(
        self, org_id: str, project_id: str, stage_name: str, task_id: str, user_id: str
    ) -> None:
        """Assign task to specified user."""
        query = """
        mutation slicer_assignTask(
            $orgId: UUID!,
            $projectId: UUID!,
            $stageName: String!,
            $taskId: UUID!,
            $userId: UUID!
        ){
            assignTask(
                orgId: $orgId
                projectId: $projectId
                stageName: $stageName
                taskId: $taskId
                userId: $userId
            ) {
                task {
                    taskId
                }
            }
        }
        """

        # EXECUTE THE QUERY
        variables = {
            "orgId": org_id,
            "projectId": project_id,
            "stageName": stage_name,
            "taskId": task_id,
            "userId": user_id,
        }

        self.client.execute_query(query, variables)
