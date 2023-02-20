from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'kappaq',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='who_scored_player_summary_scrap-dag',
    default_args=args,
    schedule_interval='@daily'
)

the_analyst_scrap = BashOperator(task_id="who_scored_player_summary_scrap",
                                 bash_command='python /opt/airflow/dags/script/who_scored_player_summary_scrap.py',
                                 dag=dag)
