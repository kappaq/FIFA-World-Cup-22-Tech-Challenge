from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='ranking-dag',
    default_args=args,
    schedule_interval='@daily'
)

ranking = BashOperator(task_id="ranking",
                                     bash_command='python /opt/airflow/dags/script/ranking_scrap.py',
                                     dag=dag)
