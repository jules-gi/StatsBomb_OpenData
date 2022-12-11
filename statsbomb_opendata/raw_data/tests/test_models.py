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
            name='CompetitionName',
            statsbomb_id=1
        )
        cls.competition.save()

        cls.season = Season(
            name='SeasonName',
            statsbomb_id=6
        )
        cls.season.save()

        cls.competition_edition = CompetitionEdition(
            competition=cls.competition,
            season=cls.season,
            country='WW'
        )
        cls.competition_edition.save()
        
        cls.referee = Referee(
            name='RefereeName',
            statsbomb_id=5
        )
        cls.referee.save()
        
        cls.stadium = Stadium(
            name='StadiumName',
            statsbomb_id=7
        )
        cls.stadium.save()

        cls.away_manager = Manager(
            name='AwayManagerName',
            statsbomb_id=3
        )
        cls.away_manager.save()
        
        cls.home_manager = Manager(
            name='HomeManagerName',
            statsbomb_id=4
        )
        cls.home_manager.save()
        
        cls.away_team = Team(
            name='AwayTeamName',
            gender='M',
            statsbomb_id=8
        )
        cls.away_team.save()
        
        cls.home_team = Team(
            name='HomeTeamName',
            gender='W',
            statsbomb_id=9
        )
        cls.home_team.save()

        cls.game = Game(
            competition_edition=cls.competition_edition,
            home_team=cls.home_team,
            away_team=cls.away_team,
            kick_off=datetime(2020, 2, 10, 20, 0, 0),
            stadium=cls.stadium,
            referee=cls.referee,
            home_manager=cls.home_manager,
            away_manager=cls.away_manager,
            last_updated=datetime.now(),
            statsbomb_id=2
        )
        cls.game.save()
    
    def test_created_properly(self):

        values_to_test = [
            (self.competition, ('CompetitionName', 1)),
            (self.competition_edition, ('CompetitionName SeasonName', None)),
            (self.game, ('HomeTeamName vs. AwayTeamName (2020-02-10)', 2)),
            (self.away_manager, ('AwayManagerName', 3)),
            (self.home_manager, ('HomeManagerName', 4)),
            (self.referee, ('RefereeName', 5)),
            (self.season, ('SeasonName', 6)),
            (self.stadium, ('StadiumName', 7)),
            (self.away_team, ('AwayTeamName', 8)),
            (self.home_team, ('HomeTeamName', 9))
        ]

        for instance, (name, statsbomb_id) in values_to_test:
            self.assertIsNotNone(instance.id)
            self.assertEqual(instance.name, name)
            self.assertEqual(instance.statsbomb_id, statsbomb_id)
