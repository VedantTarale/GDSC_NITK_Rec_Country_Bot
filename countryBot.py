# library to handle HTTP requests made to the API
from tabnanny import check
import requests

# telegram bot labrary
from telegram import *
from telegram.ext import *

#defining a global variable to store the data so that it can be accessed by all functions.
global data
check = 0

# creating the bot object with the unique token generated from BotFather
updater = Updater(
    token='5433609138:AAGFmV9kis1O3HNqkZe9htilJYX5nRSHYEA', use_context=True)
dispatcher = updater.dispatcher


# start command  /start
def start(update, context):
    global check
    check = 0
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome To CountryBot!\nHere's a list of commands: \n/help\n/hello\n/info")


# hello command /hello
def hello(update, context):
    global check
    check = 0
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Great to see you!")


# info command  /info <country_name>
def info(update, context):
    global data
    global check
    # user_params stores the <country_name> sent with /info <country_name> command
    user_params = " ".join(context.args)

    # if no country parameter is entered
    if user_params != "":

        # requesting a response from the API
        response = requests.get(
            'https://restcountries.com/v3.1/name/'+user_params)

        # checking for a successful response
        if (response.status_code == 200):
            buttons = [[KeyboardButton("All Details")], [KeyboardButton("Official Name")], [KeyboardButton("Capital")], [KeyboardButton("Languages Spoken")], [KeyboardButton("Currency")], [KeyboardButton("Area")], [KeyboardButton("Population")], [KeyboardButton("Continent")], [KeyboardButton("Flag")], [KeyboardButton("Map")]]

            # storing the recieved json response
            data = response.json()[0]
            check = 1
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Please select an option",reply_markup=ReplyKeyboardMarkup(buttons))
        # If response was not generated successfully
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Something went wrong!!")

    # if country_name parameter is not entered
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter the country name (example: /info belgium)")


# Function to handle text-inputs for selectively displaying the deatils of the country
def options_handler(update, context):
    global data
    global check
    if check:
        if "All Details" in update.message.text:
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
            reply_text += "Continent: " + \
                str(data['continents'][0])+"\n"
            reply_text += "Flag: "+str(data['flags']['png'])+"\n"
            reply_text += "Map: "+str(data['maps']['googleMaps'])
            # Sending the data to the user
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=reply_text)
        elif "Official Name" in update.message.text:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="Official Name: "+str(data['name']['official'])+"\n")
        elif "Capital" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Capital: "+str(data['capital'][0])+"\n")
        elif "Languages Spoken" in update.message.text:
            languages = ','.join(list(data['languages'].values()))
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Languages Spoken: "+languages+"\n")
        elif "Currency" in update.message.text:
            currency_data = list(data['currencies'].values())
            context.bot.send_message(chat_id=update.effective_chat.id, text="Currency: " +
                                    str(currency_data[0]['name']) +
                                    "("+str(currency_data[0]['symbol'])+")\n")
        elif "Area" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Area: "+str(data['area'])+" km^2\n")
        elif "Population" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Population: "+str(data['population'])+"\n")
        elif "Continent" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Continent: " + str(data['continents'][0])+"\n")
        elif "Flag" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Flag: "+str(data['flags']['png'])+"\n")
        elif "Map" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Map: "+str(data['maps']['googleMaps']))
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Sorry, entered text is invalid.")
    else:
        context.bot.send_message(
                chat_id=update.effective_chat.id, text="Please use /info <country_name>")

#Help function to display list of available commands    /help
def help(update, context):
    global check
    check = 0
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here are the currently defined commands: \n/start\n/hello\n/info")


# function to tackle unknown commands
def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, entered text is invalid.")


# creating handlers for commands and text:
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, options_handler))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
