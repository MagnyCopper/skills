# East Asia — 中国 / 日本 / 韩国

## 中国 (China / CN)

```
# C-CN-1: Baidu search with Chinese name (use Baidu if available)
<company_name_chinese> 官网

# C-CN-2: Chinese name + official site keywords
<company_name_chinese> 官方网站

# C-CN-3: ccTLD filter
"<company_name>" site:.cn OR site:.com.cn

# C-CN-4: Combined
<company_name_chinese> 官方网站 公司
```

Preferred engines: Baidu (primary), Google (secondary), Bing (tertiary).

## 日本 (Japan / JP)

```
# C-JP-1: Japanese ccTLD
"<company_name>" site:.jp OR site:.co.jp

# C-JP-2: Japanese name if discoverable
<company_name_japanese> 公式サイト

# C-JP-3: Combined
"<company_name>" 公式サイト OR "official site"
```

Japanese companies often use `.co.jp` for their primary domain. Also check `.jp` and `.or.jp`.

Preferred engines: Google (primary), Bing (secondary).

## 韩国 (South Korea / KR)

```
# C-KR-1: Korean ccTLD
"<company_name>" site:.kr OR site:.co.kr

# C-KR-2: Korean name if discoverable
<company_name_korean> 공식 홈페이지
```

Preferred engines: Google (primary), Naver (secondary if available).

## ccTLD Reference

| Country | ccTLD | Common 2nd-level |
|---|---|---|
| China | .cn | .com.cn, .org.cn |
| Japan | .jp | .co.jp, .or.jp, .ne.jp |
| South Korea | .kr | .co.kr, .or.kr |
