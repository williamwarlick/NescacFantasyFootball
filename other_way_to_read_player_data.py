import ssl
import pandas as pd

amherst_url = "https://athletics.amherst.edu/sports/football/roster"
bates_url = "https://gobatesbobcats.com/sports/football/roster"
bowdoin_url = "https://athletics.bowdoin.edu/sports/football/roster"
colby_url = "https://colbyathletics.com/sports/football/roster"
trinty_url = "https://bantamsports.com/sports/football/roster"
wesleyan_url = "https://athletics.wesleyan.edu/sports/football/roster"
middelbury_url = "https://athletics.middlebury.edu/sports/football/roster"
tufts_url = "https://gotuftsjumbos.com/sports/football/roster"
hamilton_url = "https://athletics.hamilton.edu/sports/football/roster"

amherst_pd = pd.read_html(amherst_url)[2]
bates_pd = pd.read_html(bates_url)
bowdoin_pd = pd.read_html(bowdoin_url)
colby_pd = pd.read_html(colby_url)
# trinty_pd = pd.read_html(trinty_url)
# wesleyan_pd = pd.read_html(wesleyan_url)
# middelbury_pd = pd.read_html(middelbury_url)
# tufts_pd = pd.read_html(tufts_url)
# hamilton_pd = pd.read_html(hamilton_url)

pd_list = [amherst_pd, bates_pd, bowdoin_pd,
           colby_pd #trinty_pd, wesleyan_pd, middelbury_pd, tufts_pd, hamilton_pd
            ]
dfs = [d[2] for d in pd_list]
pds_formated = [p.set_index('Name') for p in dfs]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(pd.concat(pds_formated, axis=0))
