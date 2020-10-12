from airflow.exceptions import AirflowException
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import os
import subprocess
import json

#TWITTER_DIR  = os.environ.get('TWITTER_DIR')

with open('/Users/~/Desktop/projects/data_eng/geo_twitter/config/config.json') as data_file:
                data = json.load(data_file)
print(data)
#data_dict = json.loads(data)
#def auto_fail():
#	raise AirflowException('File not parsed completely/correctly')

#def print_hello():
#    return 'Hello world John!'

dag = DAG('geo_twitter', description='DAG Schedule for Geo Twitter Ingestion.',
          schedule_interval='*/30  * * * *',
          start_date=datetime(2019, 11, 16), catchup=False)

#dummy_operator = PythonOperator(task_id='dummy_task2', retries=1, dag=dag,python_callable=auto_fail )

#hello_operator = PythonOperator(task_id='hello_task2', python_callable=print_hello, dag=dag)

#dummy_operator >> hello_operator

#this_dir = subprocess.run(['echo $TWITTER_DIR'])


task_1 = BashOperator(task_id = 'raw_ingestion', bash_command = 'python {{params.TWITTER_DIR}}/twitter.py', params = data, dag = dag)

task_2 = BashOperator(task_id = 'raw_clean', bash_command = 'python {{params.TWITTER_DIR}}/tweets_clean.py',params = data,  dag = dag)

task_3 = BashOperator(task_id = 'data_load', bash_command = 'python {{params.TWITTER_DIR}}/load_files.py',params = data, dag = dag)

task_2_1 = BashOperator(task_id = 'publish_kafka', bash_command = 'python {{params.TWITTER_DIR}}/kafka_publish.py', params = data, dag = dag)

#task_2_1.set_upstream(task_1)
#task_1 >> task_2_1
#task_1 >> task_2 >> task_3

task_1 >> task_2 >> task_3
task_2 >> task_2_1
