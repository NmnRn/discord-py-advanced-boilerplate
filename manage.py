# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import pathlib

APP_PATH = pathlib.Path(__file__).parent.resolve()

def print_help():
    print("Welcome to Bot Manager!")
    print("Available commands:")
    print("  python manage.py build         - Setups the project folders and default files")
    print("  python manage.py run           - Starts the bot (runs app.py)")
    print("  python manage.py makecommand   - Creates a new command template. Usage: makecommand <command_name>")
    print("  python manage.py makeevent     - Creates a new event template. Usage: makeevent <event_name>")
    print("  python manage.py resetdb       - Note: Not implemented yet")


def build_project():
    print("Building project and enforcing structure...")
    try:
        from Project.settings import controlProject
        controlProject()
    except Exception as e:
        print(f"Failed to build project settings: {e}")

def run_project():
    print("Starting bot...")
    app_py_path = APP_PATH / "app.py"
    if not app_py_path.exists():
        print("app.py does not exist! Run 'python manage.py build' first.")
        return
        
    subprocess.run([sys.executable, "-X", "utf8", str(app_py_path)])

def make_command(name):
    commands_dir = APP_PATH / "Commands"
    if not commands_dir.exists():
        print("Commands directory does not exist. Run 'python manage.py build' first.")
        return
        
    if not name.endswith(".py"):
        name += ".py"
        
    file_path = commands_dir / name
    if file_path.exists():
        print(f"Command '{name}' already exists!")
        return
        
    class_name = name[:-3].replace("_", " ").title().replace(" ", "") + "Command"
    command_name = name[:-3].lower()

    text = f'''from Project.libraries import *

class {class_name}(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="{command_name}", description="Description for {command_name}")
    async def {command_name}(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is a new {command_name} command!")

async def setup(bot):
    await bot.add_cog({class_name}(bot))
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text.strip())
        
    print(f"Created new command template: {file_path}")

def make_event(name):
    events_dir = APP_PATH / "Events"
    if not events_dir.exists():
        print("Events directory does not exist. Run 'python manage.py build' first.")
        return
        
    if not name.endswith(".py"):
        name += ".py"
        
    file_path = events_dir / name
    if file_path.exists():
        print(f"Event '{name}' already exists!")
        return
        
    class_name = name[:-3].replace("_", " ").title().replace(" ", "") + "Event"

    text = f'''from Project.libraries import *

class {class_name}(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Example: @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     pass

async def setup(bot):
    await bot.add_cog({class_name}(bot))
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text.strip())
        
    print(f"Created new event template: {file_path}")


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "build":
        build_project()
    elif command == "run":
        run_project()
    elif command in ("makecommand", "startcommand"):
        if len(sys.argv) < 3:
            print("Please provide a name. Example: python manage.py makecommand ping")
        else:
            make_command(sys.argv[2])
    elif command in ("makeevent", "startevent"):
        if len(sys.argv) < 3:
            print("Please provide a name. Example: python manage.py makeevent user_join")
        else:
            make_event(sys.argv[2])
    elif command == "help":
        print_help()
    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
