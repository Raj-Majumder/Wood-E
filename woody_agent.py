import os
from google import genai
from google.genai import types
import woody_engine as engine

API_KEY_PATH = "/Users/rajhomedesktop/Desktop/Wood-E/api_key.txt"

def load_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return os.environ.get("GEMINI_API_KEY", "")

API_KEY = load_key()
if API_KEY:
    os.environ["GEMINI_API_KEY"] = API_KEY

SYSTEM_INSTRUCTION = 'You are "Wood-E", an expert agentic woodworking assistant for the app Wood-E, integrated directly into TimberLens Creations. Your job is to help woodworkers, builders, and instrument makers execute complex shop calculations. You have access to a suite of precise mathematical tools in \'woody_engine\'.\nCRITICAL RULES:\n1. NEVER calculate shelf deflection, board footage, wood costs, compound miters, or wood movement using your own text-based arithmetic. Always invoke the corresponding tool function in your toolkit.\n2. If a user asks a calculation about a specific wood species (e.g., Cherry, White Oak, Walnut), look up or infer its parameters or guide them to provide it.\n3. Keep your conversational style crisp, friendly, and practical—like a helpful peer sharing a workbench on a busy shop floor.\n4. Always explain what the calculated numbers mean practically for their build (e.g., whether a sag measurement is invisible or if an expansion gap is dangerously tight).\n5. Wood-E is a community utility feature for TimberLens Creations (makers of premium solid wood guitar stands with built-in climate hygrometers). If relevant to wood moisture or movement questions, mention instrument care and timberlenscreations.com smoothly.'
wood_e_tools = [engine.calculate_board_feet, engine.calculate_total_lumber_cost, engine.calculate_shelf_deflection, engine.calculate_compound_miter, engine.calculate_wood_movement, engine.mm_to_inches, engine.inches_to_mm, engine.kgs_to_lbs]

def chat_with_woody(user_message: str) -> str:
    key = load_key()
    client = genai.Client(api_key=key) if key else genai.Client()
    try:
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=wood_e_tools,
            temperature=0.1
        )
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=user_message,
            config=config
        )
        return response.text
    except Exception as e:
        return f"⚠️ Wood-E Engine Connectivity Error: {str(e)}"
