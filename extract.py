import pandas as pd

df = pd.read_csv("survey_results_public.csv")

df_selected = df[['ResponseId', 'Age', 'Country', 'EdLevel', 
    'Employment', 'RemoteWork', 'DevType', 'YearsCodePro', 
    'OrgSize', 'ConvertedCompYearly', 'Currency',
    'LanguageHaveWorkedWith', 'DatabaseHaveWorkedWith',
    'AISelect', 'AISent', 'AIBen']]

df_selected.sample(n=5000, random_state=42).to_csv('seeds/raw_survey.csv', index=False)

