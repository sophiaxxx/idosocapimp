import asyncio
import random
import subprocess
import sys
import time

import requests
from playwright.async_api import async_playwright


def ensure_playwright_browsers():
    """確保 Playwright 瀏覽器已安裝"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("[INIT] Playwright chromium installed successfully")
        else:
            print(f"[INIT] Playwright install warning: {result.stderr}")
    except Exception as e:
        print(f"[INIT] Playwright install error: {e}")


# 啟動時確保瀏覽器存在
ensure_playwright_browsers()

# === 設定 ===
SUPABASE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/rest/v1/board_messages"
LIKE_URL = "https://kkaoerbblpuszptiibvo.supabase.co/rest/v1/rpc/increment_board_like"
SUBMIT_URL = "https://kkaoerbblpuszptiibvo.supabase.co/functions/v1/submit-pledge"
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
    "Cheering hard!",
    "Let's win #1!",
    "Go go go! 🔥",
    "We love FLARE U!",
    "Number 1 forever! 🏆",
]

LIKE_MSG_IDS = ["1205", "520", "508", "29146", "45275"]


def generate_nickname():
    """隨機產生 nickname"""
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
        return f"{random.choice(cn_prefixes)}{random.choice(cn_names)}{random.choice(cn_suffixes)}"
    elif strategy == 12:
        return f"{random.choice(cn_phrases)}{num}"
    elif strategy == 13:
        return f"{random.choice(cn_names)}{random.choice(cn_names)}{num2}號"
    elif strategy == 14:
        connectors = ["的", "與", "和", "加"]
        return f"{random.choice(cn_prefixes)}{random.choice(cn_names)}{random.choice(connectors)}{random.choice(cn_names)}"
    else:
        name = random.choice(first_names)
        return f"{name}_{random.choice(cn_prefixes)}{random.choice(cn_names)}{num2}"


# === 非同步留言迴圈（持久瀏覽器）===

async def message_loop():
    """
    保持一個瀏覽器開著，持續取 token 並發送留言。
    取到 token -> 馬上發 -> 重新整理頁面等下一個 token -> 重複。
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--single-process",
        ])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )
        page = await context.new_page()

        # 反偵測：覆蓋 navigator.webdriver
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['zh-TW', 'zh', 'en-US', 'en'] });
            window.chrome = { runtime: {} };
        """)

        print(f"[{time.strftime('%H:%M:%S')}] 🌐 Opening {SITE_URL}...")
        await page.goto(SITE_URL, wait_until="commit", timeout=60000)
        # SPA 需要較長時間載入，等 15 秒
        await page.wait_for_timeout(15000)

        # 除錯：印出頁面狀態
        title = await page.title()
        url = page.url
        print(f"[{time.strftime('%H:%M:%S')}] Page: {title} | {url}")

        # 檢查頁面內容和 JS 狀態
        page_state = await page.evaluate("""() => {
            return {
                bodyLength: document.body ? document.body.innerHTML.length : 0,
                bodyText: document.body ? document.body.innerText.substring(0, 200) : 'no body',
                scripts: document.querySelectorAll('script').length,
                webdriver: navigator.webdriver,
                docReady: document.readyState,
                html: document.documentElement.innerHTML.substring(0, 500),
            };
        }""")
        print(f"[{time.strftime('%H:%M:%S')}] Page state: {page_state}")

        # 嘗試等待 #formPanel 出現（留言表單區塊）
        try:
            await page.wait_for_selector("#formPanel", timeout=15000)
            print(f"[{time.strftime('%H:%M:%S')}] ✅ #formPanel found!")
            await page.evaluate("document.querySelector('#formPanel').scrollIntoView()")
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ #formPanel not found: {e}")

        # 印出 turnstile 相關資訊
        debug_info = await page.evaluate("""() => {
            const inputs = document.querySelectorAll('input[name="cf-turnstile-response"]');
            const holder = document.querySelector('#cf-turnstile-holder');
            return {
                turnstileInputs: inputs.length,
                turnstileInputValue: inputs.length > 0 ? (inputs[0].value || '').substring(0, 30) : 'none',
                holderExists: !!holder,
            };
        }""")
        print(f"[{time.strftime('%H:%M:%S')}] Turnstile: {debug_info}")

        msg_count = 0
        while True:
            try:
                # 等待 turnstile token 出現
                token = await wait_for_token(page)

                if token:
                    # 取到 token，馬上發留言
                    success = send_message(token)
                    msg_count += 1
                    if success:
                        print(f"[{time.strftime('%H:%M:%S')}] ✅ Total messages sent: {msg_count}")

                    # 重新整理頁面讓 Turnstile 重新產生 token
                    await page.reload(wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(3000)
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] ⏳ No token, retrying...")
                    await page.reload(wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] MSG loop error: {e}")
                # 嘗試重新開頁面
                try:
                    await page.goto(SITE_URL, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(5000)
                except Exception:
                    pass
                await asyncio.sleep(5)


async def wait_for_token(page, timeout=30):
    """等待 Turnstile token 出現，最多等 timeout 秒"""
    for _ in range(timeout):
        token = await page.evaluate("""() => {
            // 方法1: hidden input
            const input = document.querySelector('input[name="cf-turnstile-response"]');
            if (input && input.value && input.value.length > 0) return input.value;

            // 方法2: turnstile API
            if (window.turnstile) {
                try {
                    const resp = window.turnstile.getResponse();
                    if (resp) return resp;
                } catch(e) {}
            }

            return null;
        }""")
        if token:
            print(f"[{time.strftime('%H:%M:%S')}] 🎫 Got token: {token[:30]}...")
            return token
        await asyncio.sleep(1)
    return None


def send_message(token):
    """用 token 發送留言（同步 requests）"""
    nickname = generate_nickname()
    message = random.choice(MESSAGES)

    payload = {
        "nick": nickname,
        "team": "flareu",
        "message": message,
        "token": token,
    }

    try:
        response = requests.post(SUBMIT_URL, headers=HEADERS, json=payload, timeout=10)
        result = response.text
        print(f"[{time.strftime('%H:%M:%S')}] MSG {nickname}: {message} -> {response.status_code} {result}")
        return response.status_code == 200
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] MSG Error: {e}")
        return False


# === 非同步按讚迴圈 ===

async def like_loop():
    """每 1 秒對一則留言按讚"""
    while True:
        msg_id = random.choice(LIKE_MSG_IDS)
        payload = {"msg_id": msg_id}
        try:
            response = requests.post(LIKE_URL, headers=HEADERS, json=payload, timeout=10)
            print(f"[{time.strftime('%H:%M:%S')}] LIKE msg_id={msg_id} -> {response.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] LIKE Error: {e}")
        await asyncio.sleep(1)


# === 主程式 ===

async def main():
    print("🚀 啟動非同步排程...")
    print("  - 留言：持續取 token，取到即發")
    print("  - 按讚：每 1 秒")
    print("按 Ctrl+C 停止\n")

    # 同時跑留言和按讚
    await asyncio.gather(
        message_loop(),
        like_loop(),
    )


if __name__ == "__main__":
    asyncio.run(main())
