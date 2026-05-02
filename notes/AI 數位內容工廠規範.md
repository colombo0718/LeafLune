# AI 數位內容工廠規範 
LeafLune AI 數位內容工廠規範（草案 v1.0）

---

## 0. 核心精神

LeafLune 的所有專案（卡牌、桌遊、網頁 App、RL 平台…）都遵守同一套原則：

> **「把專案拆成多個小工班，用檔案當接力棒，每一棒只做一件事。」**

- 橫向：不同程式 / 工具 **分工明確**。
- 縱向：每一階段輸入 / 輸出 **模組化**，未來可被 agent 或其他工具替換。
- 目標：  
  - 人類（我）不會被一支 3000 行的程式壓垮。  
  - AI（ChatGPT / 其他 LLM）在協助修改時，也不會顧此失彼。  

---

## 1. 檔案與模組顆粒度原則

### 1.1 1000 行上限原則

- 一個程式檔案 **建議上限約 800–1000 行**：
  - 超過 800 行 → 優先思考是否可拆模組。
  - 超過 1000 行 → 幾乎可以確定混了兩種以上責任，應拆檔。

### 1.2 「一檔一職責」原則

- 每個檔案要能用 **一句話描述它的工作**，例：
  - ✅ `pinyinDeck_ds.js`：定義 Pinyin Poker 64 的卡牌內容資料。
  - ✅ `pinyinCardLayout.html`：專心設計「單張卡面」的畫面與排版。
  - ✅ `pinyinPoker64_render.html`：讀 deck + layout，畫出 64 張卡牌並匯出 PNG。
  - ❌ 一個檔案同時：
    - 定義卡片資料
    - 設計卡片 Layout
    - 產生 64 張卡 + 排版 A4 + 匯出 PDF

### 1.3 接力棒 = 檔案

- 每一棒程式的輸入 / 輸出都要清楚：
  - `*.js`：資料定義（deck、config、清單）。
  - `cards_png/*.png`：已完成的單張卡牌素材。
  - `*_A4_color.pdf`：已排版好的列印版。
  - `*.zip`：最終上架包。
- 設計時先畫出「檔案流」，再落實到程式。

---

## 2. 人類與 AI 的分工

### 2.1 人類負責的部分

- 決策與品管：
  - 決定產品定位、價值、受眾。
  - 決定工作流顆粒度、每一棒的邊界。
  - 檢查最終輸出（卡面、PDF、說明文件）是否符合標準。
- 少量但關鍵的手工調整：
  - emoji / icon 選擇。
  - 字體大小、版面細節。
  - 最終商品定價、商品頁文案微調。

### 2.2 AI / Agent 未來要負責的部分

- 重複性高、規則清楚的工作：
  - 依輸入 `deck.js` 生成 HTML / JS 模板。
  - 批次調整 CSS / Canvas 畫法。
  - 自動產生 README 草稿、授權檔案模板。
- 長期目標：
  - 每一棒都有對應的「AI 工班」，根據 SOP 自動執行。

---

## 3. LeafLune 卡牌工作流範式

以 **Pinyin Poker 64** 為範例，定義「一整條健康的工作流」：

### 3.1 內容規劃階段

1. **Deck 資料檔（正本）**  
   - 檔名：`pinyinDeck_ds.js`（未來可改 `pinyinPoker64_deck.js`）
   - 結構：  
     - `suits`：花色資訊  
     - `cards`：每張卡的 `id, suit, hex/rank, pinyin, hanzi, emoji, tone, ...`
   - 原則：
     - ❌ 不負責畫面。
     - ✅ 專心把「這副牌要教什麼」說清楚。

### 3.2 視覺設計階段

2. **單張卡面 Layout 工具**  
   - 檔名範例：`pinyinCardLayout.html`
   - 功能：
     - 設定卡片尺寸、圓角、邊框。
     - 定義：角標 / 中央 / 底部 的區塊位置。
     - 測試用假資料（不用全部 64 張）。
   - 產出：
     - 一組可重用的 `drawCard(ctx, card)` 函式。

