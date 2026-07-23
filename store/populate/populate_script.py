import os
import sys
import django

grandparent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(grandparent_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from store.populate.games import games_data as gd
from store.models import Game, Console, Platform, Genre



def get_game_items(item, item_identifier, game_dictionary_value):
    all_items = []
    for game in gd:
        current_items = [c.strip() for c in game[game_dictionary_value].split(',')]
        all_items += current_items

    unique_items = list(set(all_items))
    items = []
    for unique_item in unique_items:
        try:
            params = {item_identifier: unique_item}
            obj = item.objects.get(**params)

            items.append(obj)
        except item.DoesNotExist:
            print(f'Error: {item.__name__} "{unique_item}" not found ')

    return items

def get_attributes(all_attributes, game_value, field_to_check):
    attributes = []
    value_as_strings = [p.strip() for p in game_value.split(',')]
    for att in all_attributes:
        current_value = getattr(att, field_to_check)
        if current_value in value_as_strings:
            attributes.append(att)
    return attributes


def create_games():
    platforms = get_game_items(Platform,'platform_name','platforms')
    consoles = get_game_items(Console,'console_name','consoles')
    genres = get_game_items(Genre,'genre_name','genres')

    for game in gd:
        game_consoles = get_attributes(all_attributes=consoles,
                              game_value=game['consoles'],
                              field_to_check='console_name')
        game_platforms = get_attributes(all_attributes=platforms,
                              game_value=game['platforms'],
                              field_to_check='platform_name')
        game_genres = get_attributes(all_attributes=genres,
                              game_value=game['genres'],
                              field_to_check='genre_name')

        game_obj, created = Game.objects.update_or_create(
            title=game['title'],
            defaults={
                "description": game['description'],
                "developer": game['developer'],
                "release_date": game['release_date'],
                "img_url": game['img_url'],
                "price": game['price'],
                "quantity_sold": game['quantity_sold']
            }
        )

        game_obj.genres.set(game_genres)
        game_obj.platforms.set(game_platforms)
        game_obj.consoles.set(game_consoles)


create_games()