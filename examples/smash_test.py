from liquipediapy.smash import smash

smash_obj = smash("appname")

players = smash_obj.get_players()

player_details = smash_obj.get_player_info('Leffen',False)

teams = smash_obj.get_teams()

team_details = smash_obj.get_team_info('Team Liquid',True)

transfers = smash_obj.get_transfers()

games = smash_obj.get_upcoming_and_ongoing_tournaments()

tournaments = smash_obj.get_tournaments()