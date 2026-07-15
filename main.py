import asyncio
import time

import aiohttp

# === 設定 ===
LIKE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/functions/v1/idolcamp-api/like"

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrYW9lcmJibHB1c3pwdGlpYnZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NDY5MTMsImV4cCI6MjA5ODEyMjkxM30.Xf549NzokL9zY7AT8Jd5NYFRj81r7z2hS6i7kZbpCMw"


CLIENT_ID = "f8e2aae9-d8e8-4736-a6af-4843ef8aeb3b"

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
    "241057", "241056", "241055", "241054","248736"
]

WORKERS_PER_MSG = 1

BASE_PAYLOAD = {
    "action": "like",
    "clientId": CLIENT_ID,
}


async def like_forever(session, message_id, worker_id):
    """不停對指定 messageId 按讚"""
    count = 0

    while True:
        payload = {
            **BASE_PAYLOAD,
            "messageId": message_id
        }

        try:
            async with session.post(
                LIKE_URL,
                headers=HEADERS,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:

                count += 1

                if resp.status == 200:
                    if count % 200 == 0:
                        print(
                            f"[{time.strftime('%H:%M:%S')}] "
                            f"messageId={message_id} worker={worker_id} "
                            f"count={count} -> 200"
                        )

                    # 成功稍微停一下，避免把 TCP 打滿
                    await asyncio.sleep(0.05)

                elif resp.status == 429:
                    print(
                        f"[{time.strftime('%H:%M:%S')}] "
                        f"messageId={message_id} -> 429 RATE LIMITED"
                    )
                    await asyncio.sleep(3)

                else:
                    text = await resp.text()
                    print(
                        f"[{time.strftime('%H:%M:%S')}] "
                        f"messageId={message_id} -> {resp.status}\n{text[:200]}"
                    )
                    await asyncio.sleep(2)

        except Exception as e:
            print(
                f"[{time.strftime('%H:%M:%S')}] "
                f"messageId={message_id} Error: {type(e).__name__}: {e}"
            )
            await asyncio.sleep(3)


async def main():
    total_workers = len(LIKE_MESSAGE_IDS) * WORKERS_PER_MSG

    print("🚀 Like 全速模式")
    print(f"Message 數量：{len(LIKE_MESSAGE_IDS)}")
    print(f"Workers：{WORKERS_PER_MSG}")
    print(f"總並行數：{total_workers}")
    print("按 Ctrl+C 停止\n")

    connector = aiohttp.TCPConnector(
        limit=total_workers,
        limit_per_host=total_workers,
        ttl_dns_cache=300,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for message_id in LIKE_MESSAGE_IDS:
            for worker in range(WORKERS_PER_MSG):
                tasks.append(
                    asyncio.create_task(
                        like_forever(session, message_id, worker)
                    )
                )

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())