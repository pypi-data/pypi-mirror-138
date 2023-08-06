import sqlite3
from sqlite3 import Error
import pandas as pd
 
 
def makeDB(db_file):
    """ create a database connection to a SQLite database """
    global conn
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
 

#
#filename="script"
#con=sqlite3.connect(filename+".db")
#wb=pd.ExcelFile(filename+'.xlsx')
#for sheet in wb.sheet_names:
#        df=pd.read_excel(filename+'.xlsx',sheetname=sheet)
#        df.to_sql(sheet,con, index=False,if_exists="replace")
#con.commit()
#con.close()