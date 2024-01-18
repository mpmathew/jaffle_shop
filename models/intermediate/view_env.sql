-- models/environment_variables_model.sql

-- Source block to define the source of your data
source: environment_variables {
  location: 'variables.csv'
  schema: 'public'
  file_format: csv
}

-- Staging model to load the environment variable names into a temporary table
model: environment_variable_names {
  SELECT
    variable
  FROM
    {{ ref('environment_variables') }};
}

-- Model block to define the transformation and fetch values using env_var()
model: environment_variables_table {
  SELECT
    variable,
    env_var(variable) as value
  FROM
    {{ ref('environment_variable_names') }};
}

