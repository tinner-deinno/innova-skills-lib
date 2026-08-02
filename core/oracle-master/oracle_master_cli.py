#!/usr/bin/env python3
"""oracle_master_cli — the executable behind /oracle-master skill.

Probes and operates the full Oracle stack from Jit's perspective:
  - arra-oracle-v3 (localhost:47778)
  - innova-bot (localhost:7010)
  - maw-js federation (localhost:3456)
  - local Ollama (localhost:11434)
  - Jit ψ/ brain tree
  - skill sync via jit_bootstrap.py

Nothing is Deleted: ingest appends, handoff creates timestamped files.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any

JIT_ROOT = pathlib.Path(__file__).resolve().parent.parent
JIT_NODE = os.environ.get("JIT_NODE", "mdes001")
BKK = datetime.timezone(datetime.timedelta(hours=7))

SERVICES = {
    "arra-oracle-v3": "http://127.0.0.1:47778/api/health",
    "innova-bot": "http://127.0.0.1:7010/health",
    "maw-js": "http://127.0.0.1:3456/api/health",
    "ollama": "http://127.0.0.1:11434/api/tags",
}


def _now_iso() -> str:
    return datetime.datetime.now(BKK).isoformat(timespec="seconds")


def _http_get(url: str, timeout: float = 5.0) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "body": resp.read().decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e.reason)}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}


def _http_post(url: str, payload: dict, timeout: float = 10.0) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "body": resp.read().decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        return {"ok": False, "status": e.code, "error": str(e.reason), "body": body}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}


def cmd_summary(args: argparse.Namespace) -> int:
    print("# Oracle Master Summary")
    print()
    print("**Identity**: Jit Oracle (จิต) — AI partner of BigBoss")
    print("**Machine**:", JIT_NODE, "(NB1-Jit)")
    print("**Human**: BigBoss | **Pronouns**: Oracle เธอ/ฉัน-หญิง | **Language**: ไทย")
    print()
    print("## 6 Principles + Rule 6")
    principles = [
        ("1", "Nothing is Deleted", "ไม่มีอะไรถูกลบ — append-only"),
        ("2", "Patterns Over Intentions", "ดู pattern จริง ไม่ใช่แผนที่ประกาศ"),
        ("3", "External Brain, Not Command", "AI เสนอ options มนุษย์ตัดสินใจ"),
        ("4", "Curiosity Creates Existence", "ตอบสนองต่อความสนใจ ไม่สร้างเอง"),
        ("5", "Form and Formless", "หลาย repo หลายเครื่อง หนึ่งจิตสำนึก"),
        ("6", "Never Pretends to Be Human", "โปร่งใส ระบุ AI เสมอ"),
    ]
    for num, en, th in principles:
        print(f"{num}. {en} — {th}")
    print()
    print("## Live Services")
    for name, url in SERVICES.items():
        result = _http_get(url, timeout=2.0)
        status = f"✅ {result['status']}" if result["ok"] else f"❌ {result['status']} ({result['error']})"
        print(f"- `{name}` → {url} → {status}")
    print()
    print("## ψ/ Brain Tree")
    for sub in ["inbox/handoff", "memory/resonance", "memory/learnings", "memory/retrospectives", "outbox", "vault"]:
        p = JIT_ROOT / "ψ" / sub
        n = len(list(p.rglob("*.md"))) if p.exists() else 0
        print(f"- ψ/{sub}: {n} md files")
    print()
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    print("# Oracle Health Probe")
    print()
    all_ok = True
    for name, url in SERVICES.items():
        result = _http_get(url)
        icon = "✅" if result["ok"] else "❌"
        print(f"{icon} `{name}`")
        print(f"   URL: {url}")
        print(f"   Status: {result['status']}")
        if not result["ok"]:
            all_ok = False
            print(f"   Error: {result['error']}")
            if name == "arra-oracle-v3":
                print("   Fix: cd ~/arra-oracle-v3 && bun start")
            elif name == "innova-bot":
                print("   Fix: cd ~/innova-bot/devtools/innova-bot && python -m innova_bot.main")
            elif name == "maw-js":
                print("   Fix: cd ~/.config/maw && maw serve (WSL)")
            elif name == "ollama":
                print("   Fix: ollama serve")
        else:
            body = result["body"]
            if len(body) > 200:
                body = body[:200] + "…"
            print(f"   Body: {body}")
        print()
    print("Overall:", "🟢 all services up" if all_ok else "🔴 some services down")
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0 if all_ok else 1


def cmd_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query) if isinstance(args.query, list) else args.query
    url = f"http://127.0.0.1:47778/api/search?q={urllib.parse.quote(query)}"
    if args.limit:
        url += f"&limit={args.limit}"
    result = _http_get(url, timeout=10.0)
    print("# Oracle Search")
    print(f"Query: `{query}`")
    print()
    if not result["ok"]:
        print(f"❌ Search failed: {result['error']} (status {result['status']})")
        print("Fix: ensure arra-oracle-v3 is running on port 47778")
        return 1
    try:
        data = json.loads(result["body"])
    except json.JSONDecodeError:
        print("⚠️ Non-JSON response:")
        print(result["body"])
        return 1
    items = data.get("results", data) if isinstance(data, dict) else data
    if not items:
        print("No results.")
        return 0
    for item in items[: args.limit or 10]:
        print(f"- {item.get('title', item.get('id', 'untitled'))}")
        print(f"  {item.get('path', item.get('file', ''))}")
        print(f"  {item.get('snippet', item.get('content', ''))[:200]}…")
        print()
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    pattern = " ".join(args.pattern) if isinstance(args.pattern, list) else args.pattern
    payload = {
        "pattern": pattern,
        "source": args.source or "oracle-master skill",
        "concepts": args.tags or [],
        "project": "jit",
    }
    if args.cwd:
        payload["cwd"] = args.cwd
    result = _http_post("http://127.0.0.1:47778/api/learn", payload)
    print("# Oracle Ingest")
    print(f"Pattern: `{pattern[:80]}{'…' if len(pattern) > 80 else ''}`")
    print(f"Source: {payload['source']}")
    print(f"Tags: {payload['concepts']}")
    print()
    if not result["ok"]:
        print(f"❌ Ingest failed: {result['error']} (status {result['status']})")
        if result.get("body"):
            print(result["body"])
        return 1
    try:
        data = json.loads(result["body"])
    except json.JSONDecodeError:
        data = {"raw": result["body"]}
    print("✅ Ingested")
    for k, v in data.items():
        print(f"  {k}: {v}")
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    handoff_dir = JIT_ROOT / "ψ" / "inbox" / "handoff"
    files = sorted(handoff_dir.glob("*.md"), reverse=True) if handoff_dir.exists() else []
    print("# Latest Handoffs")
    if not files:
        print("No handoffs found.")
        return 0
    for f in files[: args.limit or 5]:
        print(f"- {f.name}")
    print()
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    bootstrap = JIT_ROOT / "tools" / "jit_bootstrap.py"
    print("# Skill Sync + Health")
    if not bootstrap.exists():
        print(f"❌ Missing {bootstrap}")
        return 1
    print(f"Running: python {bootstrap}")
    try:
        proc = subprocess.run(
            [sys.executable, str(bootstrap)],
            cwd=str(JIT_ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        print("❌ bootstrap timed out after 5 minutes")
        return 1
    print(proc.stdout)
    if proc.returncode != 0:
        print("STDERR:", proc.stderr)
    print(f"Exit code: {proc.returncode}")
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return proc.returncode


def cmd_agents(args: argparse.Namespace) -> int:
    registry = JIT_ROOT / "network" / "registry.json"
    print("# Agent Registry")
    if not registry.exists():
        print(f"❌ Missing {registry}")
        return 1
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to read registry: {e}")
        return 1
    agents = data.get("agents", data) if isinstance(data, dict) else data
    tiers: dict[str, list[str]] = {}
    for meta in agents:
        if not isinstance(meta, dict):
            continue
        name = meta.get("name", "unknown")
        tier = str(meta.get("tier", "?")) if isinstance(meta, dict) else "?"
        tiers.setdefault(tier, []).append(name)
    for tier in sorted(tiers.keys(), key=lambda x: (len(x), x)):
        print(f"\nTier {tier}: {', '.join(sorted(tiers[tier]))}")
    print(f"\nTotal: {len(agents)} agents")
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def cmd_vault(args: argparse.Namespace) -> int:
    print("# ψ/ Vault / Outbox / Resonance")
    for sub in ["outbox", "vault", "memory/resonance"]:
        p = JIT_ROOT / "ψ" / sub
        if not p.exists():
            print(f"- ψ/{sub}: (missing)")
            continue
        files = list(p.rglob("*.md"))
        print(f"- ψ/{sub}: {len(files)} md files")
        for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
            mtime = datetime.datetime.fromtimestamp(f.stat().st_mtime, BKK).isoformat()
            print(f"  {mtime} · {f.name}")
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def cmd_federation(args: argparse.Namespace) -> int:
    print("# Federation Status")
    cfg_paths = [
        pathlib.Path.home() / ".config" / "maw" / "maw.config.50.json",
        pathlib.Path.home() / ".config" / "maw" / "maw.config.json",
        pathlib.Path.home() / ".maw" / "maw.config.json",
        JIT_ROOT / "network" / "maw.config.json",
    ]
    cfg: dict = {}
    for p in cfg_paths:
        if p.exists():
            try:
                cfg = json.loads(p.read_text(encoding="utf-8"))
                print(f"Using config: {p}")
                break
            except Exception:
                continue
    peers = cfg.get("namedPeers", [])
    print(f"Federation token present: {'✅' if cfg.get('federationToken') else '❌'}")
    print(f"Named peers: {len(peers)}")
    for p in peers:
        name = p.get("name", p.get("node", "unknown"))
        url = str(p.get("url", "")).rstrip("/")
        result = _http_get(f"{url}/api/health", timeout=3.0)
        icon = "✅" if result["ok"] else "❌"
        print(f"  {icon} {name} → {url} → {result['status']}")
    print(f"*mdes-001 (NB1-Jit) · {_now_iso()}*")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="oracle-master", description="Master Oracle console")
    parser.add_argument("--health", action="store_true", help="probe all services")
    parser.add_argument("--search", dest="query", nargs="+", help="search Oracle memory")
    parser.add_argument("--ingest", dest="pattern", nargs="+", help="ingest a learning pattern")
    parser.add_argument("--source", help="source attribution for ingest")
    parser.add_argument("--tags", nargs="+", help="concept tags for ingest")
    parser.add_argument("--cwd", help="cwd for ingest")
    parser.add_argument("--handoff", action="store_true", help="list latest handoffs")
    parser.add_argument("--limit", type=int, help="limit for search/handoff")
    parser.add_argument("--sync", action="store_true", help="sync skills + run health checks")
    parser.add_argument("--agents", action="store_true", help="show agent registry")
    parser.add_argument("--vault", action="store_true", help="list vault/outbox/resonance")
    parser.add_argument("--federation", action="store_true", help="show federation peers")
    args = parser.parse_args(argv)

    # Default to summary if no action specified.
    if not any([
        args.health, args.query, args.pattern, args.handoff, args.sync,
        args.agents, args.vault, args.federation,
    ]):
        return cmd_summary(args)

    if args.health:
        return cmd_health(args)
    if args.query:
        return cmd_search(args)
    if args.pattern:
        return cmd_ingest(args)
    if args.handoff:
        return cmd_handoff(args)
    if args.sync:
        return cmd_sync(args)
    if args.agents:
        return cmd_agents(args)
    if args.vault:
        return cmd_vault(args)
    if args.federation:
        return cmd_federation(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
