# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# In-memory chat history
chat_history = []

def chat_view(request):
    """Render the chat interface as the default page."""
    return render(request, 'chatbot/chat.html')

def parse_user_message(user_message):
    """
    Uses Gemini API to parse the user message and extract recipe-related entities.
    Returns a dictionary with extracted entities in a specific format.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "You are a recipe entity parser. Parse the following user message and extract relevant entities "
        "(ingredients, dietary restrictions, cooking time, meal type) into a JSON dictionary. "
        "Return the result in this format:\n"
        "{\n"
        "  \"ingredients\": [\"ingredient1\", \"ingredient2\"],\n"
        "  \"dietary_restrictions\": [\"restriction1\", \"restriction2\"],\n"
        "  \"cooking_time\": \"time_range\",\n"
        "  \"meal_type\": \"type\",\n"
        "  \"intent\": \"query_type\"  // e.g., 'recipe_search', 'ingredient_substitution', 'dietary_info', or 'general'\n"
        "}\n"
        "If an entity type is not found, return an empty list for it. Detect intent based on keywords like "
        "'recipe', 'substitute', 'diet', 'quick', 'easy'. If no clear intent, use 'general'. "
        "Return only the raw JSON string without backticks or markdown formatting.\n"
        f"User message: {user_message}"
    )

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip()
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:-3].strip()
        elif raw_response.startswith("```"):
            raw_response = raw_response[3:-3].strip()
        parsed_json = json.loads(raw_response)
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Parsing JSON error: {e}")
        return {
            "ingredients": [],
            "dietary_restrictions": [],
            "cooking_time": "",
            "meal_type": "",
            "intent": "general"
        }
    except Exception as e:
        print(f"Parsing error: {e}")
        return {
            "ingredients": [],
            "dietary_restrictions": [],
            "cooking_time": "",
            "meal_type": "",
            "intent": "general"
        }

def format_metta_result(result):
    """Convert MeTTa Atom objects to readable strings."""
    if isinstance(result, list):
        return [format_metta_result(item) for item in result]
    elif hasattr(result, 'get_name'):  # Check if it's an Atom
        return str(result.get_name())
    return str(result)

@csrf_exempt
def chat_api(request):
    """Handle POST requests to process chat messages with recipe context and Gemini responses."""
    if request.method == 'POST':
        try:
            # Parse JSON from request.body
            data = json.loads(request.body)
            user_message = data.get('message')
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Add user message to chat history
            chat_history.append({'role': 'user', 'content': user_message})

            # Parse user message with Gemini
            parsed_entities = parse_user_message(user_message)
            ingredients = parsed_entities.get("ingredients", [])
            dietary_restrictions = parsed_entities.get("dietary_restrictions", [])
            cooking_time = parsed_entities.get("cooking_time", "")
            meal_type = parsed_entities.get("meal_type", "")

            # Prepare context based on parsed entities
            context = []
            
            if ingredients:
                context.append(f"Looking for recipes with: {', '.join(ingredients)}")
            if dietary_restrictions:
                context.append(f"Dietary restrictions: {', '.join(dietary_restrictions)}")
            if cooking_time:
                context.append(f"Preferred cooking time: {cooking_time}")
            if meal_type:
                context.append(f"Meal type: {meal_type}")

            # Prepare full prompt with chat history and recipe context
            conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
            full_prompt = (
                "You are a recipe recommendation chatbot. Use the provided context to suggest appropriate recipes "
                "and cooking advice. Consider dietary restrictions and preferences when making recommendations. "
                "Format your response in a clear, friendly manner with recipe suggestions, ingredients, and basic steps. "
                f"Recipe context: {' '.join(context)}\nConversation history:\n{conversation}"
            )

            # Call Gemini API for final response
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(full_prompt)
            bot_response = response.text if response.text else "Sorry, I couldn't provide recipe suggestions at this time."

            # Add bot response to chat history
            chat_history.append({'role': 'assistant', 'content': bot_response})

            return JsonResponse({'response': bot_response})

        except json.JSONDecodeError as je:
            print(f"JSON error: {je}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)