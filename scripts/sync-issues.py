import os, re, hashlib
from pathlib import Path
from github import Github

REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
GLOB = os.environ.get("LEAD_GLOB", "leads/lead-*.md")
TARGET = os.environ.get("TARGET_NAME", "hunt")
MODEL_FROM_FILENAME = os.environ.get("MODEL_FROM_FILENAME", "0") == "1"

g = Github(TOKEN)
repo = g.get_repo(REPO)

STOP = re.compile(r'^\[(HYP|PARKED|FINAL|NEXT|LEARN|RISK|NEW|CHANGED|PRIO)\]')
KV = re.compile(r'^([a-z_]+):\s*(.*)$', re.I)

def parse_blocks(text, model):
    blocks, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        m = re.match(r'^\[HYP\]\s*(.*)$', lines[i].strip())
        if not m:
            i += 1
            continue
        b = {"title": m.group(1).strip(), "model": model}
        j = i + 1
        while j < len(lines):
            l = lines[j].strip()
            if not l or STOP.match(l):
                break
            kv = KV.match(l)
            if kv:
                b[kv.group(1).lower()] = kv.group(2).strip()
            j += 1
        blocks.append(b)
        i = j
    return blocks

def norm_asset(a):
    a = (a or "").strip().lower().strip("`")
    a = re.sub(r'^((get|post|put|patch|delete|head|options)s?)[/,\s]+', '', a, flags=re.I)
    a = re.sub(r'\s*\(.*?\)', ' ', a)
    a = re.sub(r'[{}[\],].*$', '', a)
    a = re.sub(r'\s+', ' ', a).strip()
    return a[:120]

def fingerprint(b):
    a = norm_asset(b.get("asset", ""))
    c = (b.get("class", "OTHER") or "OTHER").strip().lower()[:20]
    return hashlib.md5(f"{a}|{c}".encode()).hexdigest()[:12]

def issue_fingerprint(iss):
    body = iss.body or ""
    m = re.search(r'^## Target\n`(.*)`', body, re.M)
    if not m:
        return None
    mc = re.search(r'^## Class\n(.*)$', body, re.M)
    a = norm_asset(m.group(1))
    c = (mc.group(1).strip().lower()[:20] if mc else "other")
    return hashlib.md5(f"{a}|{c}".encode()).hexdigest()[:12]

def ensure_label(name):
    color = {"pending": "d4c5f9", "false-positive": "7057ff", "verified": "0e8a16",
             "reported": "fbca04", "duplicate": "b60205",
             "high-confidence": "1d76db", "bug-bounty": "5319e7",
             "ai-hypothesis": "c5def5"}.get(name, "c2e0c6")
    try:
        repo.get_label(name)
    except Exception:
        repo.create_label(name, color)
        print("label created:", name)

