# Search Strategies — Regional Index

Read the file corresponding to the target company's country/region, then apply the templates alongside the **Universal Queries** below.

## Universal Queries (apply to ALL countries)

These 3 query patterns are the minimum for any company lookup:

```
# U1: Exact name + official site
"<company_name>" official site

# U2: Exact name + country context
"<company_name>" <country_name> official website

# U3: Exact name + ccTLD filter
"<company_name>" site:<ccTLD> OR site:.com
```

## Region → File Mapping

| Country | File | ccTLD |
|---|---|---|
| 中国 (China) | [east-asia.md](east-asia.md) | .cn |
| 日本 (Japan) | [east-asia.md](east-asia.md) | .jp |
| 韩国 (South Korea) | [east-asia.md](east-asia.md) | .kr |
| 新加坡 (Singapore) | [southeast-asia.md](southeast-asia.md) | .sg |
| 马来西亚 (Malaysia) | [southeast-asia.md](southeast-asia.md) | .my |
| 印度尼西亚 (Indonesia) | [southeast-asia.md](southeast-asia.md) | .id |
| 越南 (Vietnam) | [southeast-asia.md](southeast-asia.md) | .vn |
| 泰国 (Thailand) | [southeast-asia.md](southeast-asia.md) | .th |
| 菲律宾 (Philippines) | [southeast-asia.md](southeast-asia.md) | .ph |
| 印度 (India) | [south-asia.md](south-asia.md) | .in |
| 英国 (UK) | [europe-west.md](europe-west.md) | .uk |
| 爱尔兰 (Ireland) | [europe-west.md](europe-west.md) | .ie |
| 法国 (France) | [europe-west.md](europe-west.md) | .fr |
| 比利时 (Belgium) | [europe-west.md](europe-west.md) | .be |
| 荷兰 (Netherlands) | [europe-west.md](europe-west.md) | .nl |
| 德国 (Germany) | [europe-north.md](europe-north.md) | .de |
| 瑞士 (Switzerland) | [europe-north.md](europe-north.md) | .ch |
| 瑞典 (Sweden) | [europe-north.md](europe-north.md) | .se |
| 挪威 (Norway) | [europe-north.md](europe-north.md) | .no |
| 丹麦 (Denmark) | [europe-north.md](europe-north.md) | .dk |
| 芬兰 (Finland) | [europe-north.md](europe-north.md) | .fi |
| 意大利 (Italy) | [europe-south.md](europe-south.md) | .it |
| 西班牙 (Spain) | [europe-south.md](europe-south.md) | .es |
| 葡萄牙 (Portugal) | [europe-south.md](europe-south.md) | .pt |
| 波兰 (Poland) | [europe-east.md](europe-east.md) | .pl |
| 捷克 (Czech Republic) | [europe-east.md](europe-east.md) | .cz |
| 俄罗斯 (Russia) | [europe-east.md](europe-east.md) | .ru |
| 土耳其 (Turkey) | [europe-east.md](europe-east.md) | .tr |
| 美国 (US) | [americas.md](americas.md) | .com |
| 加拿大 (Canada) | [americas.md](americas.md) | .ca |
| 巴西 (Brazil) | [americas.md](americas.md) | .br |
| 阿根廷 (Argentina) | [americas.md](americas.md) | .ar |
| 智利 (Chile) | [americas.md](americas.md) | .cl |
| 哥伦比亚 (Colombia) | [americas.md](americas.md) | .co |
| 墨西哥 (Mexico) | [americas.md](americas.md) | .mx |
| 阿联酋 (UAE) | [middle-east.md](middle-east.md) | .ae |
| 沙特阿拉伯 (Saudi Arabia) | [middle-east.md](middle-east.md) | .sa |
| 以色列 (Israel) | [middle-east.md](middle-east.md) | .il |
| 澳大利亚 (Australia) | [oceania.md](oceania.md) | .au |
| 新西兰 (New Zealand) | [oceania.md](oceania.md) | .nz |
| 南非 (South Africa) | [africa.md](africa.md) | .za |

## Cross-Validation & Verification Templates

These apply regardless of country — read [cross-validation.md](cross-validation.md) for Stage 2 and Stage 3 query templates.

## Query Construction Rules

1. Always wrap company names in double quotes for exact phrase matching.
2. Use `site:` operator to constrain results to relevant TLDs.
3. Combine OR clauses to broaden coverage without losing precision.
4. Add country-local keywords (Impressum, mentions légales, 公式サイト, 官网) when applicable.
5. Limit to 3-5 queries per stage to avoid excessive API calls.
6. Stop early if a high-confidence match is found before exhausting all templates.
