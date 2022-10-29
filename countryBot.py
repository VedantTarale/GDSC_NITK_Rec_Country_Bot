import requests  # library to handle HTTP requests made to the API

# telegram bot labrary
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(
    token='5433609138:AAGFmV9kis1O3HNqkZe9htilJYX5nRSHYEA', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome To CountryBot!")


def hello(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Great to see you!")


def info(update, context):
    user_params = " ".join(context.args)
    if user_params != " ":
        response = requests.get(
            'https://restcountries.com/v3.1/name/'+user_params)
        if (response.status_code == 200):
            data = response.json()[0]
            currency_data = list(data['currencies'].values())
            languages = ','.join(list(data['languages'].values()))
            reply_text = "Official Name: "+str(data['name']['official'])+"\n"
            reply_text += "Capital: "+str(data['capital'][0])+"\n"
            reply_text += "Languages Spoken: "+languages+"\n"
            reply_text += "Currency: " + \
                str(currency_data[0]['name']) + \
                "("+str(currency_data[0]['symbol'])+")\n"
            reply_text += "Area: "+str(data['area'])+" km^2\n"
            reply_text += "Population: "+str(data['population'])+"\n"
            reply_text += "Continent the country is situated in: " + \
                str(data['continents'][0])+"\n"
            reply_text += "Flag: "+str(data['flags']['svg'])+"\n"
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=reply_text)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Something went wrong!!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter the country name (example: /info belgium)")


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, this command doesn't exist.")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.start_polling()
