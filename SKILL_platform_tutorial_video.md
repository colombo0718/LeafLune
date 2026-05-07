# Skill: Web Platform Tutorial Video Production

**適用場景：** 對任何網頁平台錄製教學示範影片。Agent 閱讀本文件後，即可獨立為一個新的網頁平台建立完整的影片製作流程。

---

## 兩種影片類型的分野

| 類型 | 視覺素材 | 難度 | 本文件涵蓋 |
|------|---------|------|-----------|
| **念稿報告型** | 靜態投影片 PNG（Gamma 生成） | 低 | ✗ 見 `rl-basics/SOP_rl_basics_video.md` |
| **平台教學型** | Playwright 即時錄製網頁 | 高 | ✓ 本文件 |

「平台教學型」難度較高的原因：
- 畫面是動態的（動畫、圖表、程式執行輸出）
- 旁白時間必須與畫面事件精確對齊
- 若平台有 iframe、動態元素、非同步執行，selector 操作複雜度高

---

## 核心架構

```
make_XX.py          ← 入口（每支影片一個）
    ↓
video_pipeline.run_pipeline()   ← 共用流程（thesis-video-factory/video_pipeline.py）
    ├─ Step 1: edge-tts → 每個 scene 合成 MP3，量測秒數
    ├─ Step 2: set_scene_timings() → record_XX.main()  ← Playwright 錄製
    ├─ Step 3: ffmpeg mix audio（依 timing_log 的 start_ms 對齊音軌）
    └─ Step 4: ffmpeg 生成 .srt → 燒入字幕
```

**輸出物：**
- `final/XX-{timestamp}-nosub.mp4` — 無字幕版
- `final/XX-{timestamp}.srt` — 字幕檔
- `final/XX-{timestamp}.mp4` — 字幕燒入版（正式成品）

---

## 必要檔案清單

為一個新平台建立影片，需要建立以下 4 個檔案：

```
{platform}/
├── make_XX.py              # 入口腳本
├── narration_XX.json       # 旁白腳本（TTS 文字 + 語音設定）
└── scripts/
    ├── record_XX.py        # Playwright 錄製腳本（最複雜）
    └── demo_overlay.js     # 視覺標注層（可複用現有版本）
```

---

## Step 0 — 前置作業：分鏡腳本

錄製前先確認每個 scene 要展示什麼，規劃對應的口說旁白。

```markdown
# 分鏡腳本 storyboard_XX.md

| Scene ID | 畫面動作 | 旁白摘要 | 預估秒數 |
|---|---|---|---|
| s01_open | 打開平台首頁，指向目標按鈕 | "This is the main dashboard..." | ~5s |
| s02_params | 指向參數滑桿 | "These three sliders control..." | ~6s |
| s03_run | 按下 Start，等待執行完成 | "Press Start and watch..." | ~8s |
| s04_result | 高亮輸出圖表 | "The curve shows..." | ~5s |
| s05_task | 回到設定區，說明任務 | "Your task: try..." | ~4s |
```

---

## Step 1 — 建立 narration_XX.json

```json
{
  "voice": "en-US-JennyNeural",
  "rate": "-5%",
  "lead_in": 0.3,
  "lead_out": 0.5,
  "scenes": [
    {
      "id": "scene_01_open",
      "text": "This is the main dashboard. You'll see five environments on the left panel."
    },
    {
      "id": "scene_02_params",
      "text": "These three sliders control epsilon, learning rate, and discount factor."
    },
    {
      "id": "scene_03_run",
      "text": "Press Start and watch the agent begin learning in real time."
    },
    {
      "id": "scene_04_result",
      "text": "The reward curve on the right shows how the agent's performance improves over episodes."
    },
    {
      "id": "scene_05_task",
      "text": "Your task: try epsilon equals 0.9 and 0.1. Describe the difference you observe."
    }
  ]
}
```

**語音選項：**
- `en-US-JennyNeural` — 女聲，清晰，適合教學
- `en-US-AriaNeural` — 女聲，語氣偏自然
- `en-US-GuyNeural` — 男聲

**`rate`：** `-5%` 略慢於正常語速，教學場景建議值。

---

## Step 2 — 建立 make_XX.py

