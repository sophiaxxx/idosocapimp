import asyncio
import os
import random
import subprocess
import sys
import time

import aiohttp
import requests
from playwright.async_api import async_playwright


def ensure_playwright_browsers():
    """確保 Playwright 瀏覽器已安裝，以及 Xvfb"""
    # 安裝 Xvfb（虛擬螢幕，讓 headed 模式可以在無螢幕伺服器跑）
    try:
        subprocess.run(
            ["which", "xvfb-run"],
            capture_output=True, timeout=5
        )
        print("[INIT] xvfb-run already available")
    except Exception:
        try:
            subprocess.run(
                ["apt-get", "install", "-y", "xvfb"],
                capture_output=True, text=True, timeout=60
            )
            print("[INIT] Xvfb installed")
        except Exception as e:
            print(f"[INIT] Xvfb install skipped: {e}")

    # 安裝 Playwright 瀏覽器
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("[INIT] Playwright chromium installed successfully")
        else:
            print(f"[INIT] Playwright install warning: {result.stderr[:200]}")
    except Exception as e:
        print(f"[INIT] Playwright install error: {e}")


# 啟動時確保環境就緒
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

LIKE_MSG_IDS = ["1205", "520", "508", "29146", "45275", "38330", "72423", "53772","533"]


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


# === Turnstile sitekey（從前端原始碼取得）===
TURNSTILE_SITEKEY = "0x4AAAAAAD0Ey7nrVqGnKma-"

# 最小化 Turnstile HTML 頁面（本地載入用）
TURNSTILE_HTML = f"""<!DOCTYPE html>
<html><head><title>t</title></head><body>
<div id="cf-turnstile-holder"></div>
<script>
window.onTurnstileReady = function() {{
  window.turnstile.render('#cf-turnstile-holder', {{
    sitekey: '{TURNSTILE_SITEKEY}',
    theme: 'light',
    size: 'flexible',
    callback: function(token) {{
      document.getElementById('token').value = token;
    }}
  }});
}};
</script>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onTurnstileReady&render=explicit" async defer></script>
<input type="hidden" id="token" value="">
</body></html>"""


# === 非同步留言迴圈（持久瀏覽器）===

