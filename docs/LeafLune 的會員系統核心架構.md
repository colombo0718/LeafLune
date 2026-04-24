# LeafLune 的會員系統核心架構

> 核心定位：  
> **LeafLune Core = 會員＋金流＋通訊的中樞**  
> Google 負責「全球身分 & 付款」，  
> LINE / Zalo 負責「在地通訊 & 入口」，  
> 各品牌（XX / RR / SS）負責提供不同類型的價值與內容。

---

## 1. 設計目標與整體觀

### 1.1 平台目標

LeafLune 的會員系統要解決這幾件事：

1. **你是誰？（Identity）**  
   - 支援多種登入來源（Google、LINE、Zalo…），  
   - 但在內部只對應到一個 **LeafLune User ID**。

2. **你曾經做過什麼？（History / State）**  
   - 在 XX 上用過哪些教案、上過哪些課。  
   - 在 RR 上訓練過哪些 agent、完成哪些任務。  
   - 在 SS 上參加過哪些賽季、取得哪些段位。

3. **你現在擁有什麼權限？（Entitlements）**  
   - 哪些課程 / 場景 / 競技模式已解鎖。  
   - 哪些證照 / 徽章可以查驗與展示。

4. **你可以做什麼下一步？我會給你什麼回饋？（Action → Reward）**  
   - 基於上述狀態，推薦適合的下一課、任務、賽季或升級方案。  

這對應到 RL 語言就是：  
> **state（會員狀態） → action（你與平台互動） → reward（內容、認證、競技光環）**

---

### 1.2 對外平台的角色分工

- **Google**  
  - 主要登入方式（Google Login）。  
  - 未來訂閱／付款的主金流管道之一。  
  - 定位為「全球帳號 & 收費中樞」。

- **LINE（台灣） / Zalo（越南）**  
  - 在地使用者最熟悉的入口。  
  - 綁定 LeafLune 帳號後，可用於：
    - 登入捷徑（從 OA 帶你進 Web）。  
    - 通知（課程提醒、賽季結果、訂單狀態）。  
    - 少量輕量級查詢（查訂單、查課表、查段位）。

- **LeafLune 自家 Web / PWA（RR / XX / SS）**  
  - 所有正式功能與體驗的主舞台。  
  - 必須在這裡才能做到完整的學習 / 練功 / 競技 / 客服互動。

---

## 2. 資料模型總覽（核心資料表）

> 重點不是用什麼 DB，而是這些「概念表」要存在。

### 2.1 會員與登入來源

#### 2.1.1 `users`（LeafLune 會員主檔）

- `id`：LeafLune User ID（平台內唯一主鍵）  
- `display_name`：顯示名稱  
- `email`：主要聯絡信箱（可選）  
- `locale`：語系（例：`zh-TW`、`vi-VN`、`en-US`）  
- `created_at` / `updated_at`  
- 通知設定（Email / LINE / Zalo / 推播 是否開啟）

---

#### 2.1.2 `user_auth_providers`（外部登入提供者綁定）

- `id`  
- `user_id` → 對應 `users.id`  
- `provider`：`google` / `line` / `zalo` / `discord` / …  
- `provider_uid`：各平台的唯一使用者 ID（Google sub、LINE userId 等）  
- `linked_at`：綁定時間  
- `last_login_at`：最後一次用此 provider 登入時間  

> 任一 provider 成功登入 → 透過 `provider + provider_uid` 找到 `user_id` → 這才是 LeafLune 真正的會員身分。

---

### 2.2 商品、訂單與權限（Products / Orders / Entitlements）

#### 2.2.1 `products`（可販售或授權的東西）

- `id`：如 `RR-SCENE-001`、`XX-LESSON-010`、`SS-SEASON-01`  
- `brand`：`RR` / `XX` / `SS`  
- `type`：`course` / `scenario` / `license` / `pack` / `season_pass` …  
- `name` / `description`  
- `base_price` / `currency`  
- `billing_cycle`：`one_time` / `monthly` / `yearly` …（可選）  
- `metadata`：JSON，存放特殊規則（例如可開啟哪幾個場景）

---

#### 2.2.2 `orders`（訂單紀錄）

- `id`  
- `user_id`  
- `total_amount` / `currency`  
- `payment_provider`：`stripe` / `newebpay` / `zalo_pay` / `line_pay` / `bank_transfer` …  
- `status`：`pending` / `paid` / `failed` / `refunded` / `cancelled`  
- `created_at` / `paid_at` / `cancelled_at` …  
- `raw_payload`：保存金流平台的原始回應（for 對帳 / audit）