```python
"""
make_XX.py — XX Demo 製作腳本

執行：
  cd c:\\Users\\USER\\thesis-video-factory
  py -3 -X utf8 {platform}/make_XX.py

重用已有音檔（只重錄畫面）：
  py -3 -X utf8 {platform}/make_XX.py {platform}/audio/XX-20260418-123456
"""

from __future__ import annotations
import asyncio, sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from video_pipeline import run_pipeline
from {platform}.scripts import record_XX
from config import FFMPEG, FFPROBE

# narration scene id  →  record script 的 wait_id
# 兩邊的 id 不一定相同，這個表做對應
NARR_TO_WAIT = {
    "scene_01_open":    "s01_open",
    "scene_02_params":  "s02_params",
    "scene_03_run":     "s03_run",
    "scene_04_result":  "s04_result",
    "scene_05_task":    "s05_task",
}

_HERE = Path(__file__).resolve().parent

async def main(reuse: str | None = None) -> None:
    await run_pipeline(
        narration_path  = _HERE / "narration_XX.json",
        narr_to_wait    = NARR_TO_WAIT,
        record_fn       = record_XX.main,
        set_timings_fn  = record_XX.set_scene_timings,
        final_dir       = _HERE / "final",
        audio_dir       = _HERE / "audio",
        output_prefix   = "XX",
        reuse_audio_dir = Path(reuse) if reuse else None,
        ffmpeg          = FFMPEG,
        ffprobe         = FFPROBE,
    )

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else None))
```

---

## Step 3 — 建立 record_XX.py（最複雜的一步）

### 3.1 骨架結構

```python
"""record_XX.py — XX Demo 錄製腳本"""

from __future__ import annotations
import asyncio, subprocess, time
from datetime import datetime
from pathlib import Path

import sys
_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))
from config import FFMPEG

OVERLAY_JS  = Path(__file__).resolve().parent / "demo_overlay.js"
FINAL_DIR   = Path(__file__).resolve().parent.parent / "final"
PLATFORM_URL = "https://your-platform.example.com"
VIEWPORT    = {"width": 1920, "height": 1080}

# ── timing 注入 ───────────────────────────────────────────────────────────────
_SCENE_WAIT: dict[str, int] = {}
_timing_log: list[dict]     = []
_t0: float                  = 0.0

def set_scene_timings(d: dict[str, int]) -> None:
    global _SCENE_WAIT
    _SCENE_WAIT = d

def _w(scene_id: str, default_ms: int) -> int:
    return _SCENE_WAIT.get(scene_id, default_ms)

def _log(scene_id: str, dur_ms: int) -> None:
    if _t0:
        start_ms = int((time.perf_counter() - _t0) * 1000)
        _timing_log.append({"id": scene_id, "start_ms": start_ms, "dur_ms": dur_ms})

def _remain(total_ms: int, used_ms: int, min_ms: int = 900) -> int:
    return max(min_ms, total_ms - used_ms)
```

### 3.2 overlay 輔助函式

注入 `demo_overlay.js` 後，可在 Playwright 中使用以下 API：

```python
# 注入 overlay（頁面載入後執行一次）
async def inject_overlay(page) -> None:
    await page.evaluate(OVERLAY_JS.read_text(encoding="utf-8"))

# 顯示游標指向 CSS selector 的元素
async def ptr(page, selector: str, label: str = "", wait_ms: int = 1800) -> None:
    el = await page.query_selector(selector)
    if not el:
        return
    box = await el.bounding_box()
    await page.evaluate(
        "([x, y, label]) => demoOverlay.pointer(x, y, label)",
        [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, label],
    )
    await page.wait_for_timeout(wait_ms)

# 顯示紅框高亮某元素
async def focus(page, selector: str, label: str = "", wait_ms: int = 3000) -> None:
    await page.evaluate(f"demoOverlay.focusElement({selector!r}, {label!r});")
    await page.wait_for_timeout(wait_ms)

# 清除所有標注
async def clear(page) -> None:
    await page.evaluate("demoOverlay.clear();")
    await page.wait_for_timeout(250)
```

