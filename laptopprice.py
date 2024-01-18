import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

plt.rcParams.update({'figure.figsize': (7, 3), 'figure.dpi': 120})

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)

path = r'D:\CLowd\BA\MindX\Kickstarter\Homework\Bài tập\7\7_laptop_price.csv'
df = pd.read_csv(path,encoding='latin-1')

# --------------------------------------------------------------
# Studying data
# print(df.info())
# print(df.describe())
# print(df.head(10))

# -----------------------------------------------------------
# Data cleaning
# Find duplicate
# df2 = df[df.duplicated()]
# print(df2)
# Duplicates have different values, thus no need to drop

df = df.dropna()

# Check unique value from object column
# cate_columns = [col for col in df.columns if df[col].dtype == "O"]
# for col in cate_columns:
#     print("name {} : values {}".format(col,df[col].value_counts()))

# We can easily seen that columns is not cleaned, data can be further categorized and views as followings:
# Product will only take company name
# Inches have U value, after checking changed to 12, astype to int64
# ScreenResolution: divide into columns IPS(Yes or No)/TOUCHSCREEN(Yes or No)/(FULLHD or QuadHD,4K UltraHD, Retina Display/Resolution (Screen Height and Width)
# CPU: Company/GHZ
# memory GB/SSD(hdD,Flash storage,hybrid)x, Secondary Memory as well
# GPU: Company/Series

df1 = df

# -----------------------------------------
# Product
df1['Product name'] = df1['Product'].str.split(' ').str[0]

# -----------------------------------------
# Inches
# print(df1.loc[df1['Inches'] == "U"])
df1['Inches']= df1['Inches'].replace(to_replace='U',value=12)
df1['Inches'] = pd.to_numeric(df1['Inches'])
# -----------------------------------------
# ScreenResolution
df1['ScreenResolution'] = df1['ScreenResolution'].str.strip()
df1['ScreenResolution']=df1['ScreenResolution'].replace({ '/ ' : ''},regex=True)

# IPS Panel
df1['IPS Panel'] = [1 if any(i == "IPS Panel" for i in IPS) else 0 for IPS in df1['ScreenResolution'].str.split('(\w+\s\w+)\s')]
# Touch Screen
df1['Touch Screen'] = [1 if any(i == "Touchscreen" for i in IPS) else 0 for IPS in df1['ScreenResolution'].str.split('\s')]
# ScreenResolution
df1['ScreenResolution']=df1['ScreenResolution'].replace({ 'IPS Panel ' : '', "Touchscreen ":""},regex=True)
df1['Resolution']= df1['ScreenResolution'].str.split(' ').str[-1]
df1['Screen Width']=df1['Resolution'].str.split('x').str[0]
df1['Screen Height']=df1['Resolution'].str.split('x').str[1]
df1['Display'] = df1['ScreenResolution'].str.replace("\S+x\S+$", "",regex=True)
df1['Display']=df1['Display'].str.strip()
df1['Display']=df1['Display'].replace('','Standard')

# -----------------------------------------
# Cpu
df1['Cpu'] = df1['Cpu'].str.strip()
df1['Cpu Company'] = df1['Cpu'].str.split(' ').str[0]
df1['Cpu Processing Speed'] = df1['Cpu'].str.split(' ').str[-1]

# -----------------------------------------
# Memory
df1['Memory'] = df1['Memory'].str.strip()
df1['Memory 1'] = df1['Memory'].str.split('\s\W\s ').str[0]
df1['Main Memory'] = df1['Memory 1'].str.split(' ').str[0]
df1['Main Storage'] = df1['Memory 1'].str.split(n=1).str[1]
df1['Secondary memory'] = [1 if any(i == "+" for i in memory) else 0 for memory in df1['Memory'].str.split('\s')]
# Initial divided into 2 more columns for 2nd memory and 2nd storage but decided to take yes or no for 2nd memory approach ^
# df1['Memory 2']= df1['Memory'].str.split('\s\W\s ').str[1]
# df1['Secondary Memory'] = df1['Memory 2'].str.split(' ').str[0]
# df1['Secondary Storage'] = df1['Memory 2'].str.split(n=1).str[1]
# df1['Secondary Memory']= df1['Secondary Memory'].fillna('Not Included')
# df1['Secondary Storage'] =df1['Secondary Storage'].fillna('Not Included')

# -----------------------------------------
# Gpu
df1['Gpu'] = df1['Gpu'].str.strip()
df1['Gpu Company'] = df1['Gpu'].str.split(' ').str[0]
df1['Gpu Series'] = df1['Gpu'].replace({r'^\S+':'',r'\s\d+$':'',r'\s\w+\d$':'',r'\s\d\w+$':''},regex=True)

# Drop unneccessary columns
df1.drop(['Resolution','ScreenResolution','Memory','Memory 1','Gpu','Cpu','Product'],axis=1,inplace=True)
print(df1.head(10))

# --------------------------------------------------------
sns.distplot(df1['Price_euros'],hist = True)
plt.tight_layout()
plt.show()


# Label encoding
columns = ['Company', 'Ram', 'TypeName', 'Product name', 'Display','OpSys', 'Cpu Company','Cpu Processing Speed','Main Memory','Main Storage','Gpu Company','Gpu Series']
for col in columns:
    label_encoder = LabelEncoder()
    df1[col] = label_encoder.fit_transform(df1[col])
print(df1.head(10))


# -------------------------------------------------------------------------------
# Find corr between features and most related features to price_euros
# corr = df1.corr()
# matrix = np.triu(corr)
# sns.heatmap(corr, vmax=1.0, vmin=-1.0,
#             fmt='.1g', annot=True, mask = matrix)
#
# plt.title('Correlation matrix')
# plt.show()

# Drop column after selection
df1.drop(["Gpu Series"],axis = 1,inplace = True)
print(df1.head(10))

y = df1.pop('Price_euros')
X = df1
X_train, X_test, y_train, y_test  = train_test_split(X,y, test_size = 0.3, random_state = 42)

# -------------------------------------------------------------------------------
# Build model to test run
model1= RandomForestRegressor()
model1.fit(X_train,y_train)

y_pred=model1.predict(X_test)

print('R2 score',r2_score(y_test,y_pred))
print(f'MAE :{mean_absolute_error(y_test,y_pred)}')

# -------------------------------------------------------------------------------
# Conclusion
# Screen width, screen height, main storage contributes mostly to price.
# Model improve accuracy is roughly 82%, higher when compared to without eda, data preprocessing model