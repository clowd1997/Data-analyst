import pandas as pd
import pandasql as ps
import numpy as np

df = pd.read_csv('ds_salaries.csv')

# Dictionaries
Experience_dict={'SE':'Senior','MI':'Middle','EN':'Entry','EX':'Executive'}
Employment_dict={'FT':'Full Time', 'CT':'Contract', 'FL':'Freelancer', 'PT':'Part Time'}
National_dict ={'ES':'Spain', 'US':'United States of America', 'CA':'Canada',
                'DE':'Germany', 'GB':'United Kingdom of Great Britain and Northern Ireland',
                'NG':'Nigeria', 'IN':'India', 'HK':'Hong Kong', 'PT':'Portugal', 'NL':'Netherlands',
                'CH':'Switzerland', 'CF':'Central African Republic', 'FR':'France', 'AU':'Australia',
                'FI':'Finland' ,'UA':'Ukraine', 'IE':'Ireland', 'IL':'Israel', 'GH':'Ghana', 'AT':'Austria',
                'CO':'Colombia', 'SG':'Singapore', 'SE':'Sweden', 'SI':'Slovenia', 'MX':'Mexico',
                'UZ':'Uzbekistan', 'BR':'Brazil', 'TH':'Thailand', 'HR':'Croatia', 'PL':'Poland',
                'KW':'Kuwait', 'VN':'Viet Nam', 'CY':'Cyprus', 'AR':'Argentina', 'AM':'Armenia',
                'BA':'Bosnia and Herzegovina', 'KE':'Kenya', 'GR':'Greece', 'MK':'Republic of North Macedonia',
                'LV':'Latvia', 'RO':'Romania', 'PK':'Pakistan','IT':'Italy', 'MA':'Morocco','LT':'Lithuania',
                'BE':'Belgium', 'AS':'American Samoa', 'IR':'Iran', 'HU':'Hungary', 'SK':'Slovakia',
                'CN':'China', 'CZ':'Czechia', 'CR':'Costa Rica', 'TR':'Turkey','CL':'Chile', 'PR':'Puerto Rico',
                'DK':'Denmark', 'BO':'Bolivia', 'PH':'Philippines', 'DO':'Dominican Republic',
                'EG':'Egypt', 'ID':'Indonesia', 'AE':'United Arab Emirates', 'MY':'Malaysia', 'JP':'Japan',
                'EE':'Estonia', 'HN':'Honduras', 'TN':'Tunisia', 'RU':'Russian Federation', 'DZ':'Algeria',
                'IQ':'Iraq', 'BG':'Bulgaria', 'JE':'Jersey', 'RS':'Serbia', 'NZ':'New Zealand',
                'MD':'Moldova', 'LU':'Luxembourg', 'MT':'Malta'}
Company_dict={'L':'Large', 'S':'Small', 'M':'Middle'}

df = df.replace({'company_size':Company_dict})
df = df.replace({'experience_level':Experience_dict})
df = df.replace({'employment_type':Employment_dict})
df = df.replace({'company_location':National_dict})
df = df.replace({'employee_residence':National_dict})
df.to_csv('ds_salaries2.csv',index=True)

# SQL code
By_Job_Title = ps.sqldf\
    ('select work_year,job_title, sum(salary_in_usd) '
     'from df group by work_year,job_title '
     'order by salary_in_usd',locals())

# Change format of work_year data from 2020.0 to 2020
By_Job_Title['work_year']=By_Job_Title['work_year'].astype(str).str.replace('.0','')
# Drop null rows
By_Job_Title = By_Job_Title.dropna()
# Pivot
By_Job_Title=By_Job_Title.pivot(index='job_title',columns='work_year',values='sum(salary_in_usd)')
# Add one more column Total
By_Job_Title['Total']= np.nansum((By_Job_Title['2020'],By_Job_Title['2021'],By_Job_Title['2022'],By_Job_Title['2023']),axis=0)
By_Job_Title.to_csv('By_Job_Title.csv',index = True)


