from os import environ

from flask import Flask, redirect, render_template, url_for
from flask_discord import DiscordOAuth2Session

from moderationwebsite.constants import (
    DISCORD_CLIENT_ID,
    DISCORD_CLIENT_SECRET,
    DISCORD_REDIRECT_URI,
)

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


@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", title="Forbidden", body="Wait a second, you're not Tref!")


@app.errorhandler(404)
def notfound(e):
    return render_template("error.html", title="Page Not Found", body="Silly Ana, this isn't your k-pop fanpage.")


@app.errorhandler(500)
def servererror(e):
    return render_template("error.html", title="Internal Server Error", body="It seems you've angered Beano. Make him fix this.")
