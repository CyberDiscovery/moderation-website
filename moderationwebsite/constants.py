from os import environ

DISCORD_CLIENT_ID = environ.get("DISCORDCLIENTID")
DISCORD_CLIENT_SECRET = environ.get("BOT_TOKEN")
DISCORD_REDIRECT_URI = "http://127.0.0.1:5000/callback/"
