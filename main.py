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
    """隨機產生 nickname"""
    count = random.randint(1, 9999)
    patterns = [
        f"FLAREU{count}",
        f"way{count}2u",
        f"forever{count}",
        f"loveu{count}",
        f"fan{count}",
        f"yu{count}lover",
        f"foxbunny{count}",
        f"flare{count}forever",
        f"hyou{count}flare",
        f"flareu{count}fan",
        f"bunny{count}fox",
        f"u{count}flare",
        f"flare{count}love",
        f"fox{count}bunny",
        f"forever{count}flare",
        f"flare{count}star",
        f"yu{count}forever",
        f"love{count}flare",
        f"flare{count}queen",
        f"bunny{count}love",
        f"fox{count}queen",
        f"flare{count}baby",
        f"u{count}bunny",
        f"flare{count}dream",
        f"fox{count}love",
        f"flare{count}heart",
        f"bunny{count}star",
        f"u{count}fox",
        f"flareshine{count}",
        f"love{count}uuu",
        f"flare{count}power",
        f"fox{count}star",
        f"flare{count}magic",
        f"bunny{count}dream",
        f"u{count}love",
        f"flare{count}fire",
        f"fox{count}shine",
        f"flare{count}glow",
        f"bunnylight{count}",
        f"u{count}star",
        f"{count}flarejoy",
        f"fox{count}magic",
        f"flaresparkle{count}",
        f"bunny{count}shine",
        f"u{count}glow",
        f"flare{count}wonder",
        f"foxdream{count}",
        f"flare{count}bless",
        f"bunny{count}happy",
        f"u{count}smile",
        f"flare{count}bright",
        f"fox{count}wonder",
        f"flare{count}heaven",
        f"bunny{count}angel",
        f"u{count}heaven",
        f"flare{count}sun",
        f"fox{count}moon",
        f"flare{count}starlight",
        f"bunny{count}twinkle",
        f"u{count}spark",
        f"flare{count}cloud",
        f"fox{count}sky",
        f"flare{count}wind",
        f"bunny{count}breeze",
        f"star{count}yu",
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
        # 每次隨機等 2 到 5 秒
        time.sleep(random.uniform(2.0, 5.0))


if __name__ == "__main__":
    main()
