with survey as (
    select * from {{ ref('raw_survey') }}
)

select
    survey."ResponseId" as response_id,
    survey."Age" as age,
    survey."Country" as country,
    survey."EdLevel" as education_level,
    survey."Employment" as employment,
    survey."RemoteWork" as remote_work,
    survey."DevType" as dev_type,
    survey."YearsCodePro" as years_code_pro,
    survey."OrgSize" as org_size,
    survey."Currency" as currency,
    survey."LanguageHaveWorkedWith" as language_have_worked_with,
    survey."DatabaseHaveWorkedWith" as database_have_worked_with,
    survey."AISelect" as ai_select,
    survey."AISent" as ai_sent,
    survey."AIBen" as ai_ben,
    case
        when survey."ConvertedCompYearly"::text = 'NA' then NULL
        else survey."ConvertedCompYearly"::int
    end as converted_comp_yearly
from survey
where
    survey."ResponseId" is not NULL
    and survey."Country" is not NULL
    and survey."Employment" is not NULL
