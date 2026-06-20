"""
Murder Mystery Game - A Console-Based Detective Adventure
Solve the mystery by interrogating suspects and finding the murderer!
Powered by Gemini AI for dynamic content generation!
"""

import random
import json
import os

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")

# ===== GEMINI AI SETUP =====

def setup_gemini():
    """Setup Gemini API with hardcoded API key"""
    if not GEMINI_AVAILABLE:
        print("Gemini AI not available. Using default game data.")
        return False
    
    # Hardcoded API key - Replace with your actual API key from https://aistudio.google.com/app/apikey
    api_key = "AQ.Ab8RN6LlKm_tRSxVRh0n5ejNUpjsNwWzQzpgyYw2w8EDSmLG2A"
    
    try:
        genai.configure(api_key=api_key)
        print("✓ Gemini AI connected successfully!")
        return True
    except Exception as e:
        print(f"✗ Error connecting to Gemini: {e}")
        print("Using default game data instead.")
        return False


def generate_victim():
    """Generate a random victim using Gemini AI"""
    if not GEMINI_AVAILABLE:
        return {"name": "Robert Harrison", "age": 55, "title": "Wealthy businessman"}
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """Generate a single murder mystery victim as JSON.
        Return ONLY valid JSON with these fields: name, age, title
        Example: {"name": "John Smith", "age": 45, "title": "CEO"}
        Make the victim a professional or wealthy person aged 45-65."""
        
        response = model.generate_content(prompt)
        # Extract JSON from response
        text = response.text.strip()
        # Remove markdown code blocks if present
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        victim = json.loads(text)
        return victim
    except Exception as e:
        print(f"Error generating victim: {e}")
        return {"name": "Robert Harrison", "age": 55, "title": "Wealthy businessman"}


def generate_suspects_and_alibis():
    """Generate 3 unique suspects with alibis, clues, and contradictions using Gemini AI"""
    if not GEMINI_AVAILABLE:
        return get_default_suspects()
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """Generate 3 murder mystery suspects as a JSON array. Each suspect needs:
        - name: unique first and last name
        - alias: their relationship (e.g., "Chef", "Partner", "Assistant")
        - motive: reason they might want the victim dead
        - alibi: what they claim they were doing during the crime
        - clue: suspicious evidence found about them
        - nervous: boolean (true if nervous, false if calm)
        - contradictions: array of 2 strings showing conflicts between their alibi and crime scene clues
        
        Return ONLY valid JSON array. Make contradictions realistic and specific.
        Example format: [{"name": "...", "alias": "...", "motive": "...", "alibi": "...", "clue": "...", "nervous": true, "contradictions": ["...", "..."]}]"""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Remove markdown code blocks if present
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        suspects = json.loads(text)
        return suspects
    except Exception as e:
        print(f"Error generating suspects: {e}")
        return get_default_suspects()


def generate_crime_scene_clues():
    """Generate realistic crime scene clues using Gemini AI"""
    if not GEMINI_AVAILABLE:
        return get_default_clues()
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """Generate 7 murder mystery crime scene clues as a JSON array of strings.
        Each clue should be specific, realistic, and potentially contradict one of the suspect's alibis.
        Return ONLY a valid JSON array of 7 strings.
        Example: ["Wet muddy footprints near the window", "A torn piece of fabric caught on the latch"]"""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Remove markdown code blocks if present
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        clues = json.loads(text)
        return clues[:7]  # Ensure exactly 7 clues
    except Exception as e:
        print(f"Error generating clues: {e}")
        return get_default_clues()


def get_default_suspects():
    """Default suspects if Gemini fails"""
    return [
        {
            "name": "Sarah Johnson",
            "alias": "Chef",
            "motive": "Financial troubles at her restaurant",
            "alibi": "I was cooking in the kitchen all evening",
            "clue": "Found a threatening letter in her pocket",
            "nervous": True,
            "contradictions": [
                "Wet muddy footprints were found - but you claim to be cooking indoors",
                "Strong perfume smell detected - you say you were cooking"
            ]
        },
        {
            "name": "James Mitchell",
            "alias": "Business Partner",
            "motive": "Disputed inheritance claim",
            "alibi": "I was out taking a walk by the river",
            "clue": "Seen wearing muddy shoes and wet clothes",
            "nervous": False,
            "contradictions": [
                "Torn red fabric at window - but your alibi is by the river",
                "Pearl earring found - men typically don't wear earrings"
            ]
        },
        {
            "name": "Emma Davis",
            "alias": "Assistant",
            "motive": "Unfair treatment and unpaid overtime",
            "alibi": "I was at home watching TV with my cat",
            "clue": "Scratches on her hands, smells like the victim's perfume",
            "nervous": True,
            "contradictions": [
                "Lipstick stain on wine glass - your alibi says you were at home",
                "Wet muddy footprints - your home is across town"
            ]
        }
    ]


