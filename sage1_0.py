import discord
from discord.ext import commands
import datalist
from discord.ext.commands import CommandNotFound

# コマンド
import command.vstemp as vs

# 公式仕様変更に伴いメンバー取得にintentsが必要
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '/', intents=intents)

@client.event
async def on_ready():
	print('SRCWログイン成功')

	await vs.setup(client)
	client.add_view(vs.VsTempView())
	#await client.tree.sync(guild = discord.Object(id = int(1339932403526930506)))
	await client.tree.sync()

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		return

client.run(datalist.mastertoken)