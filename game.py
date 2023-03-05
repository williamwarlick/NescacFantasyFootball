import requests
from bs4 import BeautifulSoup

url = "https://nescac.com/boxscore.aspx?id=BLxxhvTBvnQI0eJFISAEu7ofiAnApjqHlzfcnOIMOH5WCy7zokfiX5xGGNlPZd4PyNEueWxWif7I3OuXVK8y6LfObP8Il9bJ51o%2bKosWUQXXx7uyaJ1LjSiz1mBS1Hn69VBuqTTne6oe0hhz%2fEXghA%3d%3d&path=football"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


