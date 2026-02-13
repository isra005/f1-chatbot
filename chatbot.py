"""
F1 Chatbot - Interactive Command Line Interface
Loads pre-trained model and provides real-time F1 information.
"""
import re
import json
import random
import torch
import torch.nn.functional as F
from utils import clean_text, Neural_Network, F1_DRIVERS, F1_TEAMS, F1_RACES, DRIVER_API_IDS
from api_functions import (
    get_last_race_results, get_next_race, get_driver_standings,
    get_constructor_standings, get_driver_info, get_race_schedule, get_race_winner
)
from advanced_ner import extract_entities_spacy

###LOAD MODEL ###
print("🏎️  F1 CHATBOT")
print("="*60)
print("\n📦 Loading model...")

try : 
    data = torch.load("model.pth", weights_only=True)
    words = data['words']
    classes = data['classes']
    input_size = data['input_size']
    output_size = data['output_size']
    
    model = Neural_Network(input_size, output_size)
    model.load_state_dict(data['model_state'])
    model.eval()
    
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Error: model.pth not found!")
    print("Please run 'python train.py' first to train the model.")
    exit()

# Load intents for responses
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

#### ENTITY EXTRACTION ###

def extract_race(text):
    text_lower = text.lower()
    sorted_races = sorted(F1_RACES.keys(), key=len, reverse=True)
    for search_term in sorted_races:
        if search_term in text_lower:
            return F1_RACES[search_term]
    return None

# combine race dictionary + spacy
def extract_race_hybrid(text):
    race = extract_race(text)
    if race : return race

    spacy_entities = extract_entities_spacy(text)
    if spacy_entities['location'] :
        return spacy_entities['location'][0]
    return None

def extract_round(text):
    match = re.search(r'(?:round|race)\s*(\d+)', text.lower())
    if match:
        return match.group(1)
    return None

#  Extract driver function :Extracts driver name from text.

def extract_driver(text):
    
    text_lower = text.lower()
    sorted_drivers = sorted(F1_DRIVERS.keys(), key=len, reverse=True)
    
    for search_driver in sorted_drivers:
        if search_driver in text_lower:
            return F1_DRIVERS[search_driver]
    
    return None

# compine the dictionary + spacy
def extract_driver_hybrid(text):
    """
    Hybrid approach:
    1. Try your dictionary first (fast, F1-specific)
    2. If not found, use spaCy (slower, but catches more)
    """

    driver = extract_driver(text)
    if driver : return driver
    spacy_entities = extract_entities_spacy(text)
    if spacy_entities['person'] : return spacy_entities['person'][0]
    return None

#  Extract Team Function :Extracts team name from text.
def extract_team(text):
    text_lower = text.lower()
    sorted_teams = sorted(F1_TEAMS.keys(), key=len, reverse=True)
    
    for search_team in sorted_teams:
        if search_team in text_lower:
            return F1_TEAMS[search_team]
    
    return None

# combine extract team + spacy
def extract_team_hybrid(text):
    team = extract_team(text)
    if team : return team

    spacy_entities = extract_entities_spacy(text)
    if spacy_entities['org'] : 
        return spacy_entities['org'][0]
    return None
# Extract year function : Extracts year from text (2000-2025)

def extract_year(text):
    
    # Find 4-digit years
    year_match = re.search(r'\b(20[0-2][0-9])\b', text)
    if year_match:
        return year_match.group(1)
    
    if "last year" in text.lower():
        return "2024"
    if "this year" in text.lower() or "current" in text.lower():
        return "2025"
    
    return None


### PEDICTION ###

def predict(sentence):
    """Predict the intent of a given sentence"""
    # Clean and prepare input
    sentence_words = clean_text(sentence)
    bag = [1 if word in sentence_words else 0 for word in words]
   
    input_tensor = torch.FloatTensor(bag).unsqueeze(0)  # Add batch dimension
    
    # Get prediction
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = F.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    return classes[predicted_class], confidence

# prediction with entities 
def predict_with_entities(sentence):
    intent , confidence = predict(sentence)
    driver = extract_driver_hybrid(sentence)
    team = extract_team_hybrid(sentence)
    year = extract_year(sentence) 
    race = extract_race_hybrid(sentence)
    round = extract_round(sentence)
    return {
        "intent": intent,
        "confidence": confidence,
        "entities": {
            "driver": driver,
            "team": team,
            "year": year,
            "race" : race,
            "round": round
        }
       }  

###  Generate response function ###

