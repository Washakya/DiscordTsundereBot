import math
import datetime

import os
import sys

import discord
from discord import app_commands
from discord.ext import commands

import google.generativeai as genai

import requests
from bs4 import BeautifulSoup

#ジョブの振り分け
part = (math.floor(datetime.datetime.now().hour / 4) + 1) % 6

#設定ファイルの読み込み
def load_character(d = "prompt"):

    with open(os.path.dirname(__file__) + "/" + d + ".txt", "r", encoding="utf-8") as f:
        return f.read()
    
prompt = load_character()
yandere = load_character("yandere")

#Geminiの設定
class gemini_settings:
    safety_settings=[
        { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
        { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
        { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
        { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    config = {
        "max_output_tokens": 2048,
        "temperature": 1,
        "top_p": 1
    }

#各種認証キー取得
GEMINI_API=os.getenv("Gemini_API_KEY")
TOKEN = os.getenv("Discord_TsundereBot_API")
SYSTEM_CHANNEL_ID = os.getenv("Discord_TsundereBot_System_Channel")

#Geminiオブジェクト作成
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

#ツンデレっぽい返しをしてくれる関数
def tsundere_response(text):
    if chat.history == []:
        return chat.send_message(prompt + text, safety_settings=gemini_settings.safety_settings).text
    else:
        return chat.send_message(text, safety_settings=gemini_settings.safety_settings).text

#おまけのwikipediaランダム記事タイトル
def wiki():
    load_url = "https://ja.wikipedia.org/wiki/特別:おまかせ表示"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    # title、h2、liタグを検索して表示する
    return soup.find("h1").get_text()

#接続に必要なオブジェクトを生成
client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
class SampleView(discord.ui.View): 
    def __init__(self, timeout=180): #初期値は180(s)
        super().__init__(timeout=timeout)

#担当時間まで待機
while part !=  math.floor(datetime.datetime.now().hour / 4):
    pass
print(part)

#起動時の処理
@client.event
async def on_ready():
    new_activity = "ツンデレ"
    await client.change_presence(activity=discord.Game(new_activity)) 
    await client.tree.sync()
    for channel in client.get_all_channels():
	    if channel.id == int(SYSTEM_CHANNEL_ID):
             await channel.send(part)
    print("ログインしました")

@client.tree.command(name="reset_cash", description="Botの会話ログキャッシュをリセットします") 
@app_commands.default_permissions(administrator=True)
async def test(interaction: discord.Interaction): 
    chat.history = []
    await interaction.response.send_message("system:リセットしました")
    print("会話ログをリセットしました")

@client.tree.command(name="reload", description = "キャラクターブックを再読み込みします")
@app_commands.default_permissions(administrator = True)
async def reload(interaction: discord.Interaction):
    prompt = load_character()
    chat.history = []
    await interaction.response.send_message("system:再読み込みしました")
    print("キャラクターブックを再読み込みしました")

@client.tree.command(name="logout", description="Botを停止します") 
@app_commands.default_permissions(administrator=True)
async def test(interaction: discord.Interaction): 
    chat.history = []
    await interaction.response.send_message("system:ログアウトしました")
    print("ログアウトしました")
    await client.close()

#メッセージ受信時の処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視
    if message.author.bot:
        if message.channel.id == int(SYSTEM_CHANNEL_ID):
            if message.content == str((part + 1) % 6):
                os._exit(0)
        else:
            pass
    elif isinstance(message.channel, discord.DMChannel) and message.author.name != "washakya":
        await message.channel.send("ちょっと、、DMで話すのは…恥ずかしい…です\nツンデレAI-βのサーバーで話しませんか？")
        print("[DM警告:" + message.author.name + "]")
    else:
        # ぬるぽ返信bot
        if message.content == "ぬるぽ":
            response_message = "ガッ"
        elif message.content == "wikirandom":
            response_message = wiki()
        else:
            try:
                response_message = tsundere_response(message.content)
                print(type(message.content))
            except:
                response_message = "API呼び出し上限に達しちゃったみたい…\nべ、べつにアンタと話したくないわけじゃ…ないから"

        await message.channel.send(response_message)
        print("受信(" + message.author.name + "):[" + message.content + "]")
        print("送信(Bot):[" + response_message.replace("\n", "") + "]")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
