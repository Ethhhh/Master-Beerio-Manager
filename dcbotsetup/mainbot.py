import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

        try:
            guild = discord.Object(id=1465518923616354565)
            synced = await self.tree.sync(guild=guild)
            print(f"Sunced {len(synced)} command(s) to guild {guild.id}")

        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1465518923616354565)


@client.tree.command(name="lograce", description="Use this function to add a race to the log and update BKR (administrator only)", guild=GUILD_ID)
async def log_race(interaction: discord.Interaction):
    await interaction.response.send_message("This is the initial UI test!")


client.run('')

#bruh i removed it??