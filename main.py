import requests
import time
import random

SUPABASE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/rest/v1/board_messages"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrYW9lcmJibHB1c3pwdGlpYnZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NDY5MTMsImV4cCI6MjA5ODEyMjkxM30.Xf549NzokL9zY7AT8Jd5NYFRj81r7z2hS6i7kZbpCMw"

HEADERS = {
    "accept": "*/*",
    "apikey": API_KEY,
    "authorization": f"Bearer {API_KEY}",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://sanbital.github.io",
    "pragma": "no-cache",
    "prefer": "return=minimal",
    "referer": "https://sanbital.github.io/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}

MESSAGES = [
    "1등 가자!",
    "推し ファイティン 🔥",
    "FLARE U🐰🦊 ♡ U're",
    "全力應援 🐰🦊 !衝呀！",
    "Fighting 🔥🔥🔥",
    "우리 플레어유 최고 ❤️",
    "FLARE U 加油！💪",
    "応援してるよ！🌟",
    "衝衝衝 🚀🚀🚀",
    "永遠支持 FLARE U 🐰🦊",
    "플레어유 사랑해 💕",
    "一起衝第一！🏆",
    "FLARE U best! ✨",
    "頑張れ！絶対1位！🥇",
    "응원합니다 화이팅! 🎉",
]


def generate_nickname():
    """隨機產生 nickname - 英文名字版本"""
    count = random.randint(1, 9999)
    names = [
        "emma", "olivia", "ava", "sophia", "mia", "luna", "chloe",
        "lily", "aria", "ella", "grace", "zoey", "nora", "riley",
        "stella", "ivy", "aurora", "violet", "ruby", "jade",
        "alice", "hannah", "claire", "maya", "elena", "sarah",
        "emily", "amber", "daisy", "hazel", "iris", "pearl",
        "willow", "sky", "summer", "autumn", "melody", "harmony",
        "celeste", "luna", "serena", "diana", "vera", "rosa",
        "clara", "mina", "yuna", "hana", "sora", "rena",
        "kate", "anna", "lena", "nina", "tara", "faye",
        "nova", "eden", "sage", "wren", "june", "rain",
    ]
    name = random.choice(names)
    patterns = [
        f"{name}{count}",
        f"{name}_flareu{count}",
        f"{name}loves{count}",
        f"{name}{count}fan",
        f"hi_{name}{count}",
        f"{name}_yu{count}",
        f"{name}xx{count}",
        f"{name}{count}u",
        f"its{name}{count}",
        f"{name}_here{count}",
    ]
    return random.choice(patterns)


def send_message():
    """發送一則留言"""
    nickname = generate_nickname()
    message = random.choice(MESSAGES)

    payload = {
        "nickname": nickname,
        "nickname_key": nickname,
        "team": "flareu",
        "message": message,
        "likes": 2,
    }

    try:
        response = requests.post(SUPABASE_URL, headers=HEADERS, json=payload, timeout=10)
        print(f"[{time.strftime('%H:%M:%S')}] {nickname}: {message} -> {response.status_code}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")


def main():
    print("🚀 開始排程，每5秒發送一則留言...")
    print("按 Ctrl+C 停止\n")

    while True:
        send_message()
        time.sleep(5)


if __name__ == "__main__":
    main()
