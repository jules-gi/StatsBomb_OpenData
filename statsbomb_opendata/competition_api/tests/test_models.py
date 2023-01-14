from datetime import datetime
from pytz import UTC

from django.test import TestCase

from ..models import Competition, CompetitionEdition, Season


class BaseApiTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        # Competitions
        cls.la_liga = Competition.objects.create(
            statsbomb_id=0,
            name='La Liga',
            is_women=False,
            is_youth=True,
            is_international=False
        )
        cls.world_cup = Competition.objects.create(
            statsbomb_id=1,
            name='Women\'s World Cup',
            is_women=True,
            is_youth=False,
            is_international=True
        )

        # Seasons
        cls.season_2018 = Season.objects.create(
            statsbomb_id=0,
            name='2018',
        )
        cls.season_2018_2019 = Season.objects.create(
            statsbomb_id=1,
            name='2018/2019',
        )
        cls.season_2020 = Season.objects.create(
            statsbomb_id=2,
            name='2020',
        )
        cls.season_2019_2020 = Season.objects.create(
            statsbomb_id=3,
            name='2019/2020',
        )

        # Competition editions
        cls.la_liga_2018_2019 = CompetitionEdition.objects.create(
            competition=cls.la_liga,
            season=cls.season_2018_2019,
            country='ES',
            match_available=datetime(2019, 1, 13, 20, 0, 0, tzinfo=UTC),
            match_available_360=datetime(2019, 1, 13, 20, 0, 0, tzinfo=UTC),
            match_updated=datetime(2019, 7, 28, 10, 30, 0, tzinfo=UTC),
            match_updated_360=datetime(2019, 7, 28, 10, 30, 0, tzinfo=UTC),
            match_outdated=False,
            match_outdated_360=False
        )
        cls.world_cup_2018 = CompetitionEdition.objects.create(
            competition=cls.world_cup,
            season=cls.season_2018,
            country='FI',
            match_available=datetime(2018, 9, 7, 14, 0, 0, tzinfo=UTC),
            match_available_360=None,
            match_updated=datetime(2018, 9, 7, 14, 00, 0, tzinfo=UTC),
            match_updated_360=None,
            match_outdated=False,
            match_outdated_360=False
        )


class TestCompetitionModel(BaseApiTestCase):
    
    def test_creation(self) -> None:
        self.assertEqual(Competition.objects.count(), 2)

        self.assertIsNotNone(self.la_liga.get_id())
        self.assertEqual(self.la_liga.statsbomb_id, 0)
        self.assertEqual(self.la_liga.name, 'La Liga')
        self.assertFalse(self.la_liga.is_women)
        self.assertTrue(self.la_liga.is_youth)
        self.assertFalse(self.la_liga.is_international)

        self.assertIsNotNone(self.world_cup.get_id())
        self.assertEqual(self.world_cup.statsbomb_id, 1)
        self.assertEqual(self.world_cup.name, 'Women\'s World Cup')
        self.assertTrue(self.world_cup.is_women)
        self.assertFalse(self.world_cup.is_youth)
        self.assertTrue(self.world_cup.is_international)

    def test__str__(self) -> None:
        self.assertEqual(str(self.la_liga), 'La Liga')
        self.assertEqual(str(self.world_cup), 'Women\'s World Cup')
    
    def test_get_id(self) -> None:
        self.assertEqual(self.la_liga.get_id(), self.la_liga.id_competition)
        self.assertEqual(self.world_cup.get_id(), self.world_cup.id_competition)

