# Bot Infrastructure & Manager 🚀

A highly automated, clean, and foundational boilerplate for building `discord.py` bots. Designed to set up your entire bot infrastructure in literal seconds using a structured management system.

## ✨ Features

- **Centralized `manage.py` System**: Run, build, and generate command files directly from your terminal just like Django.
- **One-Click Scaffold**: Automatically generates the required directory structure (`Commands`, `Events`, `Database_Processes`, `Special`).
- **Auto-Generates `app.py`**: A ready-to-use bot main file constructed with cogs (extensions) loading mechanisms and a sharded bot instance.
- **Environment Auto-Setup**: Automatically detects and creates your `.env` credentials file framework.
- **Strict Folder Protection**: Ensures users cannot tamper with core files. Any unauthorized file placed inside `Project/` is safely isolated.
- **Smart Cleanup**: Keeps your root directory clean by moving non-essential or random `.py` files to the hidden `Special` folder during initialization.

## 🛠️ Usage

1. Clone or download this repository.
2. In your terminal, navigate to the project directory and run the build command to generate the environment:

   ```bash
   python manage.py build
   ```

3. Open your newly generated `.env` file and insert your `DISCORD_TOKEN` and database credentials.

4. Start your discord bot by running:
   ```bash
   python manage.py run
   ```

## ⚙️ Management Commands

You can use `manage.py` to create code templates instantly!

- `python manage.py build` : Sets up all default folders, files, and permissions.
- `python manage.py run` : Starts the bot successfully.
- `python manage.py makecommand <name>` : Auto-generates a slash command template inside `Commands/`.
- `python manage.py makeevent <name>` : Auto-generates an event listener template inside `Events/`.

## 📂 Architecture After Initialization

After running `python manage.py build`, your repository will expand into this layout:

```text
├── Commands/               # Drop your slash command cogs here
├── Events/                 # Drop your listener events cogs here
├── Database_Processes/
│   └── db_core.py          # Auto-generated connection pool module
├── Project/
│   ├── libraries.py        # Centralized library imports
│   └── settings.py         # The infrastructure manager
├── Special/                # Hidden directory for archived/core files (random .py files are moved here)
├── .env                    # Auto-generated secrets
├── manage.py               # The CLI tool for your bot
└── app.py                  # Auto-generated Bot Heart
```

## 📝 Requirements

Make sure to install the required dependencies before running the bot:

- `discord.py`
- `python-dotenv`
- `aiomysql`

You can install them via `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

_Built to help developers skip the repetitive setup and go straight back to brewing awesome bots._
