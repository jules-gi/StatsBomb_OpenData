import uuid
from django.db import models

from django_countries.fields import CountryField


class AbstractStatsBombModel(models.Model):

    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=128)
    statsbomb_id: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        abstract = True
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} object [{self.id}]'


class Competition(AbstractStatsBombModel):

    is_women: models.BooleanField = models.BooleanField(default=False)
    is_youth: models.BooleanField = models.BooleanField(default=False)
    is_international: models.BooleanField = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Season(AbstractStatsBombModel):

    def __str__(self) -> str:
        return f'Season {self.name}'


class CompetitionEdition(AbstractStatsBombModel):

    statsbomb_id: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(null=True)

    competition: models.ForeignKey = models.ForeignKey(to=Competition, on_delete=models.SET_NULL, null=True)
    season: models.ForeignKey = models.ForeignKey(to=Season, on_delete=models.SET_NULL, null=True)
    country: CountryField = CountryField()
    match_available: models.DateTimeField = models.DateTimeField(null=True)
    match_available_360: models.DateTimeField = models.DateTimeField(null=True)
    match_updated: models.DateTimeField = models.DateTimeField(null=True)
    match_updated_360: models.DateTimeField = models.DateTimeField(null=True)
    match_outdated: models.BooleanField = models.BooleanField(default=True)
    match_outdated_360: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self) -> None:

        if not self.name:
            self.name = f'{self.competition.name} {self.season.name}'
        
        super().save()


class Manager(AbstractStatsBombModel):
    nickname: models.CharField = models.CharField(max_length=128, null=True)
    dob: models.DateField = models.DateField(null=True)
    country: CountryField = CountryField(null=True)

    def __str__(self) -> str:
        return self.nickname if self.nickname else self.name


class Referee(AbstractStatsBombModel):
    country: CountryField = CountryField(null=True)

    def __str__(self) -> str:
        return self.name


class Stadium(AbstractStatsBombModel):
    country: CountryField = CountryField(null=True)

    def __str__(self) -> str:
        return self.name


class Team(AbstractStatsBombModel):

    gender: models.CharField = models.CharField(max_length=1, choices=[('M', 'Men'), ('W', 'Women')])
    country: CountryField = CountryField(null=True)

    def __str__(self) -> str:
        return self.name


class Game(AbstractStatsBombModel):

    competition_edition: models.ForeignKey = models.ForeignKey(to=CompetitionEdition, on_delete=models.SET_NULL, null=True)
    home_team: models.ForeignKey = models.ForeignKey(to=Team, related_name='home_games', on_delete=models.SET_NULL, null=True)
    away_team: models.ForeignKey = models.ForeignKey(to=Team, related_name='away_games', on_delete=models.SET_NULL, null=True)
    
    kick_off: models.DateTimeField = models.DateTimeField()
    match_week: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(null=True)
    competition_stage: models.CharField = models.CharField(max_length=100, null=True)
    stadium: models.ForeignKey = models.ForeignKey(to=Stadium, on_delete=models.SET_NULL, null=True)
    referee: models.ForeignKey = models.ForeignKey(to=Referee, on_delete=models.SET_NULL, null=True)
    home_manager: models.ForeignKey = models.ForeignKey(to=Manager, related_name='home_games', on_delete=models.SET_NULL, null=True)
    away_manager: models.ForeignKey = models.ForeignKey(to=Manager, related_name='away_games', on_delete=models.SET_NULL, null=True)
    
    last_updated: models.DateTimeField = models.DateTimeField()
    last_updated_360: models.DateTimeField = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self) -> None:

        if not self.name:
            self.name = f'{self.home_team.name} vs. {self.away_team.name} ({self.kick_off.date()})'
        
        super().save()
