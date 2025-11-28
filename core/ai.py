import os, json
import openai
import logging

logger = logging.getLogger("ReminderBot.AI")
openai.api_key = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

def chat_reply(user_text: str, max_tokens: int = 200):
    try:
        resp = openai.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": user_text}],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        logger.exception("Chat reply failed")
        return "AI unavailable. Try later...."

def parse_reminder_with_ai(user_text: str):
    prompt = f"""
You are a JSON generator. Classify user messages as:
1. 'greeting' → {{"type":"greeting","message":"reply"}}
2. 'reminder' → [{{"task":"...", "time":"...", "repeat":1, "interval_seconds":0}}]

Return **only valid JSON**, nothing else.
User message: "{user_text}"
"""
    try:
        resp = openai.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role":"system","content":"You are a JSON generator."},
                {"role":"user","content":prompt}
            ],
            max_tokens=400,
            temperature=0
        )
        content = resp.choices[0].message.content.strip()
        idx_list = [content.find("["), content.find("{")]
        idx_list = [i for i in idx_list if i != -1]
        idx = min(idx_list) if idx_list else 0
        if idx > 0:
            content = content[idx:]

        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return [parsed]
        elif isinstance(parsed, list):
            return [p if isinstance(p, dict) else {"type": "unknown", "raw": str(p)} for p in parsed]
        else:
            return [{"type": "unknown", "raw": str(parsed)}]

    except json.JSONDecodeError:
        logger.error(f"JSON parse failed. Raw AI output: {content}")
        return []
    except Exception:
        logger.exception("AI parse error")
        return []
