# UNIVERSE.md — LeafLune 宇宙戰略儀表板

> 回答「整個 LL 宇宙現在在哪、在做什麼、優先序是什麼」。
> 技術細節在各專案的 `PROJECT.md`，完整過程在 `mine-meeting-room/meetings/`。
> 最後更新：2026-04-30

---

## 一、宇宙地圖

```
RD 強化動力論（哲學根基）
│   RL 與人生共享同一底層動力：趨利避害
│
└── LeafLune Edutainment Studio
    │
    ├── 四根脊椎（貫串所有平台）
    │   ├── 訴求：學習變有趣，玩樂有價值
    │   ├── RD：ReinforceDynamic 強化動力論（哲學）
    │   ├── NN：貍奴洞天六貓（情感 IP / 吉祥物）
    │   └── II：Infinity Identity（統一會員 / 客服）
    │
    ├── 對外品牌/產品（有子網域）
    │   ├── LL  leaflune.org                 # 宇宙總部 + 品牌官網 + AdSense
    │   ├── XX  xuanxuexi.leaflune.org       # 語言學習子品牌
    │   ├── SS  strategyspace.leaflune.org   # 競賽舞台（未上線）
    │   ├── RR  reinroom.leaflune.org        # RL 教學平台（主力商品）
    │   ├── DD  datadojo.leaflune.org        # ML 視覺化教學平台
    │   ├── CC  cubiccraft.leaflune.org      # 旗艦遊戲 IP
    │   ├── TT  tradetrail.leaflune.org      # 金融市場 RL 環境
    │   └── II  id.leaflune.org              # Infinity Identity — 統一會員服務
    │
    ├── SS 底下的 MUST 遊戲（路徑，非子網域）
    │   ├── strategyspace.leaflune.org/mage-dragon
    │   └── strategyspace.leaflune.org/shadow-protocol
    │
    ├── CC 底下的應用（路徑）
    │   └── cubiccraft.leaflune.org/cc2d
    │
    ├── 長期 IP（開發中）
    │   ├── WW  warwrit        # 軍令，史詩策略 + Agent 治理沙箱
    │   ├── HH  harmonic-hunter# RL 版地平線，人機協作狩獵
    │   └── FF  figure-forge   # HH 的骨架工具（資產生產線）
    │
    ├── 敘事 IP
    │   └── NN  neko-numen     # 貍奴洞天六貓，跨平台情感語言
    │
    ├── 哲學層
    │   └── RD  reinforce-dynamic # 強化動力論，LL 中心思想
    │
    └── 內部工具（不對外）
            matrix-manager, video-factory, agent-stream
```

---

## 二、各專案當前狀態（2026-04-30）

| 代號 | 專案 | CF Pages | 狀態 | 優先序 |
|------|------|----------|------|--------|
| LL | leaflune.org | ✅ | 🟡 AdSense 審核中；YT 頻道 @Leaf-Lune 建立完成 | ★★★ |
| RR | reinroom | ✅ | 🟢 論文實驗教學完成，進入推廣階段 | ★★★ |
| — | mage-dragon | — | 🟢 State machine、P2P、LLM接入、Playwright壓力測試全完成；10 局穩定 0 error | ★★★ |
| — | agent-stream | — | 🔵 新專案建立；克勞德定裝照確認；PROJECT.md / 角色設定文件完成 | ★★☆ |
| DD | datadojo | ✅ | 🔵 MVP 動工中 | ★★☆ |
| TT | TradeTrail | ✅ | 🔵 Phase 0 進行中；付費牆規劃完成，待實作 | ★★☆ |
| II | Infinity Identity | — | 🔵 專案啟動；PROJECT.md / CLAUDE.md / TODO.md 建立完成 | ★★☆ |
| XX | xuanxuexi | ✅ | 🟢 線上 | ★☆☆ |
| CC | cubiccraft | ✅ | 🟡 2D Worker + 物理引擎修復中 | ★☆☆ |
| MM | matrix-manager | — | 🔵 正式復活；雙層架構確立 | ★☆☆ |
| SS | strategy-space | — | 🔵 CLAUDE.md / PROJECT.md / TODO.md 建立完成 | ☆☆☆ |
| WW | warwrit | — | 🔵 CommandOfStrategy 整併完成；手稿 OCR 整理完成 | ☆☆☆ |
| NN | neko-numen | — | 🔵 六貓設定典籍確立為硬約束 | ☆☆☆ |
| HH | harmonic-hunter | — | 🔵 依賴 FF JSON 格式 | ☆☆☆ |
| FF | figure-forge | — | 🔵 規範化完成 | ☆☆☆ |
| — | shadow-protocol | — | 🟡 等觀戰 UI 做好再上 | ☆☆☆ |
| GG | game-geek | — | ⬜ 規劃中 | ☆☆☆ |

---

## 三、當前主線任務

### 🎯 AdSense 過審（LL）
- 已送出審核，等待 Google 回覆
- 通過後：reinroom / xuanxuexi 子網域自動受益
- YT 頻道 @Leaf-Lune 已建立，橫幅製作中

