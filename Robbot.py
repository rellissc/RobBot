import discord
import random
from discord.ext import commands
import math
import re

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('We are in the following guilds: '+str(bot.guilds))


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def roll(ctx, rollCommand):
    toPrint=''
    diceRolled =[]
    try:
        input=re.search('([1-9][0-9]*d[1-9][0-9]*)(kl*[1-9][0-9]*)*',rollCommand)
        rCommand=str.split(input.groups()[0],'d')
        numOfDice=int(rCommand[0])
        sizeOfDice=int(rCommand[1])
        toPrint+= 'Rolling '+str(numOfDice)+'d'+str(sizeOfDice)
        while numOfDice>0:
            diceRolled.append(random.randrange(1,sizeOfDice+1))
            numOfDice-=1
        diceCounted=diceRolled.copy()
        if(input.groups()[1]!=None):
            keepNumber=input.groups()[1].replace('k','')
            diceCounted.sort()
            operationName=' highest'
            if 'l' in keepNumber:
                keepNumber=keepNumber.replace('l','');
                diceCounted.reverse()
                operationName=' lowest'
            keepNumber=int(keepNumber)
            print(str(keepNumber))
            while keepNumber<len(diceCounted):
                print('popped ' + str(diceCounted.pop(0)))
            toPrint+=', keeping the '+str(keepNumber)+ operationName
        sumOfDice=str(sum(diceCounted))

        ##      sumOfDice+=x
        toPrint+=': '+strDiceRoll(diceRolled,diceCounted,sizeOfDice)+' = '+sumOfDice
        
    except:
        toPrint='Syntax Error: Please check your format'
        pass
    await ctx.channel.send(toPrint)

def strDiceRoll(diceRolled, diceCounted,sizeOfDice):
    toReturn='['
    for die in diceRolled:
        if diceCounted.count(die)>0:
            if int(die)==sizeOfDice:
                toReturn+='**'+str(die)+'**'
            elif int(die)==1:
                toReturn+='*'+str(die)+'*'
            else:
                toReturn+=str(die)
            diceCounted.remove(die)
        else:
            toReturn+='~~'+str(die)+'~~'
        toReturn+=','
    toReturn=toReturn.rstrip(',')
    toReturn+=']'
    return toReturn

@bot.command()
async def groupsplit(ctx, *args):
    coinTuple=parseArgs(args)
    plat=coinTuple[0]
    gold=coinTuple[1]
    silver=coinTuple[2]
    copper=coinTuple[3]
    way=coinTuple[4]
    counter=way
    groupPayout=[]
   
    while counter>0:
        memberPayout= CoinPurse()
        groupPayout.append(memberPayout)
        counter-=1

    while plat>0:
        groupPayout.sort()
        groupPayout[0].addCoin('platinum')
        plat-=1

    while gold>0:
        groupPayout.sort()
        groupPayout[0].addCoin('gold')
        gold-=1

    while silver>0:
        groupPayout.sort()
        groupPayout[0].addCoin('silver')
        silver-=1

    while copper>0:
        groupPayout.sort()
        groupPayout[0].addCoin('copper')
        copper-=1

    await ctx.channel.send(printGroupPurses(groupPayout))


def printGroupPurses(coinPurses):
    toString=''
    counter=0
    for x in coinPurses:
        counter+=1
        toString+='Person '+str(counter)+':'+str(x)+'\n'
    return toString





@bot.command()
async def banksplit(ctx, *args): 
    coinTuple=parseArgs(args)
    plat=coinTuple[0]
    gold=coinTuple[1]
    silver=coinTuple[2]
    copper=coinTuple[3]
    way=coinTuple[4]

    goldtotal = (copper / 100) + (silver / 10) + gold + (plat * 10)
    goldsplit = goldtotal/way
    silverleft = goldsplit * 10 % 10
    copperleft = silverleft * 10 % 10
    extraCopper = round((copperleft -int(copperleft))*way)
    print('Extra copper' + str(extraCopper))
    toPrint = str(way)+' Way Split '
    if(int(goldsplit)>0):
        toPrint+=' Gold: '+str(int(goldsplit))
    if(int(silverleft)>0):
        toPrint+=' Silver: '+str(int(silverleft))
    if(int(copperleft)>0):
        toPrint+=' Copper: '+str(int(copperleft))
    if(extraCopper>0):
        toPrint+=' and ' + str(int(extraCopper))+' extra copper'
    await ctx.channel.send(toPrint)
    print(goldtotal)
    print(silverleft)
    print(copperleft)

def parseArgs(*inputStrings):
  seperator=""
  inputString=seperator.join(*inputStrings)
  inputString=inputString.replace(",","")
  inputString=inputString.replace(" ","")
  inputString=inputString.replace("k","000")
  
  try: 
    gold=re.search('[0-9][0-9]*[gG]',inputString).group(0)
    gold=gold.rstrip('g')
    gold=int(gold) 
  except:
    gold=0
    pass
  try:
    silver=re.search('[0-9][0-9]*[sS]',inputString).group(0)
    silver=silver.rstrip('s') 
    silver=int(silver)
  except:
    silver=0
    pass

  try:
    copper=re.search('[0-9][0-9]*[cC]',inputString).group(0)
    copper=copper.rstrip('c') 
    copper=int(copper)
  except:
    copper=0
    pass

  try:
    plat=re.search('[0-9][0-9]*[pP]',inputString).group(0)
    plat=plat.rstrip('p')  
    plat=int(plat) 
  except:
    plat=0
    pass

  try:
    way=re.search('[0-9][0-9]*way',inputString).group(0)
    way=way.rstrip('way')  
    way=int(way) 
  except:
    way=4
    pass

  return [plat,gold,silver,copper,way]

class CoinPurse:
    
    def __init__(self, platinum=0, gold=0, silver=0, copper=0):
        self.platinum=platinum
        self.gold=gold
        self.silver=silver
        self.copper=copper

    def __lt__(self, value):
        return (self.value() < value.value())
    def __cmp__(self, other):
        return cmp(self.value(), other.value())

    def __str__(self):
        toString='[ '
        if(self.platinum>0):
            toString+='Platinum: '+str(self.platinum)+' '
        if(self.gold>0):
            toString+='Gold: '+str(self.gold)+' '
        if(self.silver>0):
            toString+='Silver: '+str(self.silver)+' '
        if(self.copper>0):
            toString+='Copper: '+str(self.copper)+' '
        toString+='] = '+str(self.value())
        return toString
    

    def value(self):
        val=round(self.platinum*10+self.gold+self.silver/10+self.copper/100,2)
        return val

    def addPlat(self):
        self.platinum+=1

    def addGold(self):
        self.gold+=1

    def addSilver(self):
        self.silver+=1

    def addCopper(self):
        self.copper+=1

    
    def addCoin(self, coinType: str):
        coinDictionary = {'platinum':self.addPlat, 'gold':self.addGold, 'silver':self.addSilver, 'copper':self.addCopper}
        coinDictionary[coinType]()
        



    



bot.run('NjY3MjE3ODQ5MzU3Njk3MDM2.Xh_hiw.6lvWb2TNE5HaJ8mPTPzOXcQBQSs')
#  667217849357697036
