{% macro log_env_variable(env_var_name) %}
  {% set env_var_value = env_var(env_var_name) %}
  {{ log("Value of " ~ env_var_name ~ ": " ~ env_var_value) }}
{% endmacro %}
