from enum import IntEnum
from typing import Union

from .base import InnotescusServiceBase
from .._grpc.ApiCommon_pb2 import ResponseStatus, FAILED
from .._grpc.ApiService_pb2 import ANNOTATION, DATASET_ITEM, SaveMetadataDefinitionRequest, SaveMetadataDefinitionResponse


class MetadataType(IntEnum):
    annotation = ANNOTATION
    dataset_item = DATASET_ITEM


class AnnotationService(InnotescusServiceBase):

    def save_metadata_definition(self, task_id: str, type: MetadataType,
                                 definition_json: Union[dict, str]) -> SaveMetadataDefinitionResponse:
        stub = self._connect_to_server()
        message = SaveMetadataDefinitionRequest(
            task_id=task_id,
            type=type,
            definition_json=definition_json
        )
        response = stub.SaveMetadataDefinition.with_call(message)
        if all([response, (hasattr(response, '__getitem__') and len(response)), ]):
            return response[0]
        return SaveMetadataDefinitionResponse(status=ResponseStatus(code=FAILED))
