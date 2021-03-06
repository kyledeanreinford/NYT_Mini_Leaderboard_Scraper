import streamlit as st 
import numpy as np 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from streamlit.report_thread import get_report_ctx

engine = 'postgresql://miniadmin:acab@localhost:5432/minitimesdb'
db = create_engine(engine)

def load_data():
    data = pd.read_sql("SELECT * FROM solves", con=db)
    print(data)
    st.write(data)

if __name__ == '__main__':
    
    st.header('NYT Mini Leaderboard')
    load_data()


    # players = []
    # result = db.execute(text("SELECT name FROM solves"))
    # for row in result:
    #     player = row.name
    #     if player not in players:
    #         players.append(player)
    # for player in players:
    #     print(player)

    # df = pd.read_sql_query("SELECT * FROM solves", con=db)
    # df