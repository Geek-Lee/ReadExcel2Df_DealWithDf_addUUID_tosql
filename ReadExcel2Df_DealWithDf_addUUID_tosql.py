import pandas as pd
import sqlite3
import uuid
from pandas import DataFrame
from sqlalchemy import create_engine

filefullpath = r"C:\Users\Administrator\Downloads\华泰大赛参赛私募基金数据填报模板2.xlsx"
df = pd.read_excel(filefullpath, sheetname=0)#0:sheet
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")
df = df.T
df.columns = df.loc['公司资料简介']#row_name
print(df)
df = df.drop('公司资料简介', axis=0, inplace=False)
print(df)
print(df['★机构简称'])
#df = df.add('datetime.datetime',axis='columns')
df.drop_duplicates(subset=['★机构简称'], inplace=True)

###此位置增加从数据库筛选的关键词遍历，if在数据库中，更新，else没在,增加uuid,更新
con = sqlite3.connect(r"C:\Users\Administrator\Desktop\excel-upload-sqlite3\mins\db.sqlite3")

sql = "SELECT shiliyi.'★机构全名' FROM shiliyi"
data = pd.read_sql(sql, con)
fund_name_list = data['★机构全名'].tolist()
print(fund_name_list)


for name in df['★机构全名'].unique():
    df.loc[df['★机构全名'] == name, 'UUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
for name in df['★机构全名'].unique():#遍历DataFrame中的数据
    if name in fund_name_list:
        df.to_sql("shiliyi", con, if_exists="replace", index=False)
        print("if")
    else:
        df.to_sql("shiliyi", con, if_exists="append", index=False)
        print("else")
print("to_sql")
