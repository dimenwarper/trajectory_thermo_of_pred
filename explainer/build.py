#!/usr/bin/env python3
"""Compile the interactive explainer from editable parts.

    content.md   — the prose and structure you edit (Markdown + a few directives)
    template.html — the page shell: <head>/CSS/fonts and the <script> widgets
    parts.html   — verbatim SVG figures and interactive-widget scaffolding

Run `python3 build.py` to regenerate intro.html.

content.md dialect
------------------
Front matter (YAML-ish `key: value`, one per line) fills the hero and footer:
    title, kicker, hero_title, hero_sub, hero_src, footer, footer_fin

Sections:            # [Entry 07 · The loophole] Write it into the world
Headings:            ### For machine learning
Paragraphs:          plain lines (blank line separates them); inline HTML is kept
                     as-is, and **double asterisks** become <strong>.

Fenced directives (open with ::: and close with a lone :::):
    :::lede             one paragraph, rendered as the section lede
    :::pull             a pull quote
    :::aside <title>    a margin aside; <title> becomes the small label
    :::raw              emitted verbatim (escape hatch for hand-tuned HTML)
    :::figure "FIG 1" <name> [plain]   figure whose SVG is parts.html fig:<name>;
                                       the body is the caption
    :::widget <name>    drops in the verbatim parts.html widget:<name>
    :::ledger <head> | <sub>           a ledger card; each body line is a row:
        <class> | <desc> | <small> | <amount>    (class: debit|credit|zero|total)
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent


def load_parts(path):
    frags = {}
    for m in re.finditer(r'<!--FRAG (\S+)(?: (\w+))?-->\n([\s\S]*?)\n<!--/FRAG-->',
                         path.read_text(encoding='utf-8')):
        frags[m.group(1)] = m.group(3)
    return frags


def inline(s):
    """Light inline Markdown; existing HTML passes through untouched."""
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


def parse_front(text):
    fm = {}
    for line in text.splitlines():
        if line.strip():
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    return fm


def render_figure(args, caption, frags):
    m = re.match(r'"([^"]+)"\s+(\S+)(?:\s+(plain))?', args.strip())
    tag, name, plain = m.group(1), m.group(2), m.group(3)
    cls = ' class="plain"' if plain else ''
    return (f'<figure{cls}>\n'
            f'  <span class="figtag">{tag}</span>\n'
            f'  {frags["fig:" + name]}\n'
            f'  <figcaption>{inline(caption)}</figcaption>\n'
            f'</figure>')


def render_ledger(args, body_lines):
    head, _, sub = args.partition(' | ')
    rows = [f'<div class="lhead"><b>{inline(head.strip())}</b>'
            f'<span>{inline(sub.strip())}</span></div>']
    for ln in body_lines:
        if not ln.strip():
            continue
        cls, desc, small, amt = (c.strip() for c in ln.split('|'))
        if cls == 'total':
            rows.append(f'<div class="lrow total"><span class="desc">{inline(desc)}'
                        f'</span><span class="amt">{inline(amt)}</span></div>')
        else:
            small_html = f'<small>{inline(small)}</small>' if small else ''
            rows.append(f'<div class="lrow {cls}"><span class="desc">{inline(desc)}'
                        f'{small_html}</span><span class="amt">{inline(amt)}</span></div>')
    return '<div class="ledger">\n  ' + '\n  '.join(rows) + '\n</div>'


def render_directive(header, body_lines, frags):
    name, _, args = header.partition(' ')
    body = '\n'.join(body_lines).strip()
    if name == 'lede':
        return f'<p class="lede">{inline(body)}</p>'
    if name == 'pull':
        return f'<div class="pull">{inline(body)}</div>'
    if name == 'raw':
        return '\n'.join(body_lines)
    if name == 'aside':
        return (f'<div class="aside"><span class="k">{inline(args.strip())}</span>'
                f'{inline(body)}</div>')
    if name == 'figure':
        return render_figure(args, body, frags)
    if name == 'widget':
        return frags['widget:' + args.strip().split('|')[0].strip()]
    if name == 'ledger':
        return render_ledger(args, body_lines)
    raise ValueError(f'unknown directive: {name}')


def render_blocks(text, frags):
    lines = text.split('\n')
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith(':::'):
            header, body = line[3:].strip(), []
            i += 1
            while i < n and lines[i].strip() != ':::':
                body.append(lines[i])
                i += 1
            i += 1  # consume closing :::
            out.append(render_directive(header, body, frags))
        elif line.startswith('### '):
            out.append(f'<h3>{inline(line[4:].strip())}</h3>')
            i += 1
        else:
            para = []
            while (i < n and lines[i].strip()
                   and not lines[i].startswith((':::', '### '))):
                para.append(lines[i].strip())
                i += 1
            out.append(f'<p>{inline(" ".join(para))}</p>')
    return out


def render_section(n, eyebrow, title, body, frags):
    inner = '\n    '.join(render_blocks(body, frags))
    return ('<section>\n  <div class="col">\n'
            f'    <div class="eyebrow"><span class="n">{n}</span> {eyebrow}</div>\n'
            f'    <h2>{title}</h2>\n'
            f'    {inner}\n'
            '  </div>\n</section>')


def render_hero(fm):
    return ('<header>\n  <div class="col">\n'
            f'    <div class="kicker"><span class="dot"></span> {fm["kicker"]}</div>\n'
            f'    <h1>{fm["hero_title"]}</h1>\n'
            f'    <p class="hero-sub">{fm["hero_sub"]}</p>\n'
            f'    <div class="hero-src">{fm["hero_src"]}</div>\n'
            '  </div>\n</header>')


def render_footer(fm):
    return ('<footer>\n  <div class="col">\n'
            f'    <p>{fm["footer"]}</p>\n'
            f'    <div class="fin">{fm["footer_fin"]}</div>\n'
            '  </div>\n</footer>')


def main():
    frags = load_parts(ROOT / 'parts.html')
    raw = (ROOT / 'content.md').read_text(encoding='utf-8')
    m = re.match(r'^---\n([\s\S]*?)\n---\n([\s\S]*)$', raw)
    fm, body = parse_front(m.group(1)), m.group(2)

    pieces = [render_hero(fm)]
    for chunk in re.split(r'(?m)^# \[', body)[1:]:
        head, _, rest = chunk.partition('\n')
        bracket, _, title = head.partition('] ')
        n, eyebrow = bracket.split(' · ', 1)
        pieces.append(render_section(n.strip(), eyebrow.strip(), title.strip(),
                                     rest, frags))
    pieces.append(render_footer(fm))
    content = '\n\n'.join(pieces)

    template = (ROOT / 'template.html').read_text(encoding='utf-8')
    template = re.sub(r'<title>.*?</title>', f'<title>{fm["title"]}</title>', template)
    (ROOT / 'intro.html').write_text(template.replace('{{CONTENT}}', content),
                                     encoding='utf-8')
    print('wrote intro.html')


if __name__ == '__main__':
    main()
