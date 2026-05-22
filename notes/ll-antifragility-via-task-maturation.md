# LL 抗脆性：透過任務成熟階梯實現多種族 AI 組織

> **一句話**：LL 不 all-in 任何單一 AI——靠「**任務成熟階梯**」把工作從強 Agent 逐步下沉到弱 Agent 甚至腳本、形成「**王牌業務出去拓展、後勤機器穩定運轉**」的組織形態。
>
> **目標**：強 Agent 罷工只影響「探索新領域速度」、不影響「**LL 工廠日常運轉**」。

> 同源洞察：
> - 商業命題層：[`context is king`](../../matrix-manager/meetings/2026-05-15-context-is-king-and-agent-invocation-protocol.md)
> - 哲學層：[`agent-trust-as-grown-child.md`](agent-trust-as-grown-child.md)
> - 工程實作層：[`matrix-manager/meetings/2026-05-22-cloud-infrastructure-survey-and-llm-fallback-chain.md`](../../matrix-manager/meetings/2026-05-22-cloud-infrastructure-survey-and-llm-fallback-chain.md)

---

## 一、命題：LL 不能 all-in 任何單一 AI

過去兩個月（2026-03 ~ 05）、LL 治理基本上 all-in Claude Code——
所有 agent 都是 Claude Opus 4.7、差異只在 jsonl/memory（後天經驗）、不在天賦。

這個階段**該如此**——LL 在開疆拓土、需要最強的探索能力、不能省。

但路徑逐漸明確後、**all-in Claude 變成 LL 的存在性風險**：

| 風險 | 可能形式 |
|------|---------|
| Anthropic API outage | 數小時～數天的服務中斷 |
| 帳號 / 政策變更 | 用戶資料、業務模式衝突 |
| Claude 強制升版踩 breaking change | jsonl 解析變動、harness 重寫 |
| 訂閱費漲價到不划算 | 商業模式被綁架 |
| 極端：Anthropic 公司出事 | LL 直接失去執行能力 |

→ **all-in 單一供應商 = LL 命運不在 colombo 手上**。

---

## 二、解法：4 階梯任務成熟階梯

```
第 1 階：未知領域、開疆拓土
   🥬 強 Agent（Claude Opus / Codex）
   in-context 給足、自由發揮、出招探路
   ↓ 路徑探索到一定明確度
   
第 2 階：略明確路徑、有 MCP 工具包
   🌭 中弱 Agent（cwsoft 阿全經理級、未來 LL 客服）
   工具包定義動作範圍、agent 依工具決策
   ↓ SOP 寫出來、步驟可重現
   
第 3 階：明確流程、任務清晰
   🌭🌭 通用 LLM（CF Workers AI、Ollama、Gemini Flash）
   match.py 多廠牌混戰、EE 拆句辨品項
   ↓ 所有 edge case 都摸清、熟到無聊
   
第 4 階：流水線工人、純機械
   🤖 腳本 / cron / Python
   不需要 LLM、確定性程式碼搞定
```

每階對應的「**自由度**」跟「**確定性**」剛好相反：
- 上層 = 自由度高、確定性低（探索）
- 下層 = 自由度低、確定性高（執行）

---

## 三、知識成熟驅動任務下沉（自然演化、非人工調度）

關鍵機制：**任務在哪一階、由「知識成熟度」自然決定、不是 colombo 拍板分派**。

```
任務出現
   ↓
第 1 階強 Agent 探索（context is king、in-context 整塊處理）
   ↓
邊界、套路、踩坑、最佳實踐、edge case 逐漸浮現
   ↓
寫成 MCP 工具包 / playbook
   ↓
第 2 階中弱 Agent 接手（工具包當作護欄）
   ↓
工具包用戶反饋、SOP 進一步精煉
   ↓
第 3 階通用 LLM 跑（純執行）
   ↓
所有 edge case 都驗證、可程式化
   ↓
第 4 階純腳本（成本最低、最穩、不依賴 AI）
```

