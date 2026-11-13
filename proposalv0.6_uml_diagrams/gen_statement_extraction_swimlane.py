"""Generate the statement-extraction pipeline swimlane diagram.

Usage:  python3 docs/diagrams/gen_statement_extraction_swimlane.py

Writes, next to this script:
  statement_extraction_swimlane.svg   standalone SVG (light/dark via prefers-color-scheme)
  statement_extraction_swimlane.html  page body published as the Claude artifact
                                      (built from statement_extraction_swimlane.template.html;
                                      the artifact host adds the doctype/head skeleton)

Layout is computed here: text is wrapped with an estimated character width, so
after editing labels, re-run and look at the output. To change the diagram, edit
the sequence of main()/node_amber()/retry_block() calls below.
"""
import html
from pathlib import Path
HERE=Path(__file__).resolve().parent
NAME="statement_extraction_swimlane"
TOKENS_LIGHT="""  --bg:#f5f7fa; --surface:#ffffff; --surface-2:#fbf8f1; --fg:#17202b; --muted:#5b6777; --rule:#d5dbe3; --line:#3b4756;
  --blue-fill:#e4eefc; --blue-stroke:#2c6bc9; --blue-ink:#1f559f;
  --amber-fill:#fdf0cf; --amber-stroke:#b57a06; --amber-ink:#8a5c00;
  --green-fill:#def3e5; --green-stroke:#23874a; --green-ink:#1a6b3a;
  --font-display:"Space Grotesk","Inter",system-ui,sans-serif;
  --font-body:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;"""
TOKENS_DARK="""  --bg:#11151b; --surface:#171c24; --surface-2:#1c1a14; --fg:#e7ebf1; --muted:#9aa5b4; --rule:#2c3440; --line:#b4bfcc;
  --blue-fill:#162c4a; --blue-stroke:#6ea6f3; --blue-ink:#9cc3fa;
  --amber-fill:#3a2b0b; --amber-stroke:#e2ad48; --amber-ink:#f0c672;
  --green-fill:#12321f; --green-stroke:#5cc086; --green-ink:#86d8a8;"""
DIAGRAM_CSS=""".lane{stroke:var(--rule);stroke-width:1}
.lane-d{fill:var(--surface)} .lane-p{fill:var(--surface-2)}
.lane-rule{stroke:var(--rule);stroke-width:1}
.lane-h{font-family:var(--font-display);font-size:13px;font-weight:600;letter-spacing:.09em;fill:var(--fg)}
.lane-f{font-family:var(--font-display);font-size:11px;font-weight:500;letter-spacing:.09em;fill:var(--muted)}
.bx{stroke-width:1.5}
.k-blue{fill:var(--blue-fill);stroke:var(--blue-stroke)}
.k-amber{fill:var(--amber-fill);stroke:var(--amber-stroke)}
.k-green{fill:var(--green-fill);stroke:var(--green-stroke)}
.eb{font-size:10.5px;font-weight:700;letter-spacing:.09em}
.eb-blue{fill:var(--blue-ink)} .eb-amber{fill:var(--amber-ink)} .eb-green{fill:var(--green-ink)}
.ttl{font-size:13.5px;font-weight:600;fill:var(--fg)}
.body{font-size:12px;fill:var(--fg)} .mk{fill:var(--muted);font-variant-numeric:tabular-nums}
.side{font-size:12.5px;font-weight:600;fill:var(--fg)}
.gq{font-size:12.5px;font-weight:600;fill:var(--fg)}
.ln{fill:none;stroke:var(--line);stroke-width:1.5;stroke-linejoin:round}
.ah{fill:var(--line)}
.nd{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.ndt{font-size:10.5px;font-weight:700;fill:var(--fg)}
.dot{fill:var(--line)} .fin-o{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.al{font-size:11.5px;font-weight:700;fill:var(--fg)}
.al2{font-size:11.5px;font-weight:500;fill:var(--muted)}"""
W=1140
RAIL=60; MX=110; MW=380; MCX=300; SX=530; SW=220; SCX=640; DIV=780; AX=810; AW=300; ACX=960
GAP=30; NR=13; GH=52; GWH=180
o=[]
esc=html.escape
def est(s,size,bold=False): return len(s)*size*(0.61 if bold else 0.565)
def wrap(s,maxw,size,bold=False):
    lines=[];cur=""
    for w in s.split():
        t=(cur+" "+w).strip()
        if est(t,size,bold)<=maxw or not cur: cur=t
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def T(x,y,s,cls,anchor="start"):
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>')
def layout(w,eyebrow,title,items,numbered=False):
    pad=14; inner=w-2*pad; L=[]; y=pad
    if eyebrow: y+=10; L.append((pad,y,"eb",eyebrow)); y+=7
    for ln in wrap(title,inner,13.5,True):
        y+=14; L.append((pad,y,"ttl",ln)); y+=4
    if items: y+=5
    for i,it in enumerate(items):
        mark=f"{i+1}." if numbered else "•"
        ind=18 if numbered else 13
        for j,ln in enumerate(wrap(it,inner-ind,12)):
            y+=12
            if j==0: L.append((pad,y,"body mk",mark))
            L.append((pad+ind,y,"body",ln)); y+=4.5
        y+=3
    return L,y+pad-(7 if items else 4)
