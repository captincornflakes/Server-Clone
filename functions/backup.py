import discord
from discord.ext import commands
import json
import os
import random
import string


def generate_password(length=8):
     """Generate a random password consisting of letters and digits."""
     characters = string.ascii_letters + string.digits
     return ''.join(random.choice(characters) for _ in range(length))


class ServerBackup(commands.Cog):
     def __init__(self, bot):
          self.bot = bot

     @commands.Cog.listener()
     async def on_ready(self):
          try:
               synced = await self.bot.tree.sync()
               print(f"Synced {len(synced)} commands globally.")
          except Exception as e:
               print(f"Error syncing commands: {e}")

     @discord.app_commands.command(name="backup", description="Back up all server channels, roles, categories, and their permissions")
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
               "channels": [],
               "categories": [],
               "password": generate_password()  # Generate and store a random password
          }

          # Backup roles (skip managed roles)
          for role in guild.roles:
               if role.managed:
                    continue  # Skip managed roles
               backup_data["roles"].append({
                    "name": role.name,
                    "permissions": role.permissions.value,
                    "color": role.color.value,
                    "hoist": role.hoist,
                    "position": role.position,
                    "mentionable": role.mentionable,
                    "id": role.id
               })

          # Backup categories
          for category in guild.categories:
               permissions = []
               for target, overwrite in category.overwrites.items():
                    permissions.append({
                         "target_id": target.id,
                         "target_type": "role" if isinstance(target, discord.Role) else "member",
                         "allow": overwrite.pair()[0].value,
                         "deny": overwrite.pair()[1].value
                    })
               backup_data["categories"].append({
                    "name": category.name,
                    "id": category.id,
                    "position": category.position,
                    "permissions": permissions
               })

          # Backup channels
          for channel in guild.channels:
               if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                    permissions = []
                    for target, overwrite in channel.overwrites.items():
                         permissions.append({
                              "target_id": target.id,
                              "target_type": "role" if isinstance(target, discord.Role) else "member",
                              "allow": overwrite.pair()[0].value,
                              "deny": overwrite.pair()[1].value
                         })
                    backup_data["channels"].append({
                         "name": channel.name,
                         "id": channel.id,
                         "type": str(channel.type),
                         "position": channel.position,
                         "category_id": channel.category.id if channel.category else None,
                         "permissions": permissions
                    })

          if not os.path.exists("datastores"):
               os.makedirs("datastores")
          file_name = f"datastores/{guild.id}.json"
          with open(file_name, "w", encoding="utf-8") as file:
               json.dump(backup_data, file, indent=4)

          await interaction.response.send_message(f"Backup completed! Saved as `{guild.id}`. The password is `{backup_data['password']}`.", ephemeral=True)


async def setup(bot):
     await bot.add_cog(ServerBackup(bot))
