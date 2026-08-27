# coding: UTF-8

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui, Interaction
from discord.ui import View, Select, Modal
from discord.enums import ButtonStyle

# データ群、設定読み込み
import datalist as dl

# モーダル
class VsTemplateModal(discord.ui.Modal):

	def __init__(self):
		super().__init__(title = 'レース募集を作成', timeout = None)

		self.day_input = discord.ui.TextInput(
			placeholder = f'例：1/1 21時から',
			required = True
		)
		self.day_label = discord.ui.Label(
			text = f'開催日時はいつに指定するの？(必須)',
			component = self.day_input
		)

		self.game_type_select = discord.ui.Select(
			options = [
				discord.SelectOption(label = f'ワルマスクワッド', value = f'ワルマスクワッド'),
				discord.SelectOption(label = f'フェスタチーム', value = f'フェスタチーム'),
				discord.SelectOption(label = f'カスタムマッチ', value = f'カスタムマッチ')
			],
			required = True
		)
		self.game_type_label = discord.ui.Label(
			text = f'募集するレース形式を選択して(必須)',
			component = self.game_type_select
		)

		self.target_late_select =  discord.ui.Select(
			options = [
				discord.SelectOption(label = f'誰でも参加OK', value = f'誰でも参加OK', default = True),
				discord.SelectOption(label = f'A～E', value = f'A～E'),
				discord.SelectOption(label = f'Legend9～Legend3', value = f'Legend9～Legend3'),
				discord.SelectOption(label = f'Legend2～', value = f'Legend2～')
			],
			required = True
		)
		self.target_late_label = discord.ui.Label(
			text = f'募集するレート帯を選択して(必須)',
			component = self.target_late_select
		)

		self.style_select =  discord.ui.Select(
			options = [
				discord.SelectOption(label = f'誰でも歓迎', value = f'誰でも歓迎', default = True),
				discord.SelectOption(label = f'エンジョイ', value = f'エンジョイ'),
				discord.SelectOption(label = f'ガチ', value = f'ガチ'),
				discord.SelectOption(label = f'練習メイン', value = f'練習メイン'),
				discord.SelectOption(label = f'雑談メイン', value = f'雑談メイン'),
				discord.SelectOption(label = f'1 VS 1', value = f'1 VS 1'),
				discord.SelectOption(label = f'VCなしOK', value = f'VCなしOK'),
				discord.SelectOption(label = f'聞き専OK', value = f'聞き専OK'),
				discord.SelectOption(label = f'配信OK', value = f'配信OK')
			],
			min_values = 1,
			max_values = 9
		)

		self.style_label = discord.ui.Label(
			text = f'募集するスタイルを全て選択して(複数選択可、1つ以上必須)',
			component = self.style_select
		)

		self.comment_input = discord.ui.TextInput(
			style = discord.TextStyle.paragraph,
			required = False
		)
		self.comment_label = discord.ui.Label(
			text = f'ルールや詳細などがあれば記載して',
			component = self.comment_input
		)

		self.add_item(self.day_label)
		self.add_item(self.game_type_label)
		self.add_item(self.target_late_label)
		self.add_item(self.style_label)
		self.add_item(self.comment_label)

	async def on_submit(self, interaction: discord.Interaction):

		party_title = f'対戦・メンバー募集'
		embed = discord.Embed(
			title = party_title,
			description = "募集の詳細を以下に表示する。内容を確認して。",
			color = discord.Colour.green()
		)
		embed.set_author(
			name = interaction.user.display_name,
			icon_url = interaction.user.display_avatar.url
		)
		embed.set_thumbnail(url=interaction.user.display_avatar.url)
		embed.add_field(
			name = f'開催日時はいつに指定するの？', value = self.day_input.value,
			inline = False
		)
		embed.add_field(
			name = f'募集するレース形式を選択して', value = self.game_type_select.values[0],
			inline = False
		)
		embed.add_field(
			name = f'募集するレート帯を選択して', value = self.target_late_select.values[0],
			inline = False
		)
		embed.add_field(
			name = f'募集するスタイルを全て選択して', value = '\n'.join(self.style_select.values),
			inline = False
        )
		if self.comment_input.value:
			embed.add_field(
	    		name = f'ルールや詳細などがあれば記載して', value = self.comment_input.value,
		    	inline = False
		    )

		await interaction.guild.get_channel(dl.recruit_channel_id).send(
			allowed_mentions = discord.AllowedMentions(roles = True),
			content = f'{interaction.user.get_role(dl.member_role_id).mention}',
			embed = embed
		)

		embed = discord.Embed(
			title = 'Success', 
			description = 'テンプレートの送信完了。確認して。', 
			color = discord.Colour.green()
		)
		await interaction.response.send_message(embed = embed, delete_after = 5.0)

# ボタン
class VsTempButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = ButtonStyle.success, label = f'募集を作成する', custom_id = 'cw_vstemp_btn')

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.send_modal(VsTemplateModal())

# ビュー
class VsTempView(discord.ui.View):
	
	def __init__(self):
		super().__init__(timeout = None)
		self.add_item(VsTempButton())

# コマンドコグ
class VsTempCommand(commands.Cog):

	def __init__(self, client):
		self.client = client

	@app_commands.command(name = 'vstemp', description = '募集テンプレート作成UIの呼び出し')
	async def _VsTemp(self, interaction: discord.Interaction):
		head_embed = discord.Embed(
			title = 'Recruit Template',
			description = f'レースの参加者募集を支援する。下のボタンを押して。',
			color = discord.Colour.blue()
		)
		await interaction.response.send_message(embed = head_embed, view = VsTempView())

# コグ登録
async def setup(client):
	await client.add_cog(VsTempCommand(client))