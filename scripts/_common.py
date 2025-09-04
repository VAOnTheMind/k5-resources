import pathlib, datetime, re

HEADER = """<header class="brandbar">
  <a href="../"><img src="../logo-h.png" alt="Bellringer Printables" style="height:40px;width:auto;"></a>
  <nav class="topnav">
    <a href="../">Home</a>
    <a href="../by-grade.html">By Grade</a>
    <a href="../by-skill.html">By Skill</a>
  </nav>
</header>"""

PAGE_OPEN = """<div class="page">
  <aside class="ad-rail"><div class="ad-box">Ad space (300x250)</div></aside>
  <main class="site">"""
PAGE_CLOSE = """  </main>
  <aside class="ad-rail"><div class="ad-box">Ad space (300x250)</div></aside>
</div>"""

def today_stamp():
    return datetime.datetime.utcnow().strftime("%Y%m%d")

def write_html(path, title, inner_html, is_root=False):
    css_path = "assets/kid_theme.css" if is_root else "../assets/kid_theme.css"
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <link rel="stylesheet" href="{css_path}"/>
</head>
<body>
{HEADER if not is_root else ""}
{inner_html}
</body>
</html>"""
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")

def update_home_list(index_path, rel_href, link_text, keep=10):
    """Insert the newest worksheet link at the top of the 'Latest Worksheets' <ul>."""
    html = pathlib.Path(index_path).read_text(encoding="utf-8")
    card_pos = html.find("Latest Worksheets")
    ul_start = html.find("<ul>", card_pos)
    ul_end = html.find("</ul>", ul_start)
    if ul_start == -1 or ul_end == -1:
        return False
    ul_content = html[ul_start+4:ul_end]
    items = re.findall(r"<li>.*?</li>", ul_content, flags=re.S)
    new_item = f'<li><a href="{rel_href}">{link_text}</a></li>'
    items = [new_item] + [it for it in items if rel_href not in it]
    items = items[:keep]
    new_ul = "<ul>\n        " + "\n        ".join(items) + "\n      </ul>"
    html = html[:ul_start] + new_ul + html[ul_end+5:]
    pathlib.Path(index_path).write_text(html, encoding="utf-8")
    return True
