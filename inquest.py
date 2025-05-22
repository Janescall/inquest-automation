import requests
import urllib3
import json
import sys
import re

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 제외할 문자열 (artifact에 포함 시 제거)
excluded_artifacts = {
    "safelinks.protection.outlook.com", "t.me", "40.113.110.67", "s.go-mpulse.net", "openai.com",
    "www.googletagmanager.com", "google.com", "storage.googleapis.com", "docs.fortinet.com",
    "www.bilibili.com", "www.adobe.com", "x.com", "8.8.8.8", "www.msftconnecttest.com",
    "raw.github.com", "d4a0fe56316a2c45b9ba9ac1005363309a3edc7acf9e4df64d326a0ff273e80f",
    "157.240.215.174", "bd2c2cf0631d881ed382817afcce2b093f4e412ffb170a719e2762f250abfea4",
    "github.com", "marketplace.visualstudio.com", "www.baidu.com", "www.sogou.com", "www.w3.org",
    "www.clarity.ms", "www.instagram.com", "1.1.1.1", "th.bing.com", "steamcommunity.com",
    "bitbucket.org", "oauth2.googleapis.com", "forms.office.com", "huggingface.co", "wix.com"
}

# 제외할 타입
excluded_types = {"yarasignature", "url"}

# 요청
response = requests.get("https://labs.inquest.net/api/iocdb/list", verify=False)
response.raise_for_status()
json_data = response.json()

items = json_data.get("data", [])
seen_artifacts = set()
filtered_data = []

# 필터링
for item in items:
    if not isinstance(item, dict):
        continue

    artifact_type = item.get("artifact_type", "").lower()
    artifact = item.get("artifact", "").lower()

    if artifact_type in excluded_types:
        continue
    if any(excluded in artifact for excluded in excluded_artifacts):
        continue
    if artifact in seen_artifacts:
        continue

    seen_artifacts.add(artifact)

    if "reference_text" in item:
        item["reference_text"] = re.sub(r'\s+', ' ', item["reference_text"]).strip()

    filtered_data.append(item)

# 저장 경로 및 파일 생성
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "inquest_feed.json")

# 결과를 한 줄로 저장 (minified JSON)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_result, f, ensure_ascii=False, separators=(',', ':'))
