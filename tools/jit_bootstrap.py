"""jit_bootstrap.py — portable Jit bootstrap + health sync across runtimes.

Usage:
    python tools/jit_bootstrap.py [--skills-only] [--health-only] [--no-pull]

Environment:
    JIT_ROOT              path to Jit repo (required if not inside one)
    INNOVA_SKILLS_LIB   path to innova-skills-lib repo (auto-clone if missing)
    CLAUDE_SKILLS_ROOT  global skills dir (default: ~/.claude/skills)
    ORACLE_URL          optional, used by health checks inside Jit
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_SKILLS_REPO = "https://github.com/tinner-deinno/innova-skills-lib.git"
SKILL_CATEGORIES = ("core", "ECC", "9arm", "finance", "gov", "private")


def _log(level: str, msg: str) -> None:
    print(f"[{level}] {msg}", flush=True)


def ok(msg: str) -> None:
    _log("OK", msg)


def warn(msg: str) -> None:
    _log("WARN", msg)


def fail(msg: str) -> None:
    _log("FAIL", msg)


def info(msg: str) -> None:
    _log("INFO", msg)


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
    )


def find_jit_root() -> Path:
    env = os.environ.get("JIT_ROOT")
    if env:
        root = Path(env).resolve()
        if (root / "eval" / "body-check.sh").exists():
            return root
        warn(f"JIT_ROOT={root} does not look like Jit; trying git detection")
    proc = run(["git", "rev-parse", "--show-toplevel"])
    if proc.returncode == 0:
        root = Path(proc.stdout.strip()).resolve()
        if (root / "eval" / "body-check.sh").exists():
            return root
    raise RuntimeError(
        "Cannot find Jit repo. Set JIT_ROOT or run inside a Jit checkout."
    )


def find_skills_lib() -> Path:
    env = os.environ.get("INNOVA_SKILLS_LIB")
    if env:
        path = Path(env).resolve()
        if path.is_dir():
            return path
    home = Path.home()
    candidates = [
        home / "DEV" / "innova-skills-lib",
        home / "innova-skills-lib",
        home / "projects" / "innova-skills-lib",
    ]
    for path in candidates:
        if (path / "tools" / "register_skills.py").exists():
            return path.resolve()
    return clone_skills_lib(home / "DEV" / "innova-skills-lib")


def clone_skills_lib(dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    info(f"cloning {DEFAULT_SKILLS_REPO} into {dest}")
    proc = run(["git", "clone", DEFAULT_SKILLS_REPO, str(dest)], timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(f"git clone failed: {proc.stderr}")
    ok(f"innova-skills-lib cloned to {dest}")
    return dest.resolve()


def update_skills_lib(path: Path, no_pull: bool) -> None:
    if no_pull:
        info("skipping git pull (--no-pull)")
        return
    info("pulling innova-skills-lib")
    proc = run(["git", "pull", "--ff-only"], cwd=path, timeout=120)
    if proc.returncode != 0:
        warn(f"git pull failed (non-fatal): {proc.stderr.strip()}")
    else:
        ok("innova-skills-lib is up to date")


def rebuild_manifests(lib_root: Path) -> None:
    tools = lib_root / "tools"
    for script in ("register_skills.py", "generate_adapters.py"):
        script_path = tools / script
        if not script_path.exists():
            warn(f"missing {script_path}; skipping")
            continue
        info(f"running {script}")
        proc = run([sys.executable, str(script_path)], cwd=lib_root, timeout=300)
        if proc.returncode != 0:
            raise RuntimeError(f"{script} failed:\n{proc.stderr}")
    ok("manifest + adapters rebuilt")


def load_skill_yaml_id(skill_dir: Path) -> str | None:
    yaml_path = skill_dir / "skill.yaml"
    if not yaml_path.exists():
        return skill_dir.name
    try:
        import yaml

        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        return data.get("id") or skill_dir.name
    except Exception:
        return skill_dir.name


def _is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (
        (path / "SKILL.md").exists() or (path / "skill.yaml").exists()
    )


def _scan_skills(lib_root: Path) -> dict[str, Path]:
    """Recursively find every skill directory under known category roots."""
    skills: dict[str, Path] = {}
    for category in SKILL_CATEGORIES:
        cat_dir = lib_root / category
        if not cat_dir.is_dir():
            continue
        for entry in sorted(cat_dir.rglob("*")):
            if not entry.is_dir():
                continue
            if not _is_skill_dir(entry):
                continue
            # Skip if a parent is also a skill dir — nested packaging should use the leaf.
            if any(_is_skill_dir(p) for p in entry.parents if p != entry and p != cat_dir):
                continue
            skill_id = load_skill_yaml_id(entry)
            if skill_id in skills:
                warn(f"duplicate skill id '{skill_id}' in {entry}")
                continue
            skills[skill_id] = entry
    return skills


def _link_or_copy(source: Path, target: Path, *, copy: bool = False) -> None:
    if target.is_symlink() or target.is_junction():
        target.unlink()
    elif target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if copy:
        shutil.copytree(source, target)
        return
    system = platform.system()
    try:
        if system == "Windows":
            # Directory junctions work without admin on Windows 10+ with Developer Mode.
            run(["cmd", "/c", "mklink", "/J", str(target), str(source)], timeout=30)
        else:
            target.symlink_to(source, target_is_directory=True)
    except Exception:
        shutil.copytree(source, target)


def sync_global_skills(lib_root: Path, global_root: Path) -> dict[str, Path]:
    skills = _scan_skills(lib_root)
    global_root.mkdir(parents=True, exist_ok=True)
    for skill_id, source_dir in skills.items():
        target = global_root / skill_id
        _link_or_copy(source_dir, target)
    ok(f"global skills synced: {len(skills)} entries -> {global_root}")
    return skills


def sync_project_skills(global_root: Path, project_root: Path) -> None:
    project_skills = project_root / ".claude" / "skills"
    project_skills.mkdir(parents=True, exist_ok=True)
    count = 0
    for entry in sorted(global_root.iterdir()):
        if not entry.is_dir():
            continue
        target = project_skills / entry.name
        _link_or_copy(entry, target)
        count += 1
    ok(f"project skills synced: {count} entries -> {project_skills}")


def _unix_path(path: Path) -> str:
    """Convert a Windows path to a Unix-style path for MSYS/Git Bash."""
    try:
        proc = subprocess.run(
            ["cygpath", "-u", str(path.resolve())],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
    except Exception:
        pass
    return path.resolve().as_posix()


def _find_bash() -> list[str]:
    """Prefer Git Bash on Windows; avoid WSL bash which mangles Windows cwd paths."""
    git = shutil.which("git")
    if git:
        git_bash = Path(git).parent.parent / "usr" / "bin" / "bash.exe"
        if git_bash.exists():
            return [str(git_bash)]
    bash_exe = shutil.which("bash.exe")
    if bash_exe and "windowsapps" not in bash_exe.lower():
        return [bash_exe]
    bash = shutil.which("bash")
    if bash:
        return [bash]
    raise RuntimeError("bash not found; cannot run health checks")


def _run_sh(script: Path, jit_root: Path) -> dict[str, Any]:
    if not script.exists():
        return {"ok": False, "error": f"missing {script}"}
    bash = _find_bash()
    # cwd uses native Windows path; the script argument uses Unix path for MSYS bash.
    proc = run(bash + [_unix_path(script)], cwd=str(jit_root.resolve()), timeout=180)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def health_checks(jit_root: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for name in ("body-check.sh", "soul-check.sh"):
        script = jit_root / "eval" / name
        info(f"running {name}")
        results[name] = _run_sh(script, jit_root)
    return results


def report_health(results: dict[str, Any]) -> int:
    fails = 0
    for name, res in results.items():
        if res.get("ok"):
            ok(f"{name} passed")
        else:
            fail(f"{name} failed: {res.get('error', res.get('stderr', '')[:200])}")
            fails += 1
    return fails


def _set_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main(argv: list[str] | None = None) -> int:
    _set_utf8_stdout()
    parser = argparse.ArgumentParser(description="Jit bootstrap + health sync")
    parser.add_argument("--skills-only", action="store_true")
    parser.add_argument("--health-only", action="store_true")
    parser.add_argument("--no-pull", action="store_true")
    args = parser.parse_args(argv)

    try:
        jit_root = find_jit_root()
        ok(f"Jit root: {jit_root}")
    except RuntimeError as e:
        fail(str(e))
        return 1

    if args.health_only:
        results = health_checks(jit_root)
        return 1 if report_health(results) else 0

    try:
        skills_lib = find_skills_lib()
        ok(f"innova-skills-lib: {skills_lib}")
        update_skills_lib(skills_lib, args.no_pull)
        rebuild_manifests(skills_lib)
        global_root = Path(
            os.environ.get("CLAUDE_SKILLS_ROOT", Path.home() / ".claude" / "skills")
        ).resolve()
        sync_global_skills(skills_lib, global_root)
        sync_project_skills(global_root, jit_root)
    except RuntimeError as e:
        fail(str(e))
        return 1

    if args.skills_only:
        return 0

    results = health_checks(jit_root)
    fails = report_health(results)
    if fails == 0:
        ok("🌟 Jit is ready")
    else:
        warn("some health checks failed — see details above")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
