from colorama import Fore
from getpass import getpass
from datetime import datetime

from mod.notifier import notify
from mod.bot import BotManager
from mod.error import CustomLogger
from mod.db import DatabaseManager
from mod.desings import LethalLogo

import logging

class LethalBot:
    def __init__(self):
        """
        Initializes an instance of LethalBot.
        """
        self.db_manager = DatabaseManager("./Modules/database/lethal.db")
        self.bot_manager = BotManager()
        self.custom_logger = CustomLogger('Login', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()
        self.logo = LethalLogo()

    def update_token(self):
        """
        method to update Discord Token in the database.
        """
        token = self.db_manager.execute_read_one_query("SELECT token FROM auth;")
        discord_token = getpass(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.LIGHTGREEN_EX}Info{Fore.WHITE}] [+] Enter Your {Fore.LIGHTMAGENTA_EX}Discord{Fore.WHITE} Token ({Fore.LIGHTGREEN_EX}Right-Click To Paste {Fore.WHITE}|{Fore.LIGHTGREEN_EX} Token Will Not Show{Fore.WHITE}): ')
        if token == discord_token:
            return self.logger.error('You cannot set the same token.')
            self.run()
        
        try:
            self.db_manager.execute_query(f"UPDATE auth SET token='{discord_token}';")
            notify("Lethals Alert", 'Discord token has been saved.')
            self.run()
        except:
            notify("Lethals Alert", 'Something has went wrong. Check error log.')
            self.run()

    def login(self):
        token = self.db_manager.execute_read_one_query("SELECT token FROM auth;")

        if token is None:
            try:
                discord_token = getpass("Enter your Discord token: ")
                self.db_manager.execute_query("INSERT INTO auth (token) VALUES (?);", (discord_token,))
                notify("Lethals Alert", 'Token has been saved locally.')
            except Exception as e:
                notify("Lethals Alert", 'Something has went wrong. Check error log.')
                return self.logger.error(e)

        self.logo.main_logo()
        self.bot_manager.run_bot()

    def run(self):
        """
        Options include:
        - 1: Login.
        - 2: Update Discord token.
        """
        self.logo.options()
        user_input = input('What would you like to do? ')

        if user_input == "1":
            self.login()

        elif user_input == "2":
            self.update_token()
        else:
            quit()
