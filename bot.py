from interactions import Client, Intents, slash_command, SlashContext, listen, slash_option, OptionType
from dotenv import load_dotenv
import os
from querying import data_querying
from manage_embedding import update_index
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Client(intents=Intents.ALL)

@listen()
async def on_ready():
    logger.info("Bot is ready")

@listen()
async def on_message_create(event):
    logger.info(f"message received: {event.message.content}")

@slash_command(name="query", description="Enter your query :)")
@slash_option(
    name="input_text",
    description="input text",
    required=True,
    opt_type=OptionType.STRING,
)
async def get_response(ctx: SlashContext, input_text: str):
    await ctx.defer()
    logger.info(f"Received query command with input_text: {input_text}")
    try:
        response = await data_querying(input_text)
        response = f'**Input Query**: {input_text}\n\n{response}'
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        response = f"An error occurred: {e}"
    await ctx.send(response)
    logger.info("Sent response to query command")

@slash_command(name="updatedb", description="Update your information database :)")
async def updated_database(ctx: SlashContext):
    await ctx.defer()
    logger.info("Received updatedb command")
    try:
        update = await update_index()
        if update:
            response = f'Updated {sum(update)} document chunks'
        else:
            response = 'Error updating index'
    except Exception as e:
        logger.error(f"Error updating database: {e}")
        response = f"An error occurred: {e}"
    await ctx.send(response)
    logger.info("Sent response to updatedb command")

bot.start(os.getenv("DISCORD_BOT_TOKEN"))
