from typing import Iterable
from enum import IntEnum

from .._grpc.ApiCommon_pb2 import ResponseStatus, FAILED
from .._grpc.ApiService_pb2 import InviteMemberToOrganizationRequest, InviteMemberToOrganizationResponse, \
    ORGANIZATION_MEMBER_ROLE_UNSPECIFIED, ORGANIZATION_MEMBER_ROLE_ANNOTATOR, ORGANIZATION_MEMBER_ROLE_ADMIN, \
    ORGANIZATION_MEMBER_ROLE_OWNER, ORGANIZATION_MEMBER_ROLE_SUPERVISOR, InviteMembersToProjectRequest, \
    InviteMembersToProjectResponse, UserProjectInvitation, GetProjectsRequest, GetProjectsResponse
from innotescus.services.base import InnotescusServiceBase


class MemberRole(IntEnum):
    unspecified = ORGANIZATION_MEMBER_ROLE_UNSPECIFIED
    annotator = ORGANIZATION_MEMBER_ROLE_ANNOTATOR
    admin = ORGANIZATION_MEMBER_ROLE_ADMIN
    owner = ORGANIZATION_MEMBER_ROLE_OWNER
    supervisor = ORGANIZATION_MEMBER_ROLE_SUPERVISOR


class MembershipService(InnotescusServiceBase):

    def invite_member(self, *, user_email: str, role: MemberRole,
                      project_names: Iterable[str] = None) -> Iterable[InviteMemberToOrganizationResponse]:
        stub = self._connect_to_server()

        message = InviteMemberToOrganizationRequest(
            user_email=user_email,
            role=role,
            project_ids=None if not project_names else [self._get_project_id_from_name(n) for n in project_names]
        )
        response = stub.InviteMemberToOrganization.with_call(message)
        if all([response, (hasattr(response, '__getitem__') and len(response)), ]):
            return response[0]
        return InviteMemberToOrganizationResponse(status=ResponseStatus(code=FAILED))

    def add_to_project(self, *, user_emails: Iterable[str], project_name: str) -> InviteMembersToProjectResponse:
        stub = self._connect_to_server()
        message = InviteMembersToProjectRequest(
            project_id=self._get_project_id_from_name(project_name),
            invitations=[UserProjectInvitation(user_email=ue) for ue in user_emails]
        )
        response = stub.InviteMembersToProject.with_call(message)
        if all([response, (hasattr(response, '__getitem__') and len(response)), ]):
            return response[0]
        return InviteMembersToProjectResponse(status=ResponseStatus(code=FAILED))

    def _get_project_id_from_name(self, project_name: str) -> str:
        stub = self._connect_to_server()
        message = GetProjectsRequest(project_name=project_name)
        response = stub.GetProjects.with_call(message)
        if (response is not None and
                response[0] is not None and
                response[0].projects is not None and
                response[0].projects[0] is not None):
            return response[0].projects[0].name
        raise Exception('Failed to retrieve the project ID')