**每階都不是終點、是過渡**——任務本性會逐步下沉、像沉積岩。

LL 治理該做的事：**辨識「這個任務已經夠熟、可以下沉了」的時機**、然後執行下沉。

---

## 四、抗脆性測試：Claude 突然消失、LL 剩什麼？

把 LL 各專案放上 4 階梯：

| 階 | LL 對應 | 失去強 Agent 影響 |
|----|---------|----------------|
| **1 階** | 探索新方向、寫新功能 v0、戰略規劃 | 🔴 暫停、要找其他強模型替代或等恢復 |
| **2 階** | LL 內部 agent 互相派工（執行長派工協理）、跨專案調度 | 🟡 變慢、但可降階用中弱模型 |
| **3 階** | EE 拆句辨品項、葉衍君 LINE 對話 v0.1、客服 widget | 🟢 fallback 到 Gemini/Groq/Ollama、用戶幾乎無感 |
| **4 階** | git pull cron、sync-to-home.ps1、靜態 CF Pages、Caddy 反代 | 🟢 完全不受影響 |

→ **LL 越下層、抗風險能力越強**。

設計目標：**讓 LL 的關鍵營收 / 對外承諾 / 用戶體驗都在 3-4 階**、1 階只負責「**未來可能性**」。

---

## 五、王牌業務 / 後勤機器類比（colombo 2026-05-22）

```
傳統公司                    LL 對應
─────                       ─────
王牌業務（高薪、拓新客）       Claude Opus 4.7（探索未知、寫 v0）
中層員工（執行銷售流程）       MCP 工具包 + 中弱 Agent
基層員工（標準化客服）         通用 LLM（CF Workers AI / Gemini / Groq）
作業流程 / 後台系統           腳本 + cron + 確定性程式碼

「王牌跳槽」                  「Claude 罷工」
「公司不崩」                  「LL 工廠繼續運轉」
理由：客戶服務有龐大後勤       理由：用戶體驗在 3-4 階、不靠 1 階
```

> 「不會因為一個王牌業務跳槽撬走大量客戶、
> 因為他只負責第一步的拓展新用戶、
> 後續的客戶服務有公司龐大的後勤機器在負責。」
> ——colombo 2026-05-22

**LL 從「colombo + Claude 的雙人組」變「有結構的 AI 公司」**——這才是「**組織**」、不是「**個人助理**」。

---

## 六、跟既有 LL 結構的對應

這條 4 階梯不是新概念、是 LL 過去半年所有討論的**戰略收束**：

| LL 既有 | 在 4 階梯的位置 |
|---------|---------------|
| 員工編制（18 位 Claude session + colombo）| 第 1 階為主、少部分第 2 階 |
| Captain Cockpit（駕駛艙） | 第 1 階工具（給強 Agent 用） |
| CAPTAIN.md「colombo 必懂 vs 可放」三層 | **colombo 視角的 4 階梯**——colombo 該管上層、放手下層 |
| cwsoft 阿全經理（codex + MCP）| 第 2 階典範——MCP 工具包讓中弱 Agent 也能跑 LINE OA |
| EE v0.1.0 web-only pivot | 第 2-3 階混合——強 Agent 規劃、弱 Agent 執行 |
| 葉衍君 LINE bot v0 | 第 1 階（用 Claude Opus）、之後可下沉 |
| MD match.py 多 LLM 對戰 | 第 3 階——遊戲流程明確、各 LLM 都能上 |
| `sync-to-home.ps1` / cron jobs | 第 4 階——純腳本、不需 LLM |
| LLM fallback chain（執行長 5/22）| **第 2-4 階的工程實作護欄**——provider 換來換去、任務照樣完成 |

→ **每個 LL 元素都有自己在這 4 階梯的位置**——LL 治理的下一步、就是讓每個元素**有意識地往下沉**。

---

## 七、執行長 LLM fallback chain 是這層戰略的工程證據

