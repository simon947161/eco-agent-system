"""Readable source coverage, no original PDF reproduction or official admission."""
from pathlib import Path
import json,csv
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.worksheet.table import Table,TableStyleInfo
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/lsps-completion'
r=json.loads((APP/'sources/lsps-context-review.json').read_text());a=json.loads((OUT/'author/narrative-review.json').read_text());registry=json.loads((APP/'COI_TASK_REGISTRY_V1_7.json').read_text())
wb=Workbook();wb.remove(wb.active)
def val(v):return json.dumps(v,ensure_ascii=False)if isinstance(v,(dict,list))else v

def sheet(name,headers,rows):
 ws=wb.create_sheet(name);ws.append(headers)
 for row in rows:ws.append([val(x)for x in row])
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 for c in ws[1]:c.fill=PatternFill('solid',fgColor='173F46');c.font=Font(color='FFFFFF',bold=True);c.alignment=Alignment(wrap_text=True)
 for row in ws.iter_rows(min_row=2):
  for cell in row:cell.alignment=Alignment(vertical='top',wrap_text=True)
 for col in ws.columns:ws.column_dimensions[col[0].column_letter].width=18 if col[0].column in [1,2]else 48
 return ws
sheet('说明',['项目','实际范围'],[
 ['来源','Snowy Monaro LSPS 2020，118页；历史原件，并非现行法律认定'],['原件SHA256',r['sourceRevision']],['阅读计数','512阅读单元含491文本与21视觉语义单元；不等同512实质段落。地图为27处出现位置。'],['图表计数','独立视觉盘点17图表出现位置；21视觉语义单元的拆分/替代映射在author/visual-occurrence-crosswalk.json。'],['保留内容','原12优先事项、83实施表行动、18冲突观察及原114记录未覆盖。'],['正式边界','独立AI原文/像素对照不是Council审批或专业人工签认；现行性/法律/地块/实际工作UNKNOWN。'],['运行验收','以acceptance.json和实际测试回执为准；本工作簿不替代浏览器/线上验收。'],['原文件恢复','Phase1审计原档已恢复；旧离线任务未提交Phase2仍不可访问，本次为官方公开原件补做。']])
sheet('118页覆盖',['PDF页','章节','原页摘要哈希','处理状态','阅读记录','仍缺'],[[p['pdfPage'],p['section'],p['pageDigest'],p['status'],p['recordIds'],p['gap']]for p in r['pages']])
units=[u for n in r['records']for u in n['facts'].get('units',[])]
sheet('512阅读单元',['ID','PDF页','类型/标题','自写摘要','原文条件','限定','原件位置','关联既有行动','语义审读'],[[u['id'],u['pdfPage'],u['unitKind']+' / '+u['heading'],u['summary'],[x['text']if isinstance(x,dict)else x for x in u['conditions']],[x['text']if isinstance(x,dict)else x for x in u['qualifiers']],u['evidenceAnchors'],u['existingActionIds'],u['reviewStatus']]for u in units])
maps=[n['facts']['map']for n in r['records']if n['category']=='LSPS_MAP']
sheet('27地图出现位置',['ID','PDF页','原图名称','解读','全部图例','条件','限定','比例/指北/CRS','图例像素锚点'],[[m['id'],m['pdfPage'],m['title'],m['summary'],m['legend'],m['conditions'],m['qualifiers'],{'scale':m['scale'],'north':m['north'],'CRS':m['coordinateReferenceSystem']},m['legendAnchor']]for m in maps])
sheet('80工程任务',['ID','状态','范围','剩余约束','下一步','证据'],[[t['id'],t['status'],t['title_and_scope'],t.get('blocker'),t.get('next_action'),t.get('evidence_links',[])]for t in registry['tasks']])
wb.save(OUT/'LSPS原文地图覆盖矩阵.xlsx')
print('PASS: readable workbook118pages/512units/27maps/80engineering tasks; no official completion promotion')
