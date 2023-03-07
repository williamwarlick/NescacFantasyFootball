"""
get_games.py
Given the url of the nescac football season overview[+some year], returns links to the stats pages for each
game that happend that season. Works until 2012, before then there are no stats.
"""
import requests
from bs4 import BeautifulSoup

nescac_football_overall_stats_all_games_url = 'https://nescac.com/stats.aspx?path=football&year=2012'

"""
Used to work around webscraping prevention feature?
when using pd.read_html() would give 404 error, I think it was actually meant to throw a 403 error(server denies
you permission to access a page on their site), but because not used often, just gave generic 404 error
Followed this video: https://www.youtube.com/watch?v=6RfyXcf_vQo
"""
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
response = requests.get(nescac_football_overall_stats_all_games_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

#Open to finding a bette rway to accese the table of all the games of a season, couldnt find one
games_table = soup.find_all('table', class_="sidearm-table")[50]
rows = games_table.find_all('td', class_="text-nowrap")

def get_game_urls():
    #url of each games stats page
    urls = []
    for content in rows:
        if content.find('a') is not None:
            urls.append('https://nescac.com/' + content.find('a')['href'])

    return urls







