"""
Train the F1 chatbot model.
Run this script when you modify intents.json.
"""

import json
import random
import numpy as np
import torch
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from utils import clean_text, Neural_Network

with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# prepare data for training 
words = []
classes = []
documents = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordlist = clean_text(pattern)
        words.extend(wordlist)  # vocabulary
        documents.append((wordlist, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(set(words))  # Remove duplicates and sort
classes = sorted(set(classes))  # Sort classes

training = []
output = [0] * len(classes)

for document in documents:
    pattern_words = document[0]
    bag = []
    for word in words:
        if word in pattern_words:
            bag.append(1)
        else:
            bag.append(0)
    row_output = list(output)    
    row_output[classes.index(document[1])] = 1   
    training.append((bag, row_output))        

random.shuffle(training)
training = np.array(training, dtype=object)
X = np.array(list(training[:, 0]), dtype=np.float32)
y = np.array([np.argmax(row) for row in training[:, 1]], dtype=np.int64)  

#convert pytorch to tensors
X_tensor = torch.from_numpy(X)
y_tensor = torch.from_numpy(y)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Intialize model 
input_size = len(words)
output_size = len(classes)

model = Neural_Network(input_size, output_size)

#Training setup
loss_fn = torch.nn.CrossEntropyLoss()  
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)  

#training

print("Training started...")
for epoch in range(200):
    model.train()  
    total_loss = 0
    for batch_x, batch_y in loader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = loss_fn(outputs, batch_y)
        loss.backward()
        optimizer.step()  
        total_loss += loss.item()
    
    if (epoch + 1) % 20 == 0: 
        print(f"Epoch [{epoch+1}/200], Loss: {total_loss/len(loader):.4f}")

print("Training completed!")

#save model
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "words": words,
    "classes": classes
}


torch.save(data, "model.pth")
print("Model saved as 'model.pth'")
