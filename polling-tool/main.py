from worker import GameWorker
from config import session, STEAM_API_KEY, engine

worker = GameWorker(session, engine, STEAM_API_KEY)
worker.run()