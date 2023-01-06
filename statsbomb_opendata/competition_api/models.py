from uuid import uuid4
from django.db import models

from django_countries.fields import CountryField


class Competition(models.Model):

    id_competition: models.UUIDField = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    statsbomb_id: models.PositiveIntegerField = models.PositiveIntegerField(unique=True)
    
    name: models.CharField = models.CharField(max_length=128, unique=True)
    is_women: models.BooleanField = models.BooleanField(default=False)
    is_youth: models.BooleanField = models.BooleanField(default=False)
    is_international: models.BooleanField = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def get_id(self) -> uuid4:
        return self.id_competition


class Season(models.Model):

    id_season: models.UUIDField = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    statsbomb_id: models.PositiveIntegerField = models.PositiveIntegerField(unique=True)
    
    name: models.CharField = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return f'Season {self.name}'

    def get_id(self) -> uuid4:
        return self.id_season


class CompetitionEdition(models.Model):

    id_competition_edition: models.UUIDField = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    competition: models.ForeignKey = models.ForeignKey(to=Competition, on_delete=models.CASCADE)
    season: models.ForeignKey = models.ForeignKey(to=Season, on_delete=models.CASCADE)

    country: CountryField = CountryField()
    match_available: models.DateTimeField = models.DateTimeField(null=True, editable=False)
    match_available_360: models.DateTimeField = models.DateTimeField(null=True, editable=False)
    match_updated: models.DateTimeField = models.DateTimeField(null=True)
    match_updated_360: models.DateTimeField = models.DateTimeField(null=True)
    match_outdated: models.BooleanField = models.BooleanField(default=True)
    match_outdated_360: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.competition.name} ({self.season.name})'

    def get_id(self) -> uuid4:
        return self.id_competition_edition