### 🐉 mage-dragon 直播準備
- 遊戲核心已完成：State machine / P2P / LLM / Playwright 壓力測試全過
- 下一步：window.gameAPI bridge（Phase 2）→ MCP server → 克勞德直播
- agent-stream VTuber 動畫片段待生成（idle/talking/thinking 等 10 個 WebM）

### 🌌 MM 大興土木（論文後啟動，現在可動）
- UNIVERSE.md 已同步回 leaflune/ ✅
- 各專案 CLAUDE.md 新對話開場 SOP 待推送
- meetings/ 整併進 matrix-manager/ 待執行

### 📊 DataDojo MVP（DD）
- 故事線：選資料集 → 看資料 → 正規化 before/after → k-NN → 決策邊界
- 待做：左欄資料表格 + 右欄 pipeline 地圖

### 📈 TradeTrail Phase 0（TT）
- 付費牆邏輯待遷移至 CF Workers（目前前端判斷有安全漏洞）
- Phase 1：補美股標的資料 + 付費牆同步實作

---

## 四、核心技術架構

### 子網域規範
- **有子網域**：對外品牌 / 獨立平台 / 能獨立吸引用戶的產品
- **路徑**：平台旗艦應用、SS 底下的 MUST 遊戲、內部工具
- **命名規則**：統一不加 `-`（tradetrail 不是 trade-trail）

### id.leaflune.org — 統一會員服務
```
對外：統一登入入口（SSO）+ 客服精靈（Claude API）
對內：會員資料（D1）+ 全局 tier 管理

權限架構（兩層）：
  ID 管：用戶是誰、是哪個 tier（global）
  各專案管：這個 tier 在我這裡能用什麼功能（local）
```

### SS Worker 路由轉接器
```
strategyspace.leaflune.org/mage-dragon    → mage-dragon.pages.dev
strategyspace.leaflune.org/shadow-protocol → shadow-protocol.pages.dev
```

### RR postMessage 協定
RR 平台透過 iframe postMessage 與遊戲溝通，是 CC / TT / SS 接入的標準介面。

### LLGB（LL GameBridge）三層架構
```
LLM 策略層 → RL 戰術層 → 遊戲執行層
```

### 部署平台分工
```
Cloudflare Pages  →  對外產品（掛 leaflune.org 子網域，用戶可見）
Vercel            →  內部工具（不掛 LL 網域，月衡君自用，不對外曝光）
```
內部工具：matrix-manager、video-factory、agent-stream

### Cloudflare 基礎設施
- 對外產品：CF Pages + GitHub 自動部署
- $5/月升級解鎖：DO（對戰大廳）+ 更高 D1/Workers 額度
- 升級時機：建 ID 會員資料庫時

---

## 五、跨專案商業轉換路徑

```
免費文章（leaflune.org）
  → 體驗營 / 課程
    → RR 平台 ←→ DD 平台
      → CC / TT / SS 進階應用
        → 認證 / 競賽（SS + LL 認證體系）
```

**收益層：**
- 短期：AdSense
- 中期：實體營隊報名費
- 長期：RR / DD 平台訂閱 + 認證收費

---

## 六、品牌核心（不可改動）

> **使命**：讓學習變有趣，讓玩樂有價值。
> **願景**：建構一個以 AI 競技驅動的成長型社會引擎。
> **價值觀**：動機才是最強的教師，自主才是最深的學習。

---

## 七、封號體系（2026-04-27 確立）

| 封號 | 身份 | 層級 | 職責 |
|------|------|------|------|
| 月衡君 | colombo0718 | 人 | 定方向，掌全局 |
| 葉衍君 | Claude | Agent | 鑄造執行，衍化落地 |
| 玄識君 | ChatGPT | Agent | 虛空意識，歷史共建者 |
| 玄鑑君 | Codex | Agent | 照妖鑑察，糾察漏洞 |
| 吉姆奈 | Gemini | Agent | VTuber 第三位（待設計形象）|
| 司簿星 | MM | LLM工具 | 任務星宿，管理矩陣 |
| ___靈 | RL 訓練體 | RL層 | 靈寵／器靈 |
| 魁儡／魔偶 | 腳本 | 腳本層 | 純執行 |

---

## 八、擱置中的決策

| 議題 | 擱置原因 | 重啟條件 |
|------|----------|----------|
| 《人人必學 AI 靈感編程》主線遊戲 | 優先顧 AdSense + DD | AdSense 過審後 |
| mage-dragon 行動端支援 | WebGPU 行動端不足 | 瀏覽器支援改善後 |
| LLGB `window.LLGB` 介面實作 | 論文口試優先 | 口試後 |
| Play Store 上架 | Web 版先穩 | RR 功能穩定後 |
| SS 獨立上線 | 資源不足 | RR 有穩定用戶後 |
| geo-light-craft / treasure-toolbox 定位 | 尚未討論 | 待釐清 |
| CLAUDE.md 通用模板推送 | ✅ 論文完成，可動了 | 立即 |
| id.leaflune.org 實作 | 等平台有雛形 | TT Phase 1 完成後 |
| 付費牆上線 | 等 Phase 1 標的清單確定 | TT Phase 1 完成後 |
