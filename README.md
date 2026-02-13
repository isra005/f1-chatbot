# 🏎️ F1 Chatbot

An AI-powered Formula 1 chatbot built with PyTorch that provides real-time F1 race information, driver statistics, and championship standings.

## 📋 Features

- **Intent Classification**: Neural network-based intent recognition with 24 F1-specific intents
- **Named Entity Recognition (NER)**: Hybrid approach combining custom dictionaries with spaCy for extracting drivers, teams, circuits, and years
- **Real-time F1 Data**: Integration with Ergast F1 API for live race results, standings, and schedules
- **Entity-Aware Responses**: Context-aware responses based on extracted entities (e.g., "2020 standings" vs "current standings")

## 🛠️ Technologies

- **PyTorch**: Neural network training and inference
- **NLTK**: Text preprocessing and tokenization
- **spaCy**: Named entity recognition
- **Ergast API**: F1 data source
- **Python 3.10+**

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/f1-chatbot.git
cd f1-chatbot
```

### 2. Create virtual environment (recommended)
```bash
# Using conda
conda create -n f1bot python=3.10
conda activate f1bot

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

## 🚀 Usage

### Train the Model (First Time Only)
```bash
python train.py
```

This will:
- Process intents from `intents.json`
- Train a neural network (200 epochs)
- Save the model to `model.pth`

### Run the Chatbot
```bash
python chatbot.py
```

Then start asking questions!

## 💬 Example Queries
```
You: When is the next race?
Bot: 📅 Next Race: Monaco Grand Prix
     📍 Circuit: Circuit de Monaco, Monaco
     🗓️ Date: 2025-05-25

You: Tell me about Max Verstappen
Bot: 👤 Max Verstappen
     🏁 Code: VER
     🔢 Number: 33
     🌍 Nationality: Dutch

You: Show me 2020 driver standings
Bot: 🏆 2020 Driver Standings (Top 10):
     1. Lewis Hamilton - 347 pts (11 wins)
        Team: Mercedes
     2. Valtteri Bottas - 223 pts (2 wins)
        Team: Mercedes
     ...

You: Who won round 5?
Bot: 🏆 Miami Grand Prix Winner
     👤 Max Verstappen
     🏎️ Team: Red Bull Racing
```

## 📊 Architecture

### Model Architecture
```
Input (Bag-of-Words) 
    ↓
FC Layer 1 (128 neurons) + ReLU + Dropout(0.5)
    ↓
FC Layer 2 (64 neurons) + ReLU + Dropout(0.5)
    ↓
Output Layer (24 intents)
```

### Data Flow
```
User Input
    ↓
Text Cleaning (lowercase, lemmatization)
    ↓
Intent Prediction (Neural Network)
    ↓
Entity Extraction (Hybrid: Dictionary + spaCy)
    ↓
API Call (if needed)
    ↓
Response Generation
```

## 📁 Project Structure
```
f1-chatbot/
├── train.py              # Model training script
├── chatbot.py            # Interactive chatbot interface
├── utils.py              # Shared utilities (model, dictionaries, text cleaning)
├── api_functions.py      # Ergast API integration
├── advanced_ner.py       # spaCy NER functions
├── intents.json          # Training data (24 intents, 150+ patterns)
├── model.pth             # Saved PyTorch model
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## 🎯 Supported Intents

- **Greetings**: greeting, goodbye, thanks
- **Race Information**: next_race, last_race, race_winner, race_schedule, race_time
- **Standings**: driver_standings, constructor_standings
- **Driver/Team Info**: driver_info, constructor_info
- **Technical F1**: drs, safety_car, pit_stop, tyre_info, points_system
- **General**: help, weather, f1_fact, fallback

## 🧪 Testing

Run the test suite:
```bash
python test_chatbot.py
```

## 🔧 Customization

### Adding New Intents
1. Edit `intents.json`:
```json
{
  "tag": "new_intent",
  "patterns": [
    "example pattern 1",
    "example pattern 2"
  ],
  "responses": [
    "Response template"
  ]
}
```

2. Retrain the model:
```bash
python train.py
```

### Adding New Entities
Edit dictionaries in `utils.py`:
```python
F1_DRIVERS["new driver"] = "New Driver Name"
```

## 📈 Model Performance

- **Accuracy**: ~92% on validation set
- **Training Time**: ~30 seconds (200 epochs, CPU)
- **Inference Speed**: <50ms per query
- **Dataset Size**: 150+ training patterns across 24 intents

## 🌐 API Information

This project uses the [Ergast F1 API](http://ergast.com/mrd/) which provides:
- Historical F1 data from 1950 to present
- Real-time race results and standings
- Driver and constructor information
- **No API key required** ✅

## 🐛 Known Limitations

- Race round numbers must be specified (race name → round mapping not implemented)
- Limited to drivers in the predefined dictionary for detailed info
- API rate limits (4 requests/second, 200/hour)

## 🚀 Future Improvements

- [ ] Add race name → round number mapping
- [ ] Implement conversation history/context
- [ ] Add support for qualifying results
- [ ] Deploy as web interface (Flask/Streamlit)
- [ ] Add multi-turn conversations

## 📝 License

MIT License - feel free to use this project for learning!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [Ergast F1 API](http://ergast.com/mrd/) for F1 data
- [spaCy](https://spacy.io/) for NER capabilities
- PyTorch community for ML framework

---

⭐ Star this repo if you found it helpful!