def main():
    files = sorted(Path(".").glob(GLOB))
    print(f"processing {len(files)} files: {GLOB}")
    blocks = []
    for f in files:
        text = f.read_text(errors="ignore")
        mh = re.search(r'\(model\s+(\w+)\)', text)
        model = mh.group(1) if mh else ("unknown")
        if model == "unknown" and MODEL_FROM_FILENAME:
            mf = re.match(r'(\w+)', f.name)
            model = mf.group(1) if mf else "unknown"
        blocks += parse_blocks(text, model)
    print("hypothesis blocks:", len(blocks))

    confs = sorted({int(b.get("confidence", 0) or 0) // 10 * 10 for b in blocks})
    models = sorted({b["model"] for b in blocks})
    all_labels = ["bug-bounty", "ai-hypothesis", "pending", "false-positive", TARGET] \
        + [f"model-{m}" for m in models] + [f"confidence-{c}" for c in confs]
    for l in all_labels:
        ensure_label(l)

    try:
        existing = list(repo.get_issues(state="all", labels=["bug-bounty"]))
    except Exception:
        existing = list(repo.get_issues(state="all"))
    by_fp = {}
    for i in existing:
        fp = issue_fingerprint(i)
        if not fp:
            m = re.search(r'<!-- fingerprint:([0-9a-f]{12}) -->', i.body or "")
            fp = m.group(1) if m else None
        if fp:
            by_fp.setdefault(fp, []).append(i)
    print("existing issues:", len(existing))

    created = updated = 0
    for b in blocks:
        conf = int(b.get("confidence", 0) or 0)
        fp = fingerprint(b)
        title = f"[{conf}%] {b['title'][:90]}"
        labels = ["bug-bounty", "ai-hypothesis", "pending", TARGET,
                  f"model-{b['model']}", f"confidence-{conf//10*10}"] \
            + (["high-confidence"] if conf >= 80 else [])
        body = (f"<!-- fingerprint:{fp} -->\n\n"
                f"## Target\n`{b.get('asset','?')}`\n\n"
                f"## Class\n{b.get('class','OTHER')}\n\n"
                f"## Confidence\n{conf}/100\n\n"
                f"## Reasoning\n{b.get('reasoning','')}\n\n"
                f"## Evidence needed\n{b.get('evidence_needed','')}\n\n"
                f"## Verify steps\n{b.get('verify_steps','')}\n\n"
                f"## Impact\n{b.get('impact','')}\n\n"
                f"## Testability\n{b.get('testability','')}\n\n"
                f"_model: {b['model']} · auto-synced from {GLOB}_")
        if fp in by_fp:
            iss = by_fp[fp][0]
            cur = {l.name for l in iss.labels}
            new = set(labels) | cur
            if new != cur:
                iss.edit(labels=list(new))
                updated += 1
        else:
            repo.create_issue(title=title, body=body, labels=labels)
            created += 1

    rejected = []
    for f in files:
        text = f.read_text(errors="ignore")
        for m in re.finditer(r'^\[LEARN\]\s*REJECTED\s+\S+\s+@\s+(\S+)', text, re.M):
            rejected.append(m.group(1))
    closed = 0
    for iss in existing:
        if iss.state != "open":
            continue
        low = (iss.title + " " + (iss.body or "")).lower()
        if any(a.lower()[:30] in low for a in rejected):
            try:
                iss.edit(state="closed", labels=list({l.name for l in iss.labels} | {"false-positive"}))
                iss.create_comment("Closed automatically: this class was REJECTED for this asset by a later analyst run.")
                closed += 1
            except Exception:
                pass

    dup_closed = 0
    for fp, isslist in by_fp.items():
        if len(isslist) > 1:
            keep = min(isslist, key=lambda i: i.created_at)
            for dup in isslist:
                if dup != keep and dup.state == "open":
                    try:
                        dup.edit(state="closed", labels=list({l.name for l in dup.labels} | {"duplicate"}))
                        dup.create_comment(f"Duplicate of #{keep.number} (same normalized asset+class). Closed by sync.")
                        dup_closed += 1
                    except Exception:
                        pass

    def norm_title(t):
        t = re.sub(r'^\[\d+%\]\s*', '', t or "")
        t = re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
        return t

    title_closed = 0
    groups = {}
    for i in existing:
        if i.state != "open":
            continue
        key = (norm_title(i.title), (re.search(r'^## Class\n(.*)$', i.body or "", re.M) or [None, "other"])[1].strip().lower())
        groups.setdefault(key, []).append(i)
    for key, isslist in groups.items():
        if len(isslist) > 1:
            keep = min(isslist, key=lambda i: i.created_at)
            for dup in isslist:
                if dup != keep:
                    try:
                        dup.edit(state="closed", labels=list({l.name for l in dup.labels} | {"duplicate"}))
                        dup.create_comment(f"Duplicate of #{keep.number} (same normalized title+class). Closed by sync.")
                        title_closed += 1
                    except Exception:
                        pass

    print(f"SUMMARY created={created} updated={updated} closed_rejected={closed} dup_closed={dup_closed} title_closed={title_closed}")

main()
