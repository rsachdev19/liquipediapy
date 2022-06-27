from urllib.request import quote
import re
import itertools
import unicodedata

class smash_team():


	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'

	def process_teamName(self,teamName):
		teamName = teamName.replace(" ","_")
		teamName = quote(teamName)

		return teamName

	def get_team_infobox(self,soup):
		team = {}
		try:
			image_url = soup.find('div', class_='img-responsive').find('img').get('src')	
			team['image'] = self.__image_base_url+image_url
		except AttributeError:
			team['image'] = ''			
		info_boxes = soup.find_all('div', class_='infobox-cell-2')
		for i in range(0,len(info_boxes),2):
			attribute = info_boxes[i].get_text().replace(':','')
			if attribute == "Sponsor" or attribute == "Location":
				value_list = []
				values = info_boxes[i+1].find_all('a')
				for value in values:
					text = value.get_text()
					if len(text) > 0:
						value_list.append(text)
				team[attribute.lower()] = value_list
			elif attribute == "Total Earnings":
				team['earnings'] = int(info_boxes[i+1].get_text().replace('$','').replace(',',''))		
			else:
				team[attribute.lower()] = unicodedata.normalize("NFKD",info_boxes[i+1].get_text().strip())


		return team

	def get_team_links(self,soup):
		team_links = {}
		try:		
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return team_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[-2].replace('https://','')
			team_links[site_name] = link.get('href')

		return team_links

	def get_team_roster(self,soup):
		roster_cards = soup.find_all('table',class_='wikitable')
		# print(roster_cards)
		#TODO: Get players from other games
		team_rosters = roster_cards[:-1]
		players = []
		for team_roster in team_rosters:
			rows = team_roster.find_all('tr')
			indexes = rows[1]
			index_values = []
			for cell in indexes.find_all('th'):
				index_values.append(unicodedata.normalize("NFKD",cell.get_text().rstrip()))	
			rows = rows[2:]
			for row in rows:
				player={}
				cells = row.find_all('td')
				for i in range(0,len(cells)):
					key = index_values[i]
					value = cells[i].get_text().strip()
					if key == 'Player':
						value = cells[i].find_all('a')
						value = value[-1].get('title')
					elif key == 'Join Date':
						value = unicodedata.normalize("NFKD",cells[i].get_text())
					elif key == 'Main':
						value = []
						imgs = cells[i].find_all('img')
						for img in imgs:
							if img == None:
								break
							else:
								value.append(img['alt'])
					if type(value) is list:
						for v in value:
							v = unicodedata.normalize("NFKD",v.rstrip())
					else:
						value = unicodedata.normalize("NFKD",value.rstrip())	
					if len(key) > 0:
						player[key] = value
				players.append(player)	
		return players