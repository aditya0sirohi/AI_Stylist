"""
llm.py
Thin wrapper around the Gemini model (via the Emergent Universal LLM key).
Two jobs:
  1) extract_intent(user_message) -> dict with occasion, gender_hint, style_keywords
  2) generate_explanation(...)    -> friendly outfit description from the stylist
"""

import os
import json
import re
import asyncio
import uuid

from emergentintegrations.llm.chat import LlmChat, UserMessage


# Pick up the Emergent Universal LLM Key from the environment.
def _get_api_key():
    key = os.environ.get("EMERGENT_LLM_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "EMERGENT_LLM_KEY not set. Add it to environment before running."
        )
    return key


# Run any async coroutine from a sync Streamlit context.
def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Streamlit can sometimes have an active loop; use a fresh one.
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)


# Build a fresh LlmChat for one-shot calls. Each call gets its own session id
# because we manage history at the Streamlit layer, not inside the SDK.
def _make_chat(system_message):
    chat = LlmChat(
        api_key=_get_api_key(),
        session_id=f"fashion-{uuid.uuid4()}",
        system_message=system_message,
    ).with_model("gemini", "gemini-2.5-flash")
    return chat


# Send a single message and collect the full streamed response into a string.
async def _ask(chat, prompt_text):
    from emergentintegrations.llm.chat import TextDelta, StreamDone

    pieces = []
    async for event in chat.stream_message(UserMessage(text=prompt_text)):
        if isinstance(event, TextDelta):
            pieces.append(event.content)
        elif isinstance(event, StreamDone):
            break
    return "".join(pieces).strip()


# Pull the first JSON object out of an LLM reply (handles ```json fences).
def _extract_json(text):
    # strip markdown fences if present
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    # otherwise grab the first {...} block
    brace = re.search(r"\{.*\}", text, re.DOTALL)
    if brace:
        return json.loads(brace.group(0))
    raise ValueError("No JSON object found in LLM response")


# Ask Gemini to convert the user's chat message into a structured intent dict.
def extract_intent(user_message):
    system = "You are a fashion assistant that returns ONLY strict JSON, no prose."
    prompt = f"""You are a fashion assistant. Extract the user's intent from this message.
Return ONLY a JSON object (no markdown, no commentary) with these fields:
- occasion: one of casual, formal, party, office, wedding, beach, date, other
- gender_hint: one of men, women, or null
- style_keywords: list of up to 3 relevant style words
- age_group: one of teen, 20s, 30s, 40s, or null

User message: "{user_message}"
"""
    chat = _make_chat(system)
    try:
        reply = _run_async(_ask(chat, prompt))
        return _extract_json(reply)
    except Exception as e:
        print(f"[llm.extract_intent] fallback due to: {e}")
        # Safe fallback so the app keeps working even if Gemini hiccups.
        return {
            "occasion": "casual",
            "gender_hint": None,
            "style_keywords": [],
            "age_group": None,
        }


# Ask Gemini to write a warm 3-4 sentence outfit explanation for the user.
def generate_explanation(user_message, profile, outfit_details, stylist_rationale):
    system = ("You are a friendly, knowledgeable fashion stylist. "
              "Reply in 3-4 conversational sentences. No bullet lists.")
    prompt = f"""A user said: "{user_message}"
Their profile: {profile.get('gender', 'unspecified')}, {profile.get('age', 'n/a')} years old,
{profile.get('occasion', 'unspecified')} occasion, prefers {profile.get('style_preference', 'classic')} style.

You are recommending this outfit:
{outfit_details}

The stylist rationale is: {stylist_rationale}

Write a warm, conversational 3-4 sentence response that:
1. Acknowledges their request
2. Presents the outfit naturally
3. Explains why the pieces work together
4. Mentions one specific styling tip

Keep it friendly, like a helpful friend who knows fashion.
"""
    chat = _make_chat(system)
    try:
        return _run_async(_ask(chat, prompt))
    except Exception as e:
        print(f"[llm.generate_explanation] fallback due to: {e}")
        return (f"Here's an outfit for your {profile.get('occasion', 'occasion')}. "
                f"{stylist_rationale}")
