
--SELECT 'DBT_ESG_DB' as variable, '{{env_var('DBT_ESG_DB')}}' as value
{{ log_variable() }}

select 1 as dummy
    