---

#### 2.2.3 `order_items`（訂單中的每個品項）

- `id`  
- `order_id`  
- `product_id`  
- `quantity`  
- `unit_price` / `discount` / `final_price`  

---

#### 2.2.4 `entitlements`（實際取得的「使用權／資格」）

- `id`  
- `user_id`  
- `product_id`  
- `source_order_id`（哪一筆訂單給你的）  
- `granted_at`  
- `expires_at`（可為 NULL，代表永久）  
- `status`：`active` / `expired` / `revoked`  

> **RR / XX / SS 前端只需要看這張表，就能知道：  
> 這個人目前對某個功能／課程／賽季是不是有權限。**

---

### 2.3 行為軌跡與成就（Activities / Badges）

#### 2.3.1 `activities`（行為紀錄）

用來存「你曾經做過什麼」，是 RL 裡 state 的時間序列版本。

- `id`  
- `user_id`  
- `brand`：`RR` / `XX` / `SS`  
- `type`：`trained_agent` / `submitted_homework` / `joined_match` / `passed_exam` …  
- `payload`：JSON，存當下細節（場景 ID、分數、勝負、時長…）  
- `created_at`

> 未來所有推薦 / 課程解鎖 / 成就系統，都可以吃這張表。

---

#### 2.3.2 （可選）`badges` & `user_badges`

- `badges` 定義所有徽章 / 段位 / 榮耀稱號  
- `user_badges` 記錄誰拿過什麼、何時取得

---

### 2.4 客服與訊息（可隨產品成熟度再補）

1. `tickets`（客服工單）  
2. `messages`（站內訊息 / 問 AI / 問助教對話 log）  
3. `notifications`（系統推播紀錄，避免重複發送）

這些可以等 RR / XX / SS 的客服流程定了，再逐步補上。

---

## 3. 登入與身分綁定流程設計

### 3.1 Google Login：主登入流程

1. 使用者在 RR / XX / SS Web 按「以 Google 登入」。  
2. 前端透過 Google Login 拿到 token。  
3. 前端呼叫 `POST /auth/google`，附上 token。  
4. LeafLune Core：
   - 驗證 token，取得 `google_sub` 與 email。  
   - 查 `user_auth_providers` 有沒有對應的 `google + google_sub`。  
   - **有** → 回傳該 `user_id` 的 access token。  
   - **沒有** → 建立新的 `users` + `user_auth_providers`，再回傳 access token。

> 從此「Google 帳號」即綁定到某個 LeafLune User ID。

---

### 3.2 LINE / Zalo 綁定流程（以 LINE 為例）

1. 使用者在 LINE OA 看到「開始使用／打開學習平台」按鈕 → 開 LIFF。  
2. LIFF 打開你的 Web（例如 `https://rr.leaflune.com/liff`），  
   透過 LIFF JS SDK 取得 `line_user_id`。  
3. 你的 Web 前端邏輯：

   - 檢查 Local 是否已有 LeafLune access token：  
     - 沒有 → 引導做 **Google Login**。  
     - 有 → 直接進入綁定流程。

4. 綁定 API：  
   - 前端呼叫 `POST /auth/line/bind`，附上：  
     - `line_user_id`  
     - 目前持有的 LeafLune access token（代表是誰要綁）  
   - 後端：
     - 驗證 access token → 得到 `user_id`  
     - 把這個 `line_user_id` 寫入 `user_auth_providers`（provider=`line`）

之後：

- 在 OA 收到訊息（webhook）時，用 `line_user_id` 就能查回 `user_id`。  
- 在 Web 裡也知道：這個 Google user 同時綁定了哪個 LINE ID，可用於發通知。

> Zalo 的流程類似，只是改用 Zalo 的 OAuth / Mini App 機制。

---

## 4. 訂閱與金流流程

> 原則：**金流供應商可以換，但 `orders` → `entitlements` 的邏輯不變。**

### 4.1 建立訂單 & 付款

1. 使用者在某個頁面點「購買 / 升級」。  
2. 前端呼叫 `POST /orders/checkout`：  
   - 帶 `product_ids[]`  
   - 帶目前登入的 `user_id`（或 token）  
   - 可帶 `region`（台 / 越 / 其他，用來決定金流與幣別）

