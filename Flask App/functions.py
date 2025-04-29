# ✅ Corrected functions.py
import difflib
import openai
import ast
import pandas as pd

# 🔹 Function to initialize conversation with system instructions
def initialize_conversation():
    system_message = {
        "role": "system",
        "content": '''
        You are an intelligent restaurant recommendation assistant.
        Strictly follow these rules:
        - Always ask users about their country, city, preferred cuisine, and budget.
        - When asking about budget, explicitly provide: "cheap", "medium", "expensive".
        - Do not use random or fancy greetings.
        - Be simple, clear, and summarize inputs as a Python dictionary.
        '''
    }
    global conversation
    conversation = [system_message]

# 🔹 Function to get assistant response from OpenAI model
def get_chat_model_completions(conversation):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response.choices[0].message.content

# 🔹 Function to detect inappropriate content
def moderation_check(user_message):
    flagged_words = ['badword1', 'badword2']
    for word in flagged_words:
        if word in user_message.lower():
            return True
    return False

# 🔹 Function to confirm if all required user preferences are captured
def intent_confirmation_layer(response_text):
    required_keys = ["country", "city", "cuisine", "price_preference"]
    try:
        user_profile = eval(response_text)
        if all(key in user_profile for key in required_keys):
            return True
    except:
        return False
    return False

# 🔹 Function to extract dictionary if present
def dictionary_present(response_text):
    try:
        user_profile = eval(response_text)
        if isinstance(user_profile, dict):
            return True, user_profile
    except:
        return False, {}

# 🔹 Function to extract dictionary directly without checks
def extract_dictionary_from_string(response_text):
    try:
        return eval(response_text)
    except:
        return {}

# 🔹 Function to return a copy of the restaurant dataset
def product_map_layer(zomato):
    return zomato.copy()

# 🔹 Function to match restaurants based on user preferences
def compare_restaurant_with_user(user_profile, restaurant_data):
    country = user_profile['country']
    city = user_profile['city']
    cuisine = user_profile['cuisine'].lower()
    price_pref = user_profile['price_preference'].lower()

    price_range_map = {
        "cheap": 1,
        "medium": 2,
        "expensive": 3
    }
    price_level = price_range_map.get(price_pref, 2)

    df = restaurant_data.copy()

    # First filter by country and city
    filtered = df[(df['Country'].str.lower() == country.lower()) &
                  (df['City'].str.lower() == city.lower())]

    # Then filter where cuisine matches partially
    filtered = filtered[filtered['Cuisines'].str.lower().str.contains(cuisine)]

    if filtered.empty:
        return pd.DataFrame()

    filtered['price_diff'] = abs(filtered['Price range'] - price_level)
    filtered = filtered.sort_values(by=['price_diff', 'Aggregate rating'], ascending=[True, False])
    top_restaurants = filtered.head(5)
    return top_restaurants[['Restaurant Name', 'Cuisines', 'Average Cost for two', 'Aggregate rating', 'Rating text']]

# 🔹 Function to initialize conversation for recommendation phase
def initialize_conv_reco():
    global conversation
    conversation.append({"role": "system", "content": "Now you have user's preferences. Recommend top restaurants."})

# 🔹 Function to check if user intends to exit
def check_exit(user_input):
    exit_phrases = ['thank you', 'bye', 'goodbye', 'exit', 'see you']
    return any(phrase in user_input.lower() for phrase in exit_phrases)

# 🔹 Typo Correction Function
def get_best_match(user_input, valid_list):
    matches = difflib.get_close_matches(user_input.lower(), [v.lower() for v in valid_list], n=1, cutoff=0.6)
    if matches:
        for item in valid_list:
            if item.lower() == matches[0]:
                return item
    return None

# 🔹 Get available countries
def get_available_countries(zomato):
    return sorted(zomato['Country'].dropna().unique())

# 🔹 Get available cities for a country
def get_available_cities(zomato, selected_country):
    return sorted(zomato[zomato['Country'].str.lower() == selected_country.lower()]['City'].dropna().unique())