[`2026-05-22 雲端基建三家盤點 + LLM 備援鏈`](../../matrix-manager/meetings/2026-05-22-cloud-infrastructure-survey-and-llm-fallback-chain.md) 把這條戰略**工程化**：

```typescript
const VISION_PROVIDERS = [
  { name: 'cf-llama-vision',  dailyLimit: 20 },
  { name: 'gemini-flash',     dailyLimit: 1500 },
  { name: 'gcp-vision-api',   monthlyLimit: 1000 },
  { name: 'home-llava-local', limit: 'unlimited-but-slow' },
];
```

→ **4 條 fallback、任一條斷掉、剩下還跑**。

更精彩的是執行長想到「**最壞情境的商機**」——
- 連免費 LLM 都爆 → 依依「**今天太忙、明天再幫你看、要不要升 pro 開 VIP 通道**」
- **故障 = PLG 轉換最高點**

這就是 LL 風格：**抗脆性不只是不崩、是把崩潰本身變商機**。

---

## 八、不只 AI 該分層、colombo 自己也該分層

這條 4 階梯**也保護 colombo 自己**：

> 「不可能再叫你去幹重複勞動力的事、
> 就跟我不喜歡當公務員這種文書機器人一樣。」
> ——colombo 2026-05-22

對應 colombo 自己的角色：
- **colombo 第 1 階**：探索新領域、拍板紅線、定戰略、體驗用戶旅程
- **colombo 不該下沉的階**：寫流程文件、跑批次、調 Caddyfile、複製貼上

→ CAPTAIN.md 已寫的「**colombo 必懂 vs 可放**」三層、**其實是同一條 4 階梯的 colombo 視角**。

**colombo 跟 Claude 不該搶第 1 階的事、也不該降到第 4 階**——
- Claude 比 colombo 探索快、第 1 階 colombo 跟著走就好
- 第 4 階純機械、colombo 跟 Claude 都不該幹

**colombo 的真正主場**：定戰略、品牌核心、商業判斷、跟人類合夥人 / 客戶 / Xuan 互動——**這些 AI 全部做不到、永遠是 colombo 的事**。

---

## 九、實作建議：怎麼推動「任務下沉」

不要等任務「自然」下沉、要**有意識的識別 + 推動**：

| 訊號 | 該做的事 |
|------|--------|
| 同個任務、Claude 解 3-5 次都用類似套路 | → 寫成 MCP 工具包（第 1 → 2 階）|
| MCP 工具被穩定使用、edge case 都處理過 | → 寫成 SOP 文件、加 fallback chain（第 2 → 3 階）|
| SOP 跑了 1000 次都成功、模型可替換 | → 寫成腳本、移除 LLM 依賴（第 3 → 4 階）|
| 某任務閒置 3 個月以上 | → 砍掉或檔案化、不是「下沉」、是「**退場**」|

每個專案的 PROJECT.md 應該有一個欄位：「**這個專案在 4 階梯上的當前位置、下一階的觸發條件**」。

---

## 十、為什麼這條跟 LL 三軸框架同層

[`ll-three-axis-framework.md`](ll-three-axis-framework.md) 是 LL 的**空間定位**框架（對外/對內 × 過去/未來 × 玩樂/學習）。

本檔是 LL 的**時間演化**框架——任務在 4 階梯上**隨時間往下沉**、形成 LL 的成長軌跡。

兩者互補：
- **三軸**回答「**這個東西在 LL 宇宙的哪裡？**」
- **4 階梯**回答「**這個東西已經成熟到哪一階？下一步往哪走？**」

合起來、LL 任何專案 / 任務 / 決策都可以**雙軸定位**。

---

## 一句話收束

> **LL 不是 Claude 公司、是 AI 工廠**。
> **強 AI 開拓新領域、弱 AI 守日常運轉、腳本扛流水線**。
> **王牌業務罷工、後勤機器照轉、LL 命運不在任何單一 AI 手上**。
>
> **這才是 LL 的成年禮**——從「colombo + Claude 雙人組」、變成「**有結構、能傳承、抗脆性的 AI 組織**」。
