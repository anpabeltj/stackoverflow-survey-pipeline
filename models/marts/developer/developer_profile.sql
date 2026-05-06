with survey as (
    select * from {{ ref('stg_survey') }}
)

select
    s.age,
    s.country,
    s.dev_type,
    s.employment,
    s.education_level,
    s.remote_work,
    s.org_size,
    case
        when s.converted_comp_yearly is null then 'Unknown'
        when s.converted_comp_yearly < 50000 then 'Entry'
        when s.converted_comp_yearly between 50001 and 100000 then 'Mid'
        else 'Senior'
    end as salary_level,
    case
        when s.years_code_pro = 'Less than 1 year' then 'Junior'
        when s.years_code_pro = 'More than 50 years' then 'Senior'
        when NULLIF(s.years_code_pro, 'NA') is null then 'Unknown'
        when NULLIF(s.years_code_pro, 'NA')::int between 0 and 3 then 'Junior'
        when NULLIF(s.years_code_pro, 'NA')::int between 4 and 7 then 'Mid'
        when NULLIF(s.years_code_pro, 'NA')::int > 7 then 'Senior'
        else 'Unknown'
    end as experience_level
from survey as s
