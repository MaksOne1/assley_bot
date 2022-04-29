import codecs
import configparser
import telebot
from api import ReMangaAPI
from chapter_parser import ChapterParser

SETTINGS_FILE = 'settings.ini'
TOKEN = '5342669633:AAEsGHGaGn2fE3lbLk-8_UvllpS-kOglsTs'

config = configparser.ConfigParser()
config.read_file(codecs.open(SETTINGS_FILE, "r", "utf8"))

parser = ChapterParser()
api = ReMangaAPI()

bot = telebot.TeleBot(TOKEN) 


@bot.message_handler(commands=['set_ids'])
def set_ids(message):
	bot.reply_to(message, 'Set ids started.')
	links = parser.get_columns(config['Worksheet']['SHEET_NAME'], 3)
	ids = api.get_branch_ids(links)
	parser.write_columns(config['Worksheet']['SHEET_NAME'], 'D', ids)

	bot.reply_to(message, 'Set ids finished')

@bot.message_handler(commands=['check_titles'])
def check_titles(message):
	bot.reply_to(message, 'Check titles started.')
	ids = parser.get_columns(config['Worksheet']['SHEET_NAME'], 4)
	info = api.get_chapters_info(ids)

	free_chapters = []
	paid_chapters = []

	for element in info:
		free_chapters.append(element[0])
		paid_chapters.append(element[1])

	parser.write_columns(config['Worksheet']['OUTPUT_SHEET_NAME'],"C", paid_chapters)
	parser.write_columns(config['Worksheet']['OUTPUT_SHEET_NAME'],"D", free_chapters)

	bot.reply_to(message, 'Check titles finished.')


bot.infinity_polling()




