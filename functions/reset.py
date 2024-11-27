import discord
from discord.ext import commands

class ResetServer(commands.Cog):
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

     @discord.app_commands.command(name="reset_server", description="Delete all roles, channels, and categories, and create a new 'general' channel")
     @discord.app_commands.default_permissions(administrator=True)
     async def reset_server(self, interaction: discord.Interaction):
          guild = interaction.guild
          if guild is None:
               await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
               return

          # Delete all roles (except @everyone)
          for role in guild.roles:
               if role.name != "@everyone":  # Skip deleting the @everyone role
                    try:
                         await role.delete()
                    except discord.Forbidden:
                         pass  # Skip if we don't have permission to delete the role

          # Delete all channels (including categories)
          for channel in guild.channels:
               try:
                    await channel.delete()
               except discord.Forbidden:
                    pass  # Skip if we don't have permission to delete the channel

          # Delete all categories
          for category in guild.categories:
               try:
                    await category.delete()
               except discord.Forbidden:
                    pass  # Skip if we don't have permission to delete the category

          # Create a new "general" text channel
          await guild.create_text_channel("general")

          await interaction.response.send_message("Server has been reset! All roles, channels, and categories have been deleted, and a new 'general' channel has been created.", ephemeral=True)

async def setup(bot):
     await bot.add_cog(ResetServer(bot))