def box(x,top,w,kind,lay):
    L,h=lay
    o.append(f'<rect x="{x}" y="{top:.1f}" width="{w}" height="{h:.1f}" rx="7" class="bx k-{kind}"/>')
    for dx,dy,cls,s in L: T(x+dx,top+dy,s,cls+(f" eb-{kind}" if cls=="eb" else ""))
    return h
def sidebox(cy,text):
    lines=wrap(text,SW-28,12.5,True); h=len(lines)*17+22; top=cy-h/2
    o.append(f'<rect x="{SX}" y="{top:.1f}" width="{SW}" height="{h}" rx="7" class="bx k-blue"/>')
    for i,ln in enumerate(lines): T(SCX,top+11+13+i*17,ln,"side","middle")
    return h
def arrow(pts,dashed=False):
    (x1,y1),(x2,y2)=pts[-2],pts[-1]
    d=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    o.append(f'<polyline points="{d}" class="ln{" dash" if dashed else ""}"/>')
    a=9;b=4.5
    if x1==x2:
        s=1 if y2>y1 else -1; p=[(x2,y2),(x2-b,y2-s*a),(x2+b,y2-s*a)]
    else:
        s=1 if x2>x1 else -1; p=[(x2,y2),(x2-s*a,y2-b),(x2-s*a,y2+b)]
    o.append('<polygon points="'+" ".join(f"{x:.1f},{y:.1f}" for x,y in p)+'" class="ah"/>')
def node(cy,n):
    o.append(f'<circle cx="{MCX}" cy="{cy:.1f}" r="{NR}" class="nd"/>'); T(MCX,cy+3.8,f"N{n}","ndt","middle")
def gate(cy,n,lines):
    p=[(MCX-GWH,cy),(MCX,cy-GH),(MCX+GWH,cy),(MCX,cy+GH)]
    o.append('<polygon points="'+" ".join(f"{x},{y:.1f}" for x,y in p)+'" class="bx k-blue"/>')
    if len(lines)==2:
        T(MCX,cy-20,f"GATE {n}","eb eb-blue","middle"); T(MCX,cy-1,lines[0],"gq","middle"); T(MCX,cy+16,lines[1],"gq","middle")
    else:
        T(MCX,cy-10,f"GATE {n}","eb eb-blue","middle"); T(MCX,cy+10,lines[0],"gq","middle")

prev=0
def main(kind,eb,title,items=(),numbered=False,from_amber=None):
    global prev
    lay=layout(MW,eb,title,list(items),numbered)
    if from_amber is None:
        top=prev+GAP; arrow([(MCX,prev),(MCX,top)])
    else:
        top=from_amber+GAP; yc=top+lay[1]/2; arrow([(ACX,from_amber),(ACX,yc),(MX+MW,yc)])
    h=box(MX,top,MW,kind,lay); prev=top+h
def node_amber(n,eb,title,items=()):
    global prev
    lay=layout(AW,eb,title,list(items)); ha=lay[1]
    yn=prev+GAP+max(ha/2,NR)
    arrow([(MCX,prev),(MCX,yn-NR)]); node(yn,n)
    arrow([(MCX+NR,yn),(AX,yn)]); box(AX,yn-ha/2,AW,"amber",lay)
    return yn,yn+ha/2
