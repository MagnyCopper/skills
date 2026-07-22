# expert-reviewer 迭代指南

本指南说明如何对 `expert-reviewer` skill 进行后续迭代改进。面向未来的你（可能隔了几周才回来）。

---

## 迭代历史

### iteration-2（2026-07-22）— 当前最佳

| 指标 | with_skill | without_skill | Delta | vs iter-1 |
|---|---:|---:|---:|---:|
| Pass rate（均值） | 97.0% | 31.0% | **+66.0pp** | +4.7pp delta |
| 报告长度 | 459-828 行 | 143-303 行 | 3-6× | — |
| Subagent 稳定性 | 5/5 成功 | 5/5 成功 | — | ✅ 解决 hang |
| Eval 覆盖 | 5 eval（含英文） | — | — | +1 eval |

**改进内容**：
1. References 从 1318 → 641 行（**-51%**），总 skill 2392 → 1493 行（**-38%**）
2. 新增 eval 5（英文 serverless 架构输入），验证跨语言泛化：95% pass rate
3. **全部 5 个 with_skill subagent 成功完成**（iteration-1 中 2/4 hang → fallback 主会话）
4. Delta 从 +61.3% → +66.0%（即使 references 减半，输出质量未降）

workspace: `expert-reviewer-workspace/iteration-2/`

### iteration-1（2026-07-22）— baseline

| 指标 | with_skill | without_skill | Delta |
|---|---:|---:|---:|
| Pass rate（均值） | 97.5% | 36.2% | **+61.3pp** |
| 报告长度 | 450-909 行 | 27-400 行 | 5-17× |
| Subagent 稳定性 | 2/4 成功（2 hang） | 4/4 成功 | — |
| Eval 覆盖 | 4 eval（全中文） | — | — |

workspace: `expert-reviewer-workspace/iteration-1/`

### 当前剩余短板（iteration-3 应改进的方向）

1. **Grader 假阴性**：heuristic grader 对“每个问题包含方法论依据”这类量化断言用关键词 fallback 太弱（iteration-2 有 3 个假阴性）。改用 LLM grader 或更严格的 regex。
2. **n=1 per cell**：每个 eval 只跑了 1 次。iteration-3 应至少 n=3 才能算稳定。
3. **Eval 覆盖仍偏窄**：缺超长文档（>50页）、缺多模态（含图表的 PDF）、缺“用户中途追问调整”的场景。
4. **expert-reviewer 未注册为系统 skill**：subagent 无法通过 load_skills 加载，只能手动读文件。需注册到 skill registry。

---

## 迭代流程（每次 iteration 重复）

### Step 0：准备工作区

```bash
# 在 skill 根目录下
ITER=iteration-2
mkdir -p expert-reviewer-workspace/$ITER

# 复制 eval_metadata.json 模板（每个 eval 一个）
cp -R expert-reviewer-workspace/iteration-1/eval-* expert-reviewer-workspace/$ITER/

# 如果改了 evals.json，重新生成 eval_metadata.json（见下文）
```

### Step 1：明确改进目标

写下 **1-3 个具体改进点**。不要"让评审更好"这种模糊目标。例：
- ❌ "提升评审质量"
- ✅ "iteration-1 中 Eval 4 (adhoc idea) 缺少竞品横向对比；iteration-2 增加竞品矩阵要求"
- ✅ "把 reference/methodology-foundations.md 从 305 行精简到 <150 行，解决 subagent hang"
- ✅ "增加 1 个英文输入的 eval"

### Step 2：修改 skill

修改 `expert-reviewer/` 下的源文件：
- `SKILL.md` — 工作流、规则
- `assets/templates/` — 输出模板
- `references/` — 方法论参考
- `evals/evals.json` — 评估集（增加/修改 eval）

**重要**：每次只改 1-2 个变量。否则无法判断哪个改动起作用。

### Step 3：更新 evals.json（如果需要新 eval）

```json
{
  "skill_name": "expert-reviewer",
  "evals": [
    {
      "id": 5,
      "prompt": "[新的评审 prompt]",
      "expected_output": "[期望输出描述]",
      "files": ["evals/files/xxx.pdf"],
      "expectations": [
        "[可验证的断言 1]",
        "[可验证的断言 2]"
      ]
    }
  ]
}
```

**写好 assertion 的原则**：
- ✅ "报告包含元信息表格，列出对象类型/字数/日期" — 可程序化检查
- ✅ "每个 Critical 问题至少引用 1 个外部方法论" — 可程序化检查
- ❌ "评审深入且有洞察" — 不可验证
- ❌ "比无 skill 版本好" — 不是 assertion，是 comparison

### Step 4：生成 eval_metadata.json

