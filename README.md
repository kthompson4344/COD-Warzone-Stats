# COD Warzone Stats
 
This Python script is used to gather player stats from https://cod.tracker.gg/warzone and calculate score for Warzone tournaments.

##Prequisites:
-Python 3 (I tested with Python 3.8, Windows 10 https://www.python.org/)
-Beautiful Soup (https://pypi.org/project/beautifulsoup4/)
-Selenium (https://pypi.org/project/selenium/)
-Google Chrome (https://www.google.com/chrome/)
-Chromedriver (https://chromedriver.chromium.org/)

##Install Instructions:
1. Install python 3.8
2. Type the following in the command prompt or terminal to install prerequisite Python packages:
	a. pip install beautifulsoup4
	b. pip install selenium
3. Download chromedriver.exe and place in the same folder where the COD_Stats.py is

##Input file format (playerList.csv):
-CSV (UTF-8)
Name, Location, ActivisionID, Email, Link

Link is a URL to the matches page for the player. The remaining fields are optional.

##User modifications:
Must configure a date range at the beginning of the COD_Stats.py. It will only gather stats during that date and time range.

Line 187 is where the score is calculated, you can modify the formula to fit your needs
