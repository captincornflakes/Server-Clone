import discord
from discord.ext import commands
import json
import os

class ServerDelete(commands.Cog):
     def __init__(self, bot):
          self.bot = bot

     @commands.Cog.listener()
     async def on_ready(self):
          try:
               synced = await self.bot.tree.sync()
               print(f"Synced {len(synced)} commands globally.")
          except Exception as e:
               print(f"Error syncing commands: {e}")


     @discord.app_commands.command(name="delete_backup", description="Delete a backup")
     @discord.app_commands.default_permissions(administrator=True)
     async def delete_backup(self, interaction: discord.Interaction, file_name: str, password: str):
          if not file_name.endswith(".json"):
               file_name += ".json"
          try:
               with open(f"datastores/{file_name}", "r", encoding="utf-8") as file:
                    backup_data = json.load(file)
               if backup_data["password"] != password:
                    await interaction.response.send_message("Incorrect password. Backup cannot be deleted.", ephemeral=True)
                    return
               file_path = f"datastores/{file_name}"
               if os.path.exists(file_path):
                    os.remove(file_path)
                    await interaction.response.send_message(f"Backup `{file_name}` has been deleted.", ephemeral=True)
               else:
                    await interaction.response.send_message(f"Backup `{file_name}` does not exist.", ephemeral=True)
          except Exception as e:
               await interaction.response.send_message(f"An error occurred while deleting the backup: {e}", ephemeral=True)

async def setup(bot):
     await bot.add_cog(ServerDelete(bot))
