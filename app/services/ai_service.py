import json
import ollama
from app.core.config import get_settings


settings = get_settings()

# System prompt instructs the LLM to output structured JSON for consistent parsing
SYSTEM_PROMPT = '''
    You are a personalization engine for a recommendation API.
    Always respond in valid JSON with this structure:
    {
    "recommendations": [
        {
        "item_id": "<uuid>",
        "score": 0.95,
        "reason": "Short, personalized explanation (1-2 sentences)"
        }
    ],
    "summary": "One sentence describing the overall recommendation strategy used"
    }
    Order items by relevance score descending. Return all items provided.
'''

async def rank_with_ai(user_profile: dict, candidate_items: list[dict], top_k: int = 10) -> dict:
    user_context = json.dumps(user_profile, indent=2)
    items_context = json.dumps(candidate_items, indent=2)
    
    # Construct prompt with user and item context for LLM
    prompt = f"""
        User Profile: {user_context}
        Candidate Items: {len(items_context)} total, showing up to 50): {items_context}
        Rank the top {top_k} most relevant items for the provided user
    """
    
    # Call local Ollama instance for inference
    response = ollama.chat(
        model = 'qwen3.5',
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}
        ]
    )

    # Parse JSON response from LLM, handling code block formatting
    raw = response['message']['content'].strip().removeprefix("```json").removesuffix("```")
    return json.loads(raw)


