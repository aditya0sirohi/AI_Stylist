import os
import json
import re
import asyncio
import uuid

from emergentintegrations.llm.chat import LlmChat, UserMessage


def get_api_key():
    """Get LLM API key from environment."""
    key = os.environ.get("EMERGENT_LLM_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("EMERGENT_LLM_KEY not set.")
    return key


def run_async(coro):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)


def make_chat(system_message):
    """Create LlmChat instance."""
    chat = LlmChat(
        api_key=get_api_key(),
        session_id=f"fashion-{uuid.uuid4()}",
        system_message=system_message,
    ).with_model("gemini", "gemini-2.5-flash")
    return chat


async def ask_llm(chat, prompt_text):
    """Send message and get response."""
    from emergentintegrations.llm.chat import TextDelta, StreamDone

    pieces = []
    async for event in chat.stream_message(UserMessage(text=prompt_text)):
        if isinstance(event, TextDelta):
            pieces.append(event.content)
        elif isinstance(event, StreamDone):
            break
    return "".join(pieces).strip()


def extract_json(text):
    """Extract JSON from text response."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    brace = re.search(r"\{.*\}", text, re.DOTALL)
    if brace:
        return json.loads(brace.group(0))
    raise ValueError("No JSON in response")


def extract_intent(user_message):
    """Extract intent from user message using LLM."""
    system = "You are a fashion assistant that returns ONLY strict JSON, no prose."
    prompt = f"""Extract the user's fashion intent from this message.
Return ONLY a JSON object with these fields:
- occasion: casual, formal, party, office, wedding, beach, date, or other
- gender_hint: men, women, or null
- style_keywords: list of 1-3 style words
- age_group: teen, 20s, 30s, 40s, or null

User: "{user_message}"
"""
    chat = make_chat(system)
    try:
        reply = run_async(ask_llm(chat, prompt))
        return extract_json(reply)
    except Exception as e:
        print(f"Error extracting intent: {e}")
        return {
            "occasion": "casual",
            "gender_hint": None,
            "style_keywords": [],
            "age_group": None,
        }


def generate_explanation(user_message, profile, outfit_details, stylist_rationale):
    """Generate outfit explanation using LLM."""
    system = "You are a friendly fashion stylist. Reply in 3-4 conversational sentences."
    prompt = f"""User said: "{user_message}"
Profile: {profile.get('gender', 'unknown')}, {profile.get('age', '?')} years old, 
{profile.get('occasion', 'casual')} occasion, {profile.get('style_preference', 'classic')} style.

Outfit: {outfit_details}
Stylist note: {stylist_rationale}

Write a 3-4 sentence response that:
1. Acknowledges their request
2. Presents the outfit
3. Explains why it works
4. Gives one styling tip
"""
    chat = make_chat(system)
    try:
        return run_async(ask_llm(chat, prompt))
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return f"Here's an outfit for your {profile.get('occasion', 'event')}. {stylist_rationale}"
