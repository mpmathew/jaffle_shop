from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.hooks.base import BaseHook
from airflow.utils.dates import days_ago
from airflow.models import Variable
import os
import yaml

# Set base directory and parent directory paths
base_directory_path = os.path.dirname(os.path.abspath(__file__))
parent_directory_path = os.path.dirname(base_directory_path)
parent_dir_name = os.path.basename(os.path.dirname(base_directory_path))
directory_name = os.path.basename(base_directory_path)
dynamic_dag_id = f"{parent_dir_name}_{directory_name}"

# Load configuration from YAML file
yml_file_path = os.path.join(parent_directory_path, 'snowflake_ci.yml')
with open(yml_file_path, 'r') as file:
    config = yaml.safe_load(file)

# # Extract configuration variables
# SNOWFLAKE_CONN_ID = config.get('SNOWFLAKE_CONN_ID', 'DEFAULT_CONNECTION')

# # Fetch Snowflake schema from the connection and folder
# extras = BaseHook.get_connection(SNOWFLAKE_CONN_ID).extra_dejson
# SNOWFLAKE_SCHEMA = extras['database'] + "." + directory_name

OWNER = config.get('OWNER', 'DEFAULT_OWNER')
TAGS = config.get('TAGS', [])

# Add owner to tags
TAGS.append(OWNER)

# Set default arguments for the DAG
default_args = {
    "owner": OWNER,
    # "snowflake_conn_id": SNOWFLAKE_CONN_ID,
}

# # Read the content of README.md
# readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
# with open(readme_path, 'r') as file:
#     readme_content = file.read()

# Initialize the DAG
dag = DAG(
    dynamic_dag_id,
    default_args=default_args,
    description='Run SQL files in Snowflake, organized by subdirectories',
    schedule_interval=None,
    template_searchpath=base_directory_path,
    start_date=days_ago(1),
    tags=TAGS,
    # doc_md=readme_content,
)

# Define target subdirectories
target_subdirs = [
    'file_formats', 
    'stages', 
    'tables',
    'views',
    'sequences',
    'streams', 
    'functions', 
    'procedures',
    'tasks',
    'test',
    'dml'
]

obj_yml_file_path = os.path.join(base_directory_path, 'objects.yml')
if os.path.exists(obj_yml_file_path):
    with open(obj_yml_file_path, 'r') as file:
        object_dirs = yaml.safe_load(file)
        if 'OBJECTS' in object_dirs and object_dirs['OBJECTS']:
            target_subdirs = object_dirs['OBJECTS']


# Create task groups and tasks
task_groups = {}
prev_group = None

for subdir_name in target_subdirs:
    subdir_path = os.path.join(base_directory_path, subdir_name)
    
    if not os.path.isdir(subdir_path):
        continue
    
    # Check if there are any .sql files in the subdirectory
    sql_files = [file for file in sorted(os.listdir(subdir_path)) if file.endswith('.sql')]
    
    if not sql_files:
        continue
    
    with TaskGroup(group_id=subdir_name.replace("/","_"), dag=dag) as tg:
        prev_task = None
        
        for file in sql_files:
            file_path = os.path.join(subdir_path, file)
            task_id = f"{file.replace('.sql', '')}"
            
            with open(file_path, 'r') as f:
                sql_query = f.read()

                # Inject schema name into the SQL query if not already present
                if "USE" not in sql_query.upper():
                    sql_query = f"USE {SNOWFLAKE_SCHEMA};\n" + sql_query
                
                task = SnowflakeOperator(
                    task_id=task_id,
                    sql=sql_query,
                    # snowflake_conn_id=SNOWFLAKE_CONN_ID,
                    # params={"schema_name": SNOWFLAKE_SCHEMA},
                    dag=dag,
                )
            
                if prev_task:
                    prev_task >> task 
            
                prev_task = task
        
        task_groups[subdir_name.replace("/","_")] = tg
        
        if prev_group:
            prev_group >> tg
        
        prev_group = tg
#test5
