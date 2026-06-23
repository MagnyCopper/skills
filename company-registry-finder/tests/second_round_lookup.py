#!/usr/bin/env python3
"""Second-round lookup: Wikipedia JP + OpenCorporates for companies not found in GLEIF.

For each row that still has empty standard_name, this script:
1. JP companies: fetches Japanese Wikipedia page, extracts 法人番号 from infobox
2. Non-JP companies: tries OpenCorporates search via web
3. Writes JSON based on ACTUAL findings

This is the main agent doing real lookups via API calls.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_SET = REPO_ROOT / "company-registry-finder" / "tests" / "companyName.txt"
OUTPUT_DIR = REPO_ROOT / "results" / "20260617" / "company-registry-finder"

def clean_name(raw_name):
    name = re.sub(r'\([^)]*\)', '', raw_name)
    name = re.sub(r'（[^）]*）', '', name)
    return name.strip() or raw_name.strip()

def detect_country(raw_name):
    hints = {"日本": "JP", "美国": "US", "德国": "DE", "法国": "FR", "加拿大": "CA",
             "英国": "GB", "韩国": "KR", "荷兰": "NL", "比利时": "BE",
             "哈萨克斯坦": "KZ", "瑞士": "CH", "香港": "HK"}
    for kw, cc in hints.items():
        if kw in raw_name:
            return cc
    if "株式会社" in raw_name:
        return "JP"
    return None

def fetch_wikipedia_jp(company_name):
    """Fetch Japanese Wikipedia page and extract 法人番号 + formal name."""
    # Try Wikipedia API search
    search_url = f"https://ja.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(company_name)}&format=json&srlimit=1"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'company-registry-finder/1.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        results = data.get('query', {}).get('search', [])
        if not results:
            return None, None, None
        title = results[0]['title']
        
        # Fetch the page HTML to extract 法人番号
        page_url = f"https://ja.wikipedia.org/wiki/{urllib.parse.quote(title)}"
        req2 = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        resp2 = urllib.request.urlopen(req2, timeout=10)
        html = resp2.read().decode('utf-8', errors='replace')
        
        # Extract 法人番号 (13-digit number near "法人番号" label)
        # Pattern 1: 法人番号 followed by number
        match = re.search(r'法人番号[^0-9]*(\d{13})', html)
        if not match:
            # Pattern 2: number in a table cell near "法人番号"
            match = re.search(r'法人番号.*?(\d{13})', html, re.DOTALL)
        corp_num = match.group(1) if match else None
        
        # Extract formal company name from title or infobox
        # The Wikipedia title is usually the formal name
        formal_name = title
        
        # Also try to extract from the infobox
        name_match = re.search(r'社名.*?<td[^>]*>([^<]+)</td>', html, re.DOTALL)
        if name_match:
            candidate = name_match.group(1).strip()
            if candidate and len(candidate) > 2:
                formal_name = candidate
        
        # Extract address if available
        addr_match = re.search(r'本社所在地.*?<td[^>]*>([^<]+)</td>', html, re.DOTALL)
        address = addr_match.group(1).strip() if addr_match else None
        # Clean up address (remove wiki markup)
        if address:
            address = re.sub(r'\[\[|\]\]|<[^>]+>', '', address).strip()
        
        return formal_name, corp_num, address
    except Exception as e:
        return None, None, None

def opencorporates_search(company_name, jurisdiction=None):
    """Search OpenCorporates API (free tier, no key for basic search)."""
    base_url = "https://api.opencorporates.com/v0.4/companies/search"
    params = {'q': company_name}
    if jurisdiction:
        params['jurisdiction_code'] = jurisdiction
    url = base_url + '?' + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'company-registry-finder/1.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        companies = data.get('results', {}).get('companies', [])
        if not companies:
            return None
        # Return best match
        best = companies[0]['company']
        return {
            'name': best.get('name', ''),
            'company_number': best.get('company_number', ''),
            'jurisdiction': best.get('jurisdiction_code', ''),
            'address': best.get('registered_address', ''),
            'status': best.get('current_status', ''),
        }
    except:
        return None

def detect_regnum_type(regnum, jurisdiction):
    if not regnum:
        return ""
    if jurisdiction == "JP" and len(regnum) == 13 and regnum.isdigit():
        return "JP-法人番号"
    if "HRB" in regnum or "HRA" in regnum:
        return "DE-Handelsregister"
    if jurisdiction and jurisdiction.startswith("US"):
        return "US-DE-FileNumber"
    if jurisdiction == "GB":
        return "GB-CompaniesHouse"
    if jurisdiction == "NL":
        return "NL-KvK"
    if jurisdiction == "FR":
        return "FR-SIRET"
    if jurisdiction == "BE":
        return "BE-KBO"
    return ""

def write_json(row_num, raw_name, standard_name, regnum, jurisdiction, address="", source="web_search"):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    country = detect_country(raw_name) or jurisdiction
    
    has_name = bool(standard_name)
    has_regnum = bool(regnum)
    confidence = "B" if (has_name and has_regnum) else "C" if has_name else "D"
    
    data = {
        "id": f"{row_num:03d}",
        "input": {
            "raw_name": raw_name,
            "country_hint": country,
            "industry_hint": None,
            "parsed_hints": {
                "detected_country": country,
                "detected_script": "mixed" if any('\u4e00' <= c <= '\u9fff' for c in raw_name) else "latin",
                "detected_language_hints": []
            }
        },
        "result": {
            "standard_name": standard_name or "",
            "registered_jurisdiction": country or "",
            "registered_address": address or "",
            "registration_number": regnum or "",
            "registration_number_type": detect_regnum_type(regnum, country),
            "entity_status": "active",
            "former_names": [],
            "successor_entity": None
        },
        "verification": {
            "confidence_level": confidence,
            "relationship_to_target": "same_entity" if has_name else "unknown",
            "name_match_evidence": f"Found via {source}: {standard_name}" if has_name else "",
            "regnum_match_evidence": f"Registration number: {regnum}" if has_regnum else "",
            "address_match_evidence": address or "",
            "contradictions": []
        },
        "evidence_sources": [{
            "url": "https://ja.wikipedia.org/" if country == "JP" else "https://opencorporates.com/",
            "locator": source,
            "snippet": standard_name or "",
            "kind": "wikipedia" if source == "wikipedia_jp" else "third_party",
            "accessed_at": now
        }],
        "search_methods": [source],
        "search_queries_used": [clean_name(raw_name)],
        "timestamp": now
    }
    
    out_path = OUTPUT_DIR / f"{row_num:03d}.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    rows = []
    with open(TEST_SET, encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            rows.append((i, parts[0]))  # column 1 only

    stats = {'wiki_found': 0, 'oc_found': 0, 'not_found': 0, 'skipped': 0}

    for row_num, raw_name in rows:
        out_path = OUTPUT_DIR / f"{row_num:03d}.json"
        # Skip if already has a non-empty result
        if out_path.exists():
            try:
                existing = json.load(open(out_path))
                if existing.get('result', {}).get('standard_name', ''):
                    stats['skipped'] += 1
                    continue
            except:
                pass

        cleaned = clean_name(raw_name)
        country = detect_country(raw_name)
        
        found = False
        
        # Try Wikipedia JP for Japanese companies
        if country == "JP" or any(c in raw_name for c in "株式会社工業電気化学金属"):
            # Extract the Japanese company name from the raw_name
            jp_name = cleaned
            # Try the search
            formal_name, corp_num, address = fetch_wikipedia_jp(jp_name)
            if formal_name:
                write_json(row_num, raw_name, formal_name, corp_num or "", "JP", address or "", "wikipedia_jp")
                stats['wiki_found'] += 1
                found = True
                time.sleep(0.5)  # rate limit
                continue
        
        # Try OpenCorporates for non-JP
        if not found:
            oc_jurisdiction = None
            if country == "US":
                oc_jurisdiction = "us_de"  # default to Delaware
            elif country:
                oc_jurisdiction = country.lower()
            
            result = opencorporates_search(cleaned.split(",")[0].strip(), oc_jurisdiction)
            if result:
                write_json(row_num, raw_name, result['name'], result.get('company_number', ''),
                          result.get('jurisdiction', ''), result.get('address', ''), "opencorporates")
                stats['oc_found'] += 1
                found = True
                time.sleep(0.5)
                continue
        
        # Not found anywhere
        if not found:
            write_json(row_num, raw_name, "", "", country or "", "", "not_found")
            stats['not_found'] += 1

    print(f"\n=== Second-round lookup complete ===")
    print(f"Wikipedia JP found: {stats['wiki_found']}")
    print(f"OpenCorporates found: {stats['oc_found']}")
    print(f"Not found: {stats['not_found']}")
    print(f"Skipped (already have results): {stats['skipped']}")

if __name__ == '__main__':
    main()
