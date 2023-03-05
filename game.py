import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

url = 'https://athletics.amherst.edu/sports/football/stats/2022/wesleyan-university/boxscore/12298'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rushing = str(soup.find('section', {'id':'individual-rushing'}))
passing = str(soup.find('section', {'id':'individual-passing'}))
receiving = str(soup.find('section', {'id':'individual-receiving'}))
defense_away = str(soup.find('section', {'id':'defense-away'}))
defense_home = str(soup.find('section', {'id':'defense-home'}))
field_goals = str(soup.find('section', {'id':'individual-fieldgoals'}))
PATs = str(soup.find('section', {'id':'individual-pat-stats'}))

def rushing_value(section):
    tables = pd.read_html(str(section))
    rushing_stats = pd.concat([table[(table['Player'] != 'Totals') & (table['Player'] != 'Team')] for table in tables], axis=0)
    rushing_stats.set_index('Player', inplace=True)
    rushing_stats.clip(lower=0, inplace=True)
    rushing_stats.fillna(0, inplace=True)
    rushing_stats['Value'] = rushing_stats['Gain'] / 10 + rushing_stats['TD'] * 6
    return rushing_stats

def passing_value(section):
    tables = pd.read_html(str(section))
    passing_stats = pd.concat([table[(table['Player'] != 'Totals') & (table['Player'] != 'Team')] for table in tables], axis=0)
    passing_stats.fillna(0, inplace=True)
    passing_stats.set_index('Player', inplace=True)
    passing_stats['Value'] = passing_stats['Yds.'] / 25 + passing_stats['TD'] * 4 + passing_stats['Int.'] * -1
    return passing_stats

def receiving_value(section):
    tables = pd.read_html(str(section))
    receiving_stats = pd.concat([table[(table['Player'] != 'Totals') & (table['Player'] != 'Team')] for table in tables], axis=0)
    receiving_stats.set_index('Player', inplace=True)
    receiving_stats.clip(lower=0, inplace=True)
    receiving_stats.fillna(0, inplace=True)
    receiving_stats['Value'] = receiving_stats['Yds.'] / 10 + receiving_stats['TD'] * 6
    return receiving_stats


def defense_value(home, away):
    defense_stats = pd.concat([
        pd.read_html(str(home))[0],
        pd.read_html(str(away))[0]
    ], axis=0)
    defense_stats.set_index('Player', inplace=True)
    defense_stats = defense_stats.apply(pd.to_numeric, errors='coerce').fillna(0)

    defense_stats['Value'] = defense_stats['TFL'] + defense_stats['INT.1'] * 3 + defense_stats['Solo'] + \
                             defense_stats['Ast'] * .5 + defense_stats['Sacks'] * 2 + defense_stats['QH'] + defense_stats['BrUp']

    return defense_stats

def field_goal_value(section):
    field_goals = pd.concat(pd.read_html(section))

    field_goal_stats = pd.DataFrame(index=field_goals['Player'].unique(), columns=['Value'])
    field_goal_stats['Value'] = 0


    for index, fieldgoal in field_goals.iterrows():
        if fieldgoal['Result'] == 'GOOD':
            if fieldgoal['Yds.'] >= 50:
                field_goal_stats.loc[fieldgoal['Player'], 'Value'] += 5
            elif 40 < fieldgoal['Yds.'] < 50:
                field_goal_stats.loc[fieldgoal['Player'], 'Value'] += 4
            else:
                field_goal_stats.loc[fieldgoal['Player'], 'Value'] += 3
        else:
            if fieldgoal['Yds.'] < 40:
                field_goal_stats.loc[fieldgoal['Player'], 'Value'] -= 2
            elif 39 < fieldgoal['Yds.'] < 50:
                field_goal_stats.loc[fieldgoal['Player'], 'Value'] -= 1
    return field_goal_stats

def PAT_value(section):
    PAT_stats = pd.concat(pd.read_html(section))

    PAT_stats.columns = PAT_stats.columns.map(lambda x: f'{x[0]} {x[1]}' if x[1] else x[0])
    PAT_stats.set_index('Player Player', inplace=True)
    PAT_stats.index.name = 'Player'
    PAT_stats['Value'] = PAT_stats['Kicks Made'] + PAT_stats['Rushes Made'] * 2 + PAT_stats['Passes Made'] * 2 + PAT_stats['Kicks Made'] - PAT_stats['Kicks ATT']

    return PAT_stats

def get_roster(urls):
    url = 'https://gobatesbobcats.com/sports/football/roster'

    # Send a GET request to the URL and parse the HTML content using BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    print(pd.read_html(str(soup.find("div", class_="sidearm-roster-grid-template-1"))))



urls = ["https://gobatesbobcats.com/sports/football/roster", "https://athletics.amherst.edu/sports/football/roster",
            "https://athletics.bowdoin.edu/sports/football/roster", "https://colbyathletics.com/sports/football/roster",
            "https://bantamsports.com/sports/football/roster", "https://athletics.wesleyan.edu/sports/football/roster",
            "https://athletics.middlebury.edu/sports/football/roster",
            "https://gotuftsjumbos.com/sports/football/roster"]

print(field_goal_value(field_goals))
