import asyncio
import os
import time
import uuid

import aiohttp

# === 設定 ===
LIKE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/functions/v1/idolcamp-api/like"

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrYW9lcmJibHB1c3pwdGlpYnZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NDY5MTMsImV4cCI6MjA5ODEyMjkxM30.Xf549NzokL9zY7AT8Jd5NYFRj81r7z2hS6i7kZbpCMw"

# 每個 worker instance 用不同的 CLIENT_ID
CLIENT_ID = os.environ.get("CLIENT_ID", str(uuid.uuid4()))

HEADERS = {
    "accept": "*/*",
    "apikey": API_KEY,
    "authorization": f"Bearer {API_KEY}",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://sanbital.github.io",
    "pragma": "no-cache",
    "referer": "https://sanbital.github.io/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}

LIKE_MESSAGE_IDS = [
    "508", "1205", "520", "29146", "38330", "72423", "53772",
    "533", "14242", "522", "495", "498", "45275",
    "238365", "238368", "238367", "238366", "238364", "238363", "238362",
    "240480", "240479", "240475",
    "240669", "240655", "240652", "240650", "240670",
    "240819", "240815", "240853", "240855",
    "502", "492", "1289", "683", "617", "490",
    "590", "366", "616", "636", "666",
    "241057", "241056", "241055", "241054", "248736",
]


async def like_all_sequential(session):
    """依序對每個 messageId 按讚一次，全部打完後等 10 秒再重來"""
    round_count = 0

    while True:
        round_count += 1
        ok = 0
        rate_limited = 0
        errors = 0

        for message_id in LIKE_MESSAGE_IDS:
            payload = {
                "messageId": message_id,
                "action": "like",
                "clientId": CLIENT_ID,
            }

            try:
                async with session.post(
                    LIKE_URL,
                    headers=HEADERS,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 200:
                        ok += 1
                    elif resp.status == 429:
                        rate_limited += 1
                    else:
                        errors += 1
                        if errors <= 3:
                            text = await resp.text()
                            print(f"[{time.strftime('%H:%M:%S')}] messageId={message_id} -> {resp.status} {text[:100]}")
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"[{time.strftime('%H:%M:%S')}] messageId={message_id} Error: {type(e).__name__}: {e}")

        print(f"[{time.strftime('%H:%M:%S')}] Round {round_count} done: ✅{ok} ⚠️429:{rate_limited} ❌{errors} (clientId={CLIENT_ID[:8]}...)")

        # 每輪完後等 10 秒
        await asyncio.sleep(10)


async def main():
    print("🚀 按讚模式（依序執行，每 10 秒一輪）")
    print(f"  - {len(LIKE_MESSAGE_IDS)} 個 messageId")
    print(f"  - clientId: {CLIENT_ID}")
    print("按 Ctrl+C 停止\n")

    async with aiohttp.ClientSession() as session:
        await like_all_sequential(session)


if __name__ == "__main__":
    asyncio.run(main())