def retry_block(n1,q1,yn_retry,n2,q2,yes_lbl,no_caption,side_text,node_n):
    global prev
    c1=prev+GAP+GH; arrow([(MCX,prev),(MCX,c1-GH)]); gate(c1,n1,q1)
    arrow([(MCX-GWH,c1),(RAIL,c1),(RAIL,yn_retry),(MCX-NR,yn_retry)])
    T((RAIL+MCX-GWH)/2,c1-7,"Yes","al","middle"); T(RAIL+10,yn_retry-8,"return exact failed checks","al2")
    c2=c1+GH+40+GH; arrow([(MCX,c1+GH),(MCX,c2-GH)]); T(MCX+8,c1+GH+22,"No","al"); gate(c2,n2,q2)
    hs=sidebox(c2,side_text)
    arrow([(MCX+GWH,c2),(SX,c2)]); T((MCX+GWH+SX)/2-2,c2-7,"No","al","middle")
    T(SCX,c2-hs/2-9,no_caption,"al2","middle")
    yn=c2+GH+46+NR; arrow([(MCX,c2+GH),(MCX,yn-NR)]); T(MCX+8,c2+GH+24,yes_lbl,"al")
    node(yn,node_n); arrow([(SCX,c2+hs/2),(SCX,yn),(MCX+NR,yn)])
    prev=yn+NR

TOP=16; HEAD=44
sy=TOP+HEAD+26
body_start=len(o)
o.append(f'<circle cx="{MCX}" cy="{sy}" r="8" class="dot"/>'); T(MCX+16,sy+4,"Annual report PDF, one parser branch","al2")
prev=sy+8
main("blue","STAGE 0","Source intake, identity, and page count",["Resolve the path, verify readable or corrupt, hash original bytes, record page count and ordinals"])
main("blue","STAGE 1","Raw parser evidence and branch health",["Run approved branches independently. Check source/parser page counts and ordinals. Record text/label/image health; preserve raw evidence.","Health gate for every parser branch: at least one parsed page must contain 100 non-whitespace characters. Failure makes that branch ineligible. This does not prove completeness."])
main("blue","STAGE 2","Reversible evidence normalization",["Crop/media box and coordinate origin","Page rotation with forward/inverse transform","Detached opening parenthesis","Same-row detached closing parenthesis","Adjacent-row detached closing parenthesis","Rule/version, before/after, object lineage"],numbered=True)
main("green","STAGE 3","Parser-evidence comparison",["Compare raw and normalized pages, blocks, tables, cells, geometry, and transform lineage","Do not repair, merge, vote, or select"])
yn,ab=node_amber(1,"STAGE 4","Primary-statement location hypotheses",["Return bounded contiguous ranges with page roles, source-addressable semantic evidence, recomputable table structure, and alternatives"])
main("blue","STAGE 5","Validate every hypothesis claim",["Check IDs/order/span, exact quotes/coordinates, table properties, page roles, and explicit contradictions"],from_amber=ab)
retry_block(1,["Retryable evidence failure","and attempts used < 3?"],yn,2,["At least one hypothesis","admitted?"],"Yes","failed after 3 or nonretryable","Record location as ineligible with its failed gate IDs",2)
main("green","STAGE 5","Compare hypothesis sets",["Retain admitted/rejected ranges and evidence differences"])
yn,ab=node_amber(3,"STAGE 6A","Select one admitted range",["Return selected_hypothesis_id or unresolved"])
main("blue","STAGE 6A","Test range selection",["Require membership in the admitted set"],from_amber=ab)
retry_block(3,["Retryable selection failure","and attempts used < 3?"],yn,4,["One admitted range","selected?"],"Yes","ambiguous or exhausted","Record statement/branch as ineligible",4)
yn,ab=node_amber(5,"STAGE 6B","Isolated semantic extraction",["Receive only the selected range and return one complete typed candidate with assignments, hierarchy, alternatives, and evidence"])
main("blue","STAGE 7–8","Deterministic extraction gates",["[V7] Selected-range provenance, source, schema, and scope","[V8] Derivation and accounting","[V10] Fine-grained parent/child coverage","Run V10 even when V8 fails"],from_amber=ab)
retry_block(5,["Retryable gate failed","and attempts used < 3?"],yn,6,["V7, V8, V10 passed?"],"Yes · pass","failed after 3 or nonretryable","Record statement/branch as ineligible with its failed gate IDs",6)
main("green","STAGE 9","Cross-branch statement and coverage comparison",["[V9/R9] Compare structured results and eligibility","[V11/R11] Compare full object universes and ledgers","Do not repair, merge, vote, or select","Retain separate R9 and R11 records, statuses, evidence, and eligibility"])
main("blue","STAGE 10","Standard-concept mapping",["[V12] Candidate retrieval","Retrieve a bounded XBRL candidate set from a pinned index"])
main("green","STAGE 11","Mapping comparison",["Compare validated candidate sets and selections","No repair or score-based selection"])
main("blue","STAGE 12","Branch selection, readiness, persistence",["Apply frozen primary/fallback/no-mixing policy","Consume every gate and comparison; persist all branches"])
c=prev+GAP+GH; arrow([(MCX,prev),(MCX,c-GH)]); gate(c,7,["Ready?"])
lay=layout(MW,None,"Release the versioned evidence package and non-approving downstream candidates",[])
top=c+GH+44; arrow([(MCX,c+GH),(MCX,top)]); T(MCX+8,c+GH+24,"Yes","al"); h=box(MX,top,MW,"blue",lay); yr=top+h/2
ha=sidebox(c,"Keep the blocked package inspectable"); arrow([(MCX+GWH,c),(SX,c)]); T((MCX+GWH+SX)/2-2,c-7,"No","al","middle")
lines=wrap("Do not send it to automatic reconstruction",SW-28,12.5,True); hb=len(lines)*17+22
arrow([(SCX,c+ha/2),(SCX,yr-hb/2)]); sidebox(yr,"Do not send it to automatic reconstruction")
yn=top+h+GAP+NR; arrow([(MCX,top+h),(MCX,yn-NR)]); node(yn,7); arrow([(SCX,yr+hb/2),(SCX,yn),(MCX+NR,yn)])
fy=yn+NR+GAP+10; arrow([(MCX,yn+NR),(MCX,fy-10)])
o.append(f'<circle cx="{MCX}" cy="{fy}" r="10" class="fin-o"/><circle cx="{MCX}" cy="{fy}" r="5.5" class="dot"/>'); T(MCX+18,fy+4,"Finish","al2")
H=fy+10+34+TOP
body=o[body_start:]
pre=[f'<rect x="16" y="{TOP}" width="{DIV-16}" height="{H-2*TOP:.0f}" class="lane lane-d"/>',
     f'<rect x="{DIV}" y="{TOP}" width="{W-16-DIV}" height="{H-2*TOP:.0f}" class="lane lane-p"/>',
     f'<line x1="16" y1="{TOP+HEAD}" x2="{W-16}" y2="{TOP+HEAD}" class="lane-rule"/>']
