from typing import Union
import nextcord
import json
from nextcord.ext import commands
from helper import *
import ast

json_data = json.load(open("config.json", "r"))

bot = commands.Bot(command_prefix=json_data["prefix"], case_insensitive=True, strip_after_prefix=True)

@bot.event
async def on_ready():
    print("Ready!")

@bot.command(name="аниме")
async def anime(ctx: commands.Context):
    animes = do_to_database("SELECT * FROM anime")
    ids = 0
    await ctx.message.delete()

    mess = await ctx.send(embed=BuildEmbed(title=animes[ids][1], desc=animes[ids][2], image=animes[ids][3]))

    def w(emoj: nextcord.reaction, man):
        # print(str(emoj))
        return man.id == ctx.author.id and str(emoj) in ("➡️", "⬅️", "❌", "🔗")

    while True:
        await mess.add_reaction("⬅️")
        await mess.add_reaction("❌")
        await mess.add_reaction("🔗")
        await mess.add_reaction("➡️")
        emoj, man = await bot.wait_for("reaction_add", check=w)
        emoj = str(emoj)
        if emoj == "➡️":
            ids += 1
        elif emoj == "⬅️":
            ids -= 1
        elif emoj == "❌":
            await mess.delete()
            break
        elif emoj == "🔗":
            await ctx.send(f"{ctx.author.mention}-сан, ссылка на аниме \"" + animes[ids][1] + "\". " + animes[ids][4])
        else:
            await mess.delete()
            await ctx.send("Произошла неожиданная ошибка", delete_after=3)
            break

        if ids < 0: ids = len(animes) - 1
        if ids > len(animes) - 1: ids = 0

        await mess.edit(embed=BuildEmbed(title=animes[ids][1], desc=animes[ids][2], image=animes[ids][3]))
        await mess.clear_reactions()

@bot.command(name="фильм")
async def film(ctx: commands.Context):
    animes = do_to_database("SELECT * FROM film")
    ids = 0
    await ctx.message.delete()

    mess = await ctx.send(embed=BuildEmbed(title=animes[ids][1], desc=animes[ids][2], image=animes[ids][3]))

    def w(emoj: nextcord.reaction, man):
        # print(str(emoj))
        return man.id == ctx.author.id and str(emoj) in ("➡️", "⬅️", "❌", "🔗")

    while True:
        await mess.add_reaction("⬅️")
        await mess.add_reaction("❌")
        await mess.add_reaction("🔗")
        await mess.add_reaction("➡️")
        emoj, man = await bot.wait_for("reaction_add", check=w)
        emoj = str(emoj)
        if emoj == "➡️":
            ids += 1
        elif emoj == "⬅️":
            ids -= 1
        elif emoj == "❌":
            await mess.delete()
            break
        elif emoj == "🔗":
            await ctx.send(f"{ctx.author.mention}, ссылка на фильм \"" + animes[ids][1] + "\". " + animes[ids][4])
        else:
            await mess.delete()
            await ctx.send("Произошла неожиданная ошибка", delete_after=3)
            break

        if ids < 0: ids = len(animes) - 1
        if ids > len(animes) - 1: ids = 0

        await mess.edit(embed=BuildEmbed(title=animes[ids][1], desc=animes[ids][2], image=animes[ids][3]))
        await mess.clear_reactions()

bot.run(json_data["token"])
