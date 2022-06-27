import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
from liquipediapy.smash_modules.player import smash_player
from liquipediapy.smash_modules.team import smash_team

class smash():

	def __init__(self,appname):
		self.appname = appname
		self.liquipedia = liquipediapy(appname,'smash')
		self.__image_base_url = 'https://liquipedia.net'
		


	def get_players(self):
		# Retrieves prominent Smash players from all Smash games
		soup,__ = self.liquipedia.parse('Portal:Players')
		rows = soup.findAll('ul')
		players = []
		for row in rows:
			if len(row) == 1:
				player={}
				cells = row.find_all('a')
				print(cells)
				player['Country'] = cells[0].get('title')
				player['Player'] = cells[1].get('title')
				if len(player) > 0:
					players.append(player)

		return players
	
	def get_player_info(self,playerName,results=False):
		# Retrieves player info for a given player
		player_object = smash_player()
		playerName = player_object.process_playerName(playerName)
		soup,redirect_value = self.liquipedia.parse(playerName)
		if redirect_value is not None:
			playerName = redirect_value
		player = {}
		player['info'] = player_object.get_player_infobox(soup)
		player['links'] = player_object.get_player_links(soup)
		player['history'] = player_object.get_player_history(soup)
		player['achievements'] = player_object.get_player_achivements(soup)
		if results:
			parse_value = playerName + "/Results"
			try:
				soup,__ = self.liquipedia.parse(parse_value)
			except ex.RequestsException:
				player['results'] = []
			else:	
				player['results'] = player_object.get_player_achivements(soup)

		return player


	def get_teams(self):
		# Retrieves a list of teams with sponsored Smash players
		soup,__ = self.liquipedia.parse('Portal:Teams')
		teams = []
		templates = soup.find_all('span',class_="team-template-team-standard")
		for team in templates:
			teams.append(team.a['title'])
			
		return teams


	def get_team_info(self,teamName):
		# Retrieves info for a given team
		team_object = smash_team()
		teamName = team_object.process_teamName(teamName)	
		soup,redirect_value = self.liquipedia.parse(teamName)
		if redirect_value is not None:
			teamName = redirect_value
		team = {}	
		team['info'] = team_object.get_team_infobox(soup)
		team['team_roster'] = team_object.get_team_roster(soup)

		return team	

	def get_transfers(self):
		# Retrieves list of transfers
		transfers = []
		soup,__ = self.liquipedia.parse('Player_Transfers')
		indexes = soup.find('div',class_='divHeaderRow')
		index_values = []
		for cell in indexes.find_all('div'):
			index_values.append(cell.get_text())
		rows = soup.find_all('div',class_='divRow')
		for row in rows:
			transfer = {}
			cells = row.find_all('div',class_='divCell')
			for i in range(0,len(cells)):
				key = index_values[i]
				value = cells[i].get_text()
				if key == "Player":
					value = [val for val in value.split(' ') if len(val) > 0]
				if key == "Old":
					try:
						value = cells[i].find('a').get('title')	
					except	AttributeError:
						value = "None"
				if key == "New":
					try:
						value = cells[i].find('a').get('title')	
					except	AttributeError:
						value = "None"
				transfer[key] = value
			transfer = {k: v for k, v in transfer.items() if len(k) > 0}	
			transfers.append(transfer)	

		return transfers	

	def get_tournaments(self):
		# Retrieves completed, ongoing, and upcoming tournaments
		tournaments = []
		soup,__ = self.liquipedia.parse('Liquipedia:Tournaments')
		listed_tournaments = soup.find_all('li')
		status = ''
		for listed_tournament in listed_tournaments:
			tournament = {}
			cells = listed_tournament.get_text().split('|')
			if len(cells) == 1:
				status = cells[1]
			else:
				try:
					tournament['Tournament'] = cells[1]
					tournament['Start Date'] = cells[3].split('=')[1]
					tournament['End Date'] = cells[4].split('=')[1]
				except AttributeError:
					continue		
				tournaments.append(tournament)
		return tournaments