By_Experience_Level = ps.sqldf\
    ('select work_year,experience_level, sum(salary_in_usd) '
     'from df group by work_year,experience_level '
     'order by salary_in_usd desc',locals())
By_Experience_Level['work_year']=By_Experience_Level['work_year'].astype(str).str.replace('.0','')
By_Experience_Level = By_Experience_Level.replace({'experience_level':Experience_dict})
By_Experience_Level = By_Experience_Level.dropna()
By_Experience_Level=By_Experience_Level.pivot(index='experience_level',columns='work_year',values='sum(salary_in_usd)')
By_Experience_Level['Total']= np.nansum((By_Experience_Level['2020'],By_Experience_Level['2021'],By_Experience_Level['2022'],By_Experience_Level['2023']),axis=0)
By_Experience_Level.to_csv('By_Experience_Level.csv',index = True)

By_Employment_Type = ps.sqldf\
    ('select work_year,employment_type, sum(salary_in_usd) '
     'from df group by work_year,employment_type '
     'order by salary_in_usd desc',locals())
By_Employment_Type['work_year']=By_Employment_Type['work_year'].astype(str).str.replace('.0','')
By_Employment_Type = By_Employment_Type.replace({'employment_type':Employment_dict})
By_Employment_Type = By_Employment_Type.dropna()
By_Employment_Type=By_Employment_Type.pivot(index='employment_type',columns='work_year',values='sum(salary_in_usd)')
By_Employment_Type['Total']= np.nansum((By_Employment_Type['2020'],By_Employment_Type['2021'],By_Employment_Type['2022'],By_Employment_Type['2023']),axis=0)
By_Employment_Type.to_csv('By_Employment_Type.csv',index = True)

By_Country = ps.sqldf\
    ('select work_year,company_location, sum(salary_in_usd) '
     'from df group by work_year,company_location '
     'order by salary_in_usd desc',locals())
By_Country['work_year']=By_Country['work_year'].astype(str).str.replace('.0','')
By_Country = By_Country.replace({'company_location':National_dict})
By_Country = By_Country.dropna()
By_Country=By_Country.pivot(index='company_location',columns='work_year',values='sum(salary_in_usd)')
By_Country['Total']= np.nansum((By_Country['2020'],By_Country['2021'],By_Country['2022'],By_Country['2023']),axis=0)
By_Country.to_csv('By_Country.csv',index = True)

By_Remote_Ratio = ps.sqldf('select work_year,remote_ratio, sum(salary_in_usd) '
                           'from df group by work_year,remote_ratio '
                           'order by salary_in_usd desc',locals())
By_Remote_Ratio['work_year']=By_Remote_Ratio['work_year'].astype(str).str.replace('.0','')
By_Remote_Ratio = By_Remote_Ratio.dropna()
By_Remote_Ratio=By_Remote_Ratio.pivot(index='remote_ratio',columns='work_year',values='sum(salary_in_usd)')
By_Remote_Ratio['Total']= np.nansum((By_Remote_Ratio['2020'],By_Remote_Ratio['2021'],By_Remote_Ratio['2022'],By_Remote_Ratio['2023']),axis=0)
By_Remote_Ratio.to_csv('By_Remote_Ratio.csv',index = True)

By_Company_Size = ps.sqldf\
    ('select work_year,company_size, sum(salary_in_usd) '
     'from df group by work_year,company_size '
     'order by salary_in_usd desc',locals())
By_Company_Size['work_year']=By_Company_Size['work_year'].astype(str).str.replace('.0','')
By_Company_Size = By_Company_Size.replace({'company_size':Company_dict})
By_Company_Size = By_Company_Size.dropna()
By_Company_Size=By_Company_Size.pivot(index='company_size',columns='work_year',values='sum(salary_in_usd)')
By_Company_Size['Total']= np.nansum((By_Company_Size['2020'],By_Company_Size['2021'],By_Company_Size['2022'],By_Company_Size['2023']),axis=0)
By_Company_Size.to_csv('By_Company_Size.csv',index = True)