**⚠️ iframe 內的元素需特殊處理：**
```python
async def ptr_iframe(page, iframe_selector: str, inner_selector: str, label: str = "") -> None:
    """計算 iframe 內元素的絕對座標後再呼叫 demoOverlay.pointer"""
    rect = await page.evaluate("""
        ([iframeSelector, innerSelector]) => {
            const iframe = document.querySelector(iframeSelector);
            if (!iframe) return null;
            const el = iframe.contentDocument.querySelector(innerSelector);
            if (!el) return null;
            const ir = iframe.getBoundingClientRect();
            const r  = el.getBoundingClientRect();
            return { x: ir.left + r.left + r.width/2, y: ir.top + r.top + r.height/2 };
        }
    """, [iframe_selector, inner_selector])
    if rect:
        await page.evaluate("([x, y, label]) => demoOverlay.pointer(x, y, label)",
                            [rect["x"], rect["y"], label])
```

### 3.3 Scene 函式模板

每個 scene 函式的標準結構：

```python
async def scene_01_open(page) -> None:
    print("  [Scene 1] 描述這個 scene 在做什麼")
    dur = _w("s01_open", 5000)   # default_ms = 分鏡腳本的預估秒數 * 1000
    _log("s01_open", dur)        # 必須在 scene 開始時立刻 log（記錄 start_ms）
    used = 0

    # 執行畫面操作
    await page.click("#some-button")
    used += 700

    await ptr(page, "#target-element", "Click here", wait_ms=1500)
    used += 1500

    # 最後用 _remain 填滿剩餘時間，確保 scene 總時長 = dur
    await focus(page, "#result-area", "Result", wait_ms=_remain(dur, used))
    await clear(page)
```

**關鍵規則：**
1. `_log(scene_id, dur)` 必須在 scene **開始時**立刻呼叫，才能記錄正確的 `start_ms`
2. `_remain()` 用於最後一個等待，確保 scene 總長不短於 `dur`
3. `await clear(page)` 在每個 scene 結束時清除標注

### 3.4 等待非同步操作的模式

```python
# 等待某個 DOM 元素出現
await page.wait_for_selector("#result-chart", timeout=30_000)

# 等待 JS 條件成立（例如訓練跑了 50 回合）
await page.wait_for_function(
    "window.trainingLog && window.trainingLog.length >= 50",
    timeout=60_000,
)

# 等待頁面 networkidle（初次載入）
await page.goto(URL, wait_until="networkidle", timeout=30_000)

# 等待 Jupyter kernel 閒置（B 系列用）
async def wait_idle(page, timeout_s: int = 120) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        busy = await page.evaluate("""
            (() => {
                const indicators = document.querySelectorAll(
                    '.kernel_busy_icon, [data-status="busy"]'
                );
                return indicators.length > 0;
            })()
        """)
        if not busy:
            return
        await page.wait_for_timeout(500)
```

### 3.5 main 函式骨架

```python
async def main() -> tuple[Path, list[dict]]:
    from playwright.async_api import async_playwright
    global _timing_log, _t0

    _timing_log = []
    overlay_js  = OVERLAY_JS.read_text(encoding="utf-8")
    timestamp   = datetime.now().strftime("%Y%m%d-%H%M%S")
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    webm_out = FINAL_DIR / f"XX-demo-{timestamp}.webm"
    mp4_out  = FINAL_DIR / f"XX-demo-{timestamp}.mp4"

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False,              # headless=False 才能觸發 canvas 動畫
            args=["--lang=en-US,en"],
        )
        ctx = await browser.new_context(
            viewport=VIEWPORT,
            locale="en-US",
            record_video_dir=str(FINAL_DIR),
            record_video_size=VIEWPORT,
        )
        page = await ctx.new_page()
        _t0 = time.perf_counter()

        await page.goto(PLATFORM_URL, wait_until="networkidle", timeout=30_000)
        await page.wait_for_timeout(2000)
        await inject_overlay(page)

        # 按分鏡順序執行所有 scene
        await scene_01_open(page)
        await scene_02_params(page)
        await scene_03_run(page)
        await scene_04_result(page)
        await scene_05_task(page)

        await ctx.close()

    # 找最新的 webm → 改名 → 轉 mp4
    webm_files = sorted(FINAL_DIR.glob("*.webm"), key=lambda p: p.stat().st_mtime)
    if webm_files:
        webm_files[-1].rename(webm_out)
        subprocess.run([
            FFMPEG, "-y", "-i", str(webm_out),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            str(mp4_out),
        ], check=True, capture_output=True, text=True, encoding="utf-8")
        print(f"✅ Raw video: {mp4_out.name}")
    else:
        mp4_out = None

    return mp4_out, _timing_log


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Step 4 — 複製 demo_overlay.js

從現有產線複製，無需修改：

```bash
# A 系列（RR 平台，含 iframe 支援）
cp rr/scripts/rr_demo_overlay.js {platform}/scripts/demo_overlay.js

