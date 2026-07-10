# NexGen Agent Skills

Production-ready AI agent skills for business automation.

**Verified • Audited • Battle-tested**

---

## 🛡️ Security Guarantee

Every skill in this repository has passed our **Security Audit**:

- ✅ GitHub repo origin only
- ✅ Owner verified organization OR ≥10k stars with healthy ratio
- ✅ No eval/exec/backdoors/malware
- ✅ MIT/Apache/BSD license only
- ✅ Stars-to-watchers ratio ≤50:1 (no bought stars)

Use the auditor:
```bash
python3 tools/audit_skill.py <repo_url>
```

---

## 🎯 The 7 Business Agents

Each department has a core agent that coordinates related skills:

| Agent | Skills | What It Does |
|---|---|---|
| **Sales Agent** | ICP Research • Lead Sourcing • Cold Email • Sequencing | Finds, qualifies, and books meetings |
| **Deals Agent** | Proposal Writer • Call Prep • Contract Mgmt • Pipeline | Closes and manages active opportunities |
| **Marketing Agent** | Content Creation • Social Media • SEO • Analytics | Produces and distributes content |
| **Operations Agent** | Onboarding • Project Mgmt • Reliability • SOPs | Runs the business |
| **Intelligence Agent** | Market Signals • Competitor Intel • People Intel | Watches for opportunities |
| **Customer Agent** | Support Tickets • Community • Success • Voice | Serves clients and users |
| **Back Office Agent** | Invoicing • Hiring • Legal • Records | Handles admin and compliance |

---

## 🚀 Installation

### Into Hermes Agent (Recommended)
```bash
# Copy SKILL.md to your skills folder
cp skills/sales/icp-definition.md ~/.hermes/skills/
# In Hermes session:
/skill icp-definition
```

### Using the Auditor First
```bash
# Verify any skill before installing
python3 tools/audit_skill.py https://github.com/sickn33/agentic-awesome-skills
# {"passed": false, "score": 52, ...}
```

---

## 📊 Current Skills

### Sales (3)
- `icp-definition.md` — Ideal Customer Profile research
- `lead-sourcing.md` — Prospect list generation
- `cold-email.md` — Personalized outreach sequences

### Customer (1)
- `support-tickets.md` — Support inbox automation

### Marketing (1)
- `content-creation.md` — Multi-platform content engine

### Operations (1)
- `onboarding.md` — Client kickoff automation

### Intelligence (1)
- `signals.md` — Market event monitoring

### Back Office (1)
- `invoicing.md` — Invoice generation and collections

---

## 🏗️ Roadmap

- [ ] Deals agent skills (proposal, contracts)
- [ ] Full LinkedIn scraping integration
- [ ] Stripe/QuickBooks live connectors
- [ ] Community skills (contribution process)
- [ ] Skill compatibility matrix

---

## License

MIT — Free to use, modify, and deploy in your agents.