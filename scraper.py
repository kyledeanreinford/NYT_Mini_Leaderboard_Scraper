import argparse
import requests
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup 

parser = argparse.ArgumentParser(description="Get Mini Times")
parser.add_argument(
    '-u', '--username', required=True)
parser.add_argument(
    '-p', '--password', required=True)
parser.add_argument(
    '-o', '--output-csv', default='data.csv'
)


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

def get_mini_times(cookie):
    url = "https://www.nytimes.com/puzzles/leaderboards"
    response = requests.get(url, cookies={
        'NYT-S': cookie,
    },
    )
    page = soup(response.content, features='html.parser')
    solvers = page.find_all('div', class_='lbd-score')
    for solver in solvers:
        name = solver.find('p', class_='lbd-score__name').text.strip()
        time = solver.find('p', class_='lbd-score__time').text.strip()
        rank = solver.find('p', class_='lbd-score__rank').text.strip()
        print(name, time, rank)
    

if __name__ == '__main__':
    args = parser.parse_args()
    cookie = login(args.username, args.password)
    get_mini_times(cookie)
    