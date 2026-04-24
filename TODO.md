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

## 宇宙文件（docs/）

- [ ] 建立 `LL_Protocol_SAR_v1.md`（State / Action / Reward 通訊協定總文件）
  > 供 GG ↔ 遊戲、RR ↔ 遊戲環境、SS ↔ 競技賽事共同參考

- [ ] 建立 `LL_Projects_Index_v1.md`（所有專案索引，掛在 HackMD `/LL/Projects/`）

- [ ] 補寫 `LL_RL_Philosophy_v1.md`（RL 人生觀系統）
  > 概念已在 MasterPlan 有大綱，需獨立成文

---

## 系統層

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
