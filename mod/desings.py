"""
You can add custom logos here.
Lethal used patorjk.

Link: https://patorjk.com/software/taag/
"""
import os

class LethalLogo:
    def __init__(self):
        pass

    @staticmethod
    def purplepink(text):
        faded = ""
        red = 40
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        return faded

    def main_logo(self):
        os.system("cls")
        logo = """
        ██╗     ███████╗████████╗██╗  ██╗ █████╗ ██╗     
        ██║     ██╔════╝╚══██╔══╝██║  ██║██╔══██╗██║     
        ██║     █████╗     ██║   ███████║███████║██║     
        ██║     ██╔══╝     ██║   ██╔══██║██╔══██║██║     
        ███████╗███████╗   ██║   ██║  ██║██║  ██║███████╗
        ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
        ╔═══════════════════════════════════════════════╗
        ║   TOS: Lethal Holds No Responsibility At ALL! ║ 
        ║      Version: 2.0 | https://lethals.org       ║
        ╚═══════════════════════════════════════════════╝
        """
        print(self.purplepink(logo))

    def options(self):
        os.system("cls")
        logo = """
        ██╗     ███████╗████████╗██╗  ██╗ █████╗ ██╗     
        ██║     ██╔════╝╚══██╔══╝██║  ██║██╔══██╗██║     
        ██║     █████╗     ██║   ███████║███████║██║     
        ██║     ██╔══╝     ██║   ██╔══██║██╔══██║██║     
        ███████╗███████╗   ██║   ██║  ██║██║  ██║███████╗
        ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
        ╔═════════════════════════════════════════════════╗
        ║ Options: 1. Login | 2. Change Discord Token     ║ 
        ║ NOTE: Everything gets stored inside a local DB  ║            
        ╚═════════════════════════════════════════════════╝
        """
        print(self.purplepink(logo))
