import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://athletics.amherst.edu/sports/football/stats/2022/middlebury-college/boxscore/12292'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rushing = str(soup.find('section', {'id':'individual-rushing'}))
passing = str(soup.find('section', {'id':'individual-passing'}))
receiving = str(soup.find('section', {'id':'individual-receiving'}))
defense_away = str(soup.find('section', {'id':'defense-away'}))
defense_home = str(soup.find('section', {'id':'defense-home'}))

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

print(defense_value(defense_home, defense_away))