def get_default_clues():
    """Default clues if Gemini fails"""
    return [
        "Wet muddy footprints near the window",
        "A torn piece of red fabric caught on the window latch",
        "An empty wine glass with lipstick stain on the victim's desk",
        "A handwritten note that says 'We need to talk about the money'",
        "A pearl earring found under the desk",
        "Strong perfume smell detected in the office",
        "Security footage shows someone arriving at 7:30 PM"
    ]


# ===== GAME DATA =====
# These will be populated dynamically
suspects = []
crime_scene_clues = []
victim = None

# Game variables
murderer = None
victim = None  # Randomly selected victim
crime_scene = ""  # Will be generated based on victim
detective_score = 0  # Track detective score
found_contradictions = {}  # Dictionary to track found contradictions
interrogations = {}  # Dictionary to store interrogation counts per suspect
collected_clues = []  # List to store clues discovered by the player
game_over = False
correctly_accused = False


# ===== GAME FUNCTIONS =====

def start_game():
    """Initialize the game and select a random murderer and victim"""
    global murderer, victim, crime_scene, collected_clues, detective_score, found_contradictions, suspects, crime_scene_clues
    
    print("\n" + "="*60)
    print("Generating new mystery...".center(60))
    print("="*60)
    
    # Generate game content using Gemini AI
    print("Generating victim...")
    victim = generate_victim()
    
    print("Generating suspects...")
    suspects = generate_suspects_and_alibis()
    
    print("Gathering crime scene clues...")
    crime_scene_clues = generate_crime_scene_clues()
    
    # Randomly select murderer
    murderer = random.choice(suspects)
    
    # Generate crime scene description
    crime_scene = f"""
LOCATION: Executive Office, Downtown Financial Building
TIME: 8:00 PM - Crime discovered
VICTIM: {victim["name"]}, {victim["age"]}-year-old {victim["title"]}

CRIME SCENE DETAILS:
- Body found slumped over mahogany desk
- Office door was locked from inside
- Window latch broken
- Desk lamp knocked over
- Papers scattered on the floor
"""
    
    # Reset game variables
    detective_score = 0
    found_contradictions = {}
    interrogations.clear()
    
    print("\n" + "="*60)
    print("WELCOME TO MURDER MYSTERY GAME".center(60))
    print("="*60)
    print(crime_scene)
    print("="*60)
    print("\nYou are the detective assigned to solve this mystery.")
    print("\nThere are 3 suspects. Your job is to:")
    print("  1. Examine the crime scene for clues")
    print("  2. Interrogate each suspect and find contradictions")
    print("  3. Review collected clues and suspect information")
    print("  4. Accuse the person you believe is the murderer")
    print("\nFinding contradictions will increase your detective score!")
    print("\nLet's begin your investigation...\n")
    
    # Automatically collect all crime scene clues at the start
    collected_clues = crime_scene_clues.copy()


def display_menu():
    """Show the main menu options"""
    print("\n" + "-"*60)
    print("INVESTIGATION MENU".center(60))
    print(f"Detective Score: {detective_score}".center(60))
    print("-"*60)
    print("1. View crime scene")
    print("2. View collected clues")
    print("3. Interrogate a suspect")
    print("4. Review suspect information")
    print("5. View contradictions found")
    print("6. Make an accusation")
    print("7. Quit game")
    print("-"*60)
    choice = input("Enter your choice (1-7): ").strip()
    return choice


def display_suspects():
    """Show list of all suspects"""
    print("\nSuspects in custody:")
    for i, suspect in enumerate(suspects, 1):
        times_interrogated = interrogations.get(suspect["name"], 0)
        print(f"{i}. {suspect['name']} ({suspect['alias']}) - Interrogated {times_interrogated} times")


def view_crime_scene():
    """Display the crime scene details"""
    print("\n" + "="*60)
    print("CRIME SCENE INVESTIGATION".center(60))
    print("="*60)
    print(crime_scene)
    print("="*60)


def view_clues():
    """Display all collected clues"""
    print("\n" + "="*60)
    print("COLLECTED CLUES".center(60))
    print("="*60)
    
    if len(collected_clues) == 0:
        print("\nNo clues collected yet. Visit the crime scene!")
    else:
        print(f"\nYou have collected {len(collected_clues)} clues:")
        print("-"*60)
        for i, clue in enumerate(collected_clues, 1):
            print(f"{i}. {clue}")
        print("-"*60)
    print("="*60)


