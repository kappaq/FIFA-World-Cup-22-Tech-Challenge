from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='the_analyst-dag',
    default_args=args,
    schedule_interval='@daily'
)

the_analyst_scrap = BashOperator(task_id="the_analyst_scrap", 
    bash_command='python /opt/airflow/dags/script/the_analyst_scrap.py', 
    dag=dag)