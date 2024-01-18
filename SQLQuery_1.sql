Create database MindXCuoiKhoa1
Create table Salary1(
    AREA VARCHAR(50)
    ,AREA_TITLE VARCHAR(50)
    ,AREA_TYPE VARCHAR(50)
    ,PRIM_STATE VARCHAR(50)
    ,NAICS VARCHAR(50)
    ,NAICS_TITLE VARCHAR(50)
    ,I_GROUP VARCHAR(50)
    ,OWN_CODE VARCHAR(50)
    ,OCC_CODE VARCHAR(50)
    ,OCC_TITLE VARCHAR(120)
    ,O_GROUP VARCHAR(50)
    ,TOT_EMP VARCHAR(50)
    ,EMP_PRSE DEC(18,5)
    ,JOBS_1000 VARCHAR(50)
    ,LOC_QUOTIENT VARCHAR(50)
    ,PCT_TOTAL VARCHAR(50)
    ,PCT_RPT VARCHAR(50)
    ,H_MEAN VARCHAR(50)
    ,A_MEAN VARCHAR(50)
    ,MEAN_PRSE VARCHAR(50)
    ,H_PCT10 VARCHAR(50)
    ,H_PCT25 VARCHAR(50)
    ,H_MEDIAN VARCHAR(50)
    ,H_PCT75 VARCHAR(50)
    ,H_PCT90 VARCHAR(50)
    ,A_PCT10 VARCHAR(50)
    ,A_PCT25 VARCHAR(50)
    ,A_MEDIAN VARCHAR(50)
    ,A_PCT75 VARCHAR(50)
    ,A_PCT90 VARCHAR(50)
    ,ANNUAL VARCHAR(50)
    ,HOURLY VARCHAR(50)
)

BULK INSERT Salary1
FROM "C:\salary1.csv"
WITH
(
        FORMAT='CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ','
)

SELECT *
from [dbo].[Salary1]
Alter TABLE [dbo].[Salary1]
drop COLUMN [JOBS_1000]
,[LOC_QUOTIENT]
,[PCT_TOTAL]
,[PCT_RPT]

WITH raw_table as(
    Select *
    ,cast(replace(replace([H_MEAN],'*','0'), ',', '') as float) as HMean
    ,cast(replace(replace([A_MEAN],'*','0'), ',', '') as float) as AMean
    ,cast(REPLACE([TOT_EMP],',','')as float) as TotalEmployment
    ,cast([MEAN_PRSE] as float) Meanprse
    FROM [dbo].[Salary1]
    )
,fact_table as (SELECT 
[OCC_CODE]
,[OCC_TITLE]
,[O_GROUP]
,TotalEmployment
,[EMP_PRSE]
,Meanprse
,round(IIF(HMean=0,AMean/260/8,HMean),2) as HMean
,round(IIF(AMean=0,HMean*260*8,AMean),0) as AMean
,ROW_NUMBER() OVER (PARTITION BY left(OCC_CODE,2) ORDER BY left(OCC_CODE,2)) AS NumRows
FROM raw_table
WHERE O_GROUP IN ('Major','Minor'))

SELECT OCC_CODE, OCC_TITLE, O_GROUP, TotalEmployment, EMP_PRSE, Meanprse, Hmean,Amean
From fact_table
WHERE NumRows <=4




