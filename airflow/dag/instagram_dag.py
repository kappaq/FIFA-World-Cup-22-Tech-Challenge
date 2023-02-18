from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='instagram-dag',
    default_args=args,
    schedule_interval='@daily'
)

instagram_scrap = BashOperator(task_id="instagram_scrap", 
    bash_command='python /opt/airflow/dags/script/pandas_instagram_scrap.py', 
    dag=dag)