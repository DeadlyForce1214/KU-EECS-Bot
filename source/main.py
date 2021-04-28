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

tarHelpObj = open("TarHelp.txt", "r")
tarHelp = tarHelpObj.read()
tarHelpObj.close()

TOKEN = #Token Goes here

bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print(f'The bot has connected to Discord!')

@bot.command(name='servercheck', help='Checks the cycle servers to see if they are up')
async def checkServers(ctx): 
    commandCycle2 = ['nmap', '-p22', "cycle2.eecs.ku.edu"]
    cycle2up = subprocess.run(commandCycle2, capture_output=True)
    
    cycle2Output = str(cycle2up.stdout)
    cycle2HostUp = cycle2Output.find('Host is up') != -1
    cycle2Open = cycle2Output.find('tcp open  ssh') != -1

    commandCycle3 = ['nmap', '-p22', "cycle3.eecs.ku.edu"]
    cycle3up = subprocess.run(commandCycle3, capture_output=True)
    
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

@bot.command(name='classList', help='Prints out the class list on the EECS wiki')
async def printClassList(ctx):
    await ctx.send(classList)

@bot.command(name='github', help='Prints out the github link for this project')
async def printGitHub(ctx):
    await ctx.send('https://github.com/DeadlyForce1214/KU-EECS-Bot')

@bot.command(name='tarhelp', help='Prints out useful tar information')
async def printTarCommands(ctx):
    await ctx.send(tarHelp)

bot.run(TOKEN)
