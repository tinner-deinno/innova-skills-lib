"""
register_skills.py
Scans ~/.claude/skills/ and builds skills_manifest.json + skills_index.md.
Standard library only -- no external dependencies.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILLS_ROOT   = Path(r'C:\Users\MDES-DEV-NB\.claude\skills')
OUTPUT_DIR    = Path(r'C:\Users\MDES-DEV-NB\DEV\innova-skills-lib')
MANIFEST_PATH = OUTPUT_DIR / 'manifests' / 'skills_manifest.json'
INDEX_PATH    = OUTPUT_DIR / 'skills_index.md'
VERSION       = '2026.05.24'
LAST_UPDATED  = '2026-05-24T00:00:00Z'
AUTHOR        = 'team/jit-bigboss'
RUNTIMES      = ['claude']
MANIFEST_VER  = '1.0'


def parse_frontmatter(text):
    stripped = text.lstrip(chr(0xFEFF))
    if not stripped.startswith('---'):
        return {}, stripped
    rest    = stripped[3:]
    end_idx = rest.find('\n---')
    if end_idx == -1:
        return {}, stripped
    raw_fm = rest[:end_idx]
    body   = rest[end_idx + 4:].lstrip('\n')
    fm = {}
    for line in raw_fm.splitlines():
        m = re.match(r'^([\w][\w\-]*)\s*:\s*(.*)', line)
        if not m:
            continue
        key   = m.group(1).strip()
        value = m.group(2).strip()
        dq = chr(34)
        sq = chr(39)
        if len(value) >= 2 and (
            (value[0] == dq and value[-1] == dq) or
            (value[0] == sq and value[-1] == sq)
        ):
            value = value[1:-1]
        fm[key] = value
    return fm, body


def first_non_header_line(body):
    for line in body.splitlines():
        s = line.strip()
        if s and not s.startswith('#') and not s.startswith('>') and not s.startswith('---'):
            s = re.sub(r'\*{1,3}', '', s)
            s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
            s = s.strip()
            if s:
                return s[:200]
    return ''


def dir_to_slug(rel_path):
    parts = rel_path.parts
    return '-'.join(p.lower().replace(' ', '-') for p in parts)


def category_from_rel(rel_path):
    parts = rel_path.parts
    if len(parts) == 1:
        return 'core'
    return parts[0].lower()

def find_skill_dirs(root):
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        dp    = Path(dirpath)
        match = next((f for f in filenames if f.lower() == 'skill.md'), None)
        if match:
            results.append((dp, dp / match))
    results.sort(key=lambda t: str(t[0]))
    return results


def build_entry(skill_dir, skill_md, root):
    rel_path = skill_dir.relative_to(root)
    try:
        raw = skill_md.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        raw = skill_md.read_text(encoding='latin-1')
    fm, body    = parse_frontmatter(raw)
    name        = fm.get('name') or dir_to_slug(rel_path).replace('-', ' ').title()
    description = fm.get('description') or first_non_header_line(body) or name
    slug      = dir_to_slug(rel_path)
    category  = category_from_rel(rel_path)
    path_str  = str(rel_path).replace(chr(92), '/')
    return {
        'id':               slug,
        'name':             name,
        'path':             path_str,
        'version':          VERSION,
        'description':      description,
        'runtimes':         RUNTIMES,
        'adapter_status':   {'claude': 'ok'},
        'triggers':         [slug],
        'author':           AUTHOR,
        'category':         category,
        'tags':             [category],
        'last_updated':     LAST_UPDATED,
        'manifest_version': MANIFEST_VER,
    }

def write_index(entries, path, errors):
    now   = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    lines = [
        '# Skills Index',
        '',
        f'Generated: {now}  ',
        f'Total: **{len(entries)}** skills  ',
        '',
        '---',
        '',
    ]
    categories = {}
    for e in entries:
        categories.setdefault(e['category'], []).append(e)
    for cat in sorted(categories):
        lines.append(f'## {cat.upper()}')
        lines.append('')
        lines.append('| ID | Name | Description |')
        lines.append('|---|---|---|')
        for e in sorted(categories[cat], key=lambda x: x['id']):
            desc  = e['description'].replace('|', r'\|')[:100]
            id_   = e['id']
            nm    = e['name']
            lines.append('| ' + chr(96) + id_ + chr(96) + ' | ' + nm + ' | ' + desc + ' |')
        lines.append('')
    if errors:
        lines.append('## Errors')
        lines.append('')
        for err in errors:
            lines.append(f'- {err}')
        lines.append('')
    path.write_text('\n'.join(lines), encoding='utf-8')

def main():
    print(f'Scanning: {SKILLS_ROOT}')
    if not SKILLS_ROOT.exists():
        print(f'ERROR: Skills root does not exist: {SKILLS_ROOT}', file=sys.stderr)
        sys.exit(1)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    skill_dirs = find_skill_dirs(SKILLS_ROOT)
    print(f'Found {len(skill_dirs)} SKILL.md files')
    entries = []
    errors  = []
    for skill_dir, skill_md in skill_dirs:
        try:
            entry = build_entry(skill_dir, skill_md, SKILLS_ROOT)
            entries.append(entry)
        except Exception as exc:
            msg = f'{skill_dir}: {exc}'
            errors.append(msg)
            print(f'  ERROR: {msg}', file=sys.stderr)
    entries.sort(key=lambda e: e['id'])
    categories = sorted({e['category'] for e in entries})
    manifest = {
        'manifest_version': MANIFEST_VER,
        'generated':        datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'total':            len(entries),
        'categories':       categories,
        'skills':           entries,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'Manifest written: {MANIFEST_PATH}')
    write_index(entries, INDEX_PATH, errors)
    print(f'Index written:    {INDEX_PATH}')
    print()
    sep = '=' * 60
    print(sep)
    print(f'Skills registered : {len(entries)}')
    cats_str = ', '.join(categories)
    print(f'Categories        : {len(categories)} -- {cats_str}')
    if errors:
        print(f'Errors            : {len(errors)}')
        for e in errors:
            print(f'  - {e}')
    else:
        print('Errors            : 0')
    print(sep)


if __name__ == '__main__':
    main()