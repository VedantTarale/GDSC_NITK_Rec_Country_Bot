# library to handle HTTP requests made to the API
import requests

# telegram bot labrary
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# creating the bot object with the unique token generated from BotFather
updater = Updater(
    token='5433609138:AAGFmV9kis1O3HNqkZe9htilJYX5nRSHYEA', use_context=True)
dispatcher = updater.dispatcher


# start command  /start
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome To CountryBot!")


# hello command /hello
def hello(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Great to see you!")


# info command  /info <country_name>
def info(update, context):

    # user_params stores the <country_name> sent with /info <country_name> command
    user_params = " ".join(context.args)

    # if no country parameter is entered
    if user_params != "":

        # requesting a response from the API
        response = requests.get(
            'https://restcountries.com/v3.1/name/'+user_params)

        # checking for a successful response
        if (response.status_code == 200):

            # storing the recieved json response
            data = response.json()[0]
            currency_data = list(data['currencies'].values())
            languages = ','.join(list(data['languages'].values()))

            # Creating a string to store the formatted response
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

            # Sending the data to the user
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=reply_text)

        # If response was not generated successfully
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Something went wrong!!")

    # if country_name parameter is not entered
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter the country name (example: /info belgium)")


# function to tackle unknown commands
def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, this command doesn't exist.")


# creating handlers for commands:
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
