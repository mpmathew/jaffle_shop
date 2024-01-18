{% macro log_variable(my_variable) %}
 {% do log(~ argument(my_variable) ~ " : "  ~ env_var(my_variable), info=True) %}
{% endmacro %}
