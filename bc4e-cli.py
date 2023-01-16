"""
Main module for choosing a provider.
"""
import getpass
import subprocess
from providers import zoro, enime, gogo, pahe
from utils import util, arg_handler
from utils.arg_handler import parse_args

class Provider:
    """
    A class for choosing a provider.
    """
    def __init__(self):
        self.current_user = getpass.getuser()
        self.all_providers = ["zoro", "animepahe", "enime", "gogoanime"]
        self.default_provider = "zoro"

    def update(self):
        subprocess.run(["git", "pull", "https://github.com/carrotshniper21/bc4e-cli"])

def main():
    """
    Passes the arguments to the chosen provider
    would kinda look like this:
        zoro.main(quality='auto', history=False, download=False, continue=False, config=False, auto_update=False, vlc=False, sources=False)
    """
    args = parse_args()

    providers = {
        "zoro": zoro.main,
        "animepahe": pahe.main,
        "enime": enime.main,
        "gogoanime": gogo.main,
    }
    P = Provider()
    if args.update:
        P.update()
    provider = None
    current_user = getpass.getuser()
    if provider is None:
        subprocess.run(["clear"])
        print(util.colorcodes["Bold"] + f"Hello, {current_user}!\n" + util.colorcodes["Reset"])
        print(util.colorcodes["Gray"] + "[*] This script is still in development so there will be some bugs!\nif you find any report them to: https://github.com/carrotshniper21/bc4e-cli" + util.colorcodes["Reset"])
        print(util.colorcodes["Yellow"] + "[!] WARNING: " + util.colorcodes["Reset"] + "No provider chosen choosing default\n")
        providers[P.default_provider](args)
    elif provider is not None:
        print(util.colorcodes["Bold"] + f"Hello, {current_user}!\n" + util.colorcodes["Reset"])
        print(util.colorcodes["Gray"] + "[*] This script is still in development so there will be some bugs!\nif you find any report them to: https://github.com/carrotshniper21/bc4e-cli" + util.colorcodes["Reset"])
        providers[provider](args)


if __name__ == "__main__":
    main()

