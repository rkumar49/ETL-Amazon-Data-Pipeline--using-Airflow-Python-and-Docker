from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin

# Initialize logging
log = LoggingMixin().log

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 3,  # Retry tasks up to 3 times
    'retry_delay': 300,  # Retry after 5 minutes
}

# Define the DAG
with DAG(
    'simple_postgres_dag',
    default_args=default_args,
    description='A simple DAG to create a table and insert data into Postgres',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task to create the table if it doesn't exist
    create_table_task = PostgresOperator(
        task_id='create_table',
        sql="""
            CREATE TABLE IF NOT EXISTS airflow_data (
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                city TEXT NOT NULL
            );
        """,
        postgres_conn_id='Amazon_Books_Connection',
        autocommit=True,
    )

    # Task to insert data into the table
    insert_data_task = PostgresOperator(
        task_id='insert_data',
        sql="""
            INSERT INTO airflow_data (name, age, city)
            VALUES ('John Doe', 30, 'New York'),
                   ('Jane Smith', 25, 'San Francisco'),
                   ('Alice Johnson', 28, 'Chicago');
        """,
        postgres_conn_id='Amazon_Books_Connection',
        autocommit=True,
    )

    # Log task status for debugging
    create_table_task.log.info("Create table task initialized.")
    insert_data_task.log.info("Insert data task initialized.")

    # Set task dependencies
    create_table_task >> insert_data_task
