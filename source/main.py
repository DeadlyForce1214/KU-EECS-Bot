# bot.py
import os

from discord.ext import commands

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

classFile1 = open("ClassList1.txt", "r")
classList1 = classFile1.read()
classFile1.close()

classFile2 = open("ClassList2.txt", "r")
classList2 = classFile2.read()
classFile2.close()

classFile3 = open("ClassList3.txt", "r")
classList3 = classFile3.read()
classFile3.close()

classDescriptionData = open("ClassDataDesc.txt", "r")
classData = classDescriptionData.read()
classDescriptionData.close()

makeFileObj = open("Makefile.txt", "r")
makeFile = makeFileObj.read()
makeFileObj.close()

tarHelpObj = open("TarHelp.txt", "r")
tarHelp = tarHelpObj.read()
tarHelpObj.close()

TOKEN = 'lol' #The actual token goes here

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

@bot.command(name='classList', help='Prints out the class list on the EECS wiki')
async def printClassList(ctx):
    channel = ctx.channel
    await channel.send(classList1)
    await channel.send(classList2)
    await channel.send(classList3)

@bot.command(name='classInfo', help='Prints the summary of the class')
async def printClassInfo(ctx, majorName, classNumber):
    if majorName == "EECS":
        classNameString = majorName + ' ' + classNumber
        startIndex=classData.find('<' + classNameString + '>')
        if startIndex:
            titleEndIndex = classData.find('\n',startIndex)
            if titleEndIndex:
                titleString=classData[startIndex+2+len(classNameString):titleEndIndex]
                endIndex = classData.find('</' + classNameString + '>')
                if endIndex:
                    await ctx.send("**__Class Info for " + classNameString + ": " + titleString + "__**\n" + classData[titleEndIndex:endIndex])
                else:
                    await ctx.send("Error: Could not find end index")
            else:
                await ctx.send("Error: Could not find the end of the title")
        else:
            await ctx.send("Error: Could not find the class tag")
    else:
        await ctx.send('No support for non EECS classes are currently available')


@bot.command(name='github', help='Prints out the github link for this project')
async def printGitHub(ctx):
    await ctx.send('https://github.com/DeadlyForce1214/KU-EECS-Bot')

@bot.command(name='tarhelp', help='Prints out useful tar information')
async def printTarCommands(ctx):
    await ctx.send(tarHelp)

#TODO make this work in the future better. Probably end up writing a linter for this
#@bot.command(name='memcheck', help='Checks for non deleted pointers')
#async def memCheck(ctx):
#    lines= list()
#    types=['int','double','string','char','long']
#    pointers = list()
#
#    msg = ctx.message.content
#    lastIndex=msg.find('```c++')
#    if lastIndex == -1:
#        await ctx.send('Did not find the code. Did you put it into a code block? Put it inside of a codeblock marked as c++ please!')
#        return
#    else:
#        lastIndex+=len('```c++')
#    
#    while True:
#        nextCloseBacketIndex=msg.find('}',lastIndex+1)
#        nextOpenBracketIndex=msg.find('}',lastIndex+1)
#        nextSemiColonIndex=msg.find(';',lastIndex+1)
#        if nextIndex == -1:
#            break
#        toAdd=msg[lastIndex:nextIndex]
#        lines.append(toAdd.strip())
#        lastIndex=nextIndex+1
#
#    for i in lines:
#        if i.find('*') != -1:
#            for j in types:
#                startIndex=i.find(j+'*')
#                if startIndex == 0:
#                    startIndex= i.find(' ',startIndex)
#                    if startIndex != -1:
#                        endIndex=i.find('=')
#                        if endIndex == -1:
#                            endIndex=i.find(';')
#                        if endIndex == -1:
#                            await ctx.send("Weird, couldn't find the end of this: " + i)
#                            break
#                        name=i[startIndex+len(j)+1:endIndex].strip()
#                        pointers.append(name)
#                elif startIndex != -1:
#                    print('The start index was not the beginning?')
#        if i.find('delete') != -1:
#            for j in pointers:
#                if i.find(j) != -1:
#                    pointers.remove(j)
#
#    numRemaining = len(pointers)
#    if numRemaining != 0:
#        toPrint='Not all pointers were detected deleted! Pointers that have issues:'
#        for i in pointers:
#            toPrint+='\n'+i
#        await ctx.send(toPrint)
#    else:
#        await ctx.send('All pointers seem to have been deleted')

@bot.command(name='reload',help='Admin command to reload the data files')
async def reloadFiles(ctx):
    if ctx.author.guild_permissions.administrator:
        print("Reloading data files...")
        classFile1 = open("ClassList1.txt", "r")
        classList1 = classFile1.read()
        classFile1.close()

        classFile2 = open("ClassList2.txt", "r")
        classList2 = classFile2.read()
        classFile2.close()

        classFile3 = open("ClassList3.txt", "r")
        classList3 = classFile3.read()
        classFile3.close()

        classDescriptionData = open("ClassDataDesc.txt", "r")
        classData = classDescriptionData.read()
        classDescriptionData.close()

        makeFileObj = open("Makefile.txt", "r")
        makeFile = makeFileObj.read()
        makeFileObj.close()

        tarHelpObj = open("TarHelp.txt", "r")
        tarHelp = tarHelpObj.read()
        tarHelpObj.close()
        await ctx.send('Data has been reloaded!')
    else:
        await ctx.send("Command cannot be executed. Lacking sufficient permissions.")

bot.run(TOKEN)
