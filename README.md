
# Server Backup Bot

Server Backup Bot is a Discord bot designed to back up and restore server roles and channels effortlessly. It also provides functionality to manage backups, including deleting old backup files.

---

### Install Discord
- use this link to add the existing running bot to your discord server
- https://discord.com/oauth2/authorize?client_id=1311145918938091541&permissions=8&integration_type=0&scope=bot
---
## Features

- **Backup Server Structure**: Save roles, channels, and their configurations (including categories).
- **Restore Backups**: Recreate roles, channels, and categories from a previous backup.
- **Delete Backups**: Remove outdated or unnecessary backups.
- **Slash Commands**:
  - `/backup`: Creates a new backup of the server’s roles, channels, and configurations. The backup includes a random password for restoration.
  - `/restore name:<name> password:<password>`: Restores the server structure from a specific backup. The backup is restored using the provided password (the password is generated during the backup creation).
  - `/delete_backup name:<name> password:<password>`: Deletes a specific backup .

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
            "use_Git": false,
            "repo_url": "https://github.com/captincornflakes/Server-Clone",
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
