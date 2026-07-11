import requests
import time
import random
import threading

SUPABASE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/rest/v1/board_messages"
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

# 要按讚的留言 ID
LIKE_MSG_IDS = ["1205", "520", "508", "29146", "45275"]


def generate_nickname():
    """隨機產生 nickname - 多樣化格式避免 spam 偵測（含中文）"""
    strategy = random.randint(1, 15)

    first_names = [
        "emma", "olivia", "sophia", "mia", "luna", "chloe", "lily",
        "aria", "ella", "grace", "zoey", "nora", "riley", "stella",
        "ivy", "aurora", "violet", "ruby", "jade", "alice", "hannah",
        "claire", "maya", "elena", "sarah", "emily", "amber", "daisy",
        "hazel", "iris", "pearl", "willow", "summer", "melody", "diana",
        "vera", "clara", "mina", "yuna", "hana", "kate", "anna", "lena",
        "nina", "faye", "nova", "eden", "sage", "june", "rain",
    ]

    adjectives = [
        "happy", "sunny", "lucky", "sweet", "cool", "soft", "warm",
        "wild", "free", "cute", "pure", "calm", "bold", "kind",
        "tiny", "lazy", "cozy", "mega", "mini", "super",
    ]

    nouns = [
        "star", "moon", "sun", "sky", "rain", "snow", "wind",
        "rose", "lily", "bird", "cat", "fox", "bear", "wolf",
        "dream", "love", "hope", "soul", "fate", "angel",
        "cloud", "ocean", "river", "fire", "light", "spark",
    ]

    hobbies = [
        "music", "dance", "art", "photo", "cook", "travel", "read",
        "game", "draw", "sing", "yoga", "surf", "hike", "film",
    ]

    # 中文相關素材
    cn_prefixes = [
        "小", "大", "阿", "老", "可愛的", "快樂", "幸福", "追星",
        "愛", "超級", "夢幻", "陽光", "月光", "星星",
    ]
    cn_names = [
        "兔子", "狐狸", "貓咪", "小鹿", "蝴蝶", "海豚", "熊貓",
        "櫻花", "向日葵", "薰衣草", "玫瑰", "百合", "雛菊",
        "星辰", "月亮", "太陽", "彩虹", "雲朵", "微風", "流星",
        "糖果", "蜂蜜", "奶茶", "布丁", "麻糬", "草莓", "芒果",
        "珍珠", "水晶", "鑽石", "琥珀", "翡翠", "瑪瑙",
    ]
    cn_suffixes = [
        "醬", "寶", "兒", "妹", "姐", "控", "迷", "粉",
        "啊", "呀", "唷", "嗨", "喵", "汪",
    ]
    cn_phrases = [
        "我愛追星", "追夢少女", "應援達人", "永遠的粉絲",
        "星光閃閃", "夢想起飛", "快樂每天", "幸福滿滿",
        "愛你唷", "心動瞬間", "甜甜的夢", "閃亮亮",
        "元氣滿滿", "正能量", "暖暖的", "軟萌萌",
        "奶茶控", "追星日記", "偶像萬歲", "應援一生",
        "粉紅泡泡", "彩虹天使", "夢幻旋律", "星河漫步",
    ]

    num = random.randint(0, 999)
    num2 = random.randint(10, 99)
    year = random.randint(90, 99) if random.random() > 0.5 else random.randint(0, 26)

    if strategy == 1:
        return f"{random.choice(first_names)}_{random.choice(nouns)}{num2}"
    elif strategy == 2:
        adj = random.choice(adjectives).capitalize()
        noun = random.choice(nouns).capitalize()
        return f"{adj}{noun}_{num}"
    elif strategy == 3:
        name = random.choice(first_names)
        hobby = random.choice(hobbies)
        return f"{name}.{hobby}{num2}"
    elif strategy == 4:
        name = random.choice(first_names)
        wraps = ["xo", "xx", "luv", "hi", "hey", "yo"]
        w = random.choice(wraps)
        return f"{w}_{name}_{w}{num2 if random.random() > 0.5 else ''}"
    elif strategy == 5:
        adj = random.choice(adjectives)
        name = random.choice(first_names)
        return f"{adj}.{name}{num2:02d}"
    elif strategy == 6:
        name = random.choice(first_names).capitalize()
        starters = ["its", "im", "the", "just", "hey"]
        enders = ["Here", "Today", "Now", "Daily", "Vibes", "World"]
        return f"{random.choice(starters)}{name}{random.choice(enders)}"
    elif strategy == 7:
        name = random.choice(first_names)
        hobby = random.choice(hobbies)
        return f"{name}_{year}_{hobby}"
    elif strategy == 8:
        noun = random.choice(nouns).capitalize()
        name = random.choice(first_names).capitalize()
        extras = ["light", "shine", "glow", "beam", "dust", "drop"]
        return f"{noun}{random.choice(extras)}{name}"
    elif strategy == 9:
        name = random.choice(first_names)
        adj = random.choice(adjectives)
        return f"{num2}{adj}{random.choice(['4', '_', '.'])}{name}"
    elif strategy == 10:
        name = random.choice(first_names)
        tails = ["xoxo", "luv", "yay", "uwu", "rawr", "hehe", "lol"]
        separators = ["__", "_", ".", "x"]
        return f"{name}{random.choice(separators)}{random.choice(tails)}{num}"
    elif strategy == 11:
        # 小兔子醬
        return f"{random.choice(cn_prefixes)}{random.choice(cn_names)}{random.choice(cn_suffixes)}"
    elif strategy == 12:
        # 追夢少女927
        return f"{random.choice(cn_phrases)}{num}"
    elif strategy == 13:
        # 草莓奶茶42號
        return f"{random.choice(cn_names)}{random.choice(cn_names)}{num2}號"
    elif strategy == 14:
        # 愛追星的小貓咪
        connectors = ["的", "與", "和", "加"]
        return f"{random.choice(cn_prefixes)}{random.choice(cn_names)}{random.choice(connectors)}{random.choice(cn_names)}"
    else:
        # 混合：luna_小星星99
        name = random.choice(first_names)
        return f"{name}_{random.choice(cn_prefixes)}{random.choice(cn_names)}{num2}"


