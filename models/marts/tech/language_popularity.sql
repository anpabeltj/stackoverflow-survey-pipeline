-- One row per developer per language, then count developers
with developer_languages as (
    select
        s.response_id,
        trim(unnest(string_to_array(s.language_have_worked_with, ';'))) as programming_language
    from {{ ref('stg_survey') }} as s
    where s.language_have_worked_with is not null
)

select
    programming_language,
    count(distinct response_id) as developer_count
from developer_languages
group by programming_language
order by developer_count desc