from sqlalchemy import create_engine, Table, select, MetaData
import sqlalchemy as db
import pandas as pd
import datetime
import requests
import io
import os

def updateFunction():

    # db credentials
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = 'postgres://ewxyjxpjxsqthz:e56aeb73ecb3b32ce4732e693aebcd263fabd11971ef7953f29f0f1266468796@ec2-34-194-158-176.compute-1.amazonaws.com:5432/des1cplt5kis06'
    DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')

    # engine and connection
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()

    # get last update date from table
    metadata = MetaData(bind=None)
    vars_t = Table('vars_storage', metadata, autoload=True, autoload_with=engine)

    stmt = select([vars_t.columns.var_value])

    results = conn.execute(stmt).fetchall()
    last_update_d = results[0][0]

    # get current date
    curr_date = datetime.datetime.today().day

    # check if data is old    ! for day data
    if last_update_d != curr_date:

        # get list of tables from db
        meta_data = MetaData(bind=conn)
        MetaData.reflect(meta_data)
        list_of_tables = list(meta_data.tables.keys())

        # list of table with day rate update
        list_of_tables_to_update = [table for table in list_of_tables if table.__contains__('_d')]

        for table in list_of_tables_to_update:

            # count number of rows in current table
            table_md = meta_data.tables[str(table)]
            num_rows = db.select([db.func.count()]).select_from(table_md).scalar()

            # refactor name of table to access data
            req_table = table[:-2].upper() + '_d'
            url = f'https://www.cryptodatadownload.com/cdd/Binance_{req_table}.csv'
            response = requests.get(url).content
            data = pd.read_csv(io.StringIO(response.decode('utf-8')), header=1)

            # count the difference btw new data and current data
            num_rows_to_add = len(data) - num_rows

            # display number of new rows for current table
            print(str(table) + ' : ' + str(num_rows_to_add))

            # if there are new rows then add them to db
            if num_rows_to_add > 0:
                data = data.iloc[:num_rows_to_add, :]
                data.sort_values('unix', inplace=True)
                data.to_sql(table, con=engine, if_exists='append', index=False)

        # change last update date in table vars_storage
        conn.execute(f"update vars_storage set var_value = {curr_date} where var_name = 'last_update_d'")

    conn.close()
#%%
