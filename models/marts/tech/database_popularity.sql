-- One row per developer per database, then count developers
with developer_databases as (
    select
        s.response_id,
        trim(unnest(string_to_array(s.database_have_worked_with, ';'))) as database_tools
    from {{ ref('stg_survey') }} as s
    where s.database_have_worked_with is not null
)

select
    database_tools,
    count(distinct response_id) as developer_count
from developer_databases
group by database_tools
order by developer_count desc