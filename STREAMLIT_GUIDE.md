# 🔍 Murder Mystery Detective - Streamlit Edition

## Overview

This is a web-based version of the Murder Mystery game, built with **Streamlit** and powered by **Google Gemini AI**. Solve the mystery by interrogating suspects, analyzing clues, and finding contradictions!

## Features

✨ **Detective-Themed UI**
- Dark, professional interface with gold accents
- Immersive investigation experience
- Responsive design for desktop and tablet

📊 **Investigation Dashboard**
- Real-time detective score tracking
- Suspect status monitoring
- Contradiction counter
- Victim information display

🕵️ **Suspect Cards**
- Complete suspect profiles
- Alibi statements
- Evidence tracking
- Behavioral analysis (nervous/calm)
- Contradiction history

📋 **Clue Management**
- Visual crime scene display
- Collected evidence list
- Clue-based investigation tools

## Installation

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install streamlit google-generativeai
```

## Running the Application

Run the Streamlit app with:

```bash
streamlit run streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

## How to Play

### 1. **Start Investigation**
- Click "START INVESTIGATION" to begin a new case
- The game generates a unique victim, suspects, and clues using AI

### 2. **Explore Crime Scene**
- Review the crime scene details and initial findings
- Understand the victim and location

### 3. **Analyze Suspects**
- View all suspects' profiles, motives, and alibis
- Track interrogations and contradictions
- Monitor suspect behavior (nervous vs. calm)

### 4. **Interrogate Suspects**
- Select a suspect and click "Begin Interrogation"
- Listen to their alibi and analyze evidence
- **Find contradictions** to increase your score!
- Contradictions: +10 points each

### 5. **Collect Clues**
- Review all crime scene evidence
- Use clues to identify contradictions in suspect statements

### 6. **Make Your Accusation**
- Based on your investigation, accuse the suspect you believe is guilty
- Correct accusation: +50 bonus points
- See the results immediately!

## Scoring System

- **Finding Contradictions:** +10 points each
- **Correct Accusation:** +50 bonus points
- **Total Score:** Sum of all points earned

### Score Ratings:
- **100+ points:** ⭐ Excellent Detective Work!
- **50-99 points:** ✓ Good Investigation
- **Below 50 points:** Keep practicing your detective skills!

## Game Interface

### Tabs:
1. **🔎 Crime Scene** - Initial crime scene investigation
2. **👥 Suspects** - View all suspect profiles
3. **💬 Interrogate** - Question suspects
4. **🔗 Clues** - Review collected evidence
5. **🎯 Accuse** - Make your final accusation

### Sidebar:
- **Investigation Dashboard** - Score and stats
- **Victim Information** - Victim details
- **Suspects Status** - Real-time suspect tracking
- **New Game Button** - Start a fresh investigation

## Game Features

🤖 **AI-Powered Mysteries**
- Unique victim generation for each game
- Dynamic suspect creation with realistic motives
- Authentic crime scene clues
- Procedurally generated evidence

🎮 **Interactive Investigation**
- Multiple suspect interrogations
- Contradiction detection system
- Evidence tracking
- Score progression

📈 **Statistics**
- Detective score tracking
- Interrogation counters
- Contradiction counts
- Case completion metrics

## API Key Setup

The app uses the Google Generative AI (Gemini) API. The API key is already configured in `streamlit_app.py`:

```python
api_key = "AQ.Ab8RN6LlKm_tRSxVRh0n5ejNUpjsNwWzQzpgyYw2w8EDSmLG2A"
```

To use your own API key:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Replace the key in `streamlit_app.py`

## Troubleshooting

### "Model not found" Error
- Ensure you're using a valid Gemini model name
- Currently supported: `gemini-2.5-flash`
- Check your API key is active

### Application won't load
- Ensure Streamlit is installed: `pip install streamlit`
- Try running: `streamlit run streamlit_app.py --logger.level=debug`

### API Errors
- Verify your internet connection
- Check API key validity
- Ensure API quota hasn't been exceeded

## Keyboard Shortcuts

- **R** - Refresh page
- **C** - Clear cache (Streamlit menu)

## Game Tips

💡 **Investigation Strategies:**
1. Start by examining the crime scene carefully
2. Interrogate each suspect multiple times if possible
3. Look for contradictions between alibis and evidence
4. Compare suspect statements with clues
5. Trust the contradictions you find!

🔎 **Finding Contradictions:**
- Pay attention to timing in alibis
- Match physical evidence with movements
- Look for logical inconsistencies
- Consider witness behavior patterns

## Files

- `streamlit_app.py` - Main Streamlit application
- `main.py` - Original console-based game
- `requirements.txt` - Python dependencies
- `STREAMLIT_GUIDE.md` - This file

## System Requirements

- Python 3.8+
- Modern web browser
- Internet connection (for AI API)
- 100MB+ free disk space

## Performance

- Initial load: 2-5 seconds
- Game generation: 5-10 seconds
- Interrogations: Instant
- API calls: May take 5-10 seconds depending on internet speed

## Future Enhancements

- 🎨 Additional themes (noir, modern, classic)
- 📱 Mobile optimization
- 🎵 Background music and sound effects
- 💾 Save/Load game state
- 🏆 Leaderboard system
- 🎯 Difficulty levels
- 🌍 Multiplayer investigation

## Support

For issues or suggestions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure API key is valid
4. Clear browser cache and restart

---

**Happy Investigating, Detective! 🔍**

Enjoy solving mysteries with your AI-powered investigation tool!
