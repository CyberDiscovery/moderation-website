from flask import Flask, render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session
from moderationwebsite.constants import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI
from os import environ

app = Flask(__name__)
app.secret_key = environ.get("FLASKSECRET")
app.config["DISCORD_CLIENT_ID"] = DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = DISCORD_CLIENT_SECRET
app.config["DISCORD_REDIRECT_URI"] = DISCORD_REDIRECT_URI

discordoauth = DiscordOAuth2Session(app)


def is_authenticated(user):
    guilds = discordoauth.fetch_guilds()
    guild_dict = {}
    for i in guilds:
        guild_dict[i.id] = i

    if 409851296116375565 in guild_dict.keys():
        perms = guild_dict[409851296116375565].permissions_value
        print(perms)
        if perms is 2147483647:
            return 1
        else:
            return 0
    else:
        return 0


@app.route("/home/")
def home():
    user = discordoauth.fetch_user()
    authed = is_authenticated(user)
    print(authed)
    return f"{user.name}"


@app.route("/callback/")
def callback():
    discordoauth.callback()
    return redirect(url_for(".home"))


@app.route("/login/")
def login():
    return discordoauth.create_session()


@app.route("/")
def start():
    try:
        user = discordoauth.fetch_user()
        return redirect(url_for(".home"))
    except:
        return redirect(url_for(".login"))


@app.errorhandler(404)
def notfound(e):
    return render_template("404.html")


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html")


@app.errorhandler(410)
def deleted(e):
    return render_template("410.html")


@app.errorhandler(500)
def servererror(e):
    return render_template("500.html")