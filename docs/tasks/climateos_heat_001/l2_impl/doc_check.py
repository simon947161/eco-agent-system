from pathlib import Path
import re
docs=Path("docs")
bad=[]
for p in docs.glob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)",p.read_text(encoding="utf-8")):
        target=target.split("#",1)[0]
        if not target or target.startswith(("https://","http://","mailto:")):
            continue
        if not (p.parent/target).resolve().exists(): bad.append(f"{p.name}: {target}")
slides=len(re.findall(r"^## Slide \d+",(docs/"L2_FOUNDER_ACCEPTANCE_CN.md").read_text(encoding="utf-8"),re.M))
print({"markdown_files":len(list(docs.glob("*.md"))),"broken_local_links":bad,"founder_slides":slides})
if bad or slides<8: raise SystemExit(1)
