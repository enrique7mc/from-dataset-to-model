"""Copy text edits made in the published artifact back into index.html.

    python3 -I tools/sync_from_artifact.py <artifact.html> [index.html]

The artifact's edit mode only changes the inner HTML of text blocks, so this
finds the same blocks in both files (the rule mirrors `editables` in the
deck-capture script) and splices each changed block's inner HTML into the
repo source. Everything else in index.html stays byte-for-byte as it was.
"""
import re
import sys
from html.parser import HTMLParser

TEXT = {"h1", "h2", "h3", "h4", "p", "li", "td", "th", "figcaption", "blockquote", "small"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FOREIGN = {"svg", "math"}


class Node:
    def __init__(self, tag, attrs, parent, inner_start):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children, self.direct_text = [], False
        self.inner_start = inner_start
        self.inner_end = None
        self.foreign = tag in FOREIGN or (parent is not None and parent.foreign)


class Tree(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=True)
        self.src = src
        self.lines = [0]
        for m in re.finditer("\n", src):
            self.lines.append(m.end())
        self.root = Node("#root", [], None, 0)
        self.cur = self.root
        self.feed(src)
        self.close()

    def pos_offset(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self.pos_offset()
        end = start + len(self.get_starttag_text())
        node = Node(tag, attrs, self.cur, end)
        self.cur.children.append(node)
        if tag in VOID and not self.cur.foreign:
            node.inner_end = end
        else:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        end = self.pos_offset() + len(self.get_starttag_text())
        node = Node(tag, attrs, self.cur, end)
        node.inner_end = end
        self.cur.children.append(node)

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is self.root:
            return
        pos = self.pos_offset()
        m = self.cur
        while m is not n:
            m.inner_end = pos
            m = m.parent
        n.inner_end = pos
        self.cur = n.parent

    def handle_data(self, data):
        if data.strip():
            self.cur.direct_text = True


def editables(tree):
    out = []

    def walk(el, inside):
        for c in el.children:
            if c.foreign or c.tag in ("script", "style"):
                continue
            hit = not inside and (c.tag in TEXT or c.direct_text)
            if hit:
                out.append(c)
            walk(c, inside or hit)

    def find(el):
        for c in el.children:
            if c.tag == "section" and "slide" in c.attrs.get("class", "").split():
                walk(c, False)
            else:
                find(c)

    find(tree.root)
    return out


class Tokens(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.feed(s)
        self.close()

    def handle_starttag(self, tag, attrs):
        self.out.append(("<", tag, tuple(sorted((k, v or "") for k, v in attrs))))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag not in VOID:
            self.out.append(("</", tag))

    def handle_data(self, data):
        text = re.sub(r"[ \t\n\r\f]+", " ", data)
        if self.out and self.out[-1][0] == "#":
            self.out[-1] = ("#", self.out[-1][1] + text)
        else:
            self.out.append(("#", text))


def same(a, b):
    norm = lambda s: [t for t in Tokens(s).out if t != ("#", " ")]
    return norm(a.strip()) == norm(b.strip())


def plain(s):
    return re.sub(r"<[^>]+>|\s+", " ", s).strip()[:70]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    art_path, repo_path = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "index.html"
    art_src = open(art_path, encoding="utf-8").read()
    repo_src = open(repo_path, encoding="utf-8").read()
    art, repo = editables(Tree(art_src)), editables(Tree(repo_src))
    if len(art) != len(repo):
        sys.exit(f"Block count differs (artifact {len(art)}, repo {len(repo)}). The slide structure changed; sync by hand.")
    changes = []
    for a, r in zip(art, repo):
        if a.tag != r.tag:
            sys.exit(f"Block mismatch: <{a.tag}> in the artifact vs <{r.tag}> in the repo. Sync by hand.")
        new = art_src[a.inner_start:a.inner_end]
        old = repo_src[r.inner_start:r.inner_end]
        if not same(new, old):
            changes.append((r, old, new))
    for r, _, new in sorted(changes, key=lambda c: -c[0].inner_start):
        repo_src = repo_src[:r.inner_start] + new + repo_src[r.inner_end:]
    if changes:
        open(repo_path, "w", encoding="utf-8").write(repo_src)
    for r, old, new in changes:
        print(f"<{r.tag}>  {plain(old)!r}\n   -> {plain(new)!r}")
    print(f"{len(changes)} block(s) updated in {repo_path}")


if __name__ == "__main__":
    main()
