{% macro log_variable() %}
 {% do log('DBT_ESG_DB: ' ~ env_var(DBT_ESG_DB), info=True) %}
{% endmacro %}
