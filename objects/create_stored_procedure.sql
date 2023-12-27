USE {{ params.schema_name }};

CREATE OR REPLACE PROCEDURE myproc()
  RETURNS STRING
  LANGUAGE JAVASCRIPT
  EXECUTE AS CALLER
  AS '
  return "Hello from the snowflake stored procedure!";
  ';

CALL myproc();
