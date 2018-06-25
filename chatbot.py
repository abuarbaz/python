from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('Bot')
bot.set_trainer(ListTrainer)

for files in os.listdir('D:/scripts/chatterBot/chatterbot_corpus/data/englishh/'):
        data = open('D:/scripts/chatterBot/chatterbot_corpus/data/englishh/' + files , 'r').readlines()
        bot.train(data)

while True:
        message = raw_input('You:')
        if message.strip() != 'Bye':
            
                reply = bot.get_response(message)
                print ('ChatBot :',reply)
        if message.strip() == 'Bye':
              print('ChatBot: Bye')
              break