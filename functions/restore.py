import discord
from discord.ext import commands
import json
import os

class ServerRestore(commands.Cog):
     def __init__(self, bot):
          self.bot = bot

     @commands.Cog.listener()
     async def on_ready(self):
          try:
               synced = await self.bot.tree.sync()
               print(f"Synced {len(synced)} commands globally.")
          except Exception as e:
               print(f"Error syncing commands: {e}")

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

          # Start the deferred response (to avoid timeout issues)
          await interaction.response.defer(ephemeral=True)

          try:
               # Load backup file
               with open(f"datastores/{file_name}", "r", encoding="utf-8") as file:
                    backup_data = json.load(file)

               # Check password
               if backup_data["password"] != password:
                    await interaction.followup.send("Incorrect password. Backup cannot be restored.", ephemeral=True)
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
                         category_mapping[category_data["id"]] = category
                    else:
                         category_mapping[category_data["id"]] = existing_category

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
                    category = category_mapping.get(channel_data["category_id"])
                    existing_channel = discord.utils.get(guild.channels, name=channel_data["name"])

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

               await interaction.followup.send("Restore completed!", ephemeral=True)

          except FileNotFoundError:
               await interaction.followup.send(f"File `{file_name}` not found. Please ensure it exists.", ephemeral=True)
          except Exception as e:
               await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

async def setup(bot):
     await bot.add_cog(ServerRestore(bot))