# Steam Price Tracking Tool

This is a tracking tool used to track current game prices from Steam and notify users when prices drop below a price chosen by the user. The tool is split into two parts, the API and the Worker, denoted by the root directories _api_ and _polling-tool_. The contents of which are as follows:

## API

The api directory contains the Flask backend, including database models and app initialization. This serves as the central API for the project, providing database access for the worker and future frontend.

## Polling-Tool

This directory currently hosts the config where .env variables are being imported and the db engine is being instantiated. The worker file is where the worker is located and contains all the methods for pulling data from steam and saving it to the database. The main file is where the worker is started.

### The Worker

Worker methods are as follows:

- **add_game:** Searches the Steam search page for the game the user wishes to track and pulls out the _appid_ of the game.

- **fetch_price:** Sends a request to the Steamworks endpoint and pulls out the current price of the tracked game.

- **add_to_db:** Adds the appid and name of the game being searched to the _App_ table in order to allow for less scraping of the actual Steam search page in situations where another user wishes to track the same game. The method does check for duplications to prevent duplicate errors. This method will be run periodically to ensure the app Id's are up to date.

- **add_price:** Adds the current price to the _AppPrice_ table to allow for less requests to the SteamWorks endpoint. This method will be run on a schedule to pull current data every 6 hours during normal periods and every hour during a sales period.

#### Features to come

- methods to take a user chosen price range, compare it to the current price, and determine if the price of the game has gone within the users price range.

- methods to notify users when price has reached their range.

- more to come...
