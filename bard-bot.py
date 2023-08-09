import discord
import requests
import json

def get_project_data(user, project):
    url = "https://api.github.com/repos/{}/{}".format(user, project)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer YOUR_GITHUB_TOKEN",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise Exception("Error getting project data: {}".format(response.status_code))

def plot_project_data(data):
    """Plots the project data in a Discord embed."""
    embed = discord.Embed(title="Project Data")
    for key, value in data.items():
        embed.add_field(name=key, value=value)
    return embed

def handle_project_command(client, message):
    """Handles the `/project` command."""
    user = message.author.name
    project = message.content[len("/project "):]
    try:
        data = get_project_data(user, project)
        embed = plot_project_data(data)
        client.send_message(message.channel, embed=embed)
    except Exception as e:
        client.send_message(message.channel, "Error: {}".format(e))

# set all intents to be able to receive all messages
intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.content.startswith("/project"):
        await handle_project_command(client, message)

client.run("YOUR_BOT_TOKEN")
