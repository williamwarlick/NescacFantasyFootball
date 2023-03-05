import ssl
import pandas as pd

urls = ["https://gobatesbobcats.com/sports/football/roster","https://athletics.amherst.edu/sports/football/roster",
        "https://athletics.bowdoin.edu/sports/football/roster","https://colbyathletics.com/sports/football/roster",
        "https://bantamsports.com/sports/football/roster", "https://athletics.wesleyan.edu/sports/football/roster",
        "https://athletics.middlebury.edu/sports/football/roster", "https://gotuftsjumbos.com/sports/football/roster"]

# Create SSL context
context = ssl.create_default_context()
# Disable certificate verification
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


for url in urls:
    df = pd.read_html(url)[2]
    try:
        df.drop('C', axis=1)
    except:
        #carry on
        a = 0

    df.set_index('No.', inplace=True)
    print(df.to_string())