with database as (
    select
        unnest(string_to_array(s.database_have_worked_with, ';'))
            as database_tools,
        count(*) as count
    from {{ ref('stg_survey') }} as s
    where s.database_have_worked_with is not null
    group by s.database_have_worked_with
    order by count desc
),

counted as (
    select
        database_tools,
        count(*) as developer_count
    from database
    group by database_tools
)

select * from counted
order by developer_count desc
