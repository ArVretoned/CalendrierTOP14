import os
import ics
import pytz
import locale
import argparse
import requests
from icalendar import Event
from caldav import DAVClient
from bs4 import BeautifulSoup
from tkinter import filedialog, Tk
from datetime import datetime, timedelta
from dotenv import find_dotenv, dotenv_values

if os.name == "posix":
  locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
if os.name == "nt":
  locale.setlocale(locale.LC_TIME, "french")

def get_data(env_var):
  ret = []
  print("Récupération des matchs")
  for page_number in range(1,27):
    print(f"  |--> Journée {page_number:02d} ...", end=' ')
    try:
      url = f"{env_var['URL_NLR']}/{env_var['SAISON']}/j{page_number}"
      htmldata = requests.get(url).text
      soup = BeautifulSoup(htmldata,features="html.parser")
      results_iner = soup.find("div", class_="calendar-results__inner")
      all_div = results_iner.find_all("div", recursive=False)
      passed = False
      for line_div in all_div:
        if line_div.has_attr('class') and line_div['class'][0] == 'calendar-results__fixture-date':
          day = line_div.text.replace('\n','').rstrip().lstrip()
          parts = day.split(" ", 1)[1]+f" {env_var['SAISON'].split('-')[0]}"
          dt = datetime.strptime(parts, "%d %B %Y")
          if dt.month < 8:
            dt = dt.replace(year=int(env_var['SAISON'].split('-')[1]))
          if dt < datetime.today():
            passed = True
        if passed == False:
          if line_div.has_attr('class') and line_div['class'][0] == 'calendar-results__line':
            for div in line_div.find_all("div", class_="match-line__wrapper"):
              team1 = div.find_all("div", class_="club-line club-line--reversed club-line--table-format")[0].find_all("a")[0].text.replace('\n','').rstrip().lstrip()
              team2 = div.find_all("div", class_="club-line club-line--table-format")[0].find_all("a")[0].text.replace('\n','').rstrip().lstrip()
              hour = div.find("div", class_="match-line__broadcast-infos").find("p", class_="match-line__time").text.replace('\n','').rstrip().lstrip()
              parts = day.split(" ", 1)[1] + f" {env_var['SAISON'].split('-')[0]} " + hour
              dt = pytz.timezone('Europe/Paris').localize(datetime.strptime(parts, "%d %B %Y %Hh%M"))
              if dt.month < 8:
                dt = dt.replace(year=int(env_var['SAISON'].split('-')[1]))
              str_start = dt.strftime("%Y-%m-%d %H:%M:%S%z")
              str_end = (dt+timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S%z")
              ret.append((team1,team2,str_start,str_end))
      print('matchs récupérés') if passed == False else print("journée passée")
    except:
      print('heures des matchs pas encore publiées')
  return ret

def write_local_calendar(elt):
  try:
    print('Construction du clendrier ...',end=' ')
    c = ics.Calendar()
    for evt in elt:
      team1 = evt[0]
      team2 = evt[1]
      str_start = evt[2]
      str_end = evt[3]
      e = ics.Event()
      e.name = team1 + " vs " + team2
      e.begin = str_start
      e.end = str_end
      c.events.add(e)
    print('OK')
  except:
    print('KO')
    return
  try:
    print('Ecriture du calendrier ...',end=' ')
    root = Tk()
    root.withdraw()
    filespath = filedialog.asksaveasfilename(title="Enregistrer le fichier",initialfile="top14.ics")
    with open(filespath, 'w', encoding='utf-8', newline='') as my_file:
      my_file.writelines(c.serialize_iter(),)
    print('OK')
    return
  except:
    print('KO')
    return

def add_oline_calendar(data,env_var):
  try:
    print("Connexion au calendrier ...", end=' ')
    url = env_var["URL_CLOUD"]
    username = env_var["UTILISATEUR"]
    password = env_var["CLE"]
    client = DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    for elt in calendars:
      if elt.name == "Sport":
        calendar = elt
    print('OK')
  except:
    print('KO')
    return
  try:
    print("Récupération des matchs déjà dans le calendrier ...", end=' ')
    games_already_in_cal = []
    for elt in calendar.search():
      events = Event.from_ical(elt.data)
      for component in events.walk():
        if component.name == "VEVENT":
            games_already_in_cal.append(str(component['SUMMARY']))  
    print('OK')
  except:
    print('KO')
    return
  try:
    print("Ajout des nouveaux matchs ...", end=' ')
    new_game_cpt = 0
    for evt in data:
      team1 = evt[0]
      team2 = evt[1]
      str_start = evt[2]
      str_end = evt[3]
      summary=team1 + " vs " + team2
      if summary not in games_already_in_cal:
        calendar.save_event(
          dtstart=datetime.strptime(str_start,"%Y-%m-%d %H:%M:%S%z"),
          dtend=datetime.strptime(str_end,"%Y-%m-%d %H:%M:%S%z"),
          summary=summary)
        new_game_cpt+=1
    print(f"OK, {new_game_cpt} match(s) ajouté(s)")
  except:
    print('KO')
    return

def main(**kwargs):
  print(r"""
  ____      _                _      _             _____ ___  ____  _ _  _   
 / ___|__ _| | ___ _ __   __| |_ __(_) ___ _ __  |_   _/ _ \|  _ \/ | || |  
| |   / _` | |/ _ \ '_ \ / _` | '__| |/ _ \ '__|   | || | | | |_) | | || |_ 
| |__| (_| | |  __/ | | | (_| | |  | |  __/ |      | || |_| |  __/| |__   _|
 \____\__,_|_|\___|_| |_|\__,_|_|  |_|\___|_|      |_| \___/|_|   |_|  |_|  
""")
  try:
    env_var = dotenv_values(find_dotenv())
    if not any(kwargs.values()):
      parser = argparse.ArgumentParser(description="")
      parser.add_argument("--local", action="store_true", help="Ecrire le calendrier dans un fichier ics local", required=False)
      parser.add_argument("--enligne", action="store_true", help="Ecrire le calendrier dans dans un agenda en ligne", required=False)
      args = parser.parse_args()
      kwargs = vars(args)
      if not any(kwargs.values()): # Toutes les valeurs sont False, None ou absentes.
        kwargs["local"] = True
    data = get_data(env_var)
    if kwargs.get("local", False):
      write_local_calendar(data)
    if kwargs.get("enligne", False):
      add_oline_calendar(data,env_var)
  except Exception as e:
    print(e)

if __name__ == '__main__':
  main()