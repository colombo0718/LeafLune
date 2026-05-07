# TODO.md — LeafLune 官網與宇宙建設

---

## 官網（index.html）

- [ ] 確認各品牌 CTA 按鈕連結目標（目前是否有實際頁面？）
  > 現在 hero 按鈕可能還是佔位符，確認連去哪

- [ ] RWD 手機版檢查：hero 的兩欄 grid 在小螢幕是否正確 fallback 成單欄

- [ ] privacy.html 連結確認在頁尾是否存在

---

## ReinRoom（RR）

- [ ] RR 平台 MVP 建置
  > 核心功能：Blockly + RL 引擎 + Matter.js 環境 + Q-table 視覺化
  > 需等 RL 引擎底層穩定後才能串接 Blockly UI

- [ ] 建立 `RR_Platform_Architecture_v1.md`（系統架構規格書）
  > 定義 RL 訓練資料傳遞方式、PolicyPackage `.pp` 格式

- [ ] GTM 第一階段：熟圈驗證 5~10 人
  > 先問場景，再展示 demo；不要一開始就丟網址

---

## 宣學習（XX）

- [ ] Pinyin Poker 64 完整工作流確認
  > pinyinDeck_ds.js → pinyinCardLayout.html → pinyinPoker64_render.html → PDF

- [ ] 上架打包：`PinyinPoker64_v1.0_LeafLune.zip`
  > 包含 cards_png/、printable_pdf/、docs/README-zh.md

---

## 全宇宙 docs/notes 資料夾重整

- [ ] 統一所有專案的子資料夾命名規則：
  - `docs/` = 硬約束（API 規格、架構圖、協定說明，改了會壞東西）
  - `notes/` = 軟敘述（想法、設定、世界觀、對話整理，改了沒關係）
- [x] neko-numen：`docs/` → `notes/`（現有內容全是設定筆記）
- [ ] warwrit：`docs/` → `notes/`（現有內容全是設定筆記）
- [ ] strategy-space：`docs/` 內三份文件移至 `notes/`（設計想法，非技術規格）
- [ ] 其他專案（RR、DD、TT、CC）逐一確認，按標準分類

---

## 宇宙文件（docs/）

- [ ] 建立 `LL_Protocol_SAR_v1.md`（State / Action / Reward 通訊協定總文件）
  > 供 GG ↔ 遊戲、RR ↔ 遊戲環境、SS ↔ 競技賽事共同參考

- [ ] 建立 `LL_Projects_Index_v1.md`（所有專案索引，掛在 HackMD `/LL/Projects/`）

- [ ] 補寫 `LL_RL_Philosophy_v1.md`（RL 人生觀系統）
  > 概念已在 MasterPlan 有大綱，需獨立成文

---

## 各專案分身同步（新對話開場 SOP）

- [ ] 將以下 SOP 加入所有專案的 `CLAUDE.md`（通用模板）
  > 每次新對話開始，Claude 分身依序執行：
  > 1. 讀 `PROJECT.md` — 確認自己專案現在在哪
  > 2. 讀 `C:/Users/USER/matrix-manager/UNIVERSE.md` — 確認 LL 宇宙當前狀態
  > 3. 搜尋 `C:/Users/USER/mine-meeting-room/meetings/` 最近 3 筆有自己專案名稱的會議紀錄
  > 4. 回報：「我已同步完畢，目前狀態是 ___，準備好了」
- [ ] 待 SOP 模板定稿後，逐一更新：leaflune / strategy-space / neko-numen / warwrit / harmonic-hunter / figure-forge / RR / DD
- [ ] 將「會議紀錄提醒」行為規則加入通用 CLAUDE.md 模板
  > 當對話超過約 15 則來回、或討論了架構決策/待辦變動，Claude 在回覆末尾主動提醒整理會議紀錄

---

## 系統層

- [ ] 建立 `matrix-manager/UNIVERSE.md`（LL 宇宙當前狀態快照）
  > 內容：各專案狀態、優先序、專案間依賴關係、當前開發重心
  > 這是新對話開場 SOP 的前提，要先填好才能推 SOP

- [ ] `leaflune/UNIVERSE.md` 改為轉址說明，指向 `matrix-manager/UNIVERSE.md`

- [ ] MatrixManager（MM）初版設計
  > 三大 UI 原則：人不碰底層 DB、畫面以人為本、UI 是跟 AI 說話的管道

- [ ] 司簿星（TaskTable）與 HackMD 整合規劃

---

## 擱置

- [ ] CubicCraft 前期任務規劃
  > 擱置原因：待 RR/GG MVP 完成後才進入
  > 需等 v2 宇宙建設階段啟動

- [ ] 玄機界域 SS 競技場上線
  > 擱置原因：需先定義 `SS ↔ 遊戲列表` 通訊協定，且需 GG 控制器配合
