"""
For choosing provider and running the main function
"""
import sys
from providers import zoro
from providers import enime
from providers import gogo
from providers import pahe

def choose_provider():
    """
    For choosing the provider the user wants
    """
    try:
        all_providers = ["zoro", "animepahe", "enime", "gogoanime"]
        print("[1] zoro\n[2] animepahe (slow)\n[3] enime\n[4] gogoanime\n")
        chosen_provider = int(input("{+} Choose a provider 1-4: "))
        return all_providers[chosen_provider - 1]
    except ValueError:
        print("{!} Enter a valid number")
        sys.exit()

if __name__ == "__main__":
    provider = choose_provider()
    providers = {
        "zoro": zoro.main,
        "animepahe": pahe.main,
        "enime": enime.main,
        "gogoanime": gogo.main,
    }
    providers[provider]()

