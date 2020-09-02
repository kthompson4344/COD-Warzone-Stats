import sys
import re
from time import strptime
from datetime import date
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv


#Enter the start and end dates/times for the data collection
#use format YYYY-MM-DD
startDate = '2020-08-21'
endDate = '2020-08-28'
startTime = '09'
endTime = '09'

endDateTime = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), int(endTime), 00, 00)
startDateTime = datetime.datetime(int(startDate[0:4]), int(startDate[5:7]), int(startDate[8:10]), int(startTime), 00, 00)

columns, rows = 14, 100;
data = [[0 for x in range(columns)] for y in range(rows)]

playerIndex = 0

data[playerIndex][0] = 'Name'
data[playerIndex][1] = 'Location'
data[playerIndex][2] = 'ID'
data[playerIndex][3] = 'Email'
data[playerIndex][4] = 'Player URL'
data[playerIndex][5] = 'Wins'
data[playerIndex][6] = 'Kills'
data[playerIndex][7] = 'Games'
data[playerIndex][8] = 'Score'
data[playerIndex][9] = 'Kills Per Game'
data[playerIndex][10] = 'Win Percentage'
data[playerIndex][11] = 'Top 5'
data[playerIndex][12] = 'Top 10'
data[playerIndex][13] = 'Max Kills'


today = date.today()

with open('playerList.csv', newline='') as csvfile:
    playerData = list(csv.reader(csvfile))

for i in playerData[1:]:
    error = False
    Name = i[0]
    Location = i[1]
    ID = i[2]
    Email = i[3]
    URL = i[4]
    
    #open webpage
    driver = webdriver.Chrome()
    driver.HideCommandPromptWindow = True
    print('URL:')
    print(URL)
    driver.get(URL)
    #wait for it to load
    sleep(5)
    keepLoading = True
    iterations = 0
    print('')
    print('*******' + Name + '*******')
    while keepLoading:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for days in soup.find_all('div', {'class' : 'trn-gamereport-list__group'}):
            date = days.find('h3', {'class' : 'trn-gamereport-list__title'})
            if date is not None:
                date = date.get_text().lstrip().strip()
                if date == 'Matches Today':
		    #TODO this site doesn't support year so who knows what will happen if you use this beyond 2020
                    date = today.strftime("2020-%m-%d")
                else:
                    month = date[:3]
                    month = str(strptime(month,'%b').tm_mon).zfill(2)
                    day = date[-2:].zfill(2)
		    #TODO this site doesn't support year so who knows what will happen if you use this beyond 2020
                    date = '2020-' + str(month) + '-' + str(day)
                if date < startDate:
                    keepLoading = False
                print(date)
        if keepLoading:
            print('load')
            #scroll down to see the load more matches button
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #find the load more matches button and click
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Load More Matches']"))).click()
            except:
                keepLoading = False
            #wait for them to load
            iterations = iterations + 1
            sleep(5)
            if iterations > 100:
                print('ERROR More than 100 page loads')
                error = True
                break
                

    driver.quit()

    playerIndex += 1
    totalKills = 0
    wins = 0
    games = 0
    top5 = 0
    top10 = 0
    maxKills = 0
    for days in soup.find_all('div', {'class' : 'trn-gamereport-list__group'}):
        date = days.find('h3', {'class' : 'trn-gamereport-list__title'})
        if date is not None:
                date = date.get_text().lstrip().strip()
                if date == 'Matches Today':
                    date = today.strftime("2020-%m-%d")
                    day = date[-2:].zfill(2)
                    month = date[5:7]
                else:
                    month = date[:3]
                    month = str(strptime(month,'%b').tm_mon).zfill(2)
                    day = date[-2:].zfill(2)
                    date = '2020-' + str(month) + '-' + str(day)
                if date > endDate or date < startDate:
                    continue
        print("")
        for matches in days.find_all('div', {'class' : 'match__row'}):
            print(date)
            gameMode = matches.find('span', {'class' : 'match__name'})
            gameMode = gameMode.get_text().lstrip().strip()
            if gameMode == 'BR Solos' or gameMode == 'BR Duos' or gameMode == 'BR Trios' or gameMode == 'BR Quads':
                time = matches.find('span', {'class' : 'match__time'})
                time = time.get_text().lstrip().strip()
                h = time[:2]
                m = time[3:5]
                period = time[-2:]
                if period == 'PM':
                    h = str(int(h) + 12)
                    if h == '24':
                        h = '12'
                else:
                    if h == '12':
                        h = '00'
                dateTimePlayed = datetime.datetime(2020, int(month), int(day), int(h), int(m), 00)
                print('date time: ')
                print(dateTimePlayed)
                if dateTimePlayed > startDateTime and dateTimePlayed < endDateTime:
                    placement = matches.find('div', {'class' : 'match__placement'})
                    placement = placement.get_text().lstrip().strip()
                    placement = placement[:-2]
                    if placement == '1':
                        wins += 1
                    if int(placement) <= 5:
                        top5 += 1
                    if int(placement) <= 10:
                        top10 += 1
                    kills = matches.find('div', {'class' : 'numbers'})
                    numbers = re.compile(r'\d+(?:\.\d+)?')
                    kills = numbers.findall(kills.get_text())
                    kills = kills[0]
                    if int(kills) > maxKills:
                        maxKills = int(kills)
                    totalKills += int(kills)
                    games += 1
                    
                    print("    " + time)
                    print("        " + gameMode)
                    print("        " + 'Finish: ' + placement)
                    print("        " + 'Kills: ' + kills[0])
                    print("")
                else:
                    print(time)
                    print("GAME NOT PLAYED WITHIN LIMITS")
    print('Wins: ' + str(wins))
    print('Kills: ' + str(totalKills))
    print('Games: ' + str(games))
    if games == 0:
        score = 0
        killsPerGame = 0
        winPercentage = 0
    else:
        score = ((25 * wins) + (0.5*totalKills))/games
        print('Score: ' + str(score))
        killsPerGame = totalKills/games
        print('Kills/Game: ' + str(totalKills/games))
        winPercentage = wins/games
    
    data[playerIndex][0] = Name
    data[playerIndex][1] = Location
    data[playerIndex][2] = ID
    data[playerIndex][3] = Email
    data[playerIndex][4] = URL
    data[playerIndex][5] = wins
    data[playerIndex][6] = totalKills
    data[playerIndex][7] = games
    data[playerIndex][8] = score
    data[playerIndex][9] = killsPerGame
    data[playerIndex][10] = winPercentage
    data[playerIndex][11] = top5 + wins
    data[playerIndex][12] = top10 + wins
    data[playerIndex][13] = maxKills

    with open("outputData.csv","w") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',', lineterminator='\n')
        csvWriter.writerows(data)
