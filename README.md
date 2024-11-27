
# Server Backup Bot

Server Backup Bot is a Discord bot designed to back up and restore server roles and channels effortlessly. It also provides functionality to manage backups, including deleting old backup files.

---

## Features

- **Backup Server Structure**: Save roles, channels, and their configurations.
- **Restore Backups**: Recreate roles and channels from a previous backup.
- **Delete Backups**: Remove outdated or unnecessary backups.
- **Slash Commands**:
  - `/backup`: Creates a new backup.
  - `/restore file_name:<file_name>`: Restores from a specific backup file.
  - `/delete_backup file_name:<file_name>`: Deletes a specific backup file.

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- `discord.py` library

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/server-backup-bot.git
   cd server-backup-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If the `requirements.txt` file is missing, install `discord.py` manually:
   ```bash
   pip install discord.py
   ```

3. Set up your configuration file:
   - Create `datastores/config.json` file in the root directory.

     - `config.json`:
       ```json
     {
     "token": "",
     "application_id": 0,
     "use_Git": true,
     "repo_url": "https://github.com/captincornflakes/Server-Clone",
     "repo_token": "",
     "repo_temp": "Server-Clone-main"
     }
       ```

4. Run the bot:
   ```bash
   python bot.py
   ```

---

## Troubleshooting

### 1. Missing Dependencies
If the bot fails to run due to missing dependencies, install them with:
```bash
pip install -r requirements.txt
```
If no `requirements.txt` is present, install `discord.py` manually:
```bash
pip install discord.py
```

---

### 2. Missing Configuration
If the bot cannot find the bot token, `datastores/config.json` file correctly.

---

### 3. Permissions Errors
Ensure the bot has the necessary permissions when invited to your server. Use the Discord Developer Portal to generate a proper OAuth2 URL with the Administrator permission.

---

### 4. Slash Commands Not Responding
If the bot doesn’t respond to commands:
- Ensure the bot has the necessary code to sync commands globally.
- Restart the bot and wait for command registration to complete.
- Verify the bot is added to the correct server via the Developer Portal.

---

## License

This project is licensed under the MIT License.
