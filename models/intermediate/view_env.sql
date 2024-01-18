WITH env_vars AS (
  SELECT
    UNNEST(REGEXP_MATCHES(CURRENT_SETTING(), E'\\w+=\\\'(.*?)(?=\\\'\\,\\s*\\w+=|$)')) AS kv
)
SELECT
  SPLIT_PART(kv, '=', 1) AS key,
  SPLIT_PART(kv, '=', 2) AS value
FROM env_vars;
