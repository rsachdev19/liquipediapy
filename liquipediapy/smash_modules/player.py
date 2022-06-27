import re
from urllib.request import quote
import unicodedata


class smash_player():

	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'
		self.__player_exceptions = []


	def get_player_infobox(self,soup):
		player = {}
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')		
			if 'PlayerImagePlaceholder' not in image_url:
				player['image'] = self.__image_base_url+image_url
			else:
				player['image'] = ''
		except AttributeError:
			player['image'] = ''		

		game = ''
		info_boxes = soup.find_all('div', {'class':['infobox-cell-2', 'infobox-header-2']})
		i = 0
		while i < len(info_boxes):
			if 'infobox-header-2' in info_boxes[i]['class']:
				game = info_boxes[i].get_text()
				if 'Super Smash Bros.' in game or 'Project M' in game:
					player[game] = {}
			elif 'infobox-cell-2' in info_boxes[i]['class']:
				attribute = info_boxes[i].get_text().replace(':','')
				if attribute == 'Country':
					player['country'] = info_boxes[i+1].get_text().split()
				elif attribute == 'Alternate IDs':	
					player['ids'] = info_boxes[i+1].get_text().split(',')
				elif attribute == 'Born':
					player['birth_details'] = unicodedata.normalize("NFKD",info_boxes[i+1].get_text())
				elif attribute == 'Approx. Total Earnings':
					player['earnings'] = int(info_boxes[i+1].get_text().replace('$','').replace(',','').replace('.',''))
				elif attribute == 'Team':
					player['team'] = info_boxes[i+1].get_text()
				elif attribute == 'Current Mains':
					player[game]['current_mains'] = info_boxes[i+1].get_text(';', strip=True).split(';')
				elif attribute == 'Former Mains':
					player[game]['former_mains'] = info_boxes[i+1].get_text(';', strip=True).split(';')
				elif attribute == 'Secondaries':
					player[game]['Secondaries'] = info_boxes[i+1].get_text(';', strip=True).split(';')
				else:
					attribute = attribute.lower().replace('(', '').replace(')', '').replace(' ','_')
					player[attribute] = info_boxes[i+1].get_text().rstrip()
				# Increment i once more to skip info_box[i+1] which contains data
				i += 1
			i += 1
		return player
				

	def get_player_links(self,soup):
		player_links = {}
		try:		
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return player_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[-2].replace('https://','').replace('http://','')
			player_links[site_name] = link.get('href')

		return player_links	

	def get_player_history(self,soup):
		player_history = []
		histories = soup.find_all('div', class_='infobox-center')
		try:
			histories = histories[-1].find_all('div', recursive=False)
		except IndexError:	
			return player_history
		for history in histories:
			teams_info = history.find_all('div')
			if len(teams_info) > 1:
				team = {}
				team['duration'] = teams_info[0].get_text()
				team['name'] = teams_info[1].get_text()
				player_history.append(team)

		return player_history

	def get_player_achivements(self,soup):
		achievements = []
		rows = soup.find_all('tr')
		rows = [row for row in rows if len(row)>6]
		if len(rows) == 0:
			return achievements
		indexes = rows[0]
		index_values = ['Date', 'Placement', 'Event', 'Char', 'Result', 'Opponent (Char)', 'Prize']
		for row in rows:
			achievement={}
			cells = row.find_all('td')
			for i in range(0,len(cells)):
				try:
					key = index_values[i]
					value = cells[i].get_text().rstrip()
					if key == "Date":
						value = cells[i].find(text=True)
					elif key == "Placement":
						value = re.sub('[A-Za-z]','',cells[i].find('font').get_text())
					elif key == 'Event':
						value = cells[i].find('a').get_text()
					elif key == 'Char':
						value = cells[i].find('img')
						if value == None:
							value = ''
						else:
							value = value['alt']
					elif key == "Results":
						value = cells[i].get_text()
				except (AttributeError,IndexError):
					pass	
				else:
					value = unicodedata.normalize("NFKD",value.rstrip())		
					achievement[key] = value
			achievements.append(achievement)

		return achievements	

	def process_playerName(self,playerName):
		if playerName in self.__player_exceptions:
			playerName = playerName+"_(player)"
		if not playerName[0].isdigit():
			playerName = list(playerName)
			playerName[0] = playerName[0].upper()
			playerName = "".join(playerName)	
		playerName = quote(playerName)

		return playerName		
				