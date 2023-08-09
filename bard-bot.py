import discord
import requests
import json


def get_project_data(user, project):
    url = "https://api.github.com/repos/{}/{}".format(user, project)
    response = requests.get(
        url, headers={"Authorization": "token YOUR_GITHUB_CLASSIC_TOKEN"})
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise Exception(
            "Error getting project data: {}".format(response.status_code))


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


client = discord.Client()


@client.event
async def on_ready():
    print("Bot is ready!")


@client.event
async def on_message(message):
    if message.content.startswith("/project"):
        await handle_project_command(client, message)

client.run("YOUR_BOT_TOKEN")
