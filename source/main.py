# bot.py
import os

from discord.ext import commands

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

classFile = open("ClassList.txt", "r")
classList = classFile.read()
classFile.close()

makeFileObj = open("Makefile.txt", "r")
makeFile = makeFileObj.read()
makeFileObj.close()

TOKEN = #Token goes here

bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print(f'The bot has connected to Discord!')

@bot.command(name='servercheck', help='Checks the cycle servers to see if they are up')
async def checkServers(ctx):
    #This is commented out since the EECS servers do not appreciate pings.
    #param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    #commandCycle2 = ['ping', param, '1', "cycle2.eecs.ku.edu"]
    #cycle2up = subprocess.call(commandCycle2) == 0

    #commandCycle3 = ['ping', param, '1', "cycle3.eecs.ku.edu"]
    #cycle3up = subprocess.call(commandCycle3) == 0

    #await ctx.send('Cycle2 Servers are up: ' + str(cycle2up) + '\nCycle3 Servers are up: ' + str(cycle3up))
    await ctx.send('For now, the cycle servers seem to be unable to be pinged. They may reject this protocol on the servers.')


@bot.command(name='makefile', help='Prints a makefile that is supplied by the 268 wiki')
async def printMakeFile(ctx):
    await ctx.send(makeFile)

@bot.command(name='link', help='Links a class wiki page. Syntax is -link [Class#]. Example: -link 168. Available class list: \n' + classList)
async def sendLink(ctx, classNumber):
    await ctx.send('https://wiki.ittc.ku.edu/ittc_wiki/index.php/EECS' + str(classNumber))

@bot.command(name='classList', help='Prints out the class list on the EECS wiki')
async def printClassList(ctx):
    await ctx.send(classList)

bot.run(TOKEN)
