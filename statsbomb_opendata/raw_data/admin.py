from django.contrib import admin

from raw_data import models

# Register your models here.
admin.site.register([
    models.Competition,
    models.CompetitionEdition,
    models.Game,
    models.Manager,
    models.Referee,
    models.Season,
    models.Stadium,
    models.Team
])