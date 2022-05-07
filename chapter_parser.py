import gspread
import configparser
import codecs
import time

SETTINGS_FILE = 'settings.ini'

config = configparser.ConfigParser()
config.read_file(codecs.open(SETTINGS_FILE, "r", "utf8"))

class ChapterParser:
	def __init__(self):
		gc = gspread.service_account(filename=config['Worksheet']['API_FILE'])
		self.wb = gc.open(config['Worksheet']['WORKSHEET_NAME'])

	def get_columns(self, sheet_name, column):
		ws = self.wb.worksheet(sheet_name)
		columns = ws.col_values(column)[1:]
		return columns

	def write_columns(self, sheet_name, column_name, content):
		ws = self.wb.worksheet(sheet_name)

		for (i, item) in enumerate(content):
			ws.update_acell(column_name + str(i + 2), item)
			time.sleep(1)