3. LeafLune Core：
   - 建立一筆 `orders`（status = `pending`）。  
   - 建立對應的 `order_items`。  
   - 根據 `region` & `payment_provider` 決定讓他走哪一家金流（例如台灣用 NewebPay，越南用 ZaloPay）。  
   - 回傳給前端一個「付款網址」或金流 SDK 所需參數。

4. 使用者在金流頁付款。

---

### 4.2 Webhook & Entitlement 發放

1. 金流平台於付款成功後呼叫 LeafLune 的 `/payments/webhook`。  
2. LeafLune Core：
   - 驗證簽章 / token。  
   - 找出對應 `orders.id`。  
   - 把 `orders.status` 更新為 `paid`。  
   - 根據 `order_items` 建立對應 `entitlements`。  

3. 未來的頁面權限判斷一律看 `entitlements`：  
   - 有 active entitlement → 顯示「開始使用／進入課程／進入賽季」。  
   - 沒有 → 顯示「購買 / 升級」按鈕。

---

### 4.3 退款 / 到期 / 升級

- **退款**：  
  - `orders.status = refunded`。  
  - 對應 `entitlements.status = revoked`。  

- **到期**：  
  - 定期任務或 DB 層面判斷 `expires_at < now`。  
  - 將 `status` 改為 `expired`。  

- **升級方案**：  
  - 依照不同 `product` 定義差額或包套價。  
  - 實作上仍是：新訂單 + 新 entitlements，只是金額計算不同。

---

## 5. 客服與通訊架構

### 5.1 站內客服：Web 內固定助手

- 在 RR / XX / SS 的 Web / PWA，右下角固定一個助理入口（例如「葉玄」、「司簿星」）。  
- 使用者登入後，所有對話都會附上 `user_id` 與 `context`（當前課程 / 場景）。  
- 後端可以：
  - 將訊息寫入 `tickets` / `messages`。  
  - 串接 LLM（AI 助手）＋人工客服。  
  - 視情況決定要不要生成任務、開工單、發 email/LINE 通知。

> 這是「正式客服 & AI 導師」所在的位置，  
> 必須在你自己的 Web 裏面，而不是只靠 OA。

---

### 5.2 LINE / Zalo：入口與通知

**入口功能：**

- OA 選單：  
  - 「我要上課」、「查訂單」、「看比賽結果」  
  - 多半會開一個 LIFF / Mini App，把使用者帶進對應 Web 頁面。

**通知功能：**

- 當重要事件發生時（付款成功、作業到期、賽季結果）：  
  - LeafLune Core 根據 `user_id` 查 `user_auth_providers`，  
  - 決定要不要發 LINE / Zalo 訊息通知。  

**輕量查詢（非必須，但可加分）：**

- 在 OA 中輸入關鍵字或按選單：  
  - 「查訂單」→ 呼叫 LeafLune API，回傳最近幾筆 orders 概況。  
  - 「查課程」→ 回傳目前 active entitlements 的清單。  
  - 「查段位」→ 回傳 SS 的段位與積分。  

> 但真正的「學習細節 / 討論 / 上傳作品」仍然引導回 Web。

---

## 6. 安全、權限與隱私（簡述）

- 登入／綁定流程要有基本的 token 驗證與過期機制。  
- 金流 Webhook 一定要驗簽、只回應合法請求。  
- User 資料需遵守各地隱私相關規範（未來涉歐盟則有 GDPR 議題）。  
- 管理後台（例如手動增加 entitlements 或調整 orders）必須有明確的管理員權限控管。

---

## 7. 未來擴充方向

- 增加更多 Auth provider（Discord / GitHub）給技術向產品使用。  
- 多幣別、多區域定價（`products_price_regions`）表，支援台／越／國際不同定價。  
- 更完整的成就系統（badges / levels），讓 RR / XX / SS 的成果可以在同一張「履歷／戰績」頁面展示。  
- BI / 分析層：  
  - 對 `activities` 做聚合，  
  - 分析使用者從「第一次接觸」→「付費」→「持續練功／參賽」的整體路徑。  

---

> 這份《LeafLune 的會員系統核心架構》  
> 就是之後所有東西（RR 平台、XX 教案平台、SS 競技大廳、司簿星、通用任務 Bot…）  
> 共同依附的「中樞神經與血管」。