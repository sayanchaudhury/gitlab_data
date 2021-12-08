import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow_utils import (
    DATA_IMAGE,
    clone_and_setup_extraction_cmd,
    gitlab_defaults,
    slack_failed_task,
)
from kube_secrets import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_LOAD_DATABASE,
    SNOWFLAKE_LOAD_PASSWORD,
    SNOWFLAKE_LOAD_ROLE,
    SNOWFLAKE_LOAD_USER,
    SNOWFLAKE_LOAD_WAREHOUSE,
    GITLAB_ANALYTICS_PRIVATE_TOKEN,
    GITLAB_COM_API_TOKEN,
)
from kubernetes_helpers import get_affinity, get_toleration

# Load the env vars into a dict and set Secrets
env = os.environ.copy()
pod_env_vars = {"CI_PROJECT_DIR": "/analytics"}

# Default arguments for the DAG
default_args = {
    "catchup": False,
    "depends_on_past": False,
    "on_failure_callback": slack_failed_task,
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "sla": timedelta(hours=12),
    "sla_miss_callback": slack_failed_task,
    "start_date": datetime(2019, 1, 1),
    "dagrun_timeout": timedelta(hours=2),
}

# Create the DAG
dag = DAG(
    "gitlab_data_yaml_extract",
    default_args=default_args,
    schedule_interval="0 */8 * * *",
)

# YAML Extract
data_yaml_extract_cmd = f"""
    {clone_and_setup_extraction_cmd} &&
    python gitlab_data_yaml/upload.py &&
    python gitlab_feature_flags_yaml/upload.py &&
    python gitlab_flaky_tests/upload.py
"""
data_yaml_extract = KubernetesPodOperator(
    **gitlab_defaults,
    image="registry.gitlab.com/gitlab-data/data-image/data-image:v0.0.13",
    task_id="data-yaml-extract",
    name="data-yaml-extract",
    secrets=[
        SNOWFLAKE_ACCOUNT,
        SNOWFLAKE_LOAD_DATABASE,
        SNOWFLAKE_LOAD_ROLE,
        SNOWFLAKE_LOAD_USER,
        SNOWFLAKE_LOAD_WAREHOUSE,
        SNOWFLAKE_LOAD_PASSWORD,
        GITLAB_ANALYTICS_PRIVATE_TOKEN,
        GITLAB_COM_API_TOKEN,
    ],
    affinity=get_affinity(False),
    tolerations=get_toleration(False),
    env_vars=pod_env_vars,
    arguments=[data_yaml_extract_cmd],
    dag=dag,
)
