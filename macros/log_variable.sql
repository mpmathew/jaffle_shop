{% macro log_variable(my_variable) %}
 {% do log(~ my_variable ~ ":"  ~ env_var(my_variable), info=True) %}
{% endmacro %}