def generate_response(user_input):
    """
    1.Predicts intent
    2.Extracts entities
    3.Calls appropriate API function
    4.Returns formatted response
    """
    result = predict_with_entities(user_input)
    intent = result['intent']
    confidence = result['confidence']
    entities = result['entities']
    
    # If confidence is too low, return fallback
    if confidence < 0.6:
        return "I'm not sure I understood. Can you rephrase?"
    
    # Handle each intent with API calls
    
    if intent == "greeting":
        return "Hello! How can I help you with Formula 1 today?"
    
    elif intent == "goodbye":
        return "Goodbye! Enjoy the race weekend."
    
    elif intent == "thanks":
        return "You're welcome!"
    
    elif intent == "next_race":
        race_data = get_next_race()
        if "error" in race_data:
            return "Sorry, I couldn't fetch the next race information."
        return f" Next Race: {race_data['race_name']}\n" \
               f" Circuit: {race_data['circuit']}, {race_data['country']}\n" \
               f" Date: {race_data['date']}\n" \
               f" Time: {race_data['time']}"
    
    elif intent == "last_race":
        race_data = get_last_race_results()
        if "error" in race_data:
            return "Sorry, I couldn't fetch the last race results."
        
        response = f" {race_data['race_name']} ({race_data['date']})\n"
        response += f" {race_data['circuit']}\n\n"
        response += " Podium:\n"
        for driver in race_data['top_3']:
            response += f"  {driver['position']}. {driver['driver']} ({driver['team']})\n"
        return response
    
    elif intent == "driver_standings":
        year = entities['year'] if entities['year'] else 'current'
        standings_data = get_driver_standings(year)
        if "error" in standings_data:
            return "Sorry, I couldn't fetch the driver standings."
        
        response = f" {standings_data['season']} Driver Standings (Top 10):\n\n"
        for driver in standings_data['standings']:
            response += f"{driver['position']}. {driver['driver']} - {driver['points']} pts ({driver['wins']} wins)  Team: {driver['team']}\n"
        return response
    
    elif intent == "constructor_standings":
        year = entities['year'] if entities['year'] else 'current'
        standings_data = get_constructor_standings(year)
        if "error" in standings_data:
            return "Sorry, I couldn't fetch the constructor standings."
        
        response = f" {standings_data['season']} Constructor Standings:\n\n"
        for team in standings_data['standings']:
            response += f"{team['position']}. {team['constructor']} - {team['points']} pts ({team['wins']} wins)\n"
        return response
    
    elif intent == "driver_info":
        driver_name = entities['driver']
        if not driver_name:
            return "Please specify which driver you'd like to know about."
        
        # Get API ID for driver
        api_id = DRIVER_API_IDS.get(driver_name)
        if not api_id:
            return f"Sorry, I don't have detailed info for {driver_name} yet."
        
        driver_data = get_driver_info(api_id)
        if "error" in driver_data:
            return f"Sorry, I couldn't find information about {driver_name}."
        
        return f" {driver_data['full_name']}\n" \
               f" Code: {driver_data['code']}\n" \
               f" Number: {driver_data['number']}\n" \
               f" Nationality: {driver_data['nationality']}\n" \
               f" Born: {driver_data['birth_day']}\n" \
               f" More info: {driver_data['url']}"
    
    elif intent == "race_schedule":
        year = entities['year'] if entities['year'] else 'current'
        schedule_data = get_race_schedule(year)
        if "error" in schedule_data:
            return "Sorry, I couldn't fetch the race schedule."
        
        response = f" {schedule_data['season']} F1 Calendar ({schedule_data['total_races']} races):\n\n"
        for race in schedule_data['races'][:5]:  # Show first 5
            response += f"Round {race['round']}: {race['race_name']} ({race['date']})\n"
            response += f"   {race['circuit']}, {race['country']}\n"
        response += f"\n... and {schedule_data['total_races'] - 5} more races!"
        return response
    
    elif intent =="race_winner":
        year = entities['year'] if entities['year'] else '2024'
        round_number = entities['round'] 
        if not round_number and entities['race'] :
            return f"Which round was {entities['race']}? Please specify the round number."
        if not round_number:
          return "Please specify which race"
        race_data = get_race_winner(year , round_number)
        if "error" in race_data: return "Sorry , couldn't find that race"
        return f" race name :{race_data['race_name']} \n"\
               f"winner : {race_data['winner']}\n"\
               f"Team: {race_data['team']}\n"\
               f"Date : {race_data['date']}"
    
    
    else:
        # Default response from intents.json
        for intent_data in intents['intents']:
            if intent_data['tag'] == intent:
                return random.choice(intent_data['responses'])
        
        return "I'm not sure how to help with that."


### MAIN CHATBOT ###

def chat():
    print("\n" + "="*60)
    print("Chat started! Type 'quit' or 'exit' to stop.")
    print("="*60 + "\n")

    while True :
        try : 
            user_input = input("USER : ").strip()
            if not user_input : continue
            if user_input.lower() in ['exit' , 'quit' , 'goodbye' , 'bye'] :
                print("Bot : Bye ! , see you later ")
                break
            response = generate_response(user_input)
            print(f"Bot: {response}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat()

