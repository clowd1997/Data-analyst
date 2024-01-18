import pandas as pd

# Pandas settings for visualization
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Import csv using pandas
clean = pd.read_csv('national_M2022_dl.csv')
df1 = pd.DataFrame(clean)

# Cleaning data
# Drop unnecessary columns
df1.drop(columns=['AREA', 'AREA_TITLE', 'AREA_TYPE', 'PRIM_STATE',
                  'NAICS', 'NAICS_TITLE','I_GROUP', 'OWN_CODE',
                  'JOBS_1000','LOC_QUOTIENT', 'PCT_TOTAL', 'PCT_RPT',
                  'H_PCT10', 'H_PCT25', 'H_MEDIAN', 'H_PCT75',
                  'H_PCT90', 'A_PCT10','A_PCT25', 'A_MEDIAN',
                  'A_PCT75', 'A_PCT90', 'ANNUAL', 'HOURLY'],
         inplace=True)

# Replace columns name
df1.rename(columns = {'OCC_CODE':'Occupation Code', 'OCC_TITLE':'Occupation Title',
                      'O_GROUP':'Occupation Group', 'TOT_EMP':'Total Employee',
                      'EMP_PRSE':'Employee PRSE','H_MEAN':'Hour Mean', 'A_MEAN':'Annual Mean',
                      'MEAN_PRSE':'Mean PRSE'}, inplace = True)

# Fill H_Mean value using A_MEAN value: H_MEAN = A_MEAN/260/8
i1 = df1.index
index = df1["Hour Mean"] == '*'
result1 = i1[index]
result1.tolist()
df1['Annual Mean']=df1['Annual Mean'].str.replace(',','')
df1.loc[result1, 'Hour Mean'] = df1.loc[result1,'Annual Mean'].astype('float')/260/8
df1['Hour Mean'] = df1['Hour Mean'].astype('float').map("{:,.2f}".format)


# Fill A_MEAN value using H_MEAN value: A_MEAN = H_MEAN*260*8
i2 = df1.index
index = df1["Annual Mean"] == '*'
result2 = i2[index]
result2.tolist()
df1['Hour Mean']=df1['Hour Mean'].str.replace(',','')
df1.loc[result2, 'Annual Mean'] = df1.loc[result2,'Hour Mean'].astype('float')*260*8
df1['Annual Mean'] = df1['Annual Mean'].astype('float').map("{:,}".format)

# Divide main table into job group type and employee situation
Emp = df1.loc[(df1['Occupation Group'] == 'minor') | (df1['Occupation Group'] == 'major')]
Emp = Emp[['Occupation Code', 'Occupation Title', 'Occupation Group', 'Total Employee', 'Employee PRSE']]

list_OCC_CODE = df1['Occupation Code'].astype(str).str[:2]

list_OCC_CODE = list(dict.fromkeys(list_OCC_CODE))

Emp1 = pd.DataFrame()

for x in list_OCC_CODE:
    Emp2 = Emp[Emp['Occupation Code'].astype(str).str[:2] == x]
    Emp2.loc[:,'Total Employee'] = Emp['Total Employee'].str.replace(',','').astype('int')

    Emp1 = pd.concat([Emp1,Emp2[Emp2['Occupation Group'] == 'major']])

    list_emp = Emp2[Emp2['Occupation Group']=='minor'].loc[:,['Total Employee']].values.flatten().tolist()
    list_emp.sort()

    y = 1
    while y <= len(list_emp):
        Emp1 = pd.concat([Emp1,Emp2[Emp2['Total Employee']==list_emp[-y]]])
        y+=1
        if y == 4:
            break

Emp1['Total Employee'] = Emp1['Total Employee'].astype('int').map("{:,}".format)

Emp1.to_csv('National_Emp.csv',index=False)


# # Divide main table into job group type and wage situation
Wage = df1.loc[(df1['Occupation Group'] == 'minor') | (df1['Occupation Group'] == 'major')]
Wage = Wage[['Occupation Code', 'Occupation Title', 'Occupation Group', 'Hour Mean','Annual Mean', 'Mean PRSE']]

# list_OCC_CODE = df1['OCC_CODE'].astype(str).str[:2]
#
# list_OCC_CODE = list(dict.fromkeys(list_OCC_CODE))

Wage1 = pd.DataFrame()

for x in list_OCC_CODE:
    Wage2 = Wage[Wage['Occupation Code'].astype(str).str[:2] == x]
    Wage2.loc[:,'Annual Mean'] = Wage['Annual Mean'].str.replace(',','').astype('float')

    Wage1 = pd.concat([Wage1,Wage2[Wage2['Occupation Group'] == 'major']])

    list_wage = Wage2[Wage2['Occupation Group']=='minor'].loc[:,['Annual Mean']].values.flatten().tolist()
    list_wage.sort()

    y = 1
    while y <= len(list_wage):
        Wage1 = pd.concat([Wage1,Wage2[Wage2['Annual Mean']==list_wage[-y]]])
        y+=1
        if y == 4:
            break


Wage1['Annual Mean'] = Wage1['Annual Mean'].astype('int').map("{:,}".format)

Wage1.to_csv('National_Wage.csv',index=False)