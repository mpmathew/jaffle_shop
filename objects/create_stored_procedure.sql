USE SCHEMA TEST_DEV_DB.TEST_SCHEMA;

CREATE OR REPLACE PROCEDURE myproc(from_table string, to_table string, count int)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.8'
  packages = ('snowflake-snowpark-python')
  HANDLER = 'run'
as
$$
def run(session, from_table, to_table, count):
  session.table(from_table).limit(count).write.save_as_table(to_table)
  return "SUCCESS"
$$;

CALL myproc('my_table', 'table_b', 1);
