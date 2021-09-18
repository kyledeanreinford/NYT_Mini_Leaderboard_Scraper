# NYT Mini Leaderboard Scraper

I play the NY Times Mini Crossword with several of my friends, and while we could see the daily leaderboard, there was no way to see who had yesterday's best time, or who had the most wins. This made trash talking difficult. 

I created this app which uses Python and Beautiful Soup to log in to my NY Times account and scrape all of the times into a database. I set up a cron on my server to do this one minute before the current day's puzzle disappears (9pm central Monday-Friday, 5pm Saturday-Sunday). Initially I was using a Postgres DB and Streamlit, but decided I wanted a more robust setup, so I shifted to MongoDB and built a MERN app, with visualizations using Nivo. 

Scraper portion of my Mini Scraper. See an example at <a href="https://young-ocean-41803.herokuapp.com/">Heroku</a>.

Full MERN Stack code is <a href="https://github.com/kyledeanreinford/Mini_1.0.0">here</a>.

To run with your own friends:
Change list of players to a list of your friends' usernames

to run: python scraper.py -u {username} -p {password}