3. **整副卡牌預覽 & PNG 匯出**  
   - 檔名：`pinyinPoker64_render.html`
   - 輸入：
     - `pinyinDeck_ds.js`（內容）
     - `drawCard`（Layout）
   - 功能：
     - 畫出 64 張卡片（Grid 排列，方便人工檢查）。
     - 一鍵匯出 64 張 PNG：`PinyinPoker_L0.png ... PinyinPoker_WF.png`
   - 輸出：
     - `cards_png/` 資料夾。

### 3.3 列印與封裝階段

4. **A4 排版 / PDF 生成器**  
   - 檔名：`pinyinPoker_sheets.html` 或獨立工具（可重用到其他牌組）
   - 輸入：
     - `cards_png/*.png`
   - 功能：
     - 依規格把 8 張牌排成一張 A4（2x4 或 3x3）。
     - 一鍵匯出 `PinyinPoker_A4_color.pdf`（必要時再出背面版）。
   - 原則：
     - 對卡片「內容」一無所知，只管排版。

5. **文件與打包**  
   - `docs/README-zh.md` / `README-en.md`：玩法、印法、用途。
   - 授權：
     - `OpenMoji-License.txt`、其他 emoji 庫 license。
   - `version.txt`：版本與作者。
   - 最終壓縮：
     - `PinyinPoker64_v1.0_LeafLune.zip`

---

## 4. Workflow 設計準則（通用於所有專案）

### 4.1 可重用優先

- 儘量把程式分成：
  - **內容無關**的模組（例如：A4 排版器、PDF 生成器）。
  - **風格無關**的模組（例如：讀 deck、管理 state、RL 任務規則）。
- 目標：  
  - 換一副卡，只是換 deck + 少量 CSS，不用重寫整條管線。

### 4.2 不在一檔裡塞滿所有步驟

- 一支程式同時：
  - 讀資料 → 畫畫面 → 匯出 PNG → 排成 A4 → 匯出 PDF  
  → 這種會被判定為「**不健康工作流**」。
- 每一棒的入口 / 出口盡量是 **明確的檔案或資料格式**。

### 4.3 優先考慮「未來要怎麼交棒給 agent」

設計每一棒時先問自己：

1. 這一棒的輸入是什麼檔案 / JSON？
2. 這一棒的輸出是什麼檔案 / JSON？
3. 若未來交給 agent，自動跑時：
   - 是否不需要人類互動？
   - 是否錯了也能在下一版修正？

---

## 5. 命名與資料夾規範（草案）

以卡牌專案為例：

```text
PinyinPoker64_v1.0/
├─ src/                 # 原始程式（可不對外）
│  ├─ pinyinDeck_ds.js
│  ├─ pinyinCardLayout.html
│  ├─ pinyinPoker64_render.html
│  └─ pinyinPoker_sheets.html
├─ cards_png/           # 對外：單張卡牌素材
├─ printable_pdf/       # 對外：列印版 PDF
├─ web_demo/            # 可選：網頁 demo 版本
├─ docs/                # README & 授權
│  ├─ README-zh.md
│  ├─ README-en.md
│  ├─ OpenMoji-License.txt
│  └─ ...
└─ version.txt
```

未來其他產品（HSK 戰鬥卡、Crazy Cat、RL Lab 任務卡…）可以類似：

- `ProductName_vX.Y/` 為根目錄。
- `src/` 不一定要公開；`cards_png/`、`printable_pdf/`、`docs/` 為對用戶重要的輸出。

---

## 6. 未來延伸

- 建立共用的：
  - `LeafLune_Icon_Policy.md`（統一 emoji / icon 來源與授權寫法）
  - `LeafLune_Card_Product_Spec.md`（已存在，可持續更新）
- 把每一條工作流都畫成：
  - mermaid flowchart  
  - 或簡單的步驟表（Step 1–5）
- 之後接上：
  - Groq / OpenAI / 其他 LLM agent  
  - 讓「每一棒」都可以被自動化執行。

---

（本檔為草案，可隨 Pinyin Poker 與後續專案實作狀況逐版修正。）
