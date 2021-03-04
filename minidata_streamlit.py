import streamlit as st 
import numpy as np 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from streamlit.report_thread import get_report_ctx

engine = 'postgresql://miniadmin:acab@localhost:5432/minitimesdb'
db = create_engine(engine)

if __name__ == '__main__':
    
    st.header('NYT Mini Leaderboard')

    # players = []
    # result = db.execute(text("SELECT * FROM solves WHERE name = 'Ericki'"))
    # for row in result:
    #     print(f"x: {row.name} y: {row.time}")

    df = pd.read_sql_query("SELECT * FROM solves", con=db)
    df