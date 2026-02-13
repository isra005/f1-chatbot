import re
import nltk
from nltk.stem import WordNetLemmatizer
import torch
import torch.nn as nn
import torch.nn.functional as F

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


lemmatizer = WordNetLemmatizer()

#  F1 driver dictionary
F1_DRIVERS = {
    
    "verstappen": "Max Verstappen",
    "max verstappen": "Max Verstappen",
    "max": "Max Verstappen",
    
    "hamilton": "Lewis Hamilton",
    "lewis hamilton": "Lewis Hamilton",
    "lewis": "Lewis Hamilton",
    
    "leclerc": "Charles Leclerc",
    "charles leclerc": "Charles Leclerc",
    "charles": "Charles Leclerc",
    
    "norris": "Lando Norris",
    "lando norris": "Lando Norris",
    "lando": "Lando Norris",
    
    "sainz": "Carlos Sainz",
    "carlos sainz": "Carlos Sainz",
    "carlos": "Carlos Sainz",
    
    "perez": "Sergio Perez",
    "sergio perez": "Sergio Perez",
    "sergio": "Sergio Perez",
    "checo": "Sergio Perez",
    
    "alonso": "Fernando Alonso",
    "fernando alonso": "Fernando Alonso",
    "fernando": "Fernando Alonso",
    
    "russell": "George Russell",
    "george russell": "George Russell",
    "george": "George Russell",
    
    "piastri": "Oscar Piastri",
    "oscar piastri": "Oscar Piastri",
    "oscar": "Oscar Piastri",
    
    "schumacher": "Michael Schumacher",
    "michael schumacher": "Michael Schumacher",
    "michael": "Michael Schumacher",
    
    "vettel": "Sebastian Vettel",
    "sebastian vettel": "Sebastian Vettel",
    "sebastian": "Sebastian Vettel",
}

#  API ID mapping (for Ergast API)
DRIVER_API_IDS = {
    "Max Verstappen": "max_verstappen",
    "Lewis Hamilton": "hamilton",
    "Charles Leclerc": "leclerc",
    "Lando Norris": "norris",
    "Carlos Sainz": "sainz",
    "Sergio Perez": "perez",
    "Fernando Alonso": "alonso",
    "George Russell": "russell",
    "Oscar Piastri": "piastri",
}

#  F1 Teams Dictionary
F1_TEAMS = {
    "red bull": "Red Bull Racing",
    "redbull": "Red Bull Racing",
    "rb": "Red Bull Racing",
    
    "ferrari": "Scuderia Ferrari",
    
    "mercedes": "Mercedes-AMG Petronas",
    "merc": "Mercedes-AMG Petronas",
    
    "mclaren": "McLaren F1 Team",
    
    "aston martin": "Aston Martin F1 Team",
    "aston": "Aston Martin F1 Team",
    
    "alpine": "BWT Alpine F1 Team",
    
    "williams": "Williams Racing",
    
    "alfa romeo": "Alfa Romeo F1 Team Stake",
    "alfa": "Alfa Romeo F1 Team Stake",
}
 #  Extract race names
F1_RACES = {
    "monaco": "Monaco",
    "silverstone": "Silverstone",
    "spa": "Spa",
    "monza": "Monza",
    "suzuka": "Suzuka",
    "austin": "Austin",
    "singapore": "Singapore",
    "bahrain": "Bahrain",
    "jeddah": "Jeddah",
    "melbourne": "Melbourne",
    "imola": "Imola",
    "miami": "Miami",
    "barcelona": "Barcelona",
    "montreal": "Montreal",
    "austria": "Austria",
    "hungary": "Hungary",
    "zandvoort": "Zandvoort",
    "baku": "Baku",
    "qatar": "Qatar",
    "mexico": "Mexico",
    "brazil": "Brazil",
    "las vegas": "Las Vegas",
    "abu dhabi": "Abu Dhabi"
}



# clean text and lemmatize 
def clean_text(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-z\s]', "", sentence)
    words = nltk.word_tokenize(sentence)
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Neural network ( input , 2 hidden layers , output layer )
class Neural_Network(nn.Module):
    def __init__(self, input_size, output_size):
        super(Neural_Network, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.fc1(x))   
        x = self.dropout(x)
        x = F.relu(self.fc2(x))   
        x = self.dropout(x)
        x = self.fc3(x)
        return x  
