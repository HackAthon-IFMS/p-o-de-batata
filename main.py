import telepotpro
from multiprocessing import Process
import crawller
import contaPalavras

bot = telepotpro.Bot("YOUR_TOKEN")

def startMsg(chat_id):
	bot.sendMessage(chat_id, '🤖 Hello')

def errorMsg(chat_id, error_type):
	if error_type == 'invalid_command':
		bot.sendMessage(chat_id, '*Oops! Invalid command!')


def validInput(userInput, chat_id):
    userInput = userInput[6:].split()
    print(userInput)

    SITES_TEXTOS = crawller.pegar_texto_dos_sites_google(userInput)

    for site_texto in SITES_TEXTOS:
        Nome_site = site_texto['site']
        Texto_do_site = site_texto['texto']
        print(site_texto['site'], '\n', site_texto['texto'])

    #bot.sendMessage(chat_id, 'em ', len(SITES_TEXTOS) ,' foram encontradas ', contaPalavras.contar(site_texto['texto'], userInput), ' palavras referentes ao assunto, resultando em ', (100*contaPalavras.contar(site_texto['texto'], userInput))/len(SITES_TEXTOS), ' "%" de sites que mencionaram o assunto')


def recebendoMsg(msg):
	userInput = msg['text']
	chat_id = msg['chat']['id']
	chat_type = msg['chat']['type']

	if chat_type == 'group':
		if '@checkfakenews_bot' in userInput:
			userInput = userInput.replace('@checkfakenews_bot', '')

	if userInput.startswith('/start'):
		startMsg(chat_id)

	elif userInput.startswith('/check') and userInput!='':
		validInput(userInput, chat_id)

	else:
		errorMsg(chat_id, 'invalid_command')

def main(msg):
    recebendoMsg(msg)

bot.message_loop(main, run_forever=True)