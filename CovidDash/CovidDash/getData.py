from sqlalchemy import create_engine
import pandas as pd
import os

#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = 'postgres://ewxyjxpjxsqthz:e56aeb73ecb3b32ce4732e693aebcd263fabd11971ef7953f29f0f1266468796@ec2-34-194-158-176.compute-1.amazonaws.com:5432/des1cplt5kis06'
DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')
conn = create_engine(DATABASE_URL)

def getDataFromDB(table_name):
    return pd.read_sql(table_name.lower(), con=conn)