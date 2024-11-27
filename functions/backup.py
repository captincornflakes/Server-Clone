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
          # Sync commands globally
          try:
               synced = await self.bot.tree.sync()
               print(f"Synced {len(synced)} commands globally.")
          except Exception as e:
               print(f"Error syncing commands: {e}")

     @discord.app_commands.command(name="backup", description="Back up all server channels, roles, and categories")
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

          # Backup categories
          for category in guild.categories:
               backup_data["categories"].append({
                    "name": category.name,
                    "id": category.id,
                    "position": category.position
               })

          # Backup channels (including category info for proper restoration)
          for channel in guild.channels:
               if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                    backup_data["channels"].append({
                         "name": channel.name,
                         "id": channel.id,
                         "type": str(channel.type),
                         "position": channel.position,
                         "category_id": channel.category.id if channel.category else None
                    })

          # Save to file
          if not os.path.exists("datastores"):
               os.makedirs("datastores")
          file_name = f"datastores/{guild.id}.json"
          with open(file_name, "w", encoding="utf-8") as file:
               json.dump(backup_data, file, indent=4)

          # Return guild ID and password in response message
          await interaction.response.send_message(f"Backup completed! Saved as `{guild.id}`. The password is `{backup_data['password']}`.", ephemeral=True)

     @discord.app_commands.command(name="restore", description="Restore server structure")
     @discord.app_commands.default_permissions(administrator=True)
     async def restore(self, interaction: discord.Interaction, file_name: str, password: str):
          guild = interaction.guild
          if guild is None:
               await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
               return

          # Ensure the file name ends with .json
          if not file_name.endswith(".json"):
               file_name += ".json"

          try:
               with open(f"datastores/{file_name}", "r", encoding="utf-8") as file:
                    backup_data = json.load(file)

               # Check if the provided password matches the one in the backup
               if backup_data["password"] != password:
                    await interaction.response.send_message("Incorrect password. Backup cannot be restored.", ephemeral=True)
                    return

               # Restore categories first (only if category does not already exist)
               category_mapping = {}
               for category_data in backup_data["categories"]:
                    existing_category = discord.utils.get(guild.categories, name=category_data["name"])
                    if not existing_category:
                         category = await guild.create_category(
                         name=category_data["name"],
                         position=category_data["position"]
                         )
                         category_mapping[category_data["id"]] = category  # Map category ID to the created category
                    else:
                         category_mapping[category_data["id"]] = existing_category  # Use the existing category

               # Restore roles (only if role does not already exist)
               for role_data in reversed(backup_data["roles"]):  # Reverse to maintain hierarchy
                    existing_role = discord.utils.get(guild.roles, name=role_data["name"])
                    if not existing_role:
                         await guild.create_role(
                         name=role_data["name"],
                         permissions=discord.Permissions(role_data["permissions"]),
                         color=discord.Color(role_data["color"]),
                         hoist=role_data["hoist"],
                         mentionable=role_data["mentionable"]
                         )

               # Restore channels (only if channel does not already exist)
               for channel_data in backup_data["channels"]:
                    category = category_mapping.get(channel_data["category_id"])  # Get the category from the map
                    existing_channel = discord.utils.get(guild.channels, name=channel_data["name"])

                    # Check if the channel already exists
                    if not existing_channel:
                         if channel_data["type"] == "text":
                              await guild.create_text_channel(
                                   name=channel_data["name"],
                                   category=category,
                                   position=channel_data["position"]
                              )
                         elif channel_data["type"] == "voice":
                              await guild.create_voice_channel(
                                   name=channel_data["name"],
                                   category=category,
                                   position=channel_data["position"]
                              )

               await interaction.response.send_message("Restore completed!", ephemeral=True)

          except FileNotFoundError:
               await interaction.response.send_message(f"File `{file_name}` not found. Please ensure it exists.", ephemeral=True)

     @discord.app_commands.command(name="delete_backup", description="Delete a backup")
     @discord.app_commands.default_permissions(administrator=True)
     async def delete_backup(self, interaction: discord.Interaction, file_name: str, password: str):
          # Ensure the file name ends with .json
          if not file_name.endswith(".json"):
               file_name += ".json"

          try:
               with open(f"datastores/{file_name}", "r", encoding="utf-8") as file:
                    backup_data = json.load(file)

               # Check if the provided password matches the one in the backup
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
     await bot.add_cog(ServerBackup(bot))
