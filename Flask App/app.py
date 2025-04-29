import pandas as pd
from flask import Flask, redirect, url_for, render_template, request
from functions import initialize_conversation, initialize_conv_reco, product_map_layer, get_chat_model_completions, moderation_check, intent_confirmation_layer, dictionary_present, compare_restaurant_with_user, check_exit, get_best_match, get_available_countries, get_available_cities

import openai
import ast
import re
import json

client = openai.OpenAI(api_key="<Open AI Secret Key>")

app = Flask(__name__)
app.secret_key = "your_secret_key"

zomato = pd.read_csv('data/zomato.csv', encoding='latin1')
country = pd.read_excel('data/Country-Code.xlsx')

zomato = zomato.merge(country, how='left', on='Country Code')
zomato = zomato.dropna(subset=['Restaurant Name', 'Cuisines'])
zomato = zomato[['Restaurant Name', 'Country', 'City', 'Cuisines', 'Average Cost for two',
                 'Currency', 'Has Table booking', 'Has Online delivery', 'Price range',
                 'Aggregate rating', 'Rating text']]

conversation_bot = []
conversation = []
recommended_restaurant = None

user_profile = {
    "country": None,
    "city": None,
    "cuisine": None,
    "price_preference": None
}
conversation_stage = 0
conversation_mode = None

@app.route("/")
def default_func():
    global conversation_bot, conversation, recommended_restaurant
    return render_template("index.html", name_xyz=conversation_bot)

@app.route("/end_conv", methods=['POST', 'GET'])
def end_conv():
    global conversation_bot, conversation, recommended_restaurant, user_profile, conversation_stage, conversation_mode
    conversation_bot = []
    conversation = []
    user_profile = {
        "country": None,
        "city": None,
        "cuisine": None,
        "price_preference": None
    }
    conversation_stage = 0
    conversation_mode = None
    recommended_restaurant = None
    return redirect(url_for('default_func'))

@app.route("/invite", methods=["POST", "GET"])
def invite():
    global conversation_bot, conversation, recommended_restaurant
    global conversation_stage, user_profile, conversation_mode

    if request.method == "POST":
        user_input = request.form.get("user_input").strip()

        if moderation_check(user_input):
            conversation_bot.append({'bot': "Inappropriate content detected. Ending chat."})
            return redirect(url_for('default_func'))

        if check_exit(user_input):
            conversation_bot.append({'bot': "Goodbye! Have a great day! 👋"})
            return redirect(url_for('default_func'))

        if conversation_stage == 0:
            conversation_bot.append({'bot': "👋 Hello! Welcome to the Restaurant Recommender!"})
            conversation_bot.append({'bot': "I will ask you a few quick questions to find the best restaurant for you."})
            conversation_bot.append({'bot': "Which country are you in?"})
            conversation_stage = 1
            return redirect(url_for('default_func'))

        if conversation_stage == 1:
            available_countries = get_available_countries(zomato)
            best_country = get_best_match(user_input, available_countries)
            if best_country:
                user_profile['country'] = best_country
                conversation_bot.append({'user': best_country})
                conversation_bot.append({'bot': "Which city are you located in?"})
                conversation_stage = 2
            else:
                conversation_bot.append({'bot': f"Sorry, couldn't recognize country. Example countries: {', '.join(available_countries[:5])}..."})

        elif conversation_stage == 2:
            available_cities = get_available_cities(zomato, user_profile['country'])
            best_city = get_best_match(user_input, available_cities)
            if best_city:
                user_profile['city'] = best_city
                conversation_bot.append({'user': best_city})
                conversation_bot.append({'bot': "What type of cuisine would you prefer? (e.g., Indian, Chinese, Italian)"})
                conversation_stage = 3
            else:
                conversation_bot.append({'bot': f"Sorry, couldn't recognize city. Example cities: {', '.join(available_cities[:5])}..."})

        elif conversation_stage == 3:
            # ✅ Validation for Cuisine Stage
            if user_input.lower() in ["cheap", "medium", "expensive"]:
                conversation_bot.append({'bot': "Oops! That looks like a budget. Please tell me a cuisine (e.g., Indian, Chinese, Italian)."})
            else:
                user_profile['cuisine'] = user_input.title()
                conversation_bot.append({'user': user_input})
                conversation_bot.append({'bot': "What is your budget preference? (cheap / medium / expensive)"})
                conversation_stage = 4

        elif conversation_stage == 4:
            # ✅ Validation for Budget Stage
            if user_input.lower() not in ["cheap", "medium", "expensive"]:
                conversation_bot.append({'bot': "Please select your budget as: cheap / medium / expensive."})
            else:
                user_profile['price_preference'] = user_input.lower()
                conversation_bot.append({'user': user_input})
                conversation_bot.append({'bot': "✅ Thank you for providing all the details! Finding best restaurants for you..."})

                try:
                    restaurant_data = product_map_layer(zomato)
                    reco = compare_restaurant_with_user(user_profile, restaurant_data)
                except Exception as e:
                    print("🔥 Error inside recommendation logic:", str(e))
                    raise e

                if reco.empty:
                    conversation_bot.append({'bot': "Sorry, no matching restaurants found based on your preferences."})
                else:
                    conversation_bot.append({'bot': "✅ Here are the top recommended restaurants for you:"})
                    for index, row in reco.iterrows():
                        rest_info = f"- {row['Restaurant Name']} ({row['Cuisines']}) – Rating: {row['Aggregate rating']} – {row['Rating text']}"
                        conversation_bot.append({'bot': rest_info})

                conversation_bot.append({'bot': "Would you like to change country, city, cuisine, start a new search, or exit?"})
                conversation_stage = 5

        elif conversation_stage == 5:
            user_response = user_input.lower()

            if "country" in user_response:
                conversation_bot.append({'bot': "Which country are you in?"})
                conversation_stage = 1

            elif "city" in user_response:
                conversation_bot.append({'bot': "Which city are you located in?"})
                conversation_stage = 2

            elif "cuisine" in user_response:
                conversation_bot.append({'bot': "What type of cuisine would you prefer? (e.g., Indian, Chinese, Italian)"})
                conversation_stage = 3

            elif "new" in user_response or "start" in user_response:
                conversation_bot.append({'bot': "Starting a new search!"})
                user_profile = {
                    "country": None,
                    "city": None,
                    "cuisine": None,
                    "price_preference": None
                }
                conversation_stage = 1
                conversation_bot.append({'bot': "Which country are you in?"})

            elif "exit" in user_response:
                conversation_bot.append({'bot': "Thank you! Have a great day! 👋"})
                conversation_stage = 0

            else:
                conversation_bot.append({'bot': "Sorry, I didn't understand. Please type: country / city / cuisine / new search / exit."})

    return render_template("index.html", name_xyz=conversation_bot)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
