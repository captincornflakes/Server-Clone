import discord
from discord.ext import commands
import json
import os

class ServerBackup(commands.Cog):
     def __init__(self, bot):
          self.bot = bot

     @commands.Cog.listener()
     async def on_ready(self):
          # Sync commands globally
          try:
               synced = await self.bot.tree.sync()
               print(f"Synced {len(synced)} commands globally.")
          except Exception as e:
               print(f"Error syncing commands: {e}")

     @discord.app_commands.command(name="backup", description="Back up all server channels and roles")
     @discord.app_commands.default_permissions(administrator=True)
     async def backup(self, interaction: discord.Interaction):
          guild = interaction.guild
          if guild is None:
               await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
               return

          backup_data = {
               "guild_name": guild.name,
               "guild_id": guild.id,
               "roles": [],
               "channels": []
          }

          # Backup roles
          for role in guild.roles:
               backup_data["roles"].append({
                    "name": role.name,
                    "permissions": role.permissions.value,
                    "color": role.color.value,
                    "hoist": role.hoist,
                    "position": role.position,
                    "mentionable": role.mentionable,
                    "id": role.id
               })

          # Backup channels
          for channel in guild.channels:
               backup_data["channels"].append({
                    "name": channel.name,
                    "id": channel.id,
                    "type": str(channel.type),
                    "position": channel.position,
                    "category": channel.category.name if channel.category else None
               })

          # Save to file
          if not os.path.exists("backups"):
               os.makedirs("backups")
          file_name = f"backups/{guild.id}.json"
          with open(file_name, "w", encoding="utf-8") as file:
               json.dump(backup_data, file, indent=4)

          await interaction.response.send_message(f"Backup completed! Saved as `{guild.id}`.", ephemeral=True)

     @discord.app_commands.command(name="restore", description="Restore server structure from a backup file")
     @discord.app_commands.default_permissions(administrator=True)
     async def restore(self, interaction: discord.Interaction, file_name: str):
          guild = interaction.guild
          if guild is None:
               await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
               return

          try:
               with open(f"backups/{file_name}.json", "r", encoding="utf-8") as file:
                    backup_data = json.load(file)

               # Restore roles
               for role_data in reversed(backup_data["roles"]):  # Reverse to maintain hierarchy
                    await guild.create_role(
                         name=role_data["name"],
                         permissions=discord.Permissions(role_data["permissions"]),
                         color=discord.Color(role_data["color"]),
                         hoist=role_data["hoist"],
                         mentionable=role_data["mentionable"]
                    )

               # Restore channels
               for channel_data in backup_data["channels"]:
                    if channel_data["type"] == "text":
                         await guild.create_text_channel(
                         name=channel_data["name"],
                         category=discord.utils.get(guild.categories, name=channel_data["category"]),
                         position=channel_data["position"]
                         )
                    elif channel_data["type"] == "voice":
                         await guild.create_voice_channel(
                         name=channel_data["name"],
                         category=discord.utils.get(guild.categories, name=channel_data["category"]),
                         position=channel_data["position"]
                         )

               await interaction.response.send_message("Restore completed!", ephemeral=True)

          except FileNotFoundError:
               await interaction.response.send_message(f"File `{file_name}` not found. Please ensure it exists in the `backups` folder.", ephemeral=True)

async def setup(bot):
     await bot.add_cog(ServerBackup(bot))
