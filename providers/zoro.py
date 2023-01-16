import subprocess
import json
import sys
from pyfzf.pyfzf import FzfPrompt
from utils import util
import requests

#TODO Add subtitles later cause i dont want to even though its easy to do

def choose_best_quality(qualities):
    ordered_qualities = ["1080", "720", "480", "360", "240"]

    for quality in ordered_qualities:
        if quality in qualities:
            return quality

    return qualities[0]


class ZoroClient:
    def __init__(self):
        self.fzf = FzfPrompt()
        self.BASE_URL = "https://api.consumet.org/anime/zoro/"

    def watch_zoro(self, name):
        if name == "quit":
            sys.exit()
        r = requests.get(f"{self.BASE_URL}{name}")
        return json.loads(r.text)

    # Media Types --> (TV), (ONA), (SPECIAL), (MOVIE)

    def parse_data(self):
        try:
            query = input("{+} Enter a anime name: ")
            json_data = self.watch_zoro(query)
            if len(json_data["results"]) == 0:
                print("{!} No Results Found")
                exit()
            else:
                strings = [
                    f'{e["id"]}\t{e["title"]} ({e["type"]})'
                    for e in json_data["results"]
                ]
                output = self.fzf.prompt(
                    strings, "--border -1 --reverse --with-nth 2.."
                )
                [id, name] = output[0].split("\t")
        except IndexError:
            sys.exit()

        return id, name

    def get_anime_info(self, id):
        # print(f"{self.BASE_URL}zoro/info?id={id}")
        f = requests.get(f"{self.BASE_URL}info?id={id}")
        return json.loads(f.text)


    def handle_shows(self, anime_data, args):

        number_of_episodes = -1
        for episode in anime_data["episodes"]:
            number_of_episodes += 1
        try:
            episode_number = int(
                input("{+} Please choose a episode 1-" + f"{number_of_episodes + 1}: ")
            )
        except ValueError:
            print("{!} Invalid Choice")

        for episode in anime_data["episodes"]:
            if episode["number"] == episode_number:
                selected_episode = episode
                _id = selected_episode["id"]
                _title = selected_episode["title"]
                _episode_number = selected_episode["number"]

        a = requests.get(
            f"{self.BASE_URL}watch?episodeId={_id}"
        )
        anime_linkss = json.loads(a.text)
        if args.sources:
            print(anime_linkss)
        try:
            links = [f'{qq["url"]} {qq["quality"]}' for qq in anime_linkss["sources"]]
            qualities = [p["quality"] for p in anime_linkss["sources"]]
        except KeyError as e:
            print(util.colorcodes["Yellow"] + "[!] WARNING: " + util.colorcodes["Reset"] + f"An error occured: {e} Exiting...")
            sys.exit()
        best_quality = choose_best_quality(qualities)
        try:
            for link in links:
                if best_quality in link:
                    link = link.split()[0]
                    print(f"Now Playing 'Episode {_episode_number} {_title}'")
                    print("{+} Press Ctrl+C to exit the program")
                    result = subprocess.run(
                        ["mpv", "--fs", f"{link}", f"--title={_title}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except KeyboardInterrupt:
            sys.exit()


    def get_anime_links(self, id, args):
        anime_data = self.get_anime_info(id)
        anime_id = [f'{d["id"]}' for d in anime_data["episodes"]]
        if anime_data["totalEpisodes"] > 1:
            self.handle_shows(anime_data, args)
            sys.exit()

        return anime_id

    def get_episodes(self, anime_id, name, args):
        h = requests.get(
            f"{self.BASE_URL}watch?episodeId={anime_id[0]}"
        )
        anime_links = json.loads(h.text)
        if args.sources:
            print(anime_links)
        try:
            links = [f'{q["url"]} {q["quality"]}' for q in anime_links["sources"]]
        except KeyError as e:
            print(util.colorcodes["Yellow"] + "[!] WARNING: " + util.colorcodes["Reset"] + f"An error occured: {e} Exiting...")
            sys,exit()
        qualities = [p["quality"] for p in anime_links["sources"]]
        best_quality = choose_best_quality(qualities)
        try:
            for link in links:
                if best_quality in link:
                    link = link.split()[0]
                    print(f"Now Playing '{name.rsplit(' ', 1)[0]}'")
                    print("[+] Press Ctrl+C to exit the program")
                    result = subprocess.run(
                        ["mpv", "--fs", f"{link}", f"--title={name.rsplit(' ', 1)[0]}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except KeyboardInterrupt:
            sys.exit()


def main(args):
    zoro_client = ZoroClient()
    id, name = zoro_client.parse_data()
    anime_id = zoro_client.get_anime_links(id, args)
    zoro_client.get_episodes(anime_id, name, args)


if __name__ == "__main__":
    main()