# B 系列（Jupyter notebook）
cp colab/scripts/colab_demo_overlay.js {platform}/scripts/demo_overlay.js
```

**overlay API 速查：**

| 函式 | 效果 |
|------|------|
| `demoOverlay.pointer(x, y, label?)` | 顯示 👆 游標 + 文字標籤 |
| `demoOverlay.movePointer(x, y, label?, ms?)` | 緩動移動游標 |
| `demoOverlay.highlight(x, y, w, h, label?)` | 紅框高亮指定區域 |
| `demoOverlay.focusElement(selector, label?)` | 依 CSS selector 紅框 |
| `demoOverlay.caption(text)` | 底部字幕條 |
| `demoOverlay.clear()` | 清除所有標注 |

---

## 執行與迭代

### 首次完整執行
```bash
cd C:/Users/USER/thesis-video-factory
py -3 -X utf8 {platform}/make_XX.py
```

### 只重錄畫面（沿用已有音檔）
```bash
py -3 -X utf8 {platform}/make_XX.py {platform}/audio/XX-20260418-123456
```
適用場景：旁白滿意但畫面操作需要調整。

### 只調旁白（旁白→音檔→重錄）
直接修改 `narration_XX.json` 的 `text` 欄位後完整執行，舊音檔會被覆蓋。

---

## 常見問題排查

| 症狀 | 原因 | 解法 |
|------|------|------|
| 音軌比畫面早結束 | `default_ms` 設太短 | 在 scene 函式裡調高 `default_ms` 或增加 `_remain` 的 `min_ms` |
| 旁白念完畫面還沒出現 | 平台載入慢 | 在 scene 開頭加 `await page.wait_for_selector(...)` |
| `_log` 時間對不上 | `_log()` 呼叫位置錯誤 | 確保 `_log()` 在 scene **第一行**呼叫，操作前 |
| webm 轉 mp4 失敗 | ffmpeg 路徑錯誤 | 檢查 `config.py` 的 `FFMPEG` 路徑 |
| headless=True 下動畫不執行 | 瀏覽器 GPU 被禁用 | 保持 `headless=False`（或加 `--use-gl=swiftshader`） |
| iframe 內 selector 找不到 | iframe 跨 document 邊界 | 使用 `ptr_iframe()` 計算絕對座標，或 `page.frame_locator("#iframe-id").locator(...)` |
| Jupyter kernel 未跑完就截圖 | 未等待 idle | 在 `run_code_cell()` 後加 `await wait_idle(page, timeout_s=120)` |

---

## Slider 操作

許多平台有滑桿元素，直接用 JS 注入值最可靠（避免 drag 模擬偏差）：

```python
async def set_slider(page, slider_id: str, value: float) -> None:
    ok = await page.evaluate("""
        ([id, val]) => {
            const el = document.getElementById(id);
            if (!el) return false;
            el.value = String(val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
    """, [slider_id, value])
    if not ok:
        raise RuntimeError(f"slider not found: #{slider_id}")
    await page.wait_for_timeout(800)
```

---

## 相關檔案位置（本 repo）

```
thesis-video-factory/
├── video_pipeline.py           ← 共用流程（所有 make_XX.py 都 import 這裡）
├── config.py                   ← FFMPEG / FFPROBE 路徑
├── rr/                         ← A 系列（RR 平台）— 參考實作
│   ├── make_A1.py
│   ├── narration_A1.json
│   └── scripts/record_A1.py   ← 最完整的 record 範例（含 iframe 處理）
└── colab/                      ← B 系列（Jupyter notebook）— 參考實作
    ├── make_B1.py
    ├── narration_B1.json
    └── scripts/record_B1.py   ← Jupyter 專用（含 pre-patch notebook、wait_idle）
```