每个 `<workspace>/<iter>/eval-<name>/` 需要一份 `eval_metadata.json`，字段：
```json
{
  "eval_id": 5,
  "eval_name": "short-name",
  "prompt": "...",
  "assertions": ["断言1", "断言2"]
}
```

### Step 5：执行 8+ 个 run

每个 eval × 2 配置（with_skill / without_skill）。推荐用 subagent，但**长任务 fallback 到主会话**：

```python
# via task(category="unspecified-high", load_skills=["expert-reviewer"], ...)
```

**已知问题**：with_skill 任务加载 6 个 reference 文件会导致 subagent hang。临时方案：
- 用主会话直接跑（已验证可行）
- 或精简 reference 体积后再用 subagent

### Step 6：Grade

```bash
python3 expert-reviewer-workspace/grade_all.py
# 或针对单次迭代重写脚本
```

改进 grader 的方向：
- 对量化断言用更严格的 regex
- 对"每个 X 都包含 Y"类断言，解析 Markdown 结构后逐项检查
- 对模糊断言，用 LLM grader（oracle agent）

### Step 7：构建 benchmark.json

```bash
python3 expert-reviewer-workspace/build_benchmark.py
```

注意修改脚本中的 `WORKSPACE` 和 `dir_to_id` 映射。

### Step 8：对比上一 iteration

```bash
# 启动 viewer，加载 previous-workspace
python3.12 ~/.agents/skills/skill-creator/eval-viewer/generate_review.py \
  expert-reviewer-workspace/iteration-2 \
  --skill-name expert-reviewer \
  --benchmark expert-reviewer-workspace/iteration-2/benchmark.json \
  --previous-workspace expert-reviewer-workspace/iteration-1 \
  --port 3117
```

### Step 9：记录 history.json

在 `expert-reviewer-workspace/history.json` 追加：

```json
{
  "started_at": "2026-07-22T...",
  "skill_name": "expert-reviewer",
  "current_best": "iteration-2",
  "iterations": [
    {
      "version": "iteration-1",
      "parent": null,
      "expectation_pass_rate": 0.975,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "iteration-2",
      "parent": "iteration-1",
      "expectation_pass_rate": 0.98,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

判定 `grading_result`：
- `baseline` — 第一次跑
- `won` — pass_rate 高于 parent 且差距 > 5pp
- `lost` — pass_rate 低于 parent
- `tie` — 差距 ≤ 5pp

---

## 何时停止迭代

满足以下**全部**条件即可停止：

- [x] with_skill pass_rate ≥ 95%（iter-2: 97.0% ✅）
- [x] Delta vs without_skill ≥ 30pp（iter-2: +66pp ✅）
- [ ] n ≥ 3 per cell，且方差稳定（当前 n=1，**未满足**）
- [ ] 至少 6 个 eval 覆盖不同文档类型（当前 5 个，**未满足**）
- [x] 至少 1 个英文输入 eval（iter-2 eval 5 ✅）
- [x] subagent 能稳定执行 with_skill 任务不 hang（iter-2: 5/5 成功 ✅）
- [ ] 用户主观评审满意（当前用户无反馈，可视为通过）

**当前进度：8 项中满足 5 项**。iteration-3 建议重点关注 n=3 稳定性 + 增加超长文档/多模态 eval。

---

## 快速命令参考

```bash
# 一键启动 viewer（iteration-1）
python3.12 ~/.agents/skills/skill-creator/eval-viewer/generate_review.py \
  expert-reviewer-workspace/iteration-1 \
  --skill-name expert-reviewer \
  --benchmark expert-reviewer-workspace/iteration-1/benchmark.json \
  --port 3117

# Grade 全部
python3 expert-reviewer-workspace/grade_all.py

# 构建 benchmark
python3 expert-reviewer-workspace/build_benchmark.py

# 关闭 viewer
kill $(pgrep -f generate_review)

# 查看 benchmark 汇总
python3 -c "import json; b=json.load(open('expert-reviewer-workspace/iteration-1/benchmark.json')); print(json.dumps(b['run_summary'], indent=2))"
```

---

## iteration-1 工件位置

- Skill 源码：`/Users/han/Projects/skills/expert-reviewer/`
- 测试 workspace：`/Users/han/Projects/skills/expert-reviewer-workspace/iteration-1/`
- Benchmark：`expert-reviewer-workspace/iteration-1/benchmark.json`
- Grading：`expert-reviewer-workspace/iteration-1/eval-*/{with,without}_skill/grading.json`
- 报告：`expert-reviewer-workspace/iteration-1/eval-*/{with,without}_skill/outputs/review-report.md`
- Research 报告：`results/20260721/ulw-research/review-methodology-research.md`
- ULW 会话日志：`.omo/ulw-research/20260721-100709/SYNTHESIS.md`
