import asyncio
import os
import random
import sys
import time

import aiohttp


# === 設定 ===
LIKE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/rest/v1/rpc/increment_board_like"
SITE_URL = "https://idolcamp.muniverse.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrYW9lcmJibHB1c3pwdGlpYnZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NDY5MTMsImV4cCI6MjA5ODEyMjkxM30.Xf549NzokL9zY7AT8Jd5NYFRj81r7z2hS6i7kZbpCMw"

HEADERS = {
    "accept": "*/*",
    "apikey": API_KEY,
    "authorization": f"Bearer {API_KEY}",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": SITE_URL,
    "pragma": "no-cache",
    "prefer": "return=minimal",
    "referer": f"{SITE_URL}/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}

LIKE_MSG_IDS = ["1205", "520", "508", "29146", "45275", "38330", "72423", "53772", "533"]


# === 非同步按讚迴圈 ===

async def like_loop():
    """每秒對所有留言都按讚（並行發送）"""
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [_like_one(session, msg_id) for msg_id in LIKE_MSG_IDS]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, Exception):
                    print(f"[{time.strftime('%H:%M:%S')}] LIKE Error: {r}")
            await asyncio.sleep(1)


async def _like_one(session, msg_id):
    """發送單次按讚請求"""
    payload = {"msg_id": msg_id}
    try:
        async with session.post(LIKE_URL, headers=HEADERS, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} -> {resp.status}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} Error: {e}")


# === 主程式 ===

async def main():
    print("🚀 啟動按讚排程...")
    print(f"  - 每秒對 {len(LIKE_MSG_IDS)} 則留言同時按讚")
    print("按 Ctrl+C 停止\n")
    await like_loop()


if __name__ == "__main__":
    asyncio.run(main())
