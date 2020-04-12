from linebot.models import (
    SourceGroup,
    SourceRoom,
    SourceUser
)

import random

f_adjectives = open('name_adjectives.txt', 'r')
f_animals = open('name_animals.txt', 'r')
adjectives = f_adjectives.read().splitlines()
animals = f_animals.read().splitlines()

def text_contains(text, keywords, series=False, max_len=9999):
    if len(text) > max_len:
        return False

    if series:
        idx = 0
        for keyword in keywords:
            new_idx = text.find(keyword)
            if new_idx < idx:
                return False
            idx = new_idx
        return True
    
    for keyword in keywords:
        if (text.find(keyword) == -1):
            return False
    return True

def get_source_id(event):
    source_id = None
    if (isinstance(event.source, SourceGroup)):
        source_id = event.source.group_id
    if (isinstance(event.source, SourceRoom)):
        source_id = event.source.room_id
    if (isinstance(event.source, SourceUser)):
        source_id = event.source.user_id

    return source_id

def generate_random_name():
    global adjectives
    global animals

    adjective = random.choice(adjectives)
    animal = random.choice(animals)

    return f"{adjective} {animal}"