def interrogate_suspect():
    """Let player interrogate a suspect"""
    global interrogations, detective_score, found_contradictions
    
    print("\nWho would you like to interrogate?")
    display_suspects()
    
    try:
        choice = int(input("Enter suspect number (1-3): "))
        if 1 <= choice <= 3:
            suspect = suspects[choice - 1]
            
            # Update interrogation count
            if suspect["name"] not in interrogations:
                interrogations[suspect["name"]] = 0
            interrogations[suspect["name"]] += 1
            
            # Display interrogation
            print("\n" + "="*60)
            print(f"INTERROGATING: {suspect['name']} ({suspect['alias']})".center(60))
            print("="*60)
            print(f"\nYou: Tell me your alibi!")
            print(f"{suspect['name']}: {suspect['alibi']}")
            print(f"\nYou: Hmm, interesting... [You take notes]")
            print(f"\nInvestigative Finding: {suspect['clue']}")
            print(f"\nSuspect Behavior: ", end="")
            if suspect["nervous"]:
                print("Very nervous, fidgeting with hands")
            else:
                print("Calm and composed")
            
            # Check for contradictions
            print("\n" + "-"*60)
            print("CONTRADICTION ANALYSIS:")
            print("-"*60)
            if suspect["name"] not in found_contradictions:
                found_contradictions[suspect["name"]] = []
            
            contradictions_found = 0
            for contradiction in suspect["contradictions"]:
                if contradiction not in found_contradictions[suspect["name"]]:
                    print(f"⚠️  {contradiction}")
                    found_contradictions[suspect["name"]].append(contradiction)
                    detective_score += 10
                    contradictions_found += 1
            
            if contradictions_found > 0:
                print(f"\n✓ Found {contradictions_found} contradiction(s)! +{contradictions_found * 10} points")
            else:
                print("No new contradictions found in this interrogation.")
            
            print("\n" + "="*60)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def review_suspects():
    """Let player review information about all suspects"""
    print("\n" + "="*60)
    print("SUSPECT DOSSIER".center(60))
    print("="*60)
    
    for i, suspect in enumerate(suspects, 1):
        times_interrogated = interrogations.get(suspect["name"], 0)
        print(f"\n{i}. {suspect['name']} ({suspect['alias']})")
        print(f"   Motive: {suspect['motive']}")
        print(f"   Alibi: {suspect['alibi']}")
        print(f"   Evidence: {suspect['clue']}")
        print(f"   Times Interrogated: {times_interrogated}")


def view_contradictions():
    """Display all contradictions found during interrogations"""
    print("\n" + "="*60)
    print("CONTRADICTIONS FOUND".center(60))
    print("="*60)
    
    if not found_contradictions or all(len(v) == 0 for v in found_contradictions.values()):
        print("\nNo contradictions found yet. Interrogate suspects to find them!")
    else:
        total_found = sum(len(v) for v in found_contradictions.values())
        print(f"\nTotal contradictions found: {total_found}")
        print("-"*60)
        for suspect_name, contradictions_list in found_contradictions.items():
            if contradictions_list:
                print(f"\n{suspect_name}:")
                for contradiction in contradictions_list:
                    print(f"  • {contradiction}")
    print("\n" + "="*60)


def make_accusation():
    """Let player accuse a suspect of being the murderer"""
    global game_over, correctly_accused, detective_score
    
    print("\nWho do you believe is the murderer?")
    display_suspects()
    
    try:
        choice = int(input("Enter suspect number (1-3): "))
        if 1 <= choice <= 3:
            accused = suspects[choice - 1]
            
            print("\n" + "="*60)
            print("FINAL ACCUSATION".center(60))
            print("="*60)
            print(f"\nYou accuse: {accused['name']}")
            
            if accused == murderer:
                correctly_accused = True
                game_over = True
                detective_score += 50  # Bonus for correct accusation
                print("\n🎉 CORRECT! 🎉")
                print(f"\n{accused['name']} was indeed the murderer!")
                print(f"Motive: {accused['motive']}")
                print("\nYou have successfully solved the case!")
                print("The criminal has been arrested and justice is served.")
                print(f"\n+50 bonus points for correct accusation!")
            else:
                game_over = True
                print("\n❌ WRONG! ❌")
                print(f"\n{accused['name']} is innocent!")
                print(f"The murderer was actually: {murderer['name']}")
                print(f"Motive: {murderer['motive']}")
                print("\nBetter luck next time, detective...")
            print("="*60)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def run_game():
    """Main game loop"""
    global game_over
    
    # Setup Gemini AI
    setup_gemini()
    
    start_game()
    
    while not game_over:
        choice = display_menu()
        
        if choice == "1":
            view_crime_scene()
        elif choice == "2":
            view_clues()
        elif choice == "3":
            interrogate_suspect()
        elif choice == "4":
            review_suspects()
        elif choice == "5":
            view_contradictions()
        elif choice == "6":
            make_accusation()
        elif choice == "7":
            print("\nYou've quit the game. Case unsolved!")
            game_over = True
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")
    
    print("\n" + "="*60)
    print("GAME OVER - Thanks for playing!".center(60))
    print("="*60)
    print(f"\nFINAL DETECTIVE SCORE: {detective_score} points".center(60))
    if detective_score >= 100:
        print("\n⭐ EXCELLENT DETECTIVE WORK! ⭐".center(60))
    elif detective_score >= 50:
        print("\n✓ Good investigation! ".center(60))
    else:
        print("\nKeep practicing your detective skills!".center(60))
    print("\n" + "="*60 + "\n")


# ===== MAIN PROGRAM =====

if __name__ == "__main__":
    run_game()