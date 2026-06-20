"""
Murder Mystery Game - Streamlit Detective Application
A sophisticated detective adventure with AI-powered mystery generation!
"""

import streamlit as st
import random
import json
import os
import google.generativeai as genai

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="🔍 Murder Mystery Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS FOR DETECTIVE THEME =====
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #1a1a2e;
        color: #eee;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f3460;
        border-right: 3px solid #d4af37;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #d4af37;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Cards and containers */
    .suspect-card {
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border: 2px solid #d4af37;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(212, 175, 55, 0.3);
    }
    
    .clue-box {
        background-color: #0f3460;
        border-left: 4px solid #d4af37;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .crime-scene {
        background-color: #1a1a2e;
        border: 3px double #d4af37;
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #d4af37;
        color: #1a1a2e;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        background-color: #f0c674;
    }
    
    /* Sidebar info boxes */
    .sidebar-title {
        color: #d4af37;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ===== GEMINI AI SETUP =====
def setup_gemini():
    """Setup Gemini API with secure key management"""
    # Try to get API key from environment variables first, then Streamlit secrets
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        try:
            api_key = st.secrets.get("gemini_api_key")
        except:
            pass
    
    if not api_key:
        st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable or add it to Streamlit secrets.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error connecting to Gemini: {e}")
        return False


def generate_victim():
    """Generate a random victim using Gemini AI"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """Generate a single murder mystery victim as JSON.
        Return ONLY valid JSON with these fields: name, age, title
        Example: {"name": "John Smith", "age": 45, "title": "CEO"}
        Make the victim a professional or wealthy person aged 45-65."""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        return json.loads(text)
    except Exception as e:
        return {"name": "Robert Harrison", "age": 55, "title": "Wealthy businessman"}


def generate_suspects_and_alibis():
    """Generate 3 unique suspects using Gemini AI"""
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
        
        Return ONLY valid JSON array."""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        return json.loads(text)
    except Exception as e:
        return get_default_suspects()


def generate_crime_scene_clues():
    """Generate realistic crime scene clues using Gemini AI"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """Generate 7 murder mystery crime scene clues as a JSON array of strings.
        Each clue should be specific, realistic, and potentially contradict one of the suspect's alibis.
        Return ONLY a valid JSON array of 7 strings."""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        return json.loads(text)[:7]
    except Exception as e:
        return get_default_clues()


def get_default_suspects():
    """Default suspects"""
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
    """Default clues"""
    return [
        "Wet muddy footprints near the window",
        "A torn piece of red fabric caught on the window latch",
        "An empty wine glass with lipstick stain on the victim's desk",
        "A handwritten note that says 'We need to talk about the money'",
        "A pearl earring found under the desk",
        "Strong perfume smell detected in the office",
        "Security footage shows someone arriving at 7:30 PM"
    ]


# ===== SESSION STATE INITIALIZATION =====
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.victim = None
    st.session_state.suspects = []
    st.session_state.clues = []
    st.session_state.murderer = None
    st.session_state.detective_score = 0
    st.session_state.found_contradictions = {}
    st.session_state.interrogations = {}
    st.session_state.collected_clues = []
    st.session_state.game_over = False
    st.session_state.correctly_accused = False
    st.session_state.current_page = "home"


def start_new_game():
    """Initialize a new game"""
    st.session_state.victim = generate_victim()
    st.session_state.suspects = generate_suspects_and_alibis()
    st.session_state.clues = generate_crime_scene_clues()
    st.session_state.murderer = random.choice(st.session_state.suspects)
    st.session_state.detective_score = 0
    st.session_state.found_contradictions = {}
    st.session_state.interrogations = {}
    st.session_state.collected_clues = st.session_state.clues.copy()
    st.session_state.game_over = False
    st.session_state.correctly_accused = False
    st.session_state.game_started = True
    st.session_state.current_page = "investigation"


# ===== MAIN APP =====
def main():
    # Setup Gemini
    setup_gemini()
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>🔍 MURDER MYSTERY DETECTIVE 🔍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #d4af37;'>Powered by Gemini AI</h3>", unsafe_allow_html=True)
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("### 🎯 INVESTIGATION DASHBOARD")
        
        # Detective Score
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Detective Score", st.session_state.detective_score)
        with col2:
            st.metric("Contradictions", sum(len(v) for v in st.session_state.found_contradictions.values()))
        
        # Game Status
        st.divider()
        if st.session_state.game_started:
            st.markdown("<div class='sidebar-title'>📋 VICTIM</div>", unsafe_allow_html=True)
            if st.session_state.victim:
                st.write(f"**Name:** {st.session_state.victim['name']}")
                st.write(f"**Age:** {st.session_state.victim['age']}")
                st.write(f"**Title:** {st.session_state.victim['title']}")
            
            st.divider()
            st.markdown("<div class='sidebar-title'>👥 SUSPECTS STATUS</div>", unsafe_allow_html=True)
            for suspect in st.session_state.suspects:
                interrogations = st.session_state.interrogations.get(suspect["name"], 0)
                contradict_count = len(st.session_state.found_contradictions.get(suspect["name"], []))
                st.write(f"**{suspect['name']}** ({suspect['alias']})")
                st.caption(f"Interrogations: {interrogations} | Contradictions: {contradict_count}")
        
        st.divider()
        if st.button("🔄 New Game", use_container_width=True):
            start_new_game()
            st.rerun()


    # ===== MAIN CONTENT =====
    if not st.session_state.game_started:
        # HOME PAGE
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            # Welcome, Detective! 🕵️
            
            A high-profile professional has been found dead in their office. 
            The case has been assigned to you. Three suspects are in custody, 
            and the evidence is waiting to be analyzed.
            
            ### Your Mission:
            - 🔎 Examine the crime scene
            - 🗣️ Interrogate suspects
            - 📝 Collect and analyze clues
            - ⚖️ Find contradictions in their statements
            - 🎯 Solve the mystery!
            
            ### Scoring System:
            - Finding contradictions: +10 points each
            - Correct accusation: +50 points
            
            Good luck, Detective!
            """)
            
            if st.button("🎮 START INVESTIGATION", use_container_width=True, key="start_game"):
                start_new_game()
                st.rerun()
    
    else:
        # INVESTIGATION PAGE
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["🔎 Crime Scene", "📋 Suspects", "💬 Interrogate", "🔗 Clues", "🎯 Accuse"]
        )
        
        # ===== TAB 1: CRIME SCENE =====
        with tab1:
            st.markdown("<div class='crime-scene'>", unsafe_allow_html=True)
            st.markdown(f"""
## ⚠️ CRIME SCENE INVESTIGATION ⚠️

**LOCATION:** Executive Office, Downtown Financial Building  
**TIME:** 8:00 PM - Crime discovered  
**VICTIM:** {st.session_state.victim['name']}, {st.session_state.victim['age']}-year-old {st.session_state.victim['title']}

### CRIME SCENE DETAILS:
- Body found slumped over mahogany desk
- Office door was locked from inside
- Window latch broken
- Desk lamp knocked over
- Papers scattered on the floor

### INITIAL OBSERVATIONS:
The victim appears to have been poisoned and then positioned at the desk. 
The window suggests a potential entry/exit point. No signs of forced entry 
on the main door lock. The killer knew the victim.
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== TAB 2: SUSPECTS =====
        with tab2:
            st.markdown("## 👥 Suspect Profiles")
            
            for i, suspect in enumerate(st.session_state.suspects):
                with st.container():
                    st.markdown(f"<div class='suspect-card'>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### {i+1}. {suspect['name']}")
                        st.markdown(f"**Position:** {suspect['alias']}")
                    
                    with col2:
                        if st.session_state.interrogations.get(suspect["name"], 0) > 0:
                            st.info(f"⭐ Interrogated {st.session_state.interrogations[suspect['name']]} times")
                    
                    st.markdown(f"**Motive:** {suspect['motive']}")
                    st.markdown(f"**Alibi:** _{suspect['alibi']}_")
                    st.markdown(f"**Evidence:** {suspect['clue']}")
                    
                    behavior = "😰 Nervous, fidgeting" if suspect['nervous'] else "😐 Calm and composed"
                    st.markdown(f"**Behavior:** {behavior}")
                    
                    if suspect["name"] in st.session_state.found_contradictions:
                        contradictions = st.session_state.found_contradictions[suspect["name"]]
                        if contradictions:
                            st.markdown("**⚠️ Contradictions Found:**")
                            for contra in contradictions:
                                st.markdown(f"- {contra}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== TAB 3: INTERROGATE =====
        with tab3:
            st.markdown("## 💬 Suspect Interrogation Room")
            
            suspect_names = [s["name"] for s in st.session_state.suspects]
            selected_suspect_name = st.selectbox(
                "Select a suspect to interrogate:",
                suspect_names,
                key="interrogation_select"
            )
            
            if st.button("🗣️ Begin Interrogation", use_container_width=True):
                suspect = next(s for s in st.session_state.suspects if s["name"] == selected_suspect_name)
                
                # Update interrogation count
                if suspect["name"] not in st.session_state.interrogations:
                    st.session_state.interrogations[suspect["name"]] = 0
                st.session_state.interrogations[suspect["name"]] += 1
                
                # Display interrogation
                st.markdown(f"""
                <div class='suspect-card'>
                <h3>INTERROGATING: {suspect['name']} ({suspect['alias']})</h3>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
**Detective:** Tell me your alibi!

**{suspect['name']}:** "{suspect['alibi']}"

**Detective:** Hmm, interesting... [You take notes]

**Evidence Found:** {suspect['clue']}

**Suspect Behavior:** 
""")
                
                if suspect["nervous"]:
                    st.warning("😰 Very nervous, fidgeting with hands")
                else:
                    st.info("😐 Calm and composed")
                
                # Check for contradictions
                st.divider()
                st.markdown("**⚠️ CONTRADICTION ANALYSIS:**")
                
                if suspect["name"] not in st.session_state.found_contradictions:
                    st.session_state.found_contradictions[suspect["name"]] = []
                
                contradictions_found = 0
                for contradiction in suspect["contradictions"]:
                    if contradiction not in st.session_state.found_contradictions[suspect["name"]]:
                        st.error(f"🚨 {contradiction}")
                        st.session_state.found_contradictions[suspect["name"]].append(contradiction)
                        st.session_state.detective_score += 10
                        contradictions_found += 1
                    else:
                        st.caption(f"✓ (Already found)")
                
                if contradictions_found > 0:
                    st.success(f"✅ Found {contradictions_found} new contradiction(s)! +{contradictions_found * 10} points")
                else:
                    st.info("No new contradictions found in this interrogation.")
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.rerun()
        
        # ===== TAB 4: CLUES =====
        with tab4:
            st.markdown("## 📋 Collected Evidence")
            
            if len(st.session_state.collected_clues) == 0:
                st.info("No clues collected yet. Visit the crime scene!")
            else:
                st.markdown(f"**Total clues collected: {len(st.session_state.collected_clues)}**")
                
                for i, clue in enumerate(st.session_state.collected_clues, 1):
                    st.markdown(f"<div class='clue-box'>", unsafe_allow_html=True)
                    st.markdown(f"**Clue {i}:** {clue}")
                    st.markdown(f"</div>", unsafe_allow_html=True)
        
        # ===== TAB 5: ACCUSE =====
        with tab5:
            st.markdown("## 🎯 Final Accusation")
            st.markdown("Based on your investigation, who do you believe is the murderer?")
            
            suspect_names = [s["name"] for s in st.session_state.suspects]
            accused_name = st.selectbox(
                "Select the suspect you wish to accuse:",
                suspect_names,
                key="accusation_select"
            )
            
            if st.button("⚖️ MAKE ACCUSATION", use_container_width=True, type="primary"):
                accused = next(s for s in st.session_state.suspects if s["name"] == accused_name)
                
                st.markdown("<div class='crime-scene'>", unsafe_allow_html=True)
                st.markdown(f"### YOU ACCUSE: {accused['name']}")
                
                if accused == st.session_state.murderer:
                    st.session_state.game_over = True
                    st.session_state.correctly_accused = True
                    st.session_state.detective_score += 50
                    
                    st.markdown(f"""
## 🎉 CORRECT! 🎉

**{accused['name']} was indeed the murderer!**

**Motive:** {accused['motive']}

You have successfully solved the case!
The criminal has been arrested and justice is served.

**+50 bonus points for correct accusation!**

### FINAL DETECTIVE SCORE: {st.session_state.detective_score} points
                    """)
                    
                    if st.session_state.detective_score >= 100:
                        st.balloons()
                        st.markdown("### ⭐ EXCELLENT DETECTIVE WORK! ⭐")
                    
                else:
                    st.session_state.game_over = True
                    
                    st.markdown(f"""
## ❌ WRONG! ❌

**{accused['name']} is innocent!**

**The actual murderer was: {st.session_state.murderer['name']}**

**Motive:** {st.session_state.murderer['motive']}

Better luck next time, detective...

### FINAL DETECTIVE SCORE: {st.session_state.detective_score} points
                    """)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Play Again", use_container_width=True):
                        start_new_game()
                        st.rerun()
                with col2:
                    if st.button("🚪 Exit Game", use_container_width=True):
                        st.session_state.game_started = False
                        st.session_state.game_over = False
                        st.rerun()


if __name__ == "__main__":
    main()
