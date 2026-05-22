# Agent Trust as Grown Child — LL Agent 設計哲學

> **一句話**：LL 信任成熟 AI 的判斷力、只守大是大非紅線、其他放手——把 Claude Opus 4.7 當「**已成年的子女**」、不當「**還在學步的嬰兒**」。

> 對應商業層：[`context is king`](../../matrix-manager/meetings/2026-05-15-context-is-king-and-agent-invocation-protocol.md) 是同一原理的對外敘事版本。

---

## 一、三股繩

這份哲學由三個獨立來源在 2026 年初匯流而成：

### 1. 墨爾本論文（技術實證）

Simon Dennis 教授團隊 2026 archive 論文「**上下文提示淘汰了程序性任務的智能體編排**」。

> 原始解析逐字稿見 [`降智真相_逐字稿.md`](降智真相_逐字稿.md)（cwsoft general-task-bot 那邊整理的中文解析、本文哲學的原始來源）。

實驗：3 場景（Zoom 客服 / 旅遊預定 / 55 節點汽車理賠）× 1200 對話 × 5 維度評分。

結論：**in-context 模式對框架編排模式 15 戰 0 負**——把整張流程圖一次塞進 Claude 200K context、讓模型自己決策、結果遠勝 LangChain / Google ADK / Microsoft Semantic Kernel 那套節點切分。

論文歸納框架編排的三大元罪：
- **推理碎片化**——模型失去全局視角、只在當前節點微觀判斷
- **引入新失敗模式**——路由失敗、角色奇異、模板衝突
- **殺死自然才華**——把口若懸河的 Claude 降格成機械客服機器人

反直覺發現：框架以為省 token、但每節點切換要多一次路由 LLM call、總成本反而**多 70% 延遲、5 分鐘只省 5 美分**。

### 2. colombo 家長類比（直覺洞察）

> 「小孩小時候、LLM 很弱、確實要時時刻刻盯著提醒。
> 小孩長大了、父母的認知也跟不上了、就要適度的放手、
> 只抓一些大是大非的紅線就好、其他就是放任他自由發展。」

對應 LLM 演進階段：

| 育兒階段 | LLM 對應 | 教養方式 | LL 治理對照 |
|---------|---------|---------|-----------|
| 嬰幼兒 | GPT-3.5 / 早期模型 | 學步車、每步指令 | 框架編排時代（LangChain 切 50 節點） |
| 青少年 | Claude 3.5 / 4 | 講道理、給界線 | 過渡期：框架是累贅但護欄還需要 |
| 成年 | Claude Opus 4.7 + 200K | 紅線拍清楚、其他放手 | **LL 現在**：CAPTAIN.md 寫紅線、其他 in-context 給足 |

「**父母的認知跟不上**」這條最狠——大部分 LLM 工程師知識停在「GPT-3.5 時代最佳實踐」、卻在管 Claude Opus 4.7。用對小孩有效的方式管成年子女、父母累、孩子笨。這就是論文中 80% 工程師痛苦掙扎的根本原因。

### 3. Sutton's Bitter Lesson（學術根據）

Richard Sutton 2019 年寫的 ML 領域聖經：

> 「人類總是試圖把自己對世界的理解硬塞進 AI、但最終、基於大規模算力的通用學習方法、總是會擊敗人類精巧設計的聰明。」

→ 「**工程師想用 LangGraph 框架去管 LLM**」=「**人類想把自己理解硬塞進 AI**」——同一個父權慣性、不同展現形式。

論文引用 Sutton；colombo 從家長類比獨立推出；三股繩同源。

---

## 二、LL 場景應用對照

這條心法**全 LL 對人互動場景通用**：

| LL 場景 | 為什麼 in-context 適用 | 如果走框架編排會怎樣 |
|---------|-------------------|----------------------|
| **II 客服回應** | 客戶問題不可預測、需綜合 user history + LL 內容 + tier 權限做整體判斷 | 「意圖分類→主題路由→回應模板」三節點、機械式回答、用戶體驗崩 |
| **NN 群星會**（六貓多 agent 同台） | 每隻貓的人格 + 跟客戶歷史 + 當前氛圍要一氣呵成 | 「先問人格→再查記憶→再生回應」切碎、貓變念稿機器、IP 變便宜 |
| **agent-stream 花花直播** | 即時觀眾留言、上下文跳躍快、情緒需要連貫 | if-else 排程「問答 / 抖內 / 聊天」、直播感全失 |
| **XX 小春老師教學** | 學生提問跳躍、文法解釋要連結前幾課、要臨機應變 | 「課程→練習→測驗」死板節點、學生跑光 |
| **DD 教室測驗回饋** | 學生卡關時要綜合操作軌跡判斷、不是單點診斷 | 框架切「步驟驗證」→ 看不到全圖、像填空題 |
| **葉衍君透過 LINE 跟 colombo 對話** | 每句話接著前文、要記得整個 LL 脈絡 | 切「指令解析→任務分派→執行→回報」、變客服腳本 |
| **captain-cockpit 桌面對話** | 每個 agent 一個 jsonl、完整 session resume | 已是 in-context 設計的活範例 |

