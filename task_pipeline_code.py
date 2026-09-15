# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0
%restart_python

from databricks.sdk.service.jobs import JobSettings as Job


New_Job_2026_09_03_14_39_28 = Job.from_dict(
    {
        "name": "New Job 2026-09-03 14:39:28",
        "tasks": [
            {
                "task_key": "fetch_table_names",
                "notebook_task": {
                    "notebook_path": "/Workspace/05_job/02_job_notebook/01_Fetch_List_of_Tables",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Ingestion_data",
                "depends_on": [
                    {
                        "task_key": "fetch_table_names",
                    },
                ],
                "for_each_task": {
                    "inputs": "{{tasks.fetch_table_names.values.tables_list}}",
                    "concurrency": 1,
                    "task": {
                        "task_key": "Ingestion_data_iteration",
                        "notebook_task": {
                            "notebook_path": "/Workspace/jobs_demo",
                            "base_parameters": {
                                "table_name": "{{input}}",
                            },
                            "source": "WORKSPACE",
                        },
                    },
                },
            },
            {
                "task_key": "Transform",
                "depends_on": [
                    {
                        "task_key": "Ingestion_data",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/05_job/02_job_notebook/03_Transform_Data",
                    "source": "WORKSPACE",
                },
                "environment_key": "Default",
            },
            {
                "task_key": "Refresh_dashboard",
                "depends_on": [
                    {
                        "task_key": "Transform",
                    },
                ],
                "dashboard_task": {
                    "subscription": {
                    },
                    "warehouse_id": "2d218006f461f874",
                    "dashboard_id": "01f1a784d8511cab85b1ae8e39169f12",
                },
            },
        ],
        "queue": {
            "enabled": True,
        },
        "environments": [
            {
                "environment_key": "Default",
                "spec": {
                    "environment_version": "5",
                },
            },
        ],
        "performance_target": "PERFORMANCE_OPTIMIZED",
    }
)

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
w.jobs.reset(new_settings=New_Job_2026_09_03_14_39_28, job_id=749372471471313)
# or create a new job using: w.jobs.create(**New_Job_2026_09_03_14_39_28.as_shallow_dict())
