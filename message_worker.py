"""
本地留言 Worker — 直接操作真實網站頁面，讓 Turnstile 自然通過。
會彈出 Chrome 視窗，不要關掉它。

用法:
  source venv/bin/activate
  python message_worker.py
"""
import asyncio
import random
import time

from playwright.async_api import async_playwright


# === 設定 ===
SITE_URL = "https://idolcamp.muniverse.io"

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
    ]
    cn_prefixes = ["小", "大", "阿", "可愛的", "快樂", "幸福", "追星", "愛", "超級", "夢幻"]
    cn_names = [
        "兔子", "狐狸", "貓咪", "小鹿", "蝴蝶", "海豚", "熊貓",
        "櫻花", "向日葵", "玫瑰", "百合", "星辰", "月亮", "彩虹",
        "糖果", "奶茶", "布丁", "草莓", "珍珠", "水晶",
    ]
    cn_suffixes = ["醬", "寶", "兒", "妹", "控", "迷", "粉", "啊", "呀", "喵"]

    num = random.randint(0, 999)
    num2 = random.randint(10, 99)

    if strategy <= 3:
        return f"{random.choice(first_names)}_{random.choice(nouns)}{num2}"
    elif strategy <= 6:
        return f"{random.choice(adjectives).capitalize()}{random.choice(nouns).capitalize()}_{num}"
    elif strategy <= 9:
        return f"{random.choice(first_names)}.{random.choice(adjectives)}{num2}"
    elif strategy <= 12:
        return f"{random.choice(cn_prefixes)}{random.choice(cn_names)}{random.choice(cn_suffixes)}"
    else:
        return f"{random.choice(first_names)}_{random.choice(cn_prefixes)}{random.choice(cn_names)}{num2}"


async def main():
    print("=" * 50)
    print("🚀 本地留言 Worker")
    print("   直接操作真實網站，Turnstile 自然通過")
    print("   瀏覽器會彈出來，不要關掉！")
    print("   按 Ctrl+C 停止")
    print("=" * 50)
    print()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()

        # 反偵測
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            window.chrome = { runtime: {} };
        """)

        msg_count = 0

        while True:
            try:
                nickname = generate_nickname()
                message = random.choice(MESSAGES)

                print(f"[{time.strftime('%H:%M:%S')}] 🌐 載入頁面...")
                await page.goto(SITE_URL, wait_until="load", timeout=60000)
                
                # 等待 #nick 出現
                print(f"[{time.strftime('%H:%M:%S')}] ⏳ 等待表單載入...")
                try:
                    await page.wait_for_selector('#nick', timeout=30000)
                except Exception:
                    # 截圖看看頁面狀態
                    await page.screenshot(path="debug_page.png")
                    page_info = await page.evaluate("""() => ({
                        url: location.href,
                        title: document.title,
                        bodyLen: document.body ? document.body.innerHTML.length : 0,
                        bodySnippet: document.body ? document.body.innerText.substring(0, 300) : ''
                    })""")
                    print(f"[{time.strftime('%H:%M:%S')}] ❌ #nick 未出現，截圖存到 debug_page.png")
                    print(f"    {page_info}")
                    await page.wait_for_timeout(10000)
                    continue

                await page.wait_for_timeout(2000)
                print(f"[{time.strftime('%H:%M:%S')}] ✅ 表單已載入")

                # 選 team: flareu（用 JS 直接操作）
                print(f"[{time.strftime('%H:%M:%S')}] 📝 填寫表單: {nickname} / {message}")
                
                await page.evaluate("""() => {
                    const radios = document.querySelectorAll('input[name="team"]');
                    for (const r of radios) {
                        if (r.value === 'flareu') {
                            r.click();
                            r.dispatchEvent(new Event('change', {bubbles: true}));
                            return;
                        }
                    }
                    // fallback: click label
                    const labels = document.querySelectorAll('.team');
                    for (const l of labels) {
                        if (l.textContent.includes('FLARE U')) { l.click(); return; }
                    }
                }""")

                await page.wait_for_timeout(500)

                # 用 JS 填暱稱和留言（不依賴元素可見性）
                await page.evaluate(f"""() => {{
                    const nick = document.getElementById('nick');
                    const msg = document.getElementById('msg');
                    if (nick) {{
                        nick.value = '{nickname}';
                        nick.dispatchEvent(new Event('input', {{bubbles: true}}));
                    }}
                    if (msg) {{
                        msg.value = `{message}`;
                        msg.dispatchEvent(new Event('input', {{bubbles: true}}));
                    }}
                }}""")
                await page.wait_for_timeout(300)

                # 等待 Turnstile 完成（最多 60 秒）
                print(f"[{time.strftime('%H:%M:%S')}] ⏳ 等待 Turnstile 驗證...")
                token_ready = False
                for i in range(60):
                    has_token = await page.evaluate("""() => {
                        if (window.turnstile && window.__turnstileWidgetId != null) {
                            const r = window.turnstile.getResponse(window.__turnstileWidgetId);
                            if (r && r.length > 0) return true;
                        }
                        const input = document.querySelector('input[name="cf-turnstile-response"]');
                        if (input && input.value && input.value.length > 0) return true;
                        return false;
                    }""")
                    if has_token:
                        token_ready = True
                        print(f"[{time.strftime('%H:%M:%S')}] 🎫 Turnstile 通過！({i+1}s)")
                        break
                    if i % 10 == 9:
                        print(f"[{time.strftime('%H:%M:%S')}] ⏳ 仍在等待... ({i+1}s)")
                    await asyncio.sleep(1)

                if not token_ready:
                    print(f"[{time.strftime('%H:%M:%S')}] ❌ Turnstile 超時，重試...")
                    await page.wait_for_timeout(5000)
                    continue

                # 點擊發行按鈕
                issue_btn = page.locator('#issueBtn')
                if not await issue_btn.is_disabled():
                    await issue_btn.click()
                    msg_count += 1
                    print(f"[{time.strftime('%H:%M:%S')}] ✅ 已送出！Total: {msg_count}")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] ⚠️ 按鈕還是 disabled，嘗試 JS 點擊...")
                    await page.evaluate("() => { document.getElementById('issueBtn').click(); }")
                    msg_count += 1
                    print(f"[{time.strftime('%H:%M:%S')}] ✅ JS 點擊送出！Total: {msg_count}")

                # 等待處理完成
                await page.wait_for_timeout(3000)

                # 等一下再下一輪（避免被 rate limit）
                wait_time = random.uniform(3, 6)
                print(f"[{time.strftime('%H:%M:%S')}] 💤 等待 {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)

            except KeyboardInterrupt:
                print(f"\n[{time.strftime('%H:%M:%S')}] 停止，共送出 {msg_count} 則")
                break
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] ❌ Error: {e}")
                await asyncio.sleep(10)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
