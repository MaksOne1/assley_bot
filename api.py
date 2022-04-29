import configparser
import codecs
import requests
import json

SETTINGS_FILE = 'settings.ini'

config = configparser.ConfigParser()
config.read_file(codecs.open(SETTINGS_FILE, "r", "utf8"))


class ReMangaAPI:
	def get_branch_ids(self, links):
		ids_list = []
		for link in links:
			dir = link.split('/')[-1].split('?subpath=')[0]
			api_link = config['ReManga']['API'] + config['ReManga']['TITLES_ENDPOINT'] + dir
			try:
				response = json.loads(requests.get(api_link).text)['content']
				branches = response['branches']
				branch_id = branches[0]['id']

				if len(branches) > 1:
					branch_id = 'To check'
				
				ids_list.append(branch_id)
			except:
				ids_list.append('Error')

		return ids_list

	def get_chapters_info(self, branch_ids):
		info_array = []
		for branch in branch_ids:
			try:
				api_link = config['ReManga']['API'] + config['ReManga']['CHAPTERS_ENDPOINT'] + str(branch)
				response = json.loads(requests.get(api_link).text)['content']

				last_paid_chapter = response[0]['chapter']
				last_free_chapter = None

				for chapter in response:
					if not chapter['is_paid']:
						last_free_chapter = chapter['chapter']
						break;

				info_array.append([last_paid_chapter, last_free_chapter])

			except: 
				info_array.append(['', ''])

		return info_array
