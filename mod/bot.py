from discord.ext import commands

from mod.error import CustomLogger
from mod.db import DatabaseManager

import sys, os, asyncio, importlib, logging, traceback

class BotManager:
    """
    BotManager class handles the bot's setup, initialization, and running.
    It manages database operations, logging, cog setup, and bot execution.
    """
    def __init__(self):
        """
        Initializes bot manager with bot properties, logger, and database manager.
        """
        self.db_manager = DatabaseManager("./Modules/database/lethal.db")
        self.prefix = self.get_bot_prefix()
        self.bot = self.initialize_bot()
        self.custom_logger = CustomLogger('Bot', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    def get_bot_prefix(self) -> str:
        """
        Fetches the bot prefix from the database.
        """
        prefix = self.db_manager.execute_read_one_query("SELECT prefix FROM config;")
        if prefix is None:
            return
        return prefix[0]

    def initialize_bot(self):
        """
        Initializes the discord bot with the fetched prefix.
        """
        return commands.Bot(command_prefix=self.prefix, help_command=None, self_bot=True)

    def get_resource_path(self, relative_path: str) -> str:
        """
        Returns the absolute path of the given relative path.
        :param relative_path: Relative path of the resource.
        """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    async def setup_bot(self):
        """
        Sets up the bot by loading available cogs.
        """
        cogs_path = self.get_resource_path("cogs")
        for filename in os.listdir(cogs_path):
            if not filename.startswith("_") and filename.endswith(".py"):
                cog_name = filename[:-3]
                cog_module = f"cogs.{cog_name}"
                try:
                    cog = importlib.import_module(cog_module)
                    cog_instance = getattr(cog, f"{cog_name.capitalize()}Cog")(self.bot)
                    await self.bot.add_cog(cog_instance)
                except commands.ExtensionError as e:
                    self.logger.error(f"Error loading extension {cog_name}: {e}")

    def run_bot(self):
        """
        Runs the bot using the token fetched from the database.
        """
        asyncio.get_event_loop().run_until_complete(self.setup_bot())
        try:
            token = self.db_manager.execute_read_one_query("SELECT token FROM auth;")
            self.bot.run(token[0], log_handler=None)
        except LoginFailure:
            self.logger.error("Invalid bot token. Please provide a valid token.")
        except DiscordException as e:
            self.logger.error(f"An error occurred while running the bot: {e}")
            traceback.print_exc()
