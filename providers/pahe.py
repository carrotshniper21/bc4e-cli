"""
A scraper designed to watch anime tv shows and movies alike
"""

import subprocess
import json
import sys
from pyfzf.pyfzf import FzfPrompt
import requests
from utils import util

def choose_best_quality(qualities):
    ordered_qualities = ["1080", "720", "480"]

    for quality in ordered_qualities:
        if quality in qualities:
            return quality

    return qualities[0]

class PaheClient:
    def __init__(self):
        self.BASE_URL = "https://api.consumet.org/anime/animepahe/"
        self.fzf = FzfPrompt()

    def watch_pahe(self, name):
        r = requests.get(f"{self.BASE_URL}{name}")
        return json.loads(r.text)

    def parse_data(self):
        try:
            query = input("[+] Enter A Anime Name: ")
            json_data = self.watch_pahe(query)
            if len(json_data["results"]) == 0:
                print("{!} No Results Found")
                exit()
            else:
                strings = [
                    f'{e["id"]}\t{e["title"]} ({e["type"]})' for e in json_data["results"]
                ]
                output = self.fzf.prompt(
                    strings, "--border -1 --reverse --with-nth 2.."
                )
                [id, name] = output[0].split("\t")
        except IndexError:
            sys.exit()

        return id, name

    def handle_shows(self, anime_data, args):
        number_of_episodes = -1
        for episode in anime_data["episodes"]:
            number_of_episodes += 1
        try:
            episode_number = int(
                input("[+] Please choose a episode 1-" + f"{number_of_episodes + 1}: ")
            )
        except ValueError:
            print(util.colorcodes["Red"] + "[X] ERROR: " + util.colorcodes["Reset"] + "Invalid choice. Try Again.")
            sys.exit()

        for episode in anime_data["episodes"]:
            if episode["number"] == episode_number:
                selected_episode = episode
                _id = selected_episode["id"]
                _title = selected_episode["title"]
                _episode_number = selected_episode["number"]

        a = requests.get(
            f"{self.BASE_URL}watch/{_id}"
        )
        anime_links = json.loads(a.text)
        if args.sources:
            print(anime_links)
        try:
            links = [f'{q["url"]} {q["quality"]}' for q in anime_links["sources"]]
        except KeyError as e:
            print(util.colorcodes["Red"] + "[X] ERROR: " + util.colorcodes["Reset"] + f"An error occured: {e} Exiting...")
            print(util.colorcodes["Gray"] + "[*] Usually if a 'sources' error occurs I would reccomend to try again. or use a diffrent provider" + util.colorcodes["Reset"])
            sys.exit()
        qualities = [p["quality"] for p in anime_links["sources"]]
        best_quality = choose_best_quality(qualities)
        try:
            for link in links:
                if best_quality in link:
                    link = link.split()[0]
                    print(util.colorcodes["Green"] + "[*] SUCCESS: " + util.colorcodes["Reset"] + f"Now Playing 'Episode {_episode_number} {_title}'")
                    print("[+] Press Ctrl+C to exit the program")
                    result = subprocess.run(
                        ["mpv", "--fs", f"{link}", f"--title={_title}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except KeyboardInterrupt:
            clear_screen = input(util.colorcodes["Bold"] + "\n[*] Clear the screen? Y/N " + util.colorcodes["Reset"])
            if clear_screen.lower() == "y":
                subprocess.run(["clear"])
            if clear_screen.lower() == "n":
                sys.exit()

    def get_anime_info(self, id):
        f = requests.get(f"{self.BASE_URL}info/{id}")
        return json.loads(f.text)

    def get_anime_links(self, id, args):
        anime_data = self.get_anime_info(id)
        anime_id = [f'{d["id"]}' for d in anime_data["episodes"]]
        if len(anime_id) != 1:
            self.handle_shows(anime_data, args)

        return anime_id

    def get_episodes(self, anime_id, name):
        h = requests.get(f"{self.BASE_URL}watch/{anime_id[0]}")
        anime_links = json.loads(h.text)
        if args.sources:
            print(anime_links)
        try:
            links = [f'{q["url"]} {q["quality"]}' for q in anime_links["sources"]]
        except KeyError as e:
            print(util.colorcodes["Red"] + "[X] ERROR: " + util.colorcodes["Reset"] + f"An error occured: {e} Exiting...")
            print(util.colorcodes["Gray"] + "[*] Usually if a 'sources' error occurs I would reccomend to try again. or use a diffrent provider" + util.colorcodes["Reset"])
            sys.exit()
        qualities = [p["quality"] for p in anime_links["sources"]]
        best_quality = choose_best_quality(qualities)
        try:
            for link in links:
                if best_quality in link:
                    link = link.split()[0]
                    print(util.colorcodes["Green"] + "[*] SUCCESS: " + util.colorcodes["Reset"] + f"Now Playing '{_title}'")
                    print("[+] Press Ctrl+C to exit the program")
                    subprocess.run(
                        ["mpv", "--fs", f"{link}", f"--title={name.rsplit(' ', 1)[0]}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except KeyboardInterrupt:
            clear_screen = input(util.colorcodes["Bold"] + "\n[*] Clear the screen? Y/N " + util.colorcodes["Reset"])
            if clear_screen.lower() == "y":
                subprocess.run(["clear"])
            if clear_screen.lower() == "n":
                sys.exit()

def main(args):
    pahe_client = PaheClient()
    id, name = pahe_client.parse_data()
    pahe_client.get_anime_info(id)
    anime_id = pahe_client.get_anime_links(id, args)
    pahe_client.get_episodes(anime_id, name, args)

if __name__ == "__main__":
    main()
