import csv
import json
import requests
import six

from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate
from selenium import webdriver
import pandas as pd

driver = webdriver.Opera(executable_path='C:/Users/Rajinthan/Desktop/operadriver_win64/operadriver.exe')
origin = 'https://www.espncricinfo.com'
url ='https://www.espncricinfo.com/player/team/sri-lanka-8/caps/one-day-international-2'

def translate_text(text):
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language='ta')
    return result["translatedText"]

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html)
detail_content = soup.find_all("div", {"class": "d-flex px-4 player-row"})

all_player_url=[]
for td in detail_content:
  ass = td.find_all('a')
  player_url = origin + ass[1].get('href')
  all_player_url.append(player_url)
print(len(all_player_url))
data=[]

for url in all_player_url:
  r = requests.get(url)
  c = r.content
  soup = BeautifulSoup(c)
  detail_content = soup.find('div', attrs = {'class': 'player_overview-grid'})
  player_role = soup.find_all('h5', attrs = {'class': 'border-bottom-gray-300 m-0 pl-3 pb-2 table-header'})
  player_stats = soup.find_all('span', attrs = {'class': 'out-padding'})
  try:
    title = detail_content.find_all('p')
    content = detail_content.find_all('h5')
  except:
    print(i,0)
    continue
  player={}
  for j in range (len(title)):
    if title[j].get_text() == "Full Name":
      player["Name"] = translate_text(content[j].get_text())
    elif title[j].get_text() == "Born":
      player["DOB"] = translate_text(content[j].get_text().rsplit(",",1)[0])
      player["BirthPlace"] = translate_text(content[j].get_text().rsplit(",",1)[1])
    elif title[j].get_text() == "Age":
      player["Age"] = content[j].get_text().split(" ")[0].strip('y')
    elif title[j].get_text() == "Batting Style":
      player["Batting Style"] = translate_text(content[j].get_text().rsplit(" ",1)[0])
    elif title[j].get_text() == "Bowling Style":
      player["Bowling Style"] = translate_text(content[j].get_text()+" bowler").rsplit(" ",1)[0]
    elif title[j].get_text() == "Playing Role":
      player["Playing Role"] = translate_text(content[j].get_text())
    elif title[j].get_text() == "Education":
      player["Education"] = translate_text(content[j].get_text())

  if player_role[0].get_text() == "Bowling":
    count = 0
    for i in range (len(player_stats)):
      if player_stats[i].get_text() == "ODI":
        count +=1
      if player_stats[i].get_text() == "ODI" and count == 1:
        player["Matches"] = player_stats[i+1].get_text()
        player["Innings"] = player_stats[i+2].get_text()
        player["Wickets"] = player_stats[i+5].get_text()
        player["BBM"] = player_stats[i+6].get_text()
      
      if player_stats[i].get_text() == "ODI" and count == 2:
        player["Runs"] = player_stats[i+4].get_text()
        player["Highscore"] = player_stats[i+5].get_text()
        player["50s"] = player_stats[i+10].get_text()
        player["100s"] = player_stats[i+9].get_text()

  else:
    count = 0
    for i in range (len(player_stats)):
      if player_stats[i].get_text() == "ODI":
        count +=1
      if player_stats[i].get_text() == "ODI" and count == 1:
        player["Matches"] = player_stats[i+1].get_text()
        player["Innings"] = player_stats[i+2].get_text()
        player["Runs"] = player_stats[i+4].get_text()
        player["Highscore"] = player_stats[i+5].get_text()
        player["50s"] = player_stats[i+10].get_text()
        player["100s"] = player_stats[i+9].get_text()

      if player_stats[i].get_text() == "ODI" and count == 2:
        player["Wickets"] = player_stats[i+5].get_text()
        player["BBM"] = player_stats[i+6].get_text()

  data.append(player)
  print(player)

# with open('raw_data.json', 'w', encoding='utf-8') as f:
#   json.dump(data, f, ensure_ascii=False)
#   f.write("\n") 

df = pd.DataFrame(data)
df.to_excel("raw_data.xlsx",index=False) 