o[:]=[]
T((16+DIV)/2,TOP+28,"DETERMINISTIC","lane-h","middle"); T((DIV+W-16)/2,TOP+28,"PROBABILISTIC (LLM)","lane-h","middle")
T((16+DIV)/2,H-TOP-12,"DETERMINISTIC","lane-f","middle"); T((DIV+W-16)/2,H-TOP-12,"PROBABILISTIC (LLM)","lane-f","middle")
ARIA="Two-lane activity diagram of the per-parser financial statement extraction pipeline, stages 0 to 12, with three bounded LLM retry loops and seven deterministic gates."
inner="\n".join(pre+o+body)
DARK=TOKENS_DARK+"\n  color-scheme:dark"
tokens_css=(":root{\n"+TOKENS_LIGHT+"\n}\n"
  "@media (prefers-color-scheme: dark){ :root:not([data-theme=\"light\"]){\n"+DARK+" } }\n"
  ":root[data-theme=\"dark\"]{\n"+DARK+" }")
inline_svg=f'<svg viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{ARIA}">\n{inner}\n</svg>'
page=(HERE/f"{NAME}.template.html").read_text().replace("{{TOKENS_CSS}}",tokens_css).replace("{{DIAGRAM_CSS}}",DIAGRAM_CSS).replace("{{SVG}}",inline_svg)
(HERE/f"{NAME}.html").write_text(page)
standalone=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" role="img" aria-label="{ARIA}">\n'
  f'<title>Statement extraction pipeline</title>\n<style>\n{tokens_css}\nsvg{{font-family:var(--font-body)}}\n.bg{{fill:var(--bg)}}\n{DIAGRAM_CSS}\n</style>\n'
  f'<rect class="bg" width="{W}" height="{H:.0f}"/>\n{inner}\n</svg>\n')
(HERE/f"{NAME}.svg").write_text(standalone)
print(f"wrote {NAME}.svg and {NAME}.html ({W}x{H:.0f})")
