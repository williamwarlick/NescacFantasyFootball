import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
urls = ["https://gobatesbobcats.com/sports/football/roster","https://athletics.amherst.edu/sports/football/roster", "https://athletics.bowdoin.edu/sports/football/roster",
        "https://colbyathletics.com/sports/football/roster",
        "https://bantamsports.com/sports/football/roster", "https://athletics.wesleyan.edu/sports/football/roster",
        "https://athletics.middlebury.edu/sports/football/roster", "https://gotuftsjumbos.com/sports/football/roster"]

players = dict()
for url in urls:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    team = soup.title.text.split()[-2]

    for player in soup.find_all("li", class_="sidearm-roster-player"):
        name = " ".join(player.find("div", class_="sidearm-roster-player-name").get_text().split()[1:])
        number = player.find("div", class_="sidearm-roster-player-name").get_text().split()[0]
        hometown = ""
        print(name)
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

            players.update({name: {'team': team, 'number': number,  'position': position, 'height': height, 'weight': weight, 'hometown':
                            hometown, "highschool": highschool, "year": year}})

print(players)
