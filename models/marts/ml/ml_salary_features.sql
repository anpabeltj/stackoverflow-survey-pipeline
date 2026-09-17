select
    response_id,
    country,
    age,
    education_level,
    dev_type,
    employment,
    org_size,
    remote_work,
    experience_level,
    salary_level
from {{ ref('developer_profile') }}
where
    salary_level is not NULL
    and salary_level <> 'Unknown'