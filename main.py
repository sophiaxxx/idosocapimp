import asyncio
import time
import uuid

import aiohttp


# === 設定 ===
LIKE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/functions/v1/idolcamp-api/like"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrYW9lcmJibHB1c3pwdGlpYnZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NDY5MTMsImV4cCI6MjA5ODEyMjkxM30.Xf549NzokL9zY7AT8Jd5NYFRj81r7z2hS6i7kZbpCMw"

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

LIKE_MSG_IDS = ["508", "1205", "520", "29146", "38330", "72423", "53772", "533", "14242", "522", "495", "498", "45275"]

WORKERS_PER_MSG = 5  # 每個 msg_id 開幾個並行 worker


async def like_forever(session, msg_id):
    """對單個 msg_id 不停按讚，打完一次立刻打下一次"""
    count = 0
    while True:
        payload = {
            "messageId": msg_id,
            "action": "like",
            "clientId": str(uuid.uuid4()),
        }
        try:
            async with session.post(LIKE_URL, headers=HEADERS, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                count += 1
                if count % 50 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} count={count} -> {resp.status}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} Error: {e}")
            await asyncio.sleep(1)


async def main():
    print("🚀 按讚全速模式")
    print(f"  - {len(LIKE_MSG_IDS)} 個 msg_id × {WORKERS_PER_MSG} workers = {len(LIKE_MSG_IDS) * WORKERS_PER_MSG} 並行連線")
    print("  - 每個打完立刻打下一次，不等待")
    print("  - 每次用新的 clientId")
    print("按 Ctrl+C 停止\n")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for msg_id in LIKE_MSG_IDS:
            for _ in range(WORKERS_PER_MSG):
                tasks.append(like_forever(session, msg_id))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
