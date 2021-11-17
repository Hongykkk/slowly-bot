import discord
from bs4 import BeautifulSoup
import urllib.parse as parse
from urllib.request import *
from discord import channel
from discord.utils import get
from discord.ext import commands
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import gspread

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials1 = ServiceAccountCredentials.from_json_keyfile_name(
        './gkey/halogen-valve-307800-cf91cf86f772.json', scope)
gc = gspread.authorize(credentials1)
Calendar=gc.open("pythonbot").worksheet('Calendar')
Schedule=gc.open("pythonbot").worksheet('Schedule')



cred = credentials.Certificate("./slowly-b1ae9-firebase-adminsdk-b683r-4b288d66fa.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://slowly-b1ae9-default-rtdb.firebaseio.com/'
})


data = db.reference('')


client = commands.Bot(command_prefix='라이더')

raidlist = []

def dbsave(list,date):
    
    doc_ref = data.child('raid').child(date)
    doc_ref.set(list)
def dbread():
    users_ref = data.child('raid')
    docs = users_ref.get()
    return docs
def dbdelete(date):
    users_ref = data.child('raid').child(date)
    users_ref.delete()

def crawl(Id):
    url = "https://lostark.game.onstove.com/Profile/Character/" + parse.quote(Id)
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")
    list_char = []
    tmp = bsObject.select_one('div.profile-character-list').select('ul>li>span>button>span')

    for n in tmp:
        name = n.text
        url = "https://lostark.game.onstove.com/Profile/Character/" + parse.quote(name)
        html = urlopen(url)
        bsObject = BeautifulSoup(html, "html.parser")
        serv = bsObject.find_all(attrs={"class": "profile-character-info__server"})
        job = bsObject.find('img', "profile-character-info__img")
        itemlv = bsObject.find_all("div", {"class": "level-info2__item"})[0].find_all("span")[1]
        list_char.append([str(serv[0].get_text())[1:], name, job.attrs['alt'], float(itemlv.get_text()[3:].replace(',', ''))])
    list_char = sorted(list_char, key = lambda x : -1*x[3])
    
    return list_char

async def on_ready(self):
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print(client.user)
    print('------')

async def on_message(self, message):
    await client.process_commands(message)

#@clinet.command(name="역할", pass_context=True)
#async def roles(ctx,role):
@client.command(pass_context=True)
async def elsecommand(ctx,command):
    channel=ctx.channel
    if(channel.name== "봇테스트채널"):
        await ctx.message.delete()
        embed= discord.Embed(title="잘못된 명령어입니다.")
        msg = await ctx.channel.send(embed=embed)
@client.command(name="인증" ,pass_context=True)
async def cha(ctx,user):
    hash = ctx.author
    member = ctx.message.author
    channel = ctx.channel
    print(hash)
    if(channel.name == "봇테스트채널"):
        print("입장")
        print(ctx.message.content)
        if("인증" in ctx.message.content):
            await ctx.message.delete()
        else:
            await ctx.message.delete()
            embed= discord.Embed(title="잘못된 명령어입니다.")
            msg = await ctx.channel.send(embed=embed)
            return 0
        await hash.edit(nick=user)
        embed= discord.Embed(title="역할 설정중입니다 잠시만 기다려주세요.")
        await member.add_roles(get(ctx.guild.roles, name='길드원'))
        msg = await ctx.channel.send(embed=embed)
        ret =crawl(user)
        for ch in ret:
            if(ch[0]=="아브렐슈드"):
                print("캐릭터명 : " + ch[1])
                print("클래스 : " + ch[2])
                print("레벨 : " + str(ch[3]))
                if(int(ch[3])>=1490):
                    await member.add_roles(get(ctx.guild.roles, name='아브노말'))
                if(int(ch[3])>=1460):
                    await member.add_roles(get(ctx.guild.roles, name='비아하드'))
                elif(int(ch[3])>=1430):
                    await member.add_roles(get(ctx.guild.roles, name='비아노말'))
                if(int(ch[3])>=1445):
                    await member.add_roles(get(ctx.guild.roles, name='발탄하드'))
                elif(int(ch[3])>=1415):
                    await member.add_roles(get(ctx.guild.roles, name='발탄노말'))
                if(int(ch[3])>=1430):
                    await member.add_roles(get(ctx.guild.roles, name='데자뷰'))
                if(int(ch[3])>=1385):
                    await member.add_roles(get(ctx.guild.roles, name='리허설'))
    
        await msg.delete()
        msgstring = member.display_name +"에게 역할이 적용되었습니다."
        embed = discord.Embed(description= msgstring)
        await ctx.channel.send(embed=embed)