def send_message():
    """發送一則留言"""
    nickname = generate_nickname()
    message = random.choice(MESSAGES)

    payload = {
        "nickname": nickname,
        "nickname_key": nickname,
        "team": "flareu",
        "message": message,
        "likes": 0,
    }

    try:
        response = requests.post(SUPABASE_URL, headers=HEADERS, json=payload, timeout=10)
        print(f"[{time.strftime('%H:%M:%S')}] MSG {nickname}: {message} -> {response.status_code}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] MSG Error: {e}")


def send_like():
    """對指定留言按讚"""
    msg_id = random.choice(LIKE_MSG_IDS)
    payload = {"msg_id": msg_id}

    try:
        response = requests.post(LIKE_URL, headers=HEADERS, json=payload, timeout=10)
        print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} -> {response.status_code}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] LIKE Error: {e}")


def message_loop():
    """每 1 秒發送一則留言"""
    while True:
        send_message()
        time.sleep(1)


def like_loop():
    """每 1 秒對一則留言按讚"""
    while True:
        send_like()
        time.sleep(1)


def main():
    print("🚀 開始排程...")
    print("  - 留言：每 1 秒")
    print("  - 按讚：每 1 秒")
    print("按 Ctrl+C 停止\n")

    # 用兩個 thread 分別跑兩個排程
    t1 = threading.Thread(target=message_loop, daemon=True)
    t2 = threading.Thread(target=like_loop, daemon=True)

    t1.start()
    t2.start()

    # 主線程等待
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
