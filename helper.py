import discord
import datetime
import sqlite3
import json
from time import sleep

json_data = json.load(open("config.json"))

def BuildEmbed(title: str, color: discord.colour.Colour = discord.colour.Colour.green(),
               desc: str = None, image: str = None):
    
    emb = discord.Embed(title=title, colour=color)

    if desc is not None:
        emb.description = desc
    
    if image is not None:
        emb.set_image(url=image)
    
    return emb

def __isFileEmpty(filename: str):
    return open(filename, "r").read() == ""


def create_log(mess: str, code: str = "ok"):
    file = open("log.txt", "a")
    if __isFileEmpty:
        file.write("\n")
        
    out = f"[{code}][{datetime.datetime.now()}]: {mess}"
        
    if code == "ok":
        print(out)
    elif code == "error":
        print(out)
    elif code == "norm":
        print(out)
    else:
        return ValueError
    
    file.write(out)

    file.close()


def start_logging():
    file = open("log.txt", "a")
    
    file.write("\n\n")
    
    file.close()


def do_to_database(command: str, *options):
    dbFilename = "mysqldb.db"
    while True:
        try:
            conn = sqlite3.connect(dbFilename, timeout=1)
            cursor = conn.cursor()
            if options == tuple():
                returnStr = list(cursor.execute(command))
            else:
                returnStr = list(cursor.execute(command, options))
            conn.commit()
            cursor.close()
            conn.close()
            return returnStr
        except sqlite3.OperationalError as e:
            create_log(e, code="error")
            sleep(1)
            continue