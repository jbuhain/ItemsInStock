import boto3
import json
import discord
from discord.ext import commands

aws_region = 'us-west-2'  
lambda_function_name = 'webscraper-stocksinsock' 

lambda_client = boto3.client('lambda', region_name=aws_region)

sm_client = boto3.client('secretsmanager', region_name=aws_region)

secret_name = "discord-bot-token"
discord_bot_token = None
try:
    response = sm_client.get_secret_value(SecretId=secret_name)
    secret_dict = json.loads(response['SecretString'])
    discord_bot_token = secret_dict['token']

except Exception as e:
    print(f"Secret Manager Error: {e}")


intents = discord.Intents.all()
intents.typing = True  
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents = intents)


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# intro command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, I am Socks-In-Stock bot!')
    await ctx.send('Created by Joshua Buhain')

# connects to lambda
@bot.command()
async def socks(ctx):
    await ctx.send('Socks command activated! Running...')
    input_payload = {
        # 'key1': 'value1',
        # 'key2': 'value2'
    }
    
    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
        Payload=json.dumps(input_payload) if input_payload else ''
    )
    await ctx.send('Calling Lambda function...')

    # parse/extract lambda function's response
    if response.get('StatusCode') == 200:
        await ctx.send('Lambda function heard!')
        lambda_response_payload = json.loads(response['Payload'].read())
        # access the result
        desired_value = lambda_response_payload.get('body')
        print(f'Value obtained from Lambda: {desired_value}')
        await ctx.send(desired_value)
    else:
        await ctx.send(f'Lambda invocation failed with status code {response.get("StatusCode")}')
        print(f'Lambda invocation failed with status code {response.get("StatusCode")}')

# run bot
bot.run(discord_bot_token)