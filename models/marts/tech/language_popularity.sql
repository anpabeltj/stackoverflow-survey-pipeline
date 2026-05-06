with language as (
    select
        unnest(string_to_array(s.language_have_worked_with, ';'))
            as programming_language,
        count(*) as count
    from {{ ref('stg_survey') }} as s
    where s.language_have_worked_with is not null
    group by s.language_have_worked_with
    order by count desc
),

counted as (
    select
        programming_language,
        count(*) as developer_count
    from language
    group by programming_language
)

select * from counted
order by developer_count desc
