from typing import List, Optional

from .._grpc.ApiCommon_pb2 import ResponseStatus, FAILED
from .._grpc.ApiService_pb2 import CreateTaskReviewRequest, CreateTaskReviewResponse, TaskReview
from ..datatypes import DateRange
from ..helpers import to_grpc
from .base import InnotescusServiceBase


class TaskReviewService(InnotescusServiceBase):

    def create_task_review(self, *,
                           task_id: str,
                           name: str,
                           reviewer_emails: List[str],
                           percent=1.0,
                           class_names: Optional[List[str]] = None,
                           annotator_emails: Optional[List[str]] = None,
                           date_range: Optional[DateRange] = None,
                           dataset_names: Optional[List[str]] = None) -> CreateTaskReviewResponse:
        """ Creates a new Task Review.

        :param `str` task_id: ID of the task to be reviewed.
        :param `str` name: A human-readable name for the review.
        :param `List[str]` reviewer_ids: A list of user ids, who will be responsible for the review.
        :param `float` percent: Percent of dataset items to review.  Defaults to 1.0 (100%)
        :param `Optional[TimestampRange]` date_range:
        :param `Optional[List[str]]` class_ids: Optional list of Class IDs to include in the review.
            If not provided, all classes will be included.
        :param `Optional[List[str]]` annotator_ids: Optional list of Annotator IDs to include in the review.
            If not provided, work from all annotators will be included.
        :param `Optional[List[str]]` dataset_ids: Optional list of dataset ids to be included in the review.
            If not provided, all datasets will be included.
        """

        stub = self._connect_to_server()
        message = CreateTaskReviewRequest(
            task_review=TaskReview(
                index=0,
                task_id=task_id,
                date_range=to_grpc(date_range) if date_range else None,
                reviewer_ids=reviewer_emails,
                name=name,
                percent=percent,
                class_ids=class_names,
                annotator_ids=annotator_emails,
                dataset_ids=dataset_names,
                is_enabled=True
            )
        )
        response = stub.CreateTaskReview.with_call(message)
        if all([response, (hasattr(response, '__getitem__') and len(response)), ]):
            return response[0]
        return CreateTaskReviewResponse(status=ResponseStatus(code=FAILED))

    def add_review_step(self, *, task_review: TaskReview, reviewer_emails: List[str],
                        percent: float = 1.0) -> CreateTaskReviewResponse:
        """ Adds a new step to the current review.

        :param `TaskReview` task_review: the review that this step should be added to.
        :param `List[str]` reviewer_ids: A list of user ids, who will be responsible for this step.
        :param `float` percent: Percent of dataset items to review.  Defaults to 1.0 (100%)
        """
        stub = self._connect_to_server()
        message = CreateTaskReviewRequest(
            task_review=TaskReview(
                id=task_review.id,
                index=-1,  # set this to an invalid value, and let the API service determine what this should be.
                task_id=task_review.task_id,
                date_range=task_review.date_range,
                class_ids=task_review.class_ids,
                annotator_ids=task_review.annotator_ids,
                dataset_ids=task_review.dataset_ids,
                reviewer_ids=reviewer_emails,
                percent=percent,
                is_enabled=True
            )
        )
        response = stub.CreateTaskReview.with_call(message)
        if all([response, (hasattr(response, '__getitem__') and len(response)), ]):
            return response[0]
        return CreateTaskReviewResponse(status=ResponseStatus(code=FAILED))
