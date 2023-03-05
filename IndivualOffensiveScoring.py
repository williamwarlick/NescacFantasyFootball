#from GetPlayerInfo import scrapePlayerList
import pandas as pd
import ssl

# Create SSL context
context = ssl.create_default_context()

# Disable certificate verification
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

dfs = pd.read_html('https://athletics.bowdoin.edu/sports/football/roster?path=football', index_col=0)


print(dfs[2].to_string())