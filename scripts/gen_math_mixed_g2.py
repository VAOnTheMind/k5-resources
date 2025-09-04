from _common import write_html, update_home_list, PAGE_OPEN, PAGE_CLOSE, today_stamp
import os, random

PDF_LIB = '<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" integrity="sha512-YcsIPnY1Qm6tYTN3nGZxP+JmKp1Fb0DHW/1yCI1Gz9oYw4LwMe1bKjM+m3r3Zjxi9h/7t3tkQjvQlu1I3fVzLA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'

def build_set():
    items, answers = [], []
    a,b = random.randint(20,60), random.randint(10,30); items.append(f"{a} + {b} = ____"); answers.append(a+b)
    a,b = random.randint(40,80), random.randint(10,40); items.append(f"{a} − {b} = ____"); answers.append(a-b)
    a,b = random.randint(20,60), random.randint(10,40); items.append(f"{a} + {b} = ____"); answers.append(a+b)
    a,b = random.randint(60,90), random.randint(10,50); items.append(f"{a} − {b} = ____"); answers.append(a-b)
    items += [
        "9 + 8 + 7 = ____",
        "3 × 4 = ____",
        "5 × 2 = ____",
        "16 ÷ 4 = ____",
        "A pencil costs 25¢. You have 3 dimes. Enough? YES / NO",
        "1 quarter + 2 dimes = ____ cents",
        "45 minutes after 2:15 = ____",
        "Round: 6 cm is closer to 5 or 7? ____"
    ]
    answers += [24,12,10,4,"NO",45,"3:00","7 cm"]
    return items, answers

def worksheet_html(items, ws_fname, ans_fname):
    items_html = "\n        ".join([f'<div class="item"><span class="num">{i+1}</span><div class="prompt">{t}</div></div>' for i,t in enumerate(items)])
    tpl = '''
      <div class="worksheet">
        <div class="header">
          <div class="title">Math Mixed Practice (Within 100)</div>
          <div class="subhead">
            <span class="badge">Grade 2</span>
            <span>Name <span class="line"></span></span>
            <span>Date <span class="line"></span></span>
          </div>
        </div>
        <hr class="sep"/>
        <div class="directions">Solve. Show neat work.</div>
        {items}
        <div class="note">Answer key provided separately for teachers.</div>
      </div>

      <p style="display:flex;gap:8px;flex-wrap:wrap;">
        <button class="btn" id="dl-pdf">Download PDF</button>
        <button class="btn" onclick="window.print()">Print / Save PDF</button>
        <a class="btn" href="{ans}">Teacher Answer Key</a>
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
    return tpl.format(items=items_html, ans=ans_fname, pdf_lib=PDF_LIB, pdf_name=ws_fname.replace('.html', '.pdf'))

def answers_html(answers, ws_fname):
    li = "\n        ".join([f"<li>{a}</li>" for a in answers])
    return f'''
      <h1>Teacher Answer Key — Math Mixed (G2)</h1>
      <ol>{li}</ol>
      <p><a class="btn" href="{ws_fname}">← Back to worksheet</a></p>
    '''

def main():
    date = today_stamp()
    items, answers = build_set()
    ws_fname  = f"math-mixed-g2-{date}.html"
    ans_fname = f"math-mixed-g2-{date}-answers.html"
    ws_inner  = PAGE_OPEN + worksheet_html(items, ws_fname, ans_fname) + PAGE_CLOSE
    ans_inner = PAGE_OPEN + answers_html(answers, ws_fname) + PAGE_CLOSE
    write_html(os.path.join("worksheets", ws_fname), "Math Mixed Practice (G2)", ws_inner, is_root=False)
    write_html(os.path.join("worksheets", ans_fname), "Answers — Math Mixed (G2)", ans_inner, is_root=False)
    update_home_list("index.html", f"worksheets/{ws_fname}", f"Math Mixed Practice (G2) — {date}")

if __name__ == "__main__":
    main()