class TestSeasonModel(BaseApiTestCase):
    
    def test_creation(self) -> None:
        self.assertEqual(Season.objects.count(), 4)

        self.assertIsNotNone(self.season_2018.get_id())
        self.assertEqual(self.season_2018.statsbomb_id, 0)
        self.assertEqual(self.season_2018.name, '2018')

        self.assertIsNotNone(self.season_2018_2019.get_id())
        self.assertEqual(self.season_2018_2019.statsbomb_id, 1)
        self.assertEqual(self.season_2018_2019.name, '2018/2019')

        self.assertIsNotNone(self.season_2020.get_id())
        self.assertEqual(self.season_2020.statsbomb_id, 2)
        self.assertEqual(self.season_2020.name, '2020')

        self.assertIsNotNone(self.season_2019_2020.get_id())
        self.assertEqual(self.season_2019_2020.statsbomb_id, 3)
        self.assertEqual(self.season_2019_2020.name, '2019/2020')

    def test__str__(self) -> None:
        self.assertEqual(str(self.season_2018), 'Season 2018')
        self.assertEqual(str(self.season_2018_2019), 'Season 2018/2019')
        self.assertEqual(str(self.season_2020), 'Season 2020')
        self.assertEqual(str(self.season_2019_2020), 'Season 2019/2020')
    
    def test_get_id(self) -> None:
        self.assertEqual(self.season_2018.get_id(), self.season_2018.id_season)
        self.assertEqual(self.season_2018_2019.get_id(), self.season_2018_2019.id_season)
        self.assertEqual(self.season_2020.get_id(), self.season_2020.id_season)
        self.assertEqual(self.season_2019_2020.get_id(), self.season_2019_2020.id_season)

class TestCompetitionEditionModel(BaseApiTestCase):
    
    def test_creation(self) -> None:
        self.assertEqual(CompetitionEdition.objects.count(), 2)
        
        self.assertIsNotNone(self.la_liga_2018_2019.get_id())
        self.assertEqual(self.la_liga_2018_2019.competition, self.la_liga)
        self.assertEqual(self.la_liga_2018_2019.season, self.season_2018_2019)
        self.assertEqual(self.la_liga_2018_2019.country.name, 'Spain')
        self.assertEqual(self.la_liga_2018_2019.match_available, datetime(2019, 1, 13, 20, 0, 0, tzinfo=UTC))
        self.assertEqual(self.la_liga_2018_2019.match_available_360, datetime(2019, 1, 13, 20, 0, 0, tzinfo=UTC))
        self.assertEqual(self.la_liga_2018_2019.match_updated, datetime(2019, 7, 28, 10, 30, 0, tzinfo=UTC))
        self.assertEqual(self.la_liga_2018_2019.match_updated_360, datetime(2019, 7, 28, 10, 30, 0, tzinfo=UTC))
        self.assertFalse(self.la_liga_2018_2019.match_outdated)
        self.assertFalse(self.la_liga_2018_2019.match_outdated_360)

        self.assertIsNotNone(self.world_cup_2018.get_id())
        self.assertEqual(self.world_cup_2018.competition, self.world_cup)
        self.assertEqual(self.world_cup_2018.season, self.season_2018)
        self.assertEqual(self.world_cup_2018.country.name, 'Finland')
        self.assertEqual(self.world_cup_2018.match_available, datetime(2018, 9, 7, 14, 0, 0, tzinfo=UTC))
        self.assertIsNone(self.world_cup_2018.match_available_360)
        self.assertEqual(self.world_cup_2018.match_updated, datetime(2018, 9, 7, 14, 00, 0, tzinfo=UTC))
        self.assertIsNone(self.world_cup_2018.match_updated_360)
        self.assertFalse(self.world_cup_2018.match_outdated)
        self.assertFalse(self.world_cup_2018.match_outdated_360)

    def test__str__(self) -> None:
        self.assertEqual(str(self.la_liga_2018_2019), 'La Liga (2018/2019)')
        self.assertEqual(str(self.world_cup_2018), 'Women\'s World Cup (2018)')
    
    def test_get_id(self) -> None:
        self.assertEqual(self.la_liga_2018_2019.get_id(), self.la_liga_2018_2019.id_competition_edition)
        self.assertEqual(self.world_cup_2018.get_id(), self.world_cup_2018.id_competition_edition)
