import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl


# Define the URL to scrape --> one for each nescac team
urls = ["https://gobatesbobcats.com/sports/football/roster","https://athletics.amherst.edu/sports/football/roster",
        "https://athletics.bowdoin.edu/sports/football/roster","https://colbyathletics.com/sports/football/roster",
        "https://bantamsports.com/sports/football/roster", "https://athletics.wesleyan.edu/sports/football/roster",
        "https://athletics.middlebury.edu/sports/football/roster", "https://gotuftsjumbos.com/sports/football/roster"]

"""
Returns a dictinary of players, keyed on player name, to a player basic info as a dictionary. 
Basic info includes team, number, position, height, weight, hometown, high school, and class year.
"""
def scrapePlayerList():
    players = dict()
    for url in urls:

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        team = soup.title.text.split()[-2]
        #iterates throught a set comprised of each player for a given roster (in the card view)
        for player in soup.find_all("li", class_="sidearm-roster-player"):

            name = "".join(player.find("div", class_="sidearm-roster-player-name").find('a').text)
            number = player.find("div", class_="sidearm-roster-player-name").get_text().split()[0]
            hometown = ""
            if player.find("span", class_="sidearm-roster-player-hometown") is not None:
                hometown = " ".join(player.find("span", class_="sidearm-roster-player-hometown").get_text().split())
            highschool = ""
            if player.find("span", class_="sidearm-roster-player-highschool") is not None:
                highschool = " ".join(player.find("span", class_="sidearm-roster-player-highschool").get_text().split())
            year = ""
            if player.find("span", class_="sidearm-roster-player-academic-year") is not None:
                year = player.find("span", class_="sidearm-roster-player-academic-year").get_text()
            elif player.find("span", class_="sidearm-roster-player-custom2") is not None:
                year = player.find("span", class_="sidearm-roster-player-custom2").get_text()
            details = player.find("div", class_="sidearm-roster-player-position").get_text().split()
            if len(details) >= 3:
                position = details[0]
                height = details[1]
                weight = details[2]

                players.update({name: {'team': team, 'number': number,  'position': position, 'height': height,
                                         'weight': weight, 'hometown':  hometown, "highschool": highschool, "year": year}})

    return players



#if __name__ == "main":

print(scrapePlayerList())
