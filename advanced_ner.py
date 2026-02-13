import re
import spacy
from spacy.matcher import PhraseMatcher


# Load spaCy model
nlp = spacy.load("en_core_web_sm")
def extract_entities_spacy(text):
    #Uses spaCy to extract entities from text.
    #Returns:dict with entities: {person, date, org, location}
    entities ={
        'person':[],
        'date' : [],
        'location':[],
        'number' : [],
        'org'  : []
    }

    doc = nlp(text)
    for ent in doc.ents :
        if ent.label == "PERSON" :
            entities['person'].append(ent.text)
        if ent.label =="DATE" :
            entities['data'].append(ent.text)
        if ent.label=="ORG" :
            entities['org'].append(ent.text)
        elif ent.label_ == "GPE":  
            entities["location"].append(ent.text)
        elif ent.label_ == "CARDINAL": 
            entities["number"].append(ent.text)
    
    return entities


