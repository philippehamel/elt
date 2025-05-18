-- films.sql

{{ config(
    materialized='table',
    full_refresh=true
) }}

SELECT * FROM {{ source('destination_db', 'films') }}