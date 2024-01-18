-- models/environment_variables_model.sql

with source as (
    select * from {{ ref('variables') }}

),

  -- Staging model to load the environment variable names into a temporary table

environment_variable_names as (
    select 
    variable
    from source
)

-- Model block to define the transformation and fetch values using env_var()

    select 
    variable,
    "{{env_var(variable)}}" as value
    from environment_variable_names
