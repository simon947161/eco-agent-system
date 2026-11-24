"""Render the canonical 12-screen Markdown locally; no network or data access."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

def build():
    text = (ROOT / 'FOUNDER_ACCEPTANCE_CN.md').read_text(encoding='utf-8')
    pages = re.split(r'^## ', text, flags=re.M)[1:]
    assert len(pages) == 12
    sections = []
    for i, page in enumerate(pages):
        title, body = page.split('\n', 1)
        paragraphs = []
        for para in body.strip().split('\n\n'):
            if para.startswith('来源：'):
                paragraphs.append('<details><summary>展开来源与证据</summary><p>'+inline(para[3:])+'</p></details>')
            else:
                paragraphs.append('<p>'+inline(para)+'</p>')
        sections.append(f'<section id="page-{i+1}" class="slide" aria-labelledby="title-{i+1}"'+(' hidden' if i else '')+f'><div class="kicker">WHH-001 / P0—P1</div><h1 id="title-{i+1}">{inline(title)}</h1>'+''.join(paragraphs)+'</section>')
    doc='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WHH · Founder 科学准备验收</title>
<style>*{box-sizing:border-box}body{margin:0;background:#0d1915;color:#f3f8f5;font:18px/1.8 system-ui,"Microsoft YaHei",sans-serif}header,footer{padding:16px clamp(18px,5vw,80px);display:flex;gap:18px;align-items:center;justify-content:space-between}header{border-bottom:1px solid #345448;font-size:14px;color:#9fceb7}main{max-width:1100px;min-height:70vh;margin:auto;padding:40px clamp(20px,5vw,70px)}.kicker{color:#79d6a6;letter-spacing:.12em;font-size:13px}h1{font-size:clamp(27px,3.4vw,43px);line-height:1.4;margin:18px 0 28px}p{max-width:860px}strong{color:#8fe2b8}a{color:#a4dfbd;text-decoration:underline;text-underline-offset:4px}details{margin-top:30px;padding:14px 20px;background:#172d23;border:1px solid #345448;border-radius:12px;font-size:15px}summary,button{cursor:pointer}footer{border-top:1px solid #345448}button{border:1px solid #7dc79b;border-radius:8px;background:#1e4832;color:white;padding:10px 18px;font:inherit}button:disabled{opacity:.35;cursor:default}.note{font-size:12px;color:#a2b6aa}progress{width:100%;height:4px;accent-color:#86dcad;display:block}#counter{font-variant-numeric:tabular-nums}.slide[hidden]{display:none}@media(max-width:600px){body{font-size:17px}header{align-items:flex-start;flex-direction:column;gap:2px}main{padding-top:26px;min-height:72vh}footer{padding:14px;gap:8px}button{font-size:15px;padding:9px 12px}.note{font-size:11px}}@media print{.slide[hidden]{display:block}.slide{break-after:page}header,footer,progress{display:none}body{color:#111;background:white}details{display:block}a{color:#184d31}}</style>
<header><span>CLIMATEOS / 科学准备验收 · 2026.11.24</span><span>研究已整理 · 科学准入 PENDING</span></header><progress id="progress" max="12" value="1" aria-label="阅读进度"></progress><main>'''+''.join(sections)+'''</main><footer><button id="prev" type="button">← 上一屏</button><div><div id="counter" aria-live="polite">1 / 12</div><div class="note">方向键翻页 · Home / End</div></div><button id="next" type="button">下一屏 →</button></footer>
<script>const slides=[...document.querySelectorAll('.slide')];let current=0;function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.hidden=i!==current);document.getElementById('prev').disabled=current===0;document.getElementById('next').disabled=current===slides.length-1;document.getElementById('counter').textContent=`${current+1} / ${slides.length}`;document.getElementById('progress').value=current+1;history.replaceState(null,'',`#page-${current+1}`);window.scrollTo(0,0)}document.getElementById('prev').onclick=()=>show(current-1);document.getElementById('next').onclick=()=>show(current+1);document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();show(current+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(current-1)}if(e.key==='Home'){e.preventDefault();show(0)}if(e.key==='End'){e.preventDefault();show(11)}});const requested=Number(location.hash.replace('#page-',''));show(Number.isFinite(requested)&&requested>0?requested-1:0);</script></html>'''
    (ROOT / 'index.html').write_text(doc, encoding='utf-8', newline='\n')
    print('Rendered 12 screens from FOUNDER_ACCEPTANCE_CN.md; no external assets')

if __name__ == '__main__':
    build()