async def message_loop():
    """
    保持一個瀏覽器開著，用自建的 Turnstile 頁面持續取 token。
    取到 token -> 馬上發 -> 重新整理等下一個 token -> 重複。
    """
    async with async_playwright() as p:
        # 用 headed 模式 + Xvfb 虛擬螢幕，避免被 Turnstile 偵測為 headless

        # 啟動 Xvfb（如果 xvfb-run 已經在外層啟動，這裡會自動跳過）
        if not os.environ.get("DISPLAY"):
            try:
                xvfb_proc = subprocess.Popen(
                    ["Xvfb", ":99", "-screen", "0", "1280x720x24", "-nolisten", "tcp", "-ac"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                await asyncio.sleep(2)
                os.environ["DISPLAY"] = ":99"
                if xvfb_proc.poll() is not None:
                    print(f"[{time.strftime('%H:%M:%S')}] Xvfb :99 failed, trying other displays...")
                    for dn in range(10, 20):
                        xvfb_proc = subprocess.Popen(
                            ["Xvfb", f":{dn}", "-screen", "0", "1280x720x24", "-nolisten", "tcp", "-ac"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                        )
                        await asyncio.sleep(2)
                        if xvfb_proc.poll() is None:
                            os.environ["DISPLAY"] = f":{dn}"
                            print(f"[{time.strftime('%H:%M:%S')}] Xvfb started on :{dn}")
                            break
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ All Xvfb attempts failed")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Xvfb started (pid={xvfb_proc.pid}), DISPLAY=:99")
            except FileNotFoundError:
                print(f"[{time.strftime('%H:%M:%S')}] Xvfb not found, installing...")
                subprocess.run(["apt-get", "install", "-y", "-qq", "xvfb"], capture_output=True)
                xvfb_proc = subprocess.Popen(
                    ["Xvfb", ":99", "-screen", "0", "1280x720x24", "-nolisten", "tcp", "-ac"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                await asyncio.sleep(2)
                os.environ["DISPLAY"] = ":99"
                if xvfb_proc.poll() is None:
                    print(f"[{time.strftime('%H:%M:%S')}] Xvfb started after install")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Xvfb still not working after install")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Xvfb error: {e}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Using existing DISPLAY={os.environ['DISPLAY']}")

        # 必須 headed 模式，headless 無法通過 Turnstile
        display_val = os.environ.get('DISPLAY', 'NOT SET')
        print(f"[{time.strftime('%H:%M:%S')}] Launching browser headed, DISPLAY={display_val}")

        # 驗證 X server 是否可連接
        xdpyinfo_result = subprocess.run(
            ["xdpyinfo", "-display", os.environ.get("DISPLAY", ":99")],
            capture_output=True, timeout=5
        )
        if xdpyinfo_result.returncode != 0:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ X server not responding, output: {xdpyinfo_result.stderr.decode()[:200]}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] ✅ X server verified on {display_val}")

        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-blink-features=AutomationControlled",
                f"--display={os.environ.get('DISPLAY', ':99')}",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )
        page = await context.new_page()

        # 反偵測
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['zh-TW', 'zh', 'en-US', 'en'] });
            window.chrome = { runtime: {} };
        """)

        # 用自建的 Turnstile HTML 頁面，透過 route 攔截讓它看起來是從正確網域載入
        print(f"[{time.strftime('%H:%M:%S')}] 🌐 Loading Turnstile page...")

        # 只攔截 HTML document 請求，不攔截子資源（讓 Turnstile JS 正常載入）
        async def handle_route(route):
            if route.request.resource_type == "document":
                await route.fulfill(
                    status=200,
                    content_type="text/html",
                    body=TURNSTILE_HTML,
                )
            else:
                await route.continue_()

        await page.route("**/*", handle_route)
        await page.goto(SITE_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(10000)

        # 除錯：看 Turnstile 狀態
        debug = await page.evaluate("""() => {
            return {
                url: location.href,
                tokenEl: !!document.getElementById('token'),
                tokenVal: (document.getElementById('token') || {}).value || '',
                turnstileLoaded: !!window.turnstile,
                cfInput: (document.querySelector('input[name="cf-turnstile-response"]') || {}).value || '',
                holder: document.getElementById('cf-turnstile-holder') ? document.getElementById('cf-turnstile-holder').innerHTML.substring(0, 200) : 'no holder',
            };
        }""")
        print(f"[{time.strftime('%H:%M:%S')}] Debug: {debug}")

        # 嘗試點擊 Turnstile checkbox（有些 managed mode 需要互動）
        try:
            turnstile_frame = page.frame_locator("iframe[src*='challenges.cloudflare.com']")
            checkbox = turnstile_frame.locator("input[type='checkbox'], .cb-lb, body")
            if await checkbox.count() > 0:
                await checkbox.first.click(timeout=5000)
                print(f"[{time.strftime('%H:%M:%S')}] Clicked turnstile checkbox")
                await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] No clickable turnstile element: {e}")

        print(f"[{time.strftime('%H:%M:%S')}] ✅ Turnstile page loaded, starting token loop...")

        print(f"[{time.strftime('%H:%M:%S')}] ✅ Turnstile page loaded, starting token loop...")

        msg_count = 0
        while True:
            try:
                # 等待 token 出現（最多 60 秒）
                token = await wait_for_token(page, timeout=60)

                if token:
                    # 取到 token，馬上發留言
                    success = send_message(token)
                    msg_count += 1
                    if success:
                        print(f"[{time.strftime('%H:%M:%S')}] ✅ Total sent: {msg_count}")

                    # 重置 Turnstile 取下一個 token
                    await page.evaluate("""() => {
                        document.getElementById('token').value = '';
                        if (window.turnstile) {
                            try { window.turnstile.reset(); } catch(e) {}
                        }
                    }""")
                    await page.wait_for_timeout(2000)
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] ⏳ No token, reloading page...")
                    await page.goto(SITE_URL, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(10000)

            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] MSG loop error: {e}")
                try:
                    await page.goto(SITE_URL, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(10000)
                except Exception:
                    pass
                await asyncio.sleep(5)


async def wait_for_token(page, timeout=30):
    """等待 Turnstile token 出現，最多等 timeout 秒"""
    for i in range(timeout):
        token = await page.evaluate("""() => {
            // 方法1: 我們自己的 hidden input（callback 寫入）
            const el = document.getElementById('token');
            if (el && el.value && el.value.length > 0) return el.value;

            // 方法2: Turnstile 標準 input
            const input = document.querySelector('input[name="cf-turnstile-response"]');
            if (input && input.value && input.value.length > 0) return input.value;

            // 方法3: turnstile API
            if (window.turnstile) {
                try {
                    const resp = window.turnstile.getResponse();
                    if (resp) return resp;
                } catch(e) {}
            }

            return null;
        }""")
        if token:
            print(f"[{time.strftime('%H:%M:%S')}] 🎫 Got token ({i+1}s): {token[:30]}...")
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
    """每秒對所有留言都按讚（並行發送）"""
    async with aiohttp.ClientSession() as session:
        while True:
            # 對所有 msg_id 同時發送按讚請求
            tasks = []
            for msg_id in LIKE_MSG_IDS:
                tasks.append(_like_one(session, msg_id))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, Exception):
                    print(f"[{time.strftime('%H:%M:%S')}] LIKE Error: {r}")
            await asyncio.sleep(0.5)


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
    print("🚀 啟動非同步排程...")
    print("  - 留言：持續取 token，取到即發")
    print(f"  - 按讚：每秒對 {len(LIKE_MSG_IDS)} 則留言同時按讚")
    print("按 Ctrl+C 停止\n")

    # 同時跑留言和按讚
    await asyncio.gather(
        message_loop(),
        like_loop(),
    )


if __name__ == "__main__":
    asyncio.run(main())
