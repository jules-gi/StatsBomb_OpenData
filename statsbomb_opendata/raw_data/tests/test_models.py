from datetime import date, datetime

from django.test import TestCase

from raw_data.models import (
    Competition, CompetitionEdition, Game, Manager, Referee, Season, Stadium, Team
)


class BaseModelTestCase(TestCase):

    competition: Competition
    competition_edition: CompetitionEdition
    game: Game
    away_manager: Manager
    home_manager: Manager
    referee: Referee
    season: Season
    stadium: Stadium
    away_team: Team
    home_team: Team

    @classmethod
    def setUpClass(cls) -> None:
        super(BaseModelTestCase, cls).setUpClass()

        cls.competition = Competition(
            name='Friendly Cup',
            statsbomb_id=1
        )
        cls.competition.save()

        cls.season = Season(
            name='2022',
            statsbomb_id=2
        )
        cls.season.save()

        cls.competition_edition = CompetitionEdition(
            competition=cls.competition,
            season=cls.season,
            country='WW',
            match_available=datetime(2022, 8, 1, 12, 0, 0),
            match_available_360=datetime(2022, 8, 1, 12, 0, 0),
            match_updated=datetime(2022, 8, 2, 12, 0, 0),
            match_updated_360=datetime(2022, 8, 2, 12, 0, 0)
        )
        cls.competition_edition.save()
        
        cls.referee = Referee(
            name='Pierluigi Collina',
            statsbomb_id=3,
            country='IT'
        )
        cls.referee.save()
        
        cls.stadium = Stadium(
            name='Maracanã',
            statsbomb_id=4,
            country='BR'
        )
        cls.stadium.save()

        cls.home_manager = Manager(
            name='Alexander Chapman Ferguson',
            statsbomb_id=5,
            nickname='Sir Alex Ferguson',
            dob=date(1941, 12, 31),
            country='GB'
        )
        cls.home_manager.save()

        cls.away_manager = Manager(
            name='Arsène Charles Ernest Wenger',
            statsbomb_id=6,
            nickname='Arsene Wenger',
            dob=date(1949, 10, 22),
            country='FR'
        )
        cls.away_manager.save()
        
        cls.home_team = Team(
            name='Manchester United',
            country='EN',
            gender='M',
            statsbomb_id=7
        )
        cls.home_team.save()

        cls.away_team = Team(
            name='Arsenal',
            country='EN',
            gender='M',
            statsbomb_id=8
        )
        cls.away_team.save()
        
        cls.game = Game(
            competition_edition=cls.competition_edition,
            home_team=cls.home_team,
            away_team=cls.away_team,
            kick_off=datetime(2022, 7, 31, 20, 30, 0),
            match_week=1,
            competition_stage='Group stage',
            stadium=cls.stadium,
            referee=cls.referee,
            home_manager=cls.home_manager,
            away_manager=cls.away_manager,
            last_updated=datetime(2022, 8, 2, 12, 0, 0),
            last_updated_360=datetime(2022, 8, 2, 12, 0, 0),
            statsbomb_id=9
        )
        cls.game.save()


class CompetitionTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:
        
        self.assertIsNotNone(self.competition.id)
        self.assertEqual(self.competition.name, 'Friendly Cup')
        self.assertEqual(self.competition.statsbomb_id, 1)

        self.assertFalse(self.competition.is_women)
        self.assertFalse(self.competition.is_youth)
        self.assertFalse(self.competition.is_international)

    def test_str(self) -> None:

        self.assertEqual(str(self.competition), 'Friendly Cup')
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.competition), '{class_name} object [{uuid_value}]'.format(
            class_name=self.competition.__class__.__name__,
            uuid_value=self.competition.id
        ))


class SeasonTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:

        self.assertIsNotNone(self.season.id)
        self.assertEqual(self.season.name, '2022')
        self.assertEqual(self.season.statsbomb_id, 2)

    def test_str(self) -> None:

        self.assertEqual(str(self.season), 'Season 2022')    
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.season), '{class_name} object [{uuid_value}]'.format(
            class_name=self.season.__class__.__name__,
            uuid_value=self.season.id
        ))


class CompetitionEditionTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:

        self.assertIsNotNone(self.competition_edition.id)
        self.assertEqual(self.competition_edition.name, 'Friendly Cup 2022')
        self.assertIsNone(self.competition_edition.statsbomb_id)

        self.assertEqual(self.competition_edition.competition, self.competition)
        self.assertEqual(self.competition_edition.season, self.season)
        self.assertEqual(self.competition_edition.country.code, 'WW')
        self.assertEqual(self.competition_edition.match_available, datetime(2022, 8, 1, 12, 0, 0))
        self.assertEqual(self.competition_edition.match_available_360, datetime(2022, 8, 1, 12, 0, 0))
        self.assertEqual(self.competition_edition.match_updated, datetime(2022, 8, 2, 12, 0, 0))
        self.assertEqual(self.competition_edition.match_updated_360, datetime(2022, 8, 2, 12, 0, 0))
        self.assertTrue(self.competition_edition.match_outdated)
        self.assertTrue(self.competition_edition.match_outdated_360)

    def test_str(self) -> None:

        self.assertEqual(str(self.competition_edition), 'Friendly Cup 2022')
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.competition_edition), '{class_name} object [{uuid_value}]'.format(
            class_name=self.competition_edition.__class__.__name__,
            uuid_value=self.competition_edition.id
        ))


class RefereeTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:

        self.assertIsNotNone(self.referee.id)
        self.assertEqual(self.referee.name, 'Pierluigi Collina')
        self.assertEqual(self.referee.statsbomb_id, 3)

        self.assertEqual(self.referee.country.code, 'IT')

    def test_str(self) -> None:

        self.assertEqual(str(self.referee), 'Pierluigi Collina')
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.referee), '{class_name} object [{uuid_value}]'.format(
            class_name=self.referee.__class__.__name__,
            uuid_value=self.referee.id
        ))


class StadiumTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:

        self.assertIsNotNone(self.stadium.id)
        self.assertEqual(self.stadium.name, 'Maracanã')
        self.assertEqual(self.stadium.statsbomb_id, 4)

        self.assertEqual(self.stadium.country.code, 'BR')

    def test_str(self) -> None:

        self.assertEqual(str(self.stadium), 'Maracanã')
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.stadium), '{class_name} object [{uuid_value}]'.format(
            class_name=self.stadium.__class__.__name__,
            uuid_value=self.stadium.id
        ))


class ManagerTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:

        # Home manager
        self.assertIsNotNone(self.home_manager.id)
        self.assertEqual(self.home_manager.name, 'Alexander Chapman Ferguson')
        self.assertEqual(self.home_manager.statsbomb_id, 5)

        self.assertEqual(self.home_manager.nickname, 'Sir Alex Ferguson')
        self.assertEqual(self.home_manager.dob, date(1941, 12, 31))
        self.assertEqual(self.home_manager.country.code, 'GB')

        # Away manager
        self.assertIsNotNone(self.away_manager.id)
        self.assertEqual(self.away_manager.name, 'Arsène Charles Ernest Wenger')
        self.assertEqual(self.away_manager.statsbomb_id, 6)

        self.assertEqual(self.away_manager.nickname, 'Arsene Wenger')
        self.assertEqual(self.away_manager.dob, date(1949, 10, 22))
        self.assertEqual(self.away_manager.country.code, 'FR')

    def test_str(self) -> None:

        self.assertEqual(str(self.home_manager), 'Sir Alex Ferguson')
        self.assertEqual(str(self.away_manager), 'Arsene Wenger')

        self.home_manager.nickname = None
        self.assertEqual(str(self.home_manager), 'Alexander Chapman Ferguson')
        self.home_manager.nickname = 'Sir Alex Ferguson'
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.home_manager), '{class_name} object [{uuid_value}]'.format(
            class_name=self.home_manager.__class__.__name__,
            uuid_value=self.home_manager.id
        ))
        self.assertEqual(repr(self.away_manager), '{class_name} object [{uuid_value}]'.format(
            class_name=self.away_manager.__class__.__name__,
            uuid_value=self.away_manager.id
        ))


class TeamTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:
        
        # Home team
        self.assertIsNotNone(self.home_team.id)
        self.assertEqual(self.home_team.name, 'Manchester United')
        self.assertEqual(self.home_team.statsbomb_id, 7)

        self.assertEqual(self.home_team.gender, 'M')
        self.assertEqual(self.home_team.country.code, 'EN')

        # Away team
        self.assertIsNotNone(self.away_team.id)
        self.assertEqual(self.away_team.name, 'Arsenal')
        self.assertEqual(self.away_team.statsbomb_id, 8)

        self.assertEqual(self.away_team.gender, 'M')
        self.assertEqual(self.away_team.country.code, 'EN')

    def test_str(self) -> None:

        self.assertEqual(str(self.home_team), 'Manchester United')    
        self.assertEqual(str(self.away_team), 'Arsenal')
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.home_team), '{class_name} object [{uuid_value}]'.format(
            class_name=self.home_team.__class__.__name__,
            uuid_value=self.home_team.id
        ))
        self.assertEqual(repr(self.away_team), '{class_name} object [{uuid_value}]'.format(
            class_name=self.away_team.__class__.__name__,
            uuid_value=self.away_team.id
        ))


class GameTestCase(BaseModelTestCase):

    def test_created_properly(self) -> None:

        self.assertIsNotNone(self.game.id)
        self.assertEqual(self.game.name, 'Manchester United vs. Arsenal (2022-07-31)')
        self.assertEqual(self.game.statsbomb_id, 9)

        self.assertEqual(self.game.competition_edition, self.competition_edition)
        self.assertEqual(self.game.home_team, self.home_team)
        self.assertEqual(self.game.away_team, self.away_team)
        self.assertEqual(self.game.kick_off, datetime(2022, 7, 31, 20, 30, 0))
        self.assertEqual(self.game.match_week, 1)
        self.assertEqual(self.game.competition_stage, 'Group stage')
        self.assertEqual(self.game.stadium, self.stadium)
        self.assertEqual(self.game.referee, self.referee)
        self.assertEqual(self.game.home_manager, self.home_manager)
        self.assertEqual(self.game.away_manager, self.away_manager)
        self.assertEqual(self.game.stadium, self.stadium)
        self.assertEqual(self.game.last_updated, datetime(2022, 8, 2, 12, 0, 0))
        self.assertEqual(self.game.last_updated_360, datetime(2022, 8, 2, 12, 0, 0))

    def test_str(self) -> None:

        self.assertEqual(str(self.game), 'Manchester United vs. Arsenal (2022-07-31)')
    
    def test_repr(self) -> None:

        self.assertEqual(repr(self.game), '{class_name} object [{uuid_value}]'.format(
            class_name=self.game.__class__.__name__,
            uuid_value=self.game.id
        ))
