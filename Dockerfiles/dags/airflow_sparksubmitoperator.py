from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

spark_master = "spark://spark-master:7077"
spark_app_name = "spark_submit_operator"
file_path = "/opt/bitnami/airflow/airflow.cfg"

now = datetime.now()

default_args = {
    "owner": "javas",
    "start_date": datetime(2021, 7, 27)
}

dag = DAG(
    dag_id = "spark_submit_operator",
    description = "spark_submit_operator_description",
    default_args = default_args,
    schedule_interval = '*/1 * * * *',
    catchup = False)

start = DummyOperator(
    task_id = "spark_submit_operator_start",
    dag = dag)

spark_job = SparkSubmitOperator(
    task_id = "spark_submit_operator_sparkjob",
    application = "/spark/streamingspark.py",
    name = "spark_submit_operator",
    conn_id = "spark_default",
    packages = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2",
    files = "/spark/metrics.properties",
    conf = {"spark.metrics.conf" : "/spark/metrics.properties"}
)

end = DummyOperator(
    task_id = "spark_submit_operator_end",
    dag = dag)

start >> spark_job >> end