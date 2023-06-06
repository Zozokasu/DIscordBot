import discord
import settings
import openai
from googleSp import getAISettings

TOKEN = settings.TOKEN
CHANNEL_ID = settings.CHANNEL_ID
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
openai.api_key = settings.GPT_KEY


@client.event
async def on_ready():
    print('Logged in successful.')


@client.event
async def on_message(message: discord.Message):
    print(message.channel.id)
    if (message.author.bot):
        return
    if message.channel.id == CHANNEL_ID:
        print(message.type.value)
        print(message.content)
        if (message.content[0] == '!' or message.content[0] == '！'):
            return
        preset = getAISettings()
        currentMessage = message
        messages = [{"role": "system", "content": preset}]
        if (message.type.value == 19):
            referenceMessage = await getReplyChain(currentMessage)
            referenceMessage[0:1] = messages
            messages = referenceMessage
        messages.append(
            {"role": "user", "content": message.content})
        print(messages)
        response = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=messages)
        response = response["choices"][-1]["message"]["content"]
        print(response)
        await message.reply(response)


async def reply(message: discord.Message):
    reply = f'{message.author.mention} は {message.content}と述べられた。'
    await message.reply(reply, mention_author=True)


async def getReplyChain(message: discord.Message):
    replyChain = []
    currentMessage = message

    while (currentMessage.type.value == 19):
        referenceMessage = await currentMessage.channel.fetch_message(
            currentMessage.reference.message_id)
        role = "assistant" if (referenceMessage.author.bot)else "user"
        replyChain.insert(
            0, {"role": role, "content": referenceMessage.content})
        print(referenceMessage.content)
        currentMessage = referenceMessage

    return replyChain

client.run(TOKEN)
