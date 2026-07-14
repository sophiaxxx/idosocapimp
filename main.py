import asyncio
import time

import aiohttp


# === 設定 ===
LIKE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/rest/v1/rpc/increment_board_like"
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

LIKE_MSG_IDS = ["508", "1205", "520", "29146", "38330", "72423", "53772", "533", "14242", "522", "495", "498", "45275", "238365", "238368", "238367", "238366", "238364", "238363", "238362", "240480", "240479", "240475","240669","240655","240652","240650","240670","240819","240815","240853","240855","502","492","1289","683","617","490","590","366","616","636","666"]

WORKERS_PER_MSG = 2


async def like_forever(session, msg_id, worker_id):
    """對單個 msg_id 不停按讚，成功不等待，失敗才減速"""
    count = 0
    while True:
        payload = {"msg_id": msg_id}
        try:
            async with session.post(LIKE_URL, headers=HEADERS, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                count += 1
                if resp.status == 200:
                    if count % 200 == 0:
                        print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} w{worker_id} count={count} -> 200")
                    await asyncio.sleep(0.05)  # 極短暫停，避免打爆連線
                elif resp.status == 429:
                    await asyncio.sleep(3)
                else:
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} Error: {type(e).__name__}: {e}")
            await asyncio.sleep(3)


async def main():
    print("🚀 按讚全速模式")
    print(f"  - {len(LIKE_MSG_IDS)} 個 msg_id × {WORKERS_PER_MSG} workers = {len(LIKE_MSG_IDS) * WORKERS_PER_MSG} 並行連線")
    print("  - 成功立刻打下一次，失敗才減速")
    print("按 Ctrl+C 停止\n")

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=30)) as session:
        tasks = []
        for msg_id in LIKE_MSG_IDS:
            for w in range(WORKERS_PER_MSG):
                tasks.append(like_forever(session, msg_id, w))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
