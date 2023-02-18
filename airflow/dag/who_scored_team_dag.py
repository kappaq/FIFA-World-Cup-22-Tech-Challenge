from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='who_scored_team-dag',
    default_args=args,
    schedule_interval='@daily'
)

who_scored_team_scrap = BashOperator(task_id="who_scored_team_scrap", 
    bash_command='python /opt/airflow/dags/script/who_scored_team_scrap.py', 
    dag=dag)