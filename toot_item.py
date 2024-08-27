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
    with open("azken_puntuak.json", "r") as fp:
        dictionary = json.load(fp)
        word = random.choice(dictionary)
        while word and word.get("tweeted"):
            word = random.choice(dictionary)

    word["tweeted"] = True
    word["tweeted_at"] = datetime.datetime.utcnow().isoformat()
    dictionary.remove(word)
    dictionary.append(word)

    with open("azken_puntuak.json", "w") as fp:
        json.dump(dictionary, fp)

    return word


def toot_item(item):
    """effectively toot the text"""
    text = "{text} \n\n{singer}\n{url}"
    text = text.format(text=item["text"], singer=item["singer"], url=item["url"])

    text = text.strip()

    if text:
        api = Mastodon(
            access_token=os.environ.get("ACCESS_TOKEN"),
            api_base_url="https://mastodon.eus",
        )
        res = api.toot(text)
        if res.get("id"):
            print('Tooted: "{}"'.format(text))


if __name__ == "__main__":
    toot_item_from_list()