# 라이더모집 10월6일 9시 발탄노말
@client.command(name="모집", pass_context=True)
async def party(ctx,date1,date2,raid):
    channel=ctx.channel
    temp = {
       
        '파티' : raid,
        '딜러' : ' ',
        '서폿' : ' ',
    }
    dbsave(temp,date1+date2)
    list=dbread()
    embed = discord.Embed(title="레이드 현황")
    for k,v in list.items():
        print(k)
        print(v)
        embed.add_field(name=k, value=v['파티']+" 파티 "  ,inline=False)
        embed.add_field(name="딜러", value=v['딜러']+"d")
        embed.add_field(name="서폿", value=v['서폿']+"d")
    await channel.send(embed=embed)
    addraid=Schedule.find(date1)
    update=Schedule.cell(addraid.row,addraid.col+2)
    Schedule.update_cell(addraid.row,addraid.col+2, update.value +"\n" + date2+raid )
    # embed = discord.Embed(title="레이드 현황")
    # raidlist.append(temp2)
    # count=0
    # for temp in raidlist:
    #     embed.add_field(name=str(count+1)+"번파티", value=temp[0]+" 파티 " +temp[1]+" 딜러 "+str(temp[2])+" 명, 서폿"+str(temp[3])+" 명" ,inline=False)
    #     embed.add_field(name="별" ,value=temp[4])
    #     count+=1
    # await channel.send(embed=embed)
    # if(channel.name=="👹레이드-파티모집"):
    # 모집할 레이드 생성.
@client.command(name="참가", pass_context=True)
async def into(ctx,raid,role):
    channel=ctx.channel
    list=dbread()
    
    # raid = int(raid)-1
    if(role == "딜러"):
        list[raid]['딜러'] += " " + ctx.author.name
        dbsave(list)
    #     raidlist[raid][2]+=1
    #     raidlist[raid][4] += " " + ctx.author.name
    elif(role == "서폿"):
        list[raid]['서폿'] += " " + ctx.author.name
        dbsave(list)
    #     raidlist[raid][3]+=1
    #     raidlist[raid][4] +=  " " + ctx.author.name
    else:
         await channel.send("명령어를 잘못 입력하였습니다")
         return
    dbsave(list,list.c) 
    embed = discord.Embed(title="레이드 현황")
    embed.add_field(name=raid, value=list[raid]["파티"] ,inline=False)
    embed.add_field(name="딜러", value=list[raid]['딜러']+"d")
    embed.add_field(name="서폿", value=list[raid]['서폿']+"d")
    # embed = discord.Embed(title=raidlist[raid][0]+" 파티 " +raidlist[raid][1]+" 딜러"+str(raidlist[raid][2])+"명, 서폿"+str(raidlist[raid][3])+"명")
    await channel.send(embed=embed)
    # if(channel.name=""):
    #참가할 레이드 참가
@client.command(name="취소",pass_context=True)
async def delete(ctx,raid,role):
    channel=ctx.channel
    
    # raid= int(raid)-1
    # if(role == "딜러"):
    #     raidlist[raid][2]-=1
    #     raidlist[raid][4].replace(ctx.author.name,"")
    # elif(role == "서폿"):
    #     raidlist[raid][3]-=1
    #     raidlist[raid][4].replace(ctx.author.name,"")
    # else:
    #     await channel.send("명령어를 잘못 입력하였습니다")
    # embed = discord.Embed(title=raidlist[raid][0]+" 파티 " +raidlist[raid][1]+" 딜러"+str(raidlist[raid][2])+"명, 서폿"+str(raidlist[raid][3])+"명")
    # await channel.send(embed=embed)

@client.command(name="리스트",pass_context=True)
async def showlist(ctx):
    channel=ctx.channel
    list=dbread()
    print(list)
    embed = discord.Embed(title="레이드 현황")
    for k,v in list.items():
        print(k)
        print(v)
        embed.add_field(name=k, value=v["파티"]+" 파티 "  ,inline=False)
        embed.add_field(name="딜러", value=v['딜러']+"d")
        embed.add_field(name="서폿", value=v['서폿']+"d")
    await channel.send(embed=embed)
    # embed = discord.Embed(title="레이드 현황")
    # count=0
    # for temp in raidlist:
    #     embed.add_field(name=str(count+1)+"번파티", value=temp[0]+" 파티 " +temp[1]+" 딜러 "+str(temp[2])+" 명, 서폿"+str(temp[3])+" 명" ,inline=False)
    #     embed.add_field(name="별" ,value=temp[4])
    #     count+=1
    # await channel.send(embed=embed)
#라이더삭제 11/24 9시 발탄노말
@client.command(name="삭제",pass_context=True)
async def delraid(ctx,date1,date2,raid):
    dbdelete(date1+date2)
    addraid=Schedule.find(date1)
    update=Schedule.cell(addraid.row,addraid.col+2)
    temp = update.value
    temp = temp.replace("\n"+date2+raid,"")
    Schedule.update_cell(addraid.row,addraid.col+2, temp )
    list=dbread()
    embed = discord.Embed(title="레이드 현황")
    for k,v in list.items():
        print(k)
        print(v)
        embed.add_field(name=k, value=v["파티"]+" 파티 "  ,inline=False)
        embed.add_field(name="딜러", value=v['딜러']+"d")
        embed.add_field(name="서폿", value=v['서폿']+"d")
    await channel.send(embed=embed)
    # embed = discord.Embed(title="레이드 현황")
    # count=0
    # for temp in raidlist:
    #     embed.add_field(name=str(count+1)+"번파티", value=temp[0]+" 파티 " +temp[1]+" 딜러 "+str(temp[2])+" 명, 서폿"+str(temp[3])+" 명" ,inline=False)
    #     embed.add_field(name="별" ,value=temp[4])
    #     count+=1
    # await channel.send(embed=embed)

token= open('token','r').readline()
client.run('token')







