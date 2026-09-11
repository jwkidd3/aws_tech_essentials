#!/usr/bin/env python3
"""Regenerate the Markdown copy of each lab from its Reveal.js HTML.

The HTML decks are the source of truth. After editing a lab deck, run:

    python3 tools/html2md.py

Requires: beautifulsoup4  (pip install beautifulsoup4)
"""
import pathlib, re
from bs4 import BeautifulSoup, NavigableString, Tag

LABS = pathlib.Path(__file__).resolve().parent.parent / "labs"

def inline(node):
    if isinstance(node, NavigableString):
        return re.sub(r"\s+", " ", str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name
    inner = "".join(inline(c) for c in node.children)
    if name == "code":
        return f"`{inner.strip()}`"
    if name in ("strong", "b"):
        s = inner.strip()
        return f"**{s}**" if s else ""
    if name in ("em", "i"):
        s = inner.strip()
        return f"*{s}*" if s else ""
    if name == "br":
        return " "
    return inner

def tidy(s):
    return re.sub(r"[ \t]+", " ", s).strip()

def list_block(tag, depth=0):
    out, pad = [], "    "*depth
    start = int(tag.get("start", 1)) if tag.name == "ol" else 1
    n = start
    for li in tag.find_all("li", recursive=False):
        nested = [c for c in li.children if isinstance(c, Tag) and c.name in ("ul", "ol")]
        for c in nested:
            c.extract()
        text = tidy(inline(li))
        bullet = f"{n}." if tag.name == "ol" else "-"
        out.append(f"{pad}{bullet} {text}")
        for c in nested:
            out.extend(list_block(c, depth+1))
        n += 1
    return out

def table_block(tag):
    rows = tag.find_all("tr")
    if not rows:
        return []
    def cells(tr):
        return [tidy(inline(c)) for c in tr.find_all(["th", "td"])]
    head = cells(rows[0])
    is_header = bool(rows[0].find("th"))
    body = [cells(tr) for tr in (rows[1:] if is_header else rows)]
    if not is_header:
        head = [""]*max(len(r) for r in body)
    width = max([len(head)] + [len(r) for r in body])
    head += [""]*(width-len(head))
    out = ["| " + " | ".join(head) + " |", "|" + "|".join([" --- "]*width) + "|"]
    for r in body:
        r = r + [""]*(width-len(r))
        out.append("| " + " | ".join(r) + " |")
    return out

def code_block(pre):
    code = pre.find("code")
    lang = ""
    if code and code.get("class"):
        lang = [c for c in code.get("class") if c != "hljs"]
        lang = lang[0] if lang else ""
    body = (code or pre).get_text()
    return ["```" + lang, body.strip("\n"), "```"]

BOX_LABEL = {"highlight-box": "", "success": "", "warning": "", "danger": ""}

def blocks(container, level=3):
    out = []
    for el in container.children:
        if not isinstance(el, Tag):
            continue
        cls = el.get("class") or []
        if el.name in ("h1", "h2", "h3", "h4"):
            out += ["", "###" + " " + tidy(inline(el)), ""]
        elif el.name == "p":
            t = tidy(inline(el))
            if t:
                out += [t, ""]
        elif el.name in ("ul", "ol"):
            out += list_block(el) + [""]
        elif el.name == "table":
            out += table_block(el) + [""]
        elif el.name == "pre":
            out += code_block(el) + [""]
        elif "highlight-box" in cls or "key-point" in cls or "concept-box" in cls:
            inner = []
            for c in el.children:
                if isinstance(c, Tag) and c.name in ("ul", "ol"):
                    inner += list_block(c)
                elif isinstance(c, Tag) and c.name == "table":
                    inner += table_block(c)
                else:
                    t = tidy(inline(c))
                    if t:
                        inner.append(t)
            merged = []
            for line in inner:
                if merged and not line.startswith(("-", "|")) and not merged[-1].startswith(("-", "|")):
                    merged[-1] = (merged[-1] + " " + line).strip()
                else:
                    merged.append(line)
            out += ["> " + l for l in merged] + [""]
        elif el.name == "div" and ("two-columns" in cls or "three-columns" in cls or "card" in cls):
            out += blocks(el, level=level)
        elif el.name == "div":
            if "module-progress" in cls:
                continue
            out += blocks(el, level=level)
    return out

PLACEHOLDER = re.compile(r"[A-Za-z0-9._-]*<[A-Z_]+>[A-Za-z0-9._/-]*")

def protect_placeholders(md):
    out, in_fence = [], False
    for line in md.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if in_fence:
            out.append(line); continue
        parts = line.split("`")
        for i in range(0, len(parts), 2):       # even indexes are outside code spans
            parts[i] = PLACEHOLDER.sub(lambda m: "`" + m.group(0) + "`", parts[i])
        out.append("`".join(parts))
    return "\n".join(out)

def convert(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = soup.title.get_text().split("|")[0].strip() if soup.title else path.stem
    course = "AWS Technical Essentials"
    lines = [f"# {title}", "", f"*{course}*", "",
             "> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).",
             "", "---", ""]
    sections = soup.select("div.slides > section")
    for sec in sections:
        cls = sec.get("class") or []
        # Speaker notes are for the instructor only - never emit them.
        for note in sec.find_all("aside", class_="notes"):
            note.extract()
        if "title-slide" in cls or "questions-slide" in cls:
            h = sec.find(["h1", "h2"])
            heading = tidy(inline(h)) if h else ""
            subs = [tidy(inline(x)) for x in sec.find_all(["h2", "h3", "p"]) if x is not h]
            subs = [s for s in subs if s]
            lines += ["", f"## {heading}", ""]
            if subs:
                lines += ["*" + " — ".join(subs) + "*", ""]
        else:
            h = sec.find(["h1", "h2"])
            heading = tidy(inline(h)) if h else "Slide"
            lines += ["", f"## {heading}", ""]
            if h:
                h.extract()
            lines += blocks(sec, level=3)
        lines += ["---", ""]
    md = "\n".join(lines)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = protect_placeholders(md)
    md = re.sub(r" +([.,;:!?])", r"\1", md)
    md = re.sub(r"\( +", "(", md)
    md = re.sub(r" +\)", ")", md)
    md = md.rstrip() + "\n"
    out = path.with_suffix(".md")
    out.write_text(md, encoding="utf-8")
    return out

for p in sorted(LABS.glob("lab-*.html")):
    print("wrote", convert(p).name)
