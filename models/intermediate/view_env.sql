env_vars_table as (
SELECT 'DBT_ESG_DB' as variable, {{env_var('DBT_ESG_DB')}} as value UNION ALL
)
select * from env_vars_table
    
