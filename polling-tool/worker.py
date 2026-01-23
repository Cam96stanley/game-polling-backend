import os
import sys
import re
from bs4 import BeautifulSoup
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api.models.app import App, AppPrice

class GameWorker:
  def __init__(self, session, db_engine, steam_api_key):
    self.session = session
    self.engine = db_engine
    self.steam_key = steam_api_key
    
  def find_candidate_appids(self, name):
    search_term = name.replace(" ", "+")
    url = f"https://store.steampowered.com/search/?term={search_term}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.select("a.search_result_row")
    
    appids = []
    for row in results[:5]:
      match = re.search(r"/app/(\d+)/", row["href"])
      if match:
        appids.append(int(match.group(1)))
        
    return appids
  
  def validate_appids(self, appid, expected_name):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    res = requests.get(url)
    res.raise_for_status()
    
    data = res.json()
    app = data[str(appid)]
    
    if not app["success"]:
      return False
    
    actual_name = app["data"]["name"].lower()
    return expected_name.lower() == actual_name
    
  def add_game(self, name):
    candidate_ids = self.find_candidate_appids(name)
    
    for appid in candidate_ids:
      if self.validate_appids(appid, name):
        print(f"Validated appid: {appid}")
        self.add_to_db(appid, name)
        return
      
    print("No valid appid found for:", name)
    
  def fetch_price(self, appid, name):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    
    app_data = data[str(appid)]
    if not app_data["success"]:
      return None
    
    price = app_data["data"]["price_overview"]["final"]
    print(price)
    self.add_price(appid, price, name)
  
  def add_to_db(self, appid, name):
    existing = (
      self.session.query(App)
      .filter_by(app_id=appid)
      .first()
    )
    
    if existing:
      print(f"{name} already exists in database")
    else:
      game = App(
        app_id=appid,
        name=name
      )
      
      self.session.add(game)
      self.session.commit()
      print("Game added to database")
      
    self.fetch_price(appid, name)
    
  def add_price(self, appid, price, name):
    existing = self.session.query(AppPrice).filter_by(app_id=appid).first()
    if existing:
      existing.price = price
    else:
      self.session.add(AppPrice(app_id=appid, price=price, name=name))
    self.session.commit()
    
  def get_price(self, name):
    game = self.session.query(AppPrice).filter_by(name=name).first()
    if game:
      formated_price = game.price / 100
      print(f"${formated_price}")
  
  def run(self):
    game = input("Enter the game you want to track: ")
    # self.add_game(game)
    self.get_price(game)