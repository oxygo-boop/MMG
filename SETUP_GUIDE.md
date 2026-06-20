# Murder Mystery Game - Gemini AI Setup Guide

## Overview
This Murder Mystery game now uses **Google's Gemini AI** to dynamically generate:
- Unique victims with random names, ages, and titles
- Original suspects with realistic alibis and motives
- Crime scene clues specific to each mystery
- Contradictions between alibis and evidence

## Setup Instructions

### Step 1: Install Required Package
Run this command in your terminal:
```bash
pip install google-generativeai
```

### Step 2: Get a Free Gemini API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### Step 3: Run the Game
Run the game:
```bash
python main.py
```

When prompted, paste your API key. The game will connect to Gemini AI and start generating unique mysteries!

### Alternative: Set Environment Variable (Optional)
Instead of entering the API key each time, you can set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
python main.py
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
python main.py
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"
python main.py
```

### Step 4: Play!
- The game will automatically generate a new mystery each time
- Interrogate suspects to find contradictions
- Solve the case and earn detective points!

## Features
✅ AI-Generated Victims - Different person each game
✅ AI-Generated Suspects - Unique suspects with original alibis
✅ Dynamic Clues - Crime scene evidence changes every game
✅ AI-Generated Contradictions - Hidden conflicts between alibis and clues
✅ Score System - Earn points for finding contradictions
✅ Fallback Mode - Works with default data if API unavailable

## Troubleshooting

### "google-generativeai not found"
- Make sure you installed the package: `pip install google-generativeai`
- Verify installation: `pip list | grep google-generativeai`

### "Invalid API Key"
- Verify your API key at: https://makersuite.google.com/app/apikey
- Make sure there are no extra spaces or characters
- API keys are case-sensitive

### "Rate Limited"
- Gemini has free tier limits (60 requests per minute)
- Wait a few minutes and try again
- The game falls back to default data if rate-limited

### Game using default data instead of AI
- This is normal! The game is designed to work without Gemini
- Check that your API key is valid
- Check your internet connection
- Review error messages in the console

## Tips
- Each game generates completely new content
- Play multiple times for variety
- The detective score increases with difficulty of finding contradictions
- AI-generated contradictions can be very clever and realistic!

## Free Tier Limits
- **Requests per minute:** 60
- **Requests per day:** 1,500
- **Perfect for casual gaming!**

Enjoy your AI-powered murder mysteries! 🔍
