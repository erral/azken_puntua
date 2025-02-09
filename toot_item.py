# -*- coding: utf-8 -*-
"""
This script is inspired by https://github.com/ZiTAL/bermiotarra/tree/master/bot by @ZiTAL
"""
import json
import datetime
import random
from mastodon import Mastodon
import os


def toot_item_from_list():
    """main function to toot items"""
    item = get_random_item_to_toot()
    if item:
        toot_item(item)


def get_random_item_to_toot():
    """select an untooted item"""
    word = {}
    with open("azken_puntuak.json", "r") as fp:
        dictionary = json.load(fp)
        not_tweeted = [item for item in dictionary if "tweeted" not in item]
        if not_tweeted:
            word = random.choice(not_tweeted)
        
            word["tweeted"] = True
            word["tweeted_at"] = datetime.datetime.utcnow().isoformat()
            dictionary.remove(word)
            dictionary.append(word)
        
            with open("azken_puntuak.json", "w") as fp:
                json.dump(dictionary, fp, indent=4)
        
            return word
    return None


def toot_item(item):
    """effectively toot the text"""
    text = "{text} \n\n{singer}\n{url}"
    azken_puntua = item.get("text", "")
    singer = item.get("singer", "")
    if azken_puntua and singer:
        url = item.get("url", "")
        text = text.format(text=azken_puntua, singer=singer, url=url)

        text = text.strip()

        if text:
            api = Mastodon(
                access_token=os.environ.get("ACCESS_TOKEN"),
                api_base_url="https://mastodon.eus",
            )
            res = api.toot(text)
            if res.get("id"):
                print(f'Tooted: "{text}"')


if __name__ == "__main__":
    toot_item_from_list()
