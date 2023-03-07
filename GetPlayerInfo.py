import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Define the URL to scrape --> one for each nescac team
urls = ["https://athletics.amherst.edu/sports/football/roster",
        "https://gobatesbobcats.com/sports/football/roster",
        "https://athletics.bowdoin.edu/sports/football/roster",
        "https://colbyathletics.com/sports/football/roster",
        "https://bantamsports.com/sports/football/roster", #trinty
        #"https://athletics.wesleyan.edu/sports/football/roster",
        "https://athletics.hamilton.edu/sports/football/roster", # has a glitch wit the .text portion for getting team name
        "https://athletics.middlebury.edu/sports/football/roster",
        "https://gotuftsjumbos.com/sports/football/roster",
        "https://ephsports.williams.edu/sports/football/roster"
        ]

"""
Returns a dictinary of players, keyed on player name, to a player basic info as a dictionary. 
Basic info includes team, number, position, height, weight, hometown, high school, and class year.
"""
def scrapePlayerList():
    players = dict()
    for url in urls:

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.title.text.split()[-2])
        team = soup.title.text.split()[-2]
        #iterates throught a set comprised of each player for a given roster (in the card view)
        for player in soup.find_all("li", class_="sidearm-roster-player"):

            name = " ".join(player.find("div", class_="sidearm-roster-player-name").get_text().split()[1:])
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
                if team == "Bates":
                    height = details[2]
                    weight = details[3]

                else:
                    height = details[1]
                    weight = details[2]

                players.update({name: {'team': team, 'number': number,  'position': position, 'height': height,
                                         'weight': weight, 'hometown':  hometown, "highschool": highschool, "year": year}})

    return players

def get_wes():
    wesleyan_url = "https://athletics.wesleyan.edu/sports/football/roster"
    df = pd.read_html(wesleyan_url)[2].set_index('Name')
    df.insert(loc=0, column='team', value='Wesleyan')
    renamed = df.rename(columns={"No.": 'number', "Pos.": 'position', "Ht.": 'height', "Wt.": 'weight'})
    renamed[['hometown', 'highschool']] = renamed["Hometown / High School"].str.split('/', expand=True)
    renamed.drop(["C", "Hometown / High School"], axis=1, inplace=True)
    renamed.insert(loc=7, column='year', value=renamed.pop('Cl.'))
    return renamed

def to_csv():
    url = "https://athletics.wesleyan.edu/sports/football/roster"
    mega_list =  pd.DataFrame(scrapePlayerList()).transpose()
    a = pd.concat([mega_list, get_wes()], axis=0)
    a['year'] = a['year'].replace(['Fy.', '1st', 'Fr.', 'So.', 'Jr.', 'Sr.'], ['2026','2026', '2026', '2025', '2024', '2023'])
    a['height'] = a['height'].apply(lambda x: '-'.join(x.strip('\"').split('\'')))
    print(a['height'])
    return a

to_csv()
#print(to_csv())
path = r"/Users/wwarlick/development/personal/NescacFantasyFootball"

#to_csv().to_csv(path +'/NescacFootballPlayerInfo.csv')

