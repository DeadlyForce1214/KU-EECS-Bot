# bot.py
import os
import json
import difflib

from discord.ext import commands

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

majorClassesDict = {}
makeFile = ""
classData = ""
tarHelp = ""

def load():
    with os.scandir("Majors/") as entries:
        for entry in entries:
            majorName = entry.name
            filename = "Majors/" + entry.name  + "/data.json"
            print(filename)
            with open(filename) as json_file:
                print("Loaded data for " + entry.name)
                data = json.load(json_file)
                majorClassesDict[majorName] = data

    makeFileObj = open("Makefile.txt", "r")
    makeFile = makeFileObj.read()
    makeFileObj.close()

    tarHelpObj = open("TarHelp.txt", "r")
    tarHelp = tarHelpObj.read()
    tarHelpObj.close()

load()

TOKEN = #Token goes here

bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print(f'The bot has connected to Discord!')

@bot.command(name='servercheck', help='Checks the cycle servers to see if they are up')
async def checkServers(ctx): 
    commandCycle2 = ['nmap', '-p22', "cycle2.eecs.ku.edu"]
    cycle2up = subprocess.run(commandCycle2, capture_output=True,timeout=5)
    
    cycle2Output = str(cycle2up.stdout)
    cycle2HostUp = cycle2Output.find('Host is up') != -1
    cycle2Open = cycle2Output.find('tcp open  ssh') != -1

    commandCycle3 = ['nmap', '-p22', "cycle3.eecs.ku.edu"]
    cycle3up = subprocess.run(commandCycle3, capture_output=True,timeout=5)
    
    cycle3Output = str(cycle3up.stdout)
    cycle3HostUp = cycle3Output.find('Host is up') != -1
    cycle3Open = cycle3Output.find('tcp open  ssh') != -1
    
    await ctx.send('Cycle2 Servers are up: ' + str(cycle2HostUp) +  ', SSH Connection up: ' + str(cycle2Open) + '\nCycle3 Servers are up: ' + str(cycle3HostUp) + ', SSH Connection up: ' + str(cycle3Open))

@bot.command(name='makefile', help='Prints a makefile that is supplied by the 268 wiki')
async def printMakeFile(ctx):
    await ctx.send(makeFile)

@bot.command(name='link', help='Links a class wiki page. Syntax is =link [Class#]')
async def sendLink(ctx, classNumber):
    await ctx.send('https://wiki.ittc.ku.edu/ittc_wiki/index.php/EECS' + str(classNumber))

@bot.command(name='classList', help='Prints out the class list for the supplied major. Usage is =classList [major]. IE: =classList eecs')
async def printClassList(ctx, major):
    channel = ctx.channel
    majorAdjusted = str.upper(major)
    if majorClassesDict[majorAdjusted]:
        dict = majorClassesDict[majorAdjusted]
        toPrint = "**__Class list for " + majorAdjusted + '__**```\n'
        for key in dict:
            entry = '\n' + key
            tmp = toPrint + entry
            if len(tmp) >= 1997:
                await channel.send(toPrint + "```")
                toPrint = "```\n"
            else:
                toPrint += entry
        await channel.send(toPrint + "```")
    else:
        await ctx.send("Cannot find data for major " + majorAdjusted)

@bot.command(name='classInfo', help='Prints the summary of the class')
async def printClassInfo(ctx, majorName, *, args):
    majorAdjusted = str.upper(majorName)
    if majorClassesDict[majorAdjusted]:
        dict = majorClassesDict[majorAdjusted]
        adjustLength = len(majorName)+1
        found=False
        if len(args) == 3:
            for key in dict:
                if key[adjustLength:adjustLength + 3] == args:
                    await ctx.send("**__Class Info for " + key + "__**\n" + dict[key])
                    found=True
                    break

        if not found:
            matches = difflib.get_close_matches(str(args), dict.keys(), 1, 0.25)
            if len(matches) > 0:
                await ctx.send("**__Class Info for " + matches[0] + "__**\n" + dict[matches[0]])
            else:
                await ctx.send("No match found")

@bot.command(name='github', help='Prints out the github link for this project')
async def printGitHub(ctx):
    await ctx.send('https://github.com/DeadlyForce1214/KU-EECS-Bot')

@bot.command(name='tarhelp', help='Prints out useful tar information')
async def printTarCommands(ctx):
    await ctx.send(tarHelp)

@bot.command(name='reload',help='Admin command to reload the data files')
async def reloadFiles(ctx):
    if ctx.author.guild_permissions.administrator:
        print("Reloading data files...")
        load()
        print("Reload successful!")
        await ctx.send("Reload of files was successful!")
    else:
        await ctx.send("Command cannot be executed. Lacking sufficient permissions.")

bot.run(TOKEN)
