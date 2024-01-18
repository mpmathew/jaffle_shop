-- Model block to define the transformation and fetch values using env_var()
with variables as (

    select 
    variable,
    "{{env_var('variable')}}" as value 
    from {{ ref('stg_variable') }}

)
select * from variables
