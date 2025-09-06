import folium

from django.shortcuts import render
from .models import Pokemon, PokemonEntity
import django.utils.timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()
    now = django.utils.timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)

    for entity in pokemon_entities:
        entity_img_url = DEFAULT_IMAGE_URL
        if entity.pokemon and entity.pokemon.photo:
            entity_img_url = request.build_absolute_uri(entity.pokemon.photo.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_img_url
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = request.build_absolute_uri(pokemon.photo.url)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    now = django.utils.timezone.localtime()

    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=now,
        disappeared_at__gte=now
    )
    img_url = DEFAULT_IMAGE_URL
    if pokemon.photo:
        img_url = request.build_absolute_uri(pokemon.photo.url)

    previous_evolution_pokemon = None
    if pokemon.previous_evolution:
        previous_img_url = DEFAULT_IMAGE_URL
        if pokemon.previous_evolution.photo:
            previous_img_url = request.build_absolute_uri(pokemon.previous_evolution.photo.url)

        previous_evolution_pokemon = {
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': previous_img_url,
            'title_ru': pokemon.previous_evolution.title,

        }
    next_evolution_pokemon = None
    next_evolutions = pokemon.next_evolution.all()
    if next_evolutions.exists():
        next_pokemon = next_evolutions.first()
        next_evolution_img_url = DEFAULT_IMAGE_URL
        if next_pokemon.photo:
            next_evolution_img_url = request.build_absolute_uri(next_pokemon.photo.url)

        next_evolution_pokemon = {
            'pokemon_id' : next_pokemon.id,
            'img_url' : next_evolution_img_url,
            'title_ru' : next_pokemon.title,
        }

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': img_url,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution_pokemon,
        'next_evolution' : next_evolution_pokemon,
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon_entities:
        entity_img_url = DEFAULT_IMAGE_URL
        if entity.pokemon and entity.pokemon.photo:
            entity_img_url = request.build_absolute_uri(entity.pokemon.photo.url)

        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_img_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })