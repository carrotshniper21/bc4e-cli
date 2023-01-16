from pyfzf.pyfzf import FzfPrompt
import subprocess
import requests
import json
from utils import util

def choose_best_quality(qualities):
    ordered_qualities = ["1080", "720", "480"]

    for quality in ordered_qualities:
        if quality in qualities:
            return quality

    return qualities[0]


class EnimeClient():
    def __init__(self):
        self.BASE_URL = "https://api.consumet.org/anime/enime/"
        self.fzf = FzfPrompt()


    def watch_enime(self, name):
        r = requests.get(f"{self.BASE_URL}{name}")
        return json.loads(r.text)

    def parse_data(self):
        try:
            query = input("{+} Enter A Anime Name: ")
            json_data = self.watch_enime(query)
            if len(json_data["results"]) == 0:
                print("{!} No Results Found")
                exit()
            else:
                #TODO Feed to tui later
                strings = [
                    f'{e["id"]}\t{e["title"]} ({e["type"]})'
                    for e in json_data["results"]
                ]
                output = self.fzf.prompt(
                    strings, "--border -1 --reverse --with-nth 2.."
                )
                [id, name] = output[0].split("\t")
        except KeyError:
            exit()

        return id, name

    def handle_shows(self, anime_data):
        number_of_episodes = -1
        for episode in anime_data["episodes"]:
            number_of_episodes += 1
        try:    
            episode_number = int(
                input("{+} Please choose a episode 1-" + f"{number_of_episodes + 1}: ")
            )
        except ValueError:
            print("{!} Invalid Choice")
            exit()
            
        for episode in anime_data["episodes"]:
            if episode["number"] == episode_number:
                selected_episode = episode
                _id = selected_episode["id"] 
                _title = selected_episode["title"]

        a = requests.get(
            f"{self.BASE_URL}watch?episodeId={_id}"
        )
        anime_links = json.loads(a.text)
        print(anime_links)
        try:
            links = [f'{q["url"]} {q["quality"]}' for q in anime_links["sources"]]
        except KeyError as e:
            print("{!} An error occured: " + f"{e}")
            exit()
        qualities = [p["quality"] for p in anime_links["sources"]]
        best_quality = choose_best_quality(qualities)
        try:
            for link in links:
                if best_quality in link:
                    link = link.split()[0]
                    print("{+} Press Ctrl+C to exit the program")
                    result = subprocess.run(
                        ["mpv", "--fs", f"{link}", f"--title={_title.rsplit(' ', 1)[0]}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except KeyboardInterrupt:
            exit()
            
    def get_anime_info(self, id):
        #print(f"{self.BASE_URL}info?id={id}")
        f = requests.get(f"{self.BASE_URL}info?id={id}")
        return json.loads(f.text)

    def get_anime_id(self, id):
        anime_data = self.get_anime_info(id)
        anime_id = [f'{d["id"]}' for d in anime_data["episodes"]]
        if len(anime_id) != 1:
            self.handle_shows(anime_data)

        return anime_id

    def get_episodes(self, anime_id, name):
        h = requests.get(f"{self.BASE_URL}watch?episodeId={anime_id[0]}")
        anime_links = json.loads(h.text)
        print(anime_links)
        links = [f'{q["url"]} {q["quality"]}' for q in anime_links["sources"]]
        qualities = [p["quality"] for p in anime_links["sources"]]
        best_quality = choose_best_quality(qualities)
        try:
            for link in links:
                if best_quality in link:
                    link = link.split()[0]
                    print("[+] Press Ctrl+C to exit the program")
                    result = subprocess.run(
                        ["mpv", "--fs", f"{link}", f"--title={name.rsplit(' ', 1)[0]}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except KeyboardInterrupt:
            exit()            


def main():
    enime_client = EnimeClient()
    id, name = enime_client.parse_data()
    enime_client.get_anime_info(id)
    anime_id = enime_client.get_anime_id(id)
    enime_client.get_episodes(anime_id, name)

if __name__ == "__main__":
    main()