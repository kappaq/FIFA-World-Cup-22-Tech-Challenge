from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='wikipedia-dag',
    default_args=args,
    schedule_interval='@daily'
)

wikipedia_scrap = BashOperator(task_id="wikipedia_scrap", 
    bash_command='python /opt/airflow/dags/script/wikipedia_scrap.py', 
    dag=dag)