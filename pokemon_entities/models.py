from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя на китайском')
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to="pokemons",
        null=True,
        blank=True
    )
    description = models.TextField(blank=True,verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционирует'
    )

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился в')
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет в')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')
