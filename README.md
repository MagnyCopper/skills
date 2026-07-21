# skills
AI Agent 技能仓库

## 可用技能

### 数据发现与验证

- `company-domain-finder/`：根据企业名称和国家/地区，通过多源搜索和验证找到企业官网域名。输出为固定 JSON 格式，存放在 `results/<YYYYMMDD>/company-domain-finder/<company_id>.json`。

- `company-registry-finder/`：查找企业的官方注册法定名称、注册管辖区/地址和注册号。支持改名/收购解析到当前存续实体。覆盖范围：JP、US（多州）、UK、DE、FR、KR、HK、SG、TW、IN、CA、BE、NL、CH、LU、KZ。

- `overseas-registry-source-research/`：研究特定国家/地区/行业的官方数据源和第三方数据源，提供证据支撑的获取验证。

### 信息提取与分析

- `homepage-info-extractor/`：从机构或企业官网首页与必要子页面精准提取指定数据（如名称、历史、联系方式、人员）并输出为标准 Excel 扁平化报告。要求严格原文提取、提供可验证的 XPath/定位器来源。

- `website-deep-analyzer/`：通过 Playwright 或等效浏览器方式深度抓取企业官网，按照 schema 提取企业信息、补全缺失字段、保存原始页面与结果文件。

### 招聘与评估

- `resume-screener/`：简历智能筛选与评估工具。基于预定义的岗位招聘要求，对简历文件进行结构化评分和匹配度分析，生成 Markdown 筛选报告。适用于 HR 初筛和部门经理首轮筛选场景。

## 输出约定

- 结果存放在 `results/<YYYYMMDD>/<skill-name>/`，日期格式为 `YYYYMMDD`。
- 域名查找：输出为 JSON 文件，key 固定不变，`official_domain` 为唯一最佳结果或 `null`。
- 工商注册查询：每家公司一个 JSON 文件，路径为 `results/<YYYYMMDD>/company-registry-finder/<id>.json`。
- 简历筛选：输出 Markdown 格式筛选报告，可保存为 `resume-screening-report.md`。
- 网站深度分析：结果保存在 `./temp/aiparse/<website_name>/result.json`，并保存原始页面文件。

## 项目结构

```
skills/
├── homepage-info-extractor/      # 官网首页信息抽取
├── company-domain-finder/        # 企业域名查找
├── overseas-registry-source-research/  # 海外工商数据源研究
├── company-registry-finder/       # 工商注册信息查询
├── website-deep-analyzer/        # 网站深度分析
├── resume-screener/              # 简历智能筛选
├── results/                      # 各技能输出结果目录
└── AGENTS.md                     # Agent 使用指南
```