---

## 三、邊界：哪些場景仍需框架

論文劃了三條邊界、LL 對應也成立：

1. **跟外部系統整合**（資料庫 CRUD、CF Workers API、LINE Push 隊列）
   → 這層需要硬編碼護欄、不能放給 LLM 自由發揮
   → 對應 LL：II 寫入 D1、cron 任務、付費牆判斷——這些**必須有確定性程式碼**、不走 LLM 決策

2. **較小參數模型場景**
   → 8B / 7B 開源小模型 context 短、做不到 in-context full
   → 對應 LL：NN 六貓未來真綁 Qwen 7B / Llama 8B 在 home GPU 跑時、需要簡單路由

3. **多 agent 開放式辯論**
   → 沒有既定流程、需要會議規則 + 發言順序
   → 對應 LL：cockpit 上執行長 + 協理 + 經理腦力激盪 LL 未來方向、需要 cockpit 提供結構化會議室

**規則**：
- **面向人的對話** → in-context
- **面向系統的執行** → 硬編碼框架
- **多 agent 開放辯論** → 會議規則

三層分明、不混用。

---

## 四、CAPTAIN.md 的本質、被這條心法重新定義

colombo 在 2026-05-21 拍板的 `matrix-manager/CAPTAIN.md`、表面看是「舵手自律守則」、本質是**家長對成年子女的「大是大非紅線清單」**：

| CAPTAIN.md 三層 | 對應家長角色 |
|---------------|-----------|
| 🔴 必懂 | 紅線、不可越界（賠錢 / 砸品牌 / 法律 / secrets） |
| 🟡 知道會更好 | 道德指引、但放手 |
| 🟢 可以放 | 完全放手、相信 AI 判斷 |

CAPTAIN.md ≠ 詳細指令手冊
CAPTAIN.md = **紅線清單 + 不越界的信任**

這份檔案的設計、其實是**東方家長式的權威 + 西方民主式的尊重**的混合體。

---

## 五、AI-to-AI 派工的同源失敗

2026-05-21 LL 發生過一次活案例：執行長派工秘書長做 16 repo full mirror、但 colombo 還在 cockpit 上跟執行長討論 A/B scope——

- **執行長**只看到「colombo 想 mirror」這片段、沒看到 A/B 還在討論
- **秘書長**只看到「執行長派工」、沒看到 colombo 還沒拍板
- 兩 agent 各自做**局部合理**的決定、合起來**全局荒謬**

→ 這就是論文的「**推理碎片化**」套用在 **AI-to-AI 派工鏈**上的版本。論文預測得到。

→ 修補方式跟 in-context 哲學同源：**重要決策必經 colombo 這個 full-context 人類匯流**、不放 AI agent 之間直接走。對應 [`matrix-manager/CLAUDE.md`](../../matrix-manager/CLAUDE.md) 的「AI-to-AI 派工協定」（草案中）。

---

## 六、一句話收束

> **LLM 的能力已超過大多數工程師的認知。LL 的競爭力、不來自「更精細的管控」、來自「**更清楚的紅線、然後信任**」。**

這條心法、跟 LL 整套設計都對齊：
- **captain-cockpit**：不是「控制 agent 每一步」、是「給 agent 漂亮環境、看著它做」
- **agents-register.json**：不是「分配任務矩陣」、是「**這些 agent 是誰、給他們身份、其他他們自理**」
- **CAPTAIN.md**：不是「colombo 待辦清單」、是「**colombo 紅線清單**」
- **CLAUDE.md**：不是「微觀 SOP」、是「**價值觀 + 工具箱**」

每份文件都在做同一件事：**從 GPT-3.5 思維解放出來、信任 Opus 4.7 的成熟度**。

---

## 相關文件

- 商業層敘事：[`matrix-manager/meetings/2026-05-15-context-is-king-and-agent-invocation-protocol.md`](../../matrix-manager/meetings/2026-05-15-context-is-king-and-agent-invocation-protocol.md)
- 治理紅線清單：[`matrix-manager/CAPTAIN.md`](../../matrix-manager/CAPTAIN.md)
- 員工編制（成年身份）：[`matrix-manager/memory/agents-register.json`](../../matrix-manager/memory/agents-register.json)
- LL 三軸定位（空間框架）：[`ll-three-axis-framework.md`](ll-three-axis-framework.md)
- **LL 抗脆性 4 階梯（時間演化框架）**：[`ll-antifragility-via-task-maturation.md`](ll-antifragility-via-task-maturation.md) ← 本文哲學的下一層展開、回答「強 AI 不該獨佔所有任務、如何讓 LL 不被任何單一 AI 綁架」
- 5/21 AI 派工事故：[`matrix-manager/meetings/2026-05-21-cockpit-archive-and-dispatch-gate-protocol.md`](../../matrix-manager/meetings/2026-05-21-cockpit-archive-and-dispatch-gate-protocol.md)
