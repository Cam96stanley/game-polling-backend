import os
import sys
import re
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api.models.app import App, AppPrice

class GameWorker:
  def __init__(self, session, db_engine, steam_api_key):
    self.session = session
    self.engine = db_engine
    self.steam_key = steam_api_key
    
  def add_game(self, name):
    search_term = name.replace(" ", "+")
    url = f"https://store.steampowered.com/search/?term={search_term}"
    
    headers = {
      "User-Agent": "Mozilla/5.0"
    }
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    match = re.search(r"/app/(\d+)/", res.text)
    if not match:
      return None
    
    appid = int(match.group(1))
    self.add_to_db(appid, name)
    
  def fetch_price(self, appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    
    app_data = data[str(appid)]
    if not app_data["success"]:
      return None
    
    price = app_data["data"]["price_overview"]["final"]
    print(price)
    self.add_price(appid, price)
  
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
      
    self.fetch_price(appid)
    
  def add_price(self, appid, price):
    existing = self.session.query(AppPrice).filter_by(app_id=appid).first()
    if existing:
      existing.price = price
    else:
      self.session.add(AppPrice(app_id=appid, price=price))
    self.session.commit()
  
  def run(self):
    self.add_game("elden ring")