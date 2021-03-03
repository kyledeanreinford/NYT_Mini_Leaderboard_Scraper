import argparse
import requests
import csv
from psycopg2 import sql
from bs4 import BeautifulSoup as soup 
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://miniadmin:acab@localhost:5432/minitimesdb')
db = scoped_session(sessionmaker(bind=engine))

parser = argparse.ArgumentParser(description="Get Mini Times")
parser.add_argument(
    '-u', '--username', required=True)
parser.add_argument(
    '-p', '--password', required=True)
parser.add_argument(
    '-o', '--output', default='mini_data.csv'
)

players = ['kyledeanreinford', 'Ericki', 'jalopey', 'willardsmith', 'conor', 'Mark Miller', 'Szakonyi', 'd’Anthony' ]

def login(username, password):
    login_resp = requests.post(
        'https://myaccount.nytimes.com/svc/ios/v2/login',
        data={
            'login': username,
            'password': password,
        },
        headers={
            'User-Agent': 'Mozilla/5.0',
            'client_id': 'ios.crosswords',
        }
    )
    login_resp.raise_for_status()
    for cookie in login_resp.json()['data']['cookies']:
        if cookie['name'] == 'NYT-S':
            return cookie['cipheredValue']
    raise ValueError('NYT-S cookie not found')

def get_mini_times(cookie,output):
    url = "https://www.nytimes.com/puzzles/leaderboards"
    response = requests.get(url, cookies={
        'NYT-S': cookie,
    },
    )
    page = soup(response.content, features='html.parser')
    solvers = page.find_all('div', class_='lbd-score')

    # create datetime variables
    current_datetime = datetime.now()
    month = str(current_datetime.strftime("%m"))
    day = str(current_datetime.strftime("%d"))
    year = str(current_datetime.strftime("%Y"))
    daytimes=[]

    # create sql table
    db.execute("""CREATE TABLE IF NOT EXISTS solves (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        time INTEGER,
        date DATE NOT NULL DEFAULT CURRENT_DATE);""")
    db.commit()
    for solver in solvers:
        name = solver.find('p', class_='lbd-score__name').text.strip()
        try:
            time = solver.find('p', class_='lbd-score__time').text.strip()
        except:
            time="--"
        if name.endswith("(you)"):
            name_split = name.split()
            name = name_split[0]
        if name in players:
            daytimes.append([month,day,year,name,time])
            ### Keep getting 'tuple' error here ###
            db.execute("INSERT INTO solves (name, time) VALUES (?, ?)", (name, time))
            db.commit()
            
    # with open(output, 'w') as csvfile:  
    #     csvwriter = csv.writer(csvfile)              
    #     csvwriter.writerows(daytimes) 

if __name__ == '__main__':
    args = parser.parse_args()
    cookie = login(args.username, args.password)
    get_mini_times(cookie,args.output)
    