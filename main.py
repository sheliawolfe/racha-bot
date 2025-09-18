import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

class MenuView(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="checkin", style=discord.ui.ButtonStyle.green)
  async def checkin(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message("checked", ephemeral=True)

  @discord.ui.button(label="count", style=discord.ui.ButtonStyle.blurple)
  async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message("streak alive for {streak_count} days!")

  @discord.ui.button(label="ping", style=discord.ui.ButtonStyle.red)
  async def ping(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message("pong")

@bot.event
async def on_ready():
  bot.add_view(MenuView())
  await bot.tree.sync()
  print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.lower() == "ping":
    await message.channel.send("pong")
  await bot.process_commands(message)

@bot.command()
async def ping(ctx):
  await ctx.send("pong")

@bot.tree.command(name="ping2", description="pong")
async def slash_ping(interaction: discord.Interaction):
  await interaction.response.send_message("pong")

@bot.tree.command(name="menu", description="show commands")
async def menu(interaction: discord.Interaction):
  view = MenuView()
  await interaction.response.send_message("choose an option:", view=view)

bot.run(TOKEN)
