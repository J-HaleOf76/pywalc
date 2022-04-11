import pywal
import json
import os
from app import app
from flask import render_template
from flask import request
import shutil

HOME = pywal.settings.HOME
CACHE_DIR = pywal.settings.CACHE_DIR
MODULE_DIR = pywal.settings.MODULE_DIR
CONF_DIR = pywal.settings.CONF_DIR

shutil.copy(os.path.join(CACHE_DIR,"colors.json"), "backup.json")

def reload(data):
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all", methods=["GET"])
def getAll():
    info = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
    return json.dumps(info)

@app.route("/reset", methods=["GET"])
def reset():
    backup = open("backup.json")
    data = json.load(backup)
    reload(data)

    return json.dumps({"sucess": True, "message": "colors has been update"})


@app.route("/color", methods=[ "POST"])
def changeColor():
    if request.method == "POST":
        data = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
        colors = request.get_json()
        data['colors'] = colors
        reload(data)

        return json.dumps({"sucess": True, "message": "colors has been update"})

@app.route("/theme",methods=["GET"])
def theme():
    dark_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "dark"))
    dark_themes  = [theme.split('.')[0] for theme in dark_themes]

    light_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "light"))
    light_themes  = [theme.split('.')[0] for theme in light_themes]

    return json.dumps(
        {
            "dark": dark_themes,
            "light": light_themes
        }
    ) 

@app.route("/theme",methods=["POST"])
def changeTheme():
    theme = request.get_json()
    option = "" if theme['dark'] else "-l"
    command = "wal -q " + option + " --theme " + theme['name']
    os.system(command)  
    data = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
    reload(data)
    return json.dumps({"sucess": True, "message": "colors has been update"})

@app.route('/uploadWallpaper', methods=['POST'])
def uploadWallpaper():
    files = request.files.getlist("images")
    for file in files:
        file.save('/home/png/code/pwy/localhost/app/static/wallpapers/' + file.filename.split("/")[1])
    return json.dumps({"sucess": True, "message": "colors has been update"})


@app.route("/wallpaper", methods=["GET"])
def getWallpaper():
    wallpapers = os.listdir("./app/static/wallpapers")
    return json.dumps(wallpapers)


@app.route("/wallpaper", methods=["POST"])
def changeWallpaper():
    wallpaper = request.get_json()
    path = os.path.join("./app/static/wallpapers", wallpaper)
    image = pywal.image.get(path)
    pywal.wallpaper.change(image)

    return json.dumps(wallpaper)

