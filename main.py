from providers import zoro
from providers import enime
from providers import gogo
from providers import pahe


def choose_provider():
    try:
        all_providers = ["zoro", "animepahe", "enime", "gogoanime"]
        print("[1] zoro\n[2] animepahe (slow)\n[3] enime\n[4] gogoanime\n")
        provider = int(input("{+} Choose a provider 1-4: "))
        selected_provider = all_providers[provider - 1]
        return selected_provider
    except ValueError:
        print("{!} Enter a valid number")
        exit()


selected_provider = choose_provider()


def main(selected_provider):
    providers = {
        "zoro": zoro.main,
        "animepahe": pahe.main,
        "enime": enime.main,
        "gogoanime": gogo.main,
    }

    providers[selected_provider]()


if __name__ == "__main__":
    main(selected_provider)
