import os, re, hashlib
from difflib import SequenceMatcher
from pathlib import Path
from github import Github

REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
GLOB = os.environ.get("LEAD_GLOB", "leads/lead-*.md")
TARGET = os.environ.get("TARGET_NAME", "hunt")
MODEL_FROM_FILENAME = os.environ.get("MODEL_FROM_FILENAME", "0") == "1"

STOP = re.compile(r'^\[(HYP|PARKED|FINAL|NEXT|LEARN|RISK|NEW|CHANGED|PRIO)\]')
KV = re.compile(r'^([a-z_]+):\s*(.*)$', re.I)

TITLE_SIM_THRESHOLD = float(os.environ.get("TITLE_SIM_THRESHOLD", "0.82"))
COARSE_SIM_THRESHOLD = float(os.environ.get("COARSE_SIM_THRESHOLD", "0.55"))


def split_inline(title):
    """Extract inline attributes from a single-line lead of the form:
    [HYP] Title: confidence 96, class MISCONFIG, verify_steps ..., asset https://...
    Attribute matches are removed; the title is cut at the first attribute."""
    attrs = {}
    pats = [
        (r'confidence\s*(?:=|:|\s+)\s*(\d{1,3})', 'confidence', None),
        (r'conf\s*(?:=|:|\s+)\s*(\d{1,3})', 'confidence', None),
        (r'\((\d{2,3})\)\s*[:;]', 'confidence', None),
        (r'class\s*(?:=|:|\s+)\s*([A-Za-z_]+)', 'class', str.upper),
        (r'asset\s*(?:=|:|\s+)\s*(https?://[^\s,;]+|/[^\s,;]+)', 'asset', None),
        (r'severity\s*(?:=|:|\s+)\s*([A-Za-z]+)', 'severity', None),
        (r'testability\s*(?:=|:|\s+)\s*([A-Za-z_]+)', 'testability', str.upper),
        (r'verify[_\s]steps\s*(?:=|:|\s+)\s*([^\n|]+)', 'verify_steps', None),
        (r'impact\s*(?:=|:|\s+)\s*([^\n|]+)', 'impact', None),
        (r'reasoning\s*(?:=|:|\s+)\s*([^\n|]+)', 'reasoning', None),
    ]
    cut = None
    for pat, key, transform in pats:
        m = re.search(pat, title, re.I)
        if m:
            v = m.group(1).strip()
            if transform:
                v = transform(v)
            if key not in attrs:
                attrs[key] = v
            cut = m.start() if cut is None else min(cut, m.start())
    if cut is not None:
        t = title[:cut]
    else:
        t = title
    t = re.sub(r'^\s*[:,\s-]+\s*', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t, attrs


def parse_blocks(text, model):
    blocks, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        m = re.match(r'^\[HYP\]\s*(.*)$', lines[i].strip())
        if not m:
            i += 1
            continue
        raw_title = m.group(1).strip()
        b = {"title": raw_title, "model": model}
        j = i + 1
        while j < len(lines):
            l = lines[j].strip()
            if not l or STOP.match(l):
                break
            kv = KV.match(l)
            if kv:
                b[kv.group(1).lower()] = kv.group(2).strip()
            j += 1
        if "<" not in str(raw_title):
            if not any(k in b for k in ('class', 'asset', 'confidence', 'reasoning', 'verify_steps')):
                clean, attrs = split_inline(raw_title)
                b['title'] = clean
                for k, v in attrs.items():
                    b.setdefault(k.lower(), v)
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


def coarse_target(a):
    """Bare scheme+host+path of an asset (drops credentials, queries, parens)."""
    a = (a or "").strip().lower()
    a = re.sub(r'^`+|`+$', '', a)
    a = re.sub(r'^\[(get|post|put|patch|delete|head|options)s?\][\s,]+', '', a)
    m = re.match(r'^(?:https?://)?([^/\s()]+)(/[^\s()]*)?', a)
    if not m:
        return ""
    host, path = m.group(1), m.group(2) or ""
    host = re.sub(r'^www\.', '', host)
    path = path.rstrip('/')
    return host + path if path and path != "/" else host

def norm_title(t):
    t = re.sub(r'^\[\d+%\]\s*', '', t or "")
    t = re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
    return t


def fingerprint(b):
    a = norm_asset(b.get("asset", ""))
    c = (b.get("class", "OTHER") or "OTHER").strip().lower()[:20]
    if a:
        return hashlib.md5(f"{a}|{c}".encode()).hexdigest()[:12]
    # no asset -> include normalized title so distinct leads get distinct fps
    t = norm_title(b.get("title", ""))
    return hashlib.md5(f"{t}|{c}".encode()).hexdigest()[:12]


def issue_fingerprint(iss):
    """Return the canonical fingerprint for an existing issue.

    The stored <!-- fingerprint:xxx --> comment is the single source of
    truth: it was computed from the original lead and is stable across
    runs. Only fall back to recomputing from the body for issues created
    before the comment existed."""
    body = iss.body or ""
    m = re.search(r'<!-- fingerprint:([0-9a-f]{12}) -->', body)
    if m:
        return m.group(1)
    m = re.search(r'^## Target\n`(.*)`', body, re.M)
    if not m:
        return None
    mc = re.search(r'^## Class\n(.*)$', body, re.M)
    a = norm_asset(m.group(1))
    c = (mc.group(1).strip().lower()[:20] if mc else "other")
    if a:
        return hashlib.md5(f"{a}|{c}".encode()).hexdigest()[:12]
    mt = re.search(r'^## Title\n(.*)$', body, re.M)
    t = norm_title(mt.group(1) if mt else "")
    return hashlib.md5(f"{t}|{c}".encode()).hexdigest()[:12]


def ensure_label(repo, name):
    color = {"pending": "d4c5f9", "false-positive": "7057ff", "verified": "0e8a16",
             "reported": "fbca04", "duplicate": "b60205",
             "high-confidence": "1d76db", "bug-bounty": "5319e7",
             "ai-hypothesis": "c5def5"}.get(name, "c2e0c6")
    try:
        repo.get_label(name)
    except Exception:
        repo.create_label(name, color)
        print("label created:", name)


def best_title_match(block, issues, by_title_index):
    """Fuzzy-match a drifted no-asset lead against open issues.

    Returns the issue whose normalized title is most similar to the
    block title (same class, above TITLE_SIM_THRESHOLD), or None."""
    bt = norm_title(block.get("title", ""))
    if not bt:
        return None
    bc = (block.get("class", "OTHER") or "OTHER").strip().lower()[:20]
    best, best_ratio = None, 0.0
    for iss in issues:
        i_class = "other"
        mc = re.search(r'^## Class\n(.*)$', iss.body or "", re.M)
        if mc:
            i_class = mc.group(1).strip().lower()[:20]
        if i_class != bc:
            continue
        it = norm_title(iss.title)
        if not it:
            continue
        r = SequenceMatcher(None, bt, it).ratio()
        if r > best_ratio:
            best, best_ratio = iss, r
    if best and best_ratio >= TITLE_SIM_THRESHOLD:
        return best
    return None


def coarse_match(b, all_issues):
    """Same target+class and similar title (>= COARSE_SIM_THRESHOLD) ->
    treat as the same finding, even if the stored issue is closed."""
    bt = norm_title(b.get("title", ""))
    if not bt:
        return None
    ctarget = coarse_target(b.get("asset", ""))
    if not ctarget:
        return None
    bc = (b.get("class", "OTHER") or "OTHER").strip().lower()[:20]
    best, best_ratio = None, 0.0
    for iss in all_issues:
        m = re.search(r'^## Target\n`(.*)`', iss.body or "", re.M)
        if not m:
            continue
        if coarse_target(m.group(1)) != ctarget:
            continue
        mc = re.search(r'^## Class\n(.*)$', iss.body or "", re.M)
        i_class = (mc.group(1).strip().lower()[:20] if mc else "other")
        if i_class != bc:
            continue
        r = SequenceMatcher(None, bt, norm_title(iss.title)).ratio()
        if r > best_ratio:
            best, best_ratio = iss, r
    if best and best_ratio >= COARSE_SIM_THRESHOLD:
        return best
    return None

def main():
    g = Github(TOKEN)
    repo = g.get_repo(REPO)
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


    def _conf(b):
        v = b.get("confidence", 0) or 0
        try:
            return int(v)
        except (ValueError, TypeError):
            try:
                return int(float(v))
            except (ValueError, TypeError):
                return 0

    confs = sorted({_conf(b) // 10 * 10 for b in blocks})
    models = sorted({b["model"] for b in blocks})
    all_labels = ["bug-bounty", "ai-hypothesis", "pending", "false-positive", TARGET] \
        + [f"model-{m}" for m in models] + [f"confidence-{c}" for c in confs]
    for l in all_labels:
        ensure_label(repo, l)

    try:
        existing = list(repo.get_issues(state="all", labels=["bug-bounty"]))
    except Exception:
        existing = list(repo.get_issues(state="all"))
    by_fp = {}
    for i in existing:
        fp = issue_fingerprint(i)
        if fp:
            by_fp.setdefault(fp, []).append(i)
    open_issues = [i for i in existing if i.state == "open"]
    closed_issues = [i for i in existing if i.state != "open"]
    print("existing issues:", len(existing), "open:", len(open_issues))

    # in-run dedup: same fingerprint multiple times in this batch -> keep first
    seen_fp = set()
    uniq_blocks = []
    for b in blocks:
        fp = fingerprint(b)
        if fp not in seen_fp:
            seen_fp.add(fp)
            uniq_blocks.append(b)
    if len(uniq_blocks) != len(blocks):
        print(f"in-run dedup: {len(blocks)} -> {len(uniq_blocks)}")

    created = updated = 0
    fuzzy_matched = 0
    for b in uniq_blocks:
        conf = _conf(b)
        fp = fingerprint(b)
        title = f"[{conf}%] {b['title'][:90]}"
        labels = ["bug-bounty", "ai-hypothesis", "pending", TARGET,
                  f"model-{b['model']}", f"confidence-{conf//10*10}"] \
            + (["high-confidence"] if conf >= 80 else [])
        body = (f"<!-- fingerprint:{fp} -->\n\n"
                f"## Title\n{b.get('title','')}\n\n"
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
            # no exact fingerprint match: try fuzzy title match against
            # open issues before creating a duplicate (handles title drift
            # in asset-less leads across model runs)
            match = best_title_match(b, open_issues, None)
            if match is not None:
                cur = {l.name for l in match.labels}
                new = set(labels) | cur
                if new != cur:
                    match.edit(labels=list(new))
                try:
                    match.create_comment(
                        f"Fuzzy-matched to lead (title similarity ≥ {TITLE_SIM_THRESHOLD}). "
                        "No new issue created. If this is a genuinely different finding, "
                        "reword the title so it differs in the first ~6 words.")
                except Exception:
                    pass
                fuzzy_matched += 1
                continue
            # re-discovery of a CLOSED (rejected/duplicate) finding with a
            # drifted asset field: same title+class -> do not re-create
            closed_match = best_title_match(b, closed_issues, None)
            if closed_match is not None:
                try:
                    closed_match.create_comment(
                        "Re-discovered in a later analyst lead; kept closed (title matched "
                        f"a previously closed issue at similarity ≥ {TITLE_SIM_THRESHOLD}).")
                except Exception:
                    pass
                fuzzy_matched += 1
                continue
            # same bare target+class with a similar title -> duplicate
            coarse = coarse_match(b, existing)
            if coarse is not None:
                cur = {l.name for l in coarse.labels}
                new = set(labels) | cur
                if new != cur:
                    try:
                        coarse.edit(labels=list(new))
                    except Exception:
                        pass
                try:
                    coarse.create_comment(
                        f"Coarse-matched to {('#' + str(coarse.number)) if coarse.number else 'issue'} "
                        f"(same target+class, title similarity ≥ {COARSE_SIM_THRESHOLD}). "
                        "No new issue created.")
                except Exception:
                    pass
                fuzzy_matched += 1
                continue
            repo.create_issue(title=title, body=body, labels=labels)
            created += 1

    confirmed_assets = []
    for f in files:
        text = f.read_text(errors="ignore")
        for m in re.finditer(r'^\[CONFIRMED\]\s*(.*)$', text, re.M):
            confirmed_assets.append(m.group(1).strip())
    confirmed_low = ' '.join(a.lower() for a in confirmed_assets)

    verified_now = 0
    for iss in existing:
        if iss.state != "open":
            continue
        if "verified" in {l.name for l in iss.labels}:
            continue
        low = (iss.title + " " + (iss.body or "")).lower()
        if confirmed_low and (any(a and a.lower()[:40] in low for a in confirmed_assets) or confirmed_low[:40] in low):
            try:
                iss.edit(labels=list({l.name for l in iss.labels} | {"verified"}))
                iss.create_comment("Auto-verified: [CONFIRMED] evidence present in latest analyst lead.")
                verified_now += 1
            except Exception:
                pass
    print(f"auto-verified issues: {verified_now}")

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
            keep = min(isslist, key=lambda i: i.number)
            for dup in isslist:
                if dup != keep and dup.state == "open":
                    try:
                        dup.edit(state="closed", labels=list({l.name for l in dup.labels} | {"duplicate"}))
                        dup.create_comment(f"Duplicate of #{keep.number} (same normalized asset+class). Closed by sync.")
                        dup_closed += 1
                    except Exception:
                        pass

    title_closed = 0
    groups = {}
    for i in existing:
        if i.state != "open":
            continue
        key = (norm_title(i.title), (re.search(r'^## Class\n(.*)$', i.body or "", re.M) or [None, "other"])[1].strip().lower())
        groups.setdefault(key, []).append(i)
    for key, isslist in groups.items():
        if len(isslist) > 1:
            keep = min(isslist, key=lambda i: i.number)
            for dup in isslist:
                if dup != keep:
                    try:
                        dup.edit(state="closed", labels=list({l.name for l in dup.labels} | {"duplicate"}))
                        dup.create_comment(f"Duplicate of #{keep.number} (same normalized title+class). Closed by sync.")
                        title_closed += 1
                    except Exception:
                        pass

    print(f"SUMMARY created={created} updated={updated} fuzzy_matched={fuzzy_matched} "
          f"closed_rejected={closed} dup_closed={dup_closed} title_closed={title_closed}")

if __name__ == "__main__":
    main()
