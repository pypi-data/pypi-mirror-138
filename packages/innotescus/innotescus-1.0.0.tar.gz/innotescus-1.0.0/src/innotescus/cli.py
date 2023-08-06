from argparse import ArgumentParser
from sys import stdout

from google.protobuf.json_format import MessageToJson

from innotescus import client_factory, TaskType, DataType, AnnotationFormat, StorageType


def main(*args, **kwargs):
    parser = _build_argparser()
    all_args = parser.parse_args()
    client = client_factory()
    resp = getattr(client, all_args.command)(
        **{k: v for k, v in vars(all_args).items() if k != 'command'}
    )
    json_obj = MessageToJson(resp)
    stdout.write(json_obj)


def _build_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title='command', dest='command')

    hello_world_command = subparsers.add_parser('hello_world', help='Verify your connection to the server')

    get_projects_command = subparsers.add_parser('get_projects', help='Returns a list of projects')

    get_projects_by_name_command = subparsers.add_parser('get_projects_by_name')
    get_projects_by_name_command.add_argument('--project-name', dest='project_name')

    create_project_command = subparsers.add_parser('create_project')
    create_project_command.add_argument('--project-name', dest='project_name')

    create_task_command = subparsers.add_parser('create_task')
    create_task_command.add_argument('--project-name', dest='project_name')
    create_task_command.add_argument('--task-name', dest='task_name')
    create_task_command.add_argument('--task-type', dest='task_type', type=lambda val: TaskType[val])
    create_task_command.add_argument('--data-type', dest='data_type', type=lambda val: DataType[val])
    create_task_command.add_argument('--classes', dest='classes', action='append')
    create_task_command.add_argument('--datasets', dest='datasets', action='append')
    create_task_command.add_argument('--task-description', dest='task_description')
    create_task_command.add_argument('--instructions', dest='instructions')  # noop??
    create_task_command.add_argument(
        '--can-annotator-add-classes',
        dest='can_annotator_add_classes',
        type=lambda val: val.lower() in ('t', '1', 'y', 'yes', 'true', )
    )

    assign_task_to_datasets = subparsers.add_parser('assign_task_to_datasets')
    assign_task_to_datasets.add_argument('--project-name', dest='project_name')
    assign_task_to_datasets.add_argument('--assignments', dest='assignments', action='append') # todo: verify this data type.. mapping of dataset <-> tasks?

    upload_data_command = subparsers.add_parser('upload_data')
    upload_data_command.add_argument('--project-name', dest='project_name')
    upload_data_command.add_argument('--dataset-name', dest='dataset_name')
    upload_data_command.add_argument('--file-path', dest='file_paths', action='append')
    upload_data_command.add_argument('--data-type', dest='data_type', type=lambda val: DataType[val])
    upload_data_command.add_argument('--storage-type', dest='storage_type', type=lambda val: StorageType[val])

    upload_annotations_command = subparsers.add_parser('upload_annotations')
    upload_annotations_command.add_argument('--project-name', dest='project_name')
    upload_annotations_command.add_argument('--dataset-name', dest='dataset_name')
    upload_annotations_command.add_argument('--task-type', dest='task_type', type=lambda val: TaskType[val])
    upload_annotations_command.add_argument('--data-type', dest='data_type', type=lambda val: DataType[val])
    upload_annotations_command.add_argument(
        '--annotation-format',
        dest='annotation_format',
        type=lambda val: AnnotationFormat[val]
    )
    upload_annotations_command.add_argument('--file-path', action='append', dest='file_paths')
    upload_annotations_command.add_argument('--task-name', dest='task_name')
    upload_annotations_command.add_argument('--task-description', dest='task_description')
    upload_annotations_command.add_argument(
        '--overwrite-existing-annotations',
        dest='overwrite_existing_annotations',
        default=False,
        type=lambda val: val.lower() in ('t', '1', 'y', 'yes', 'true', )
    )

    export_command = subparsers.add_parser('export')
    export_command.add_argument('--export-name', dest='export_name')
    export_command.add_argument('--project-name', dest='project_name')
    export_command.add_argument('--annotation-format', dest='annotation_format')
    export_command.add_argument('--export-types', dest='export_types')
    export_command.add_argument('--dataset-names', dest='dataset_names')
    export_command.add_argument('--task-name', dest='task_name')

    download_export_command = subparsers.add_parser('download_export')
    download_export_command.add_argument('--export-name', dest='export_name')
    download_export_command.add_argument('--project-name', dest='project_name')

    get_in_progress_jobs_command = subparsers.add_parser('get_in_progress_jobs')

    get_job_status_command = subparsers.add_parser('get_job_status')
    get_job_status_command.add_argument('--job-id', dest='job_id')

    delete_project_command = subparsers.add_parser('delete_project')
    delete_project_command.add_argument('--project-name', dest='project_name')

    delete_dataset_command = subparsers.add_parser('delete_dataset')
    delete_dataset_command.add_argument('--project-name', dest='project_name', required=True)
    delete_dataset_command.add_argument('--dataset-name', dest='dataset_name', required=True)

    delete_task_command = subparsers.add_parser('delete_task')
    delete_task_command.add_argument('--project-name', dest='project_name', required=True)
    delete_task_command.add_argument('--task-name', dest='task_name', required=True)

    return parser


if __name__ == '__main__':
    main()
