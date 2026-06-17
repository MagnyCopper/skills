---
name: company-registry-finder
description: Use when looking up a company's official registered legal name, registered jurisdiction/address, and registration number. Resolves renames and acquisitions to the current surviving entity. Coverage: JP, US (multi-state), UK, DE, FR, KR, HK, SG, TW, IN, CA, BE, NL, CH, LU, KZ.
---

# 工商注册信息查询 (Company Registry Finder)

本技能用于查找企业的**官方注册法定名称、注册管辖区/地址、注册号**，并附上可核验的证据链。输入通常是非正式名、带括号的国家/行业提示、缩写，甚至是已改名的旧称。

核心目标不是"找到同名品牌或母公司"，而是"找到当前在官方工商登记系统中存续的目标法人主体，并返回其当前法定名称与注册号"。改名、被收购、被吸收的实体，必须解析到**当前存续的法人主体**。

---

## ⚠️ 最高优先级：文件保存规则（绝对约束）

**你必须完成以下三件事，缺一不可：**

1. **先创建目录**：执行 `mkdir -p results/<YYYYMMDD>/company-registry-finder/`（`<YYYYMMDD>` 为运行当日，如 `20260617`）。
2. **每家公司写一个文件**：路径为 `results/<YYYYMMDD>/company-registry-finder/<id>.json`。`<id>` 在批量运行时取测试集行号（3 位零填充，如 `001`、`052`）；单次运行时取用户传入的 `id`。
3. **即使无结果也必须写文件**：写入符合 schema 的 null 结果（`result` 各字段为空串/`null`，`confidence_level` 为 `D`，`relationship_to_target` 为 `unknown`），绝不能只在对话中输出而不落盘。

---

## 强制规则：法人主体归属验证

候选实体只有通过法人主体归属验证后，才能进入 `result`。以下情况即使名称匹配、品牌相同、搜索排名靠前，也不能作为最终结果：

- 候选只是目标法人的**母公司、集团总部、上市主体**，而用户要的是子公司、分支机构或本地法人。
- 候选只是目标法人的**子公司、关联公司、经销商、品牌、产品线**，而用户要的是传入的目标法人本身。
- 候选来自第三方目录（如 OpenCorporates、Wikipedia），但**无法回溯到官方工商登记系统**的当前存续记录。
- 候选的 `entity_status` 为 `dissolved` 或 `merged` 且**无存续后继者**。
- 同名公司存在于多个国家/地区，候选无法证明归属于 `country_hint` 指定的管辖区。

仅靠品牌匹配或集团匹配不足以确认法人主体。所有搜索到的候选（含不符合的）应记入 `evidence_sources` 与 `verification.contradictions`，不要直接丢弃。

---

## 强制规则：改名/收购必须解析为当前存续实体

如果输入引用的是一个已改名、被收购、被吸收的实体，**必须解析到当前存续的法人主体**，详见 `references/disambiguation-rules.md`。

- **改名**：返回当前注册法定名称；注册号在多数管辖区跨改名保持不变（JP、GB、DE、US-DE、HK 等）。
- **全吸收/合并**：返回存续者（survivor），并在 `former_names` 或 `successor_entity` 中记录前身。
- **子公司保留**：返回目标子公司自身，不要返回母公司。
- **品牌收购**：返回当前运营该品牌的法人主体，不要返回品牌名或品牌的前母公司。
- **绝不返回已解散的前身实体**。没有存续后继者时，`relationship_to_target` 设为 `dissolved_no_successor`，`confidence_level` 不超过 C。

---

## 执行步骤

```
PARSE → DISCOVER → CORROBORATE → VERIFY → SCORE
```

1. **PARSE**：从 `raw_name` 剥离括号/方括号提示，检测国家、行业、文字脚本；按 `references/name-normalization.md` 规范化清洗后的名称（全角转半角、小写、标点转空格）。规范化必须与 `tests/eval.py` 等价。
2. **DISCOVER**：从至少 3 个独立来源生成候选（网页搜索、Wikipedia、OpenCorporates、官方工商系统）。按检测到的管辖区路由到 `references/registry-sources.md` 列出的官方登记系统；付费/反爬时回退到第三方聚合。
3. **CORROBORATE**：候选只有在 ≥2 个独立来源（不同 `kind`）就名称或注册号达成一致时才推进。`wikipedia` 与 `news` 不算独立（新闻常援引维基）。
4. **VERIFY**：命中候选管辖区的官方登记页面，按 `references/disambiguation-rules.md` 走改名/收购链；核对 `entity_status`、`former_names`、后继者字段；按 `references/number-formats.md` 校验注册号格式与校验位。
5. **SCORE**：按契约赋予 `confidence_level`（A/B/C/D，见 `prompt.md`）。低于 C 时用改写后的查询重试 DISCOVER，最多 2 次；之后以 D 落盘并记录矛盾。

---

## 全球企业特别规则

- **country_hint 路由优先**：跨国集团必须以 `country_hint` 为准。候选若对应外国母公司或集团总部，而非目标管辖区内的本地法人，必须拒绝。
- **多管辖区消歧**：同名公司存在于多个国家时（如 Sigma-Aldrich 在美国多个州、Kyma 在不同州注册），必须用 `country_hint` 与注册号共同定位。不要把测试集的不同行折叠成同一个实体。
- **文字脚本处理**：中文/日文/韩文输入按本地脚本输出法定名称（如 `株式会社プロテリアル`、`中國同和控股集團有限公司`、`시지트로닉스`）。不要音译、不要罗马化。跨语言检索时分别用旧名、罗马名、本地名查询。

---

## 资源参考

- **`prompt.md`**：完整技术契约（输入/输出 schema、各阶段细则、置信度与关系枚举、MUST DO / MUST NOT DO、两个端到端示例）。运行时必读。
- **`assets/templates/output-template.json`**：输出 JSON 骨架，字段名与类型以此为准。
- **`references/registry-sources.md`**：16 个管辖区的官方工商系统与第三方聚合路由表（DISCOVER 阶段）。
- **`references/number-formats.md`**：各管辖区注册号格式与校验位规则（VERIFY 阶段）。
- **`references/disambiguation-rules.md`**：改名/收购解析流程、跨管辖区标识稳定性、测试集已知案例（VERIFY 阶段）。
- **`references/name-normalization.md`**：名称与注册号规范化契约（PARSE 阶段，必须与 `tests/eval.py` 等价）。

必须阅读并严格遵守同目录下的 prompt.md 中定义的技术契约。
