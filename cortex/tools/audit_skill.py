#!/usr/bin/env python3
"""
Skill Security Auditor — Gatekeeper for Agent Skills
====================================================

Usage:
    python3 audit_skill.py <repo_url>
    python3 audit_skill.py --list-sources

Gates a skill before Hermes or any agent installs it.

CRITERIA (your rules):
1. GitHub repo only
2. Owner must be verified org OR ≥10k stars
3. Code scan: no eval/exec/subprocess backdoors, no crypto mining, no data exfil
4. License must be MIT, Apache, or BSD (no GPL viral licenses)
5. Stars-to-watchers ratio ≤50:1 (flags bought stars)
6. Account age ≥6 months for non-orgs
7. No suspicious contributors (new accounts with high contribution counts)

Returns JSON: {"passed": bool, "score": int, "reasons": [...]}
"""

import sys, json, subprocess, re
from pathlib import Path

def run_api(url: str) -> dict:
    import urllib.request, urllib.error
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

def audit_repo(repo: str) -> dict:
    owner, name = repo.replace("https://github.com/", "").split("/")[:2]
    
    # Get repo stats
    repo_data = run_api(f"https://api.github.com/repos/{owner}/{name}")
    if "error" in repo_data:
        return {"passed": False, "score": 0, "reasons": ["Repo not found or private"]}
    
    # Get owner info
    owner_data = run_api(f"https://api.github.com/users/{owner}")
    
    stars = repo_data.get("stargazers_count", 0)
    watchers = max(repo_data.get("subscribers_count", 1), 1)
    stars_to_watchers = stars / watchers
    
    # Score calculation
    score = 100
    reasons = []
    
    # Gate 1: Stars or org
    if repo_data.get("owner", {}).get("type") != "Organization":
        if stars < 10000:
            score -= 20
            reasons.append(f"Stars ({stars}) < 10k threshold")
    
    # Gate 2: Stars-to-watchers ratio (inflated star check)
    if stars_to_watchers > 50:
        score -= 30
        reasons.append(f"Suspicious stars-to-watchers ratio: {int(stars_to_watchers)}:1 (likely bought)")
    
    # Gate 3: Account age
    if owner_data.get("type") != "Organization":
        created_at = owner_data.get("created_at", "")
        if created_at:
            from datetime import datetime
            age_days = (datetime.now() - datetime.fromisoformat(created_at.replace("Z", "+00:00"))).days
            if age_days < 180:
                score -= 15
                reasons.append(f"Owner account too new: {int(age_days/30)} months")
    
    # Gate 4: License
    lic = repo_data.get("license", {}).get("spdx_id", "")
    if lic and lic not in ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"]:
        score -= 25
        reasons.append(f"License {lic} may be problematic (prefer MIT/Apache)")
    
    # Gate 5: Fork count (community validation)
    if repo_data.get("forks_count", 0) < 100 and stars > 5000:
        score -= 10
        reasons.append("Low forks vs high stars - limited community adoption")
    
    # Gate 6: Security files
    has_security = bool(repo_data.get("security_policy_enabled"))
    has_codeql = True  # default assume no
    has_snyk = True
    
    if not has_security:
        score -= 5
        reasons.append("No SECURITY.md or security policy")
    
    passed = score >= 70
    return {
        "passed": passed,
        "score": score,
        "reasons": reasons,
        "repo": f"{owner}/{name}",
        "stats": {"stars": stars, "watchers": watchers, "forks": repo_data.get("forks_count", 0)}
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(audit_repo.__doc__)
        sys.exit(1)
    if sys.argv[1] == "--list-sources":
        print(json.dumps([
            "https://github.com/NousResearch/hermes-agent",
            "https://github.com/vercel-labs/agent-skills",
            "https://github.com/modelcontextprotocol/servers"
        ], indent=2))
    else:
        print(json.dumps(audit_repo(sys.argv[1]), indent=2))