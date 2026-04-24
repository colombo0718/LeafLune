# PROJECT.md — LeafLune 宇宙官網

## 這是什麼

LeafLune 官方品牌介紹網站。單頁靜態 HTML，展示 LeafLune Edutainment Studio 旗下三大品牌宇宙（宣學習、LeafLune、戰術空間）及子品牌（ReinRoom、GameGeek、CubicCraft）的定位與產品。

---

## 部署方式

- **平台**：Cloudflare Pages
- **分支策略**：
  - `dev` / `feature/xxx` → 預覽 URL（Cloudflare 自動生成）
  - `master` → 正式網址（push 後約 1 分鐘生效）
- 無 build step，純靜態文件直接上傳

---

## 目錄結構

```
leaflune/
├── index.html              # 主頁（唯一入口，單頁 landing page）
├── index1.html             # 舊版備份（勿動）
├── privacy.html            # 隱私政策頁
├── balloon_smooth.py       # 氣球 3D 模型相關腳本（輔助工具，非網站核心）
├── CLAUDE.md               # AI 協作規範（通用）
├── PROJECT.md              # 本檔案
├── leaflune_logo_nobg.png  # 官方 Logo（透明背景）
├── LeafLune_emoji.png      # LeafLune 品牌 emoji
├── StrategySpace_emoji.png # 戰術空間 emoji
├── XuanXuexi_emoji.png     # 宣學習 emoji
├── Pika.ply                # 3D 資產（Pika 角色）
├── pika_balloon.ply        # 3D 資產（氣球版 Pika）
├── index.zip               # 備份壓縮包（不上線）
└── docs/                   # 品牌策略與規劃文件（不發布到網站）
    ├── LeafLune_Brand_Core.md          # 使命/願景/價值觀（品牌核心）
    ├── LL_Universe_MasterPlan_v1.md    # 宇宙總藍圖 v1
    ├── LeafLune_Workflow_Principles.md # AI 數位內容工廠工作流規範
    ├── LeafLune_Card_Product_Spec.md   # 卡牌產品規格
    ├── RR_Go-to-Market.md              # ReinRoom GTM 策略
    └── ...（其他品牌策略文件）
```

---

## 品牌架構

### 三大對外品牌

| 代號 | 品牌名 | 定位 | 對應「三才」 |
|------|--------|------|-------------|
| XX | 宣學習 XuanXuexi | 兒童/青少年語言學習（卡牌、繪本、英語營、AI 助教） | 地／樂 |
| LL | LeafLune | 主品牌（認證、身份、RL 哲學、Edutainment 宇宙） | 人／晒 |
| SS | 戰術空間 Strategy Space | 對戰競技、RL 競賽舞台 | 天／比 |

### 技術/平台子品牌

| 代號 | 品牌名 | 定位 |
|------|--------|------|
| RR | ReinRoom 強化教室 | RL 教學平台（Blockly + RL + Matter.js，純瀏覽器） |
| GG | GameGeek 遊戲極客 | 多平台 Web 遊戲控制器 |
| CC | CubicCraft 立方星艦 | 旗艦遊戲 |
| MM | MatrixManager 矩陣總管 | 任務/資料/UI 管理 AI（內部系統） |

### 品牌核心（不可改動）

> **使命**：讓學習變有趣，讓玩樂有價值。
> **願景**：建構一個以 AI 競技驅動的成長型社會引擎。
> **價值觀**：動機才是最強的教師，自主才是最深的學習。

---

## 技術細節

- **語言**：純 HTML / CSS / JavaScript（無框架、無 build）
- **字體**：system-ui + Noto Sans TC（fallback）
- **設計主題**：深色宇宙風（`--bg: #050814`），accent 色 `#38bdf8`（天藍）
- **頁面結構（index.html section id）**：
  - `#brand` — LeafLune 品牌核心
  - `#universe` — 三大品牌宇宙概覽
  - `#xuanxuexi` — 宣學習詳細介紹
  - `#leaflune-cert` — LeafLune 認證與身份
  - `#strategy-space` — 戰術空間競賽舞台
  - `#cards` — 卡牌與親子桌遊

---

## 已知注意事項

- `index1.html` 是舊版，不要刪，作為 diff 參考
- 品牌核心文字（使命/願景/價值觀）禁止改寫，只能調整版面
- `.ply` 是 3D 點雲模型文件，與 `balloon_smooth.py` 配合使用，非網站本體

---

## 開發規範

- **語言**：commit 訊息用繁體中文
- **改動原則**：這是品牌形象頁，樣式/文字改動前要確認
- **檔名慣例**：品牌文件用 `[品牌代碼]_[主題]_[版本].md`（如 `LL_Universe_MasterPlan_v1.md`）
- **1000 行上限**：單一 JS/HTML 檔案建議不超過 1000 行，超過考慮拆模組
- **一檔一職責**：資料定義、視覺渲染、版面排版分開放

---

## 相關文件

- 宇宙總藍圖：[docs/LL_Universe_MasterPlan_v1.md](docs/LL_Universe_MasterPlan_v1.md)
- 品牌核心：[docs/LeafLune_Brand_Core.md](docs/LeafLune_Brand_Core.md)
- 工作流規範：[docs/LeafLune_Workflow_Principles.md](docs/LeafLune_Workflow_Principles.md)
- ReinRoom GTM：[docs/RR_Go-to-Market.md](docs/RR_Go-to-Market.md)
