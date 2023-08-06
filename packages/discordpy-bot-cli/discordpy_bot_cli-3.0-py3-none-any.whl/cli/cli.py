#!/usr/env/bin python

import os
import click

@click.group(invoke_without_command = True)
@click.version_option("3.0")
def main():
    os.system("pip install discordpy-bot-cli --force-reinstall")
    pass

@main.command("init")
@click.argument("name")
@click.option("--env", help = "Specifies to create an env file for token.", is_flag = True)
def dcinit(name, env):
    """
        Initializes a Discord bot project by creating bot.py, Procfile and requirements.txt files.
        Usage: dc init <project_name>
    """
    os.mkdir(name)
    os.chdir(name)

    if env:
        os.system("echo TOKEN= >> .env")
        print("INFO: .env created")
        os.system("echo import os >> bot.py")
    os.system("echo from discord.ext import commands >> bot.py")
    os.system("echo. >> bot.py")
    os.system('echo client = commands.Bot(command_prefix = "") >> bot.py')
    os.system("echo. >> bot.py")
    if env:
        os.system('echo token = os.environ.get("TOKEN") >> bot.py')
        os.system("echo client.run(token) >> bot.py")
    else:
        os.system('echo client.run("") >> bot.py')
    print("INFO: bot.py created")

    os.system("echo worker: python bot.py >> Procfile")
    print("INFO: Procfile created")

    print("Discord bot project created.")
    print("If you are using Github and Heroku, make sure you have discord.py, pipreqs and Heroku CLI installed.")
    print("\nOR\n")
    print("If you are using Git and Heroku, make sure you have discord.py, pipreqs, Git and Heroku CLI installed.")
    print("\n")
    print("Please use heroku whoami to make sure that you are logged into the correct credentials.")
    print("If you are not logged in, please log into your account in Heroku CLI.")
    print("\n")
    if env:
        print("IMPORTANT: Since you have used --env option, make sure that you write the client token in the .env file with name as TOKEN mentioned in the file.")
    else:
        print("IMPORTANT: Write the client token in the double quotes in the brackets in client.run().")
    pass

@main.command()
@click.argument("cog")
@click.option("-f", "--folder", help = "Folder in which the cog file shall be made and the folder need not be made.")
def cog(cog, folder):
    """
        Creates a cog file and adds setup.
        Usage: dc cog <file_name> [-f or --folder <folder_name>]
    """

    if os.path.exists("bot.py") or os.path.exists("client.py"):
        if not os.path.isdir("cogs"):
            os.mkdir("cogs")
        os.chdir("cogs")

        if folder:
            if not os.path.exists(folder):
                os.mkdir(folder)
            os.chdir(folder)

        os.system(f"echo from discord.ext import commands >> {cog.lower()}.py")
        os.system(f"echo. >> {cog.lower()}.py")
        os.system(f"echo class {cog}(commands.Cog): >> {cog.lower()}.py")
        os.system(f"echo    def __init__(self, client): >> {cog.lower()}.py")
        os.system(f"echo         self.client = client >> {cog.lower()}.py")
        os.system(f"echo. >> {cog.lower()}.py")
        os.system(f"echo def setup(client): >> {cog.lower()}.py")
        os.system(f"echo    client.add_cog({cog}(client)) >> {cog.lower()}.py")
    else:
        print("ERROR: bot.py or client.py not found. Make sure you have made a Discord bot project.")
    pass

@main.command()
def deploy():
    """
        Deploys the Discord bot (Use for Git and Heroku hosting).
        Usage: dcpy deploy
    """

    if os.path.exists('requirements.txt'):
        os.remove('requirements.txt')
        
    os.system("pipreqs --encoding=utf-8")

    if not os.path.isdir(".git"):
        os.system("git init")
        name = input("Heroku app name to connect to: ")
        os.system(f"heroku git:remote -a {name}")
        os.system(f"git branch -M main")
    
    os.system("git add .")
    os.system('git commit -m "Commit made with discord.py-bot-cli"')
    os.system("git push heroku main")
    print("Make sure that your bot is online by checking in the Resources tab of the project in Heroku.")
    pass

@main.command()
def wrap():
    """
        Creates a requirements file (Use for Github and Heroku hosting).
        Usage: dcpy wrap
    """
    if os.path.exists('requirements.txt'):
        os.remove('requirements.txt')
        
    os.system("pipreqs --encoding=utf-8")
    pass

def start():
    main(obj = {})

if __name__ == '__main__':
    start()