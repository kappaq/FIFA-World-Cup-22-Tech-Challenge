from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='flashscore-dag',
    default_args=args,
    schedule_interval='@daily'
)

flashscore_scrap = BashOperator(task_id="flashscore_scrap", 
    bash_command='python /opt/airflow/dags/script/flashscore_scrap.py', 
    dag=dag)