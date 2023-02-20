from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='preffered_formation-dag',
    default_args=args,
    schedule_interval='@daily'
)

preffered_formation = BashOperator(task_id="preffered_formation", 
    bash_command='python /opt/airflow/dags/script/preffered_formation.py', 
    dag=dag)