**Restaurant Recommender AI Chatbot**

**Part 1: Introduction**

**Project Background**

In today’s fast-paced lifestyle, deciding where to eat can often become overwhelming due to the vast number of options and the lack of personalized guidance. Whether it’s a casual dinner or a special outing, users often struggle to find restaurants that truly match their tastes and budgets. To solve this, we have developed Restaurant Recommender AI, a chatbot that blends the conversational power of large language models with rule-based filtering mechanisms to provide accurate, relevant, and tailored restaurant suggestions effortlessly.

**Problem Statement**

Given a dataset containing information about restaurants (Restaurant name, Country, City, Cuisine, Price Preference, Rating etc.), build a chatbot that parses the dataset and provides accurate restaurant recommendations based on user requirements.

**Dataset**

Data is gathered form Kaggle's make my trip dataset on restaurants from the follwing link: https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data

**Approach:**

1. Conversation and Information Gathering: The chatbot will utilize language models to understand and generate natural responses. Through a conversational flow, it will ask relevant questions to gather information about the user's requirements.
2. Information Extraction: Once the essential information is collected, rule-based functions come into play, extracting relevant restaurants that best matches the user's needs.
3. Personalized Recommendation: Leveraging this extracted information, the chatbot engages in further dialogue with the user, efficiently addressing their queries and aiding them in answering any question related to the package.

As shown in the image, the chatbot contains the following layers:

Intent Clarity Layer
Intent Confirmation Layer
Product Mapping Layer
Product Information Extraction Layer
Product Recommendation Layer
Major functions behind the Chatbot Let's now look at a brief overview of the major functions that form the chatbot.

** initialize_conversation(): This initializes the variable conversation with the system message.

** get_chat_model_completions(): This takes the ongoing conversation as the input and returns the response by the assistant

** moderation_check(): This checks if the user's or the assistant's message is inappropriate. If any of these is inappropriate, it ends the conversation.

** intent_confirmation_layer(): This function takes the assistant's response and evaluates if the chatbot has captured the user's profile clearly. Specifically, this checks if the following properties for the user has been captured or not. Country, City, Cuisine, Price Preference

** dictionary_present(): This function checks if the final understanding of user's profile is returned by the chatbot as a python dictionary or not. If there is a dictionary, it extracts the information as a Python dictionary.

** compare_restaurant_with_user(): This function compares the user's requirements with the different restaurant packages and come back with the top recommendations.

** initialize_conv_reco(): Initializes the recommendations conversation

**Part 3:** 
Implementation Implementing Intent Clarity & Intent Confirmation layers Let's start with the first part of the implementation - building the intent clarity and intent confirmation layers. 

As mentioned earlier, this layer helps in identifying the user requirements and passing it on to the product matching layer. Here are the functions that we would be using for building these layers:

initialize_conversation(): This initializes the variable conversation with the system message. used prompt engineering and chain of thought reasoning, the function will enable the chatbot to keep asking questions until the user requirements have been captured in a dictionary. It also includes Few Shot Prompting(sample conversation between the user and assistant) to align the model about user and assistant responses at each step.
intent_confirmation_layer(): This function takes the assistant's response and evaluates if the chatbot has captured the user's profile clearly. Specifically, this checks if the following properties for the user has been captured or not
Country
City
Cuisine
Price Preference

**Implementing dictionary present & moderation checks**

dictionary_present(): This function checks if the final understanding of user's profile is returned by the chatbot is a Python dictionary or not. This is important as it'll be used later on for finding the right restaurants using dictionary matching.
moderation_check(): This checks if the user's or the assistant's message is inappropriate. If any of these is inappropriate, one can add a break statement to end the conversation.
Implementing Product mapping and information extraction layer 
In this section, we take in the output of the previous layers, i.e. the user requirements, which is in the format of a Python dictionary, and extract the relevant restaurant recommendations based on that. Here are the functions that we will use to help us implement the information extraction and product matching layers

product_map_layer(): This function is responsible for extracting key features and criteria from restaurant dataset. Here's a breakdown of how it works:

extract_dictionary_from_string(): This function takes in the output of the previous layer and extracts the user requirements dictionary

compare_restaurant_with_user(): This function compares the user's profile with the different restaurants from the dataset and come back with the top recommendations. It will perform the following steps:

1. It will take the user requirements dictionary as input
2. Filter the restaurants based on the users input
3. Return the matching restaurants as a JSON-formatted string.
   
**Product Recommendation Layer**

Finally, we come to the product recommendation layer. It takes the output from the compare_restaurant_with_user function in the previous layer and provides the recommendations to the user. 
It has the following steps.

1. Initialize the conversation for recommendation.
2. Generate the recommendations and display in a presentable format.
3. Ask questions basis the recommendations.

**Dialogue management System**

Bringing everything together, we create a diagloue_mgmt_system() function that contains the logic of how the different layers would interact with each other. This will be the function that we'll call to initiate the chatbot User Interface Finally all the functions above are encompassed together into a UI using the Flask framework. This helps in seamless interaction between the bot and the user.

**Chatbot Functionalities , Limitations & Challenges**

1. It can cater to offensive/prohibited content generated from both user and assistant through moderation checks
2. Data has a limitation that city or country might not be present in dataset
3. One limitation of the chatbot is that it looks for the exact value entered by the user in the database and returns if there are matching rows in the data. It is unable to recommend any alternatives to keep the user engaged.
4. At the end, after all the details are fetched, user needs to enter exit to end the conversation
5. Chatbot can handle a scenario where the user provides the requirements that do not match with the dataset and replies appropriately.
6. One particular challenge faced was when I tried to increase the dataset size, the OpenAI timeout error was quite frequent. 
7. Sometimes the bot still times out when trying to fetch the results, therefore please try again should you face any such errors.



