from _common import write_html, update_home_list, PAGE_OPEN, PAGE_CLOSE, today_stamp
import os, random

# Simple 3-letter chains (one letter changes each step)
CHAINS = [
    ["cat","bat","rat","ran"],
    ["bag","bog","dog","dig"],
    ["tap","top","cop","cup"],
    ["hat","hot","dot","dog"],
    ["man","men","pen","pin"],
]

PDF_LIB = '<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" integrity="sha512-YcsIPnY1Qm6tYTN3nGZxP+JmKp1Fb0DHW/1yCI1Gz9oYw4LwMe1bKjM+m3r3Zjxi9h/7t3tkQjvQlu1I3fVzLA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'

def build_block(chain, fname):
    steps = [
        ('1', f"{chain[0][0]} {chain[0][1]} {chain[0][2]} → _ {chain[0][1]} {chain[0][2]}"),
        ('2', f"_ {chain[0][1]} {chain[0][2]} → {chain[1][0]} {chain[1][1]} {chain[1][2]}"),
        ('3', f"{chain[1][0]} {chain[1][1]} {chain[1][2]} → {chain[2][0]} {chain[2][1]} _"),
        ('4', f"{chain[2][0]} {chain[2][1]} _ → {chain[3][0]} {chain[3][1]} {chain[3][2]}"),
    ]
    items_html = "\n        ".join(
        [f'<div class="item"><span class="num">{n}</span><div class="prompt">{t}</div></div>' for n,t in steps]
    )

    tpl = '''
      <div class="worksheet">
        <div class="header">
          <div class="title">Word Ladder — Short “a”</div>
          <div class="subhead">
            <span class="badge">Grade 1</span>
            <span>Name <span class="line"></span></span>
            <span>Date <span class="line"></span></span>
          </div>
        </div>
        <hr class="sep"/>
        <div class="directions">Change ONE letter each step to make a new real word. Don’t rearrange letters.</div>
        {items}
        <div class="note">Nice job climbing!</div>
        <div class="footerbar"><span>Word Ladders</span><span>Print-friendly • B/W</span></div>
      </div>

      <p style="display:flex;gap:8px;flex-wrap:wrap;">
        <button class="btn" id="dl-pdf">Download PDF</button>
        <button class="btn" onclick="window.print()">Print / Save PDF</button>
        <a class="btn" href="../index.html">← Back to Home</a>
      </p>
      {pdf_lib}
      <script>
      (function() {{
        var btn = document.getElementById('dl-pdf');
        if(!btn) return;
        btn.addEventListener('click', function() {{
          var el = document.querySelector('.worksheet');
          html2pdf().set({{
            margin:[0.5,0.5,0.5,0.5],
            filename: '{pdf_name}',
            image: {{type:'jpeg', quality:0.98}},
            html2canvas: {{scale:2, useCORS:true, letterRendering:true}},
            jsPDF: {{unit:'in', format:'letter', orientation:'portrait'}}
          }}).from(el).save();
        }});
      }})();
      </script>
    '''
    return tpl.format(items=items_html, pdf_lib=PDF_LIB, pdf_name=fname.replace('.html', '.pdf'))

def main():
    date = today_stamp()
    chain = random.choice(CHAINS)
    fname = f"word-ladder-g1-{date}.html"
    inner = PAGE_OPEN + build_block(chain, fname) + PAGE_CLOSE
    write_html(os.path.join("worksheets", fname), "Word Ladder — Grade 1", inner, is_root=False)
    update_home_list("index.html", f"worksheets/{fname}", f"Word Ladder (G1) — {date}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
