from pathlib import Path
import json
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
root=Path(__file__).resolve().parents[1]/'qa/strategy-completion'
read=lambda n:json.loads((root/n).read_text())
wb=Workbook();wb.remove(wb.active)
def sheet(name,rows):
 ws=wb.create_sheet(name)
 for row in rows:
  ws.append([json.dumps(v,ensure_ascii=False)if isinstance(v,(list,dict))else v for v in row])
  for c in ws[ws.max_row]:
   if isinstance(c.value,str):c.data_type='s'
   c.alignment=Alignment(vertical='top',wrap_text=True)
 for c in ws[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='143A44')
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 for col in ws.columns:
  width=min(58,max(18,max(len(str(c.value or''))for c in list(col)[:15])*.7));ws.column_dimensions[get_column_letter(col[0].column)].width=width
 return ws
sheet('中文说明',[['项目','说明'],['本轮范围','CSP14目标44策略63指标；LSPS12优先事项83实施行动及18冲突观察；OP仅选定8项水务活动。'],['不是整体完成','核心条目集合完整不等于整份文件所有正文、地图、现行适用性或Council实际工作完成。'],['80项的含义','80项是工程任务：49VERIFIED、28PARTIAL、3BLOCKED。不是80个Council项目。'],['原审计恢复','原中文报告和Excel已找回并核对哈希；原任务未提交Phase2仍不可访问。本轮是从官方原件重新补做。'],['如何核对','来源条目表逐行列文档版本、PDF页、提取、实现、核验和缺口；工程状态、关系表达、逐页范围分表。'],['审批和成效','正式准入PENDING；现行法律、实际执行、实际支出、因果归因UNKNOWN。'],['应用验收与发布','最终实际结果见同目录acceptance.json和deployment.json；本表不以历史测试冒充发布验收。']])
items=read('item-coverage.json')['rows'];keys=['family','category','code','title','sourceId','sourceVersion','pdfPage','pageDigest','locator','recordedLocator','recordRevision','extracted','implemented','verification','gaps'];sheet('252来源条目', [['文件族','类别','编号','条目','来源ID','原件版本','PDF页','页摘要','核对定位','当前记录定位','记录版本','提取','实现','核验','缺口']]+[[r.get(k)for k in keys]for r in items])
tasks=read('engineering-coverage.json')['tasks'];keys=['id','engineeringStatus','scope','thisBatch','actualCodeFiles','evidence','blocker','nextAction'];sheet('80工程任务',[['任务ID','工程状态','要求范围','本轮范围','代码文件','证据','阻塞','下一步']]+[[r.get(k)for k in keys]for r in tasks])
rel=read('relationship-coverage.json');rows=[]
for group in ['existing','newSelectedWaterReferences']:
 for r in rel[group]:rows.append([group,r.get('id'),r['from'],r['to'],r.get('predicate',r.get('type')),r['sourceId'],r['sourceVersion'],r['pdfPage'],r['pageDigest'],r['implemented'],r['verification'],r.get('evidenceMeaning',r.get('meaning')),r.get('gap','Official admissionPENDING;actual/causalityUNKNOWN')])
sheet('17关系表达',[['分组','ID','起点','终点','类型','来源','原件版本','PDF页','页摘要','实现','核验','解释','缺口']]+rows)
scopes=json.loads((root.parents[1]/'sources/strategy-review-scope.json').read_text())['documents'];rows=[]
for d in scopes:
 for p in d['pages']:rows.append([d['family'],d['sourceId'],d['sourceRevision'],p['pdfPage'],p['section'],p['status'],p['gap'],p['recordIds'],p['pageDigest']])
sheet('296页范围清单',[['文件族','来源','版本','PDF页','章节','检查范围','缺口','对应记录','页摘要']]+rows)
semantic=read('independent-review/semantic-review.json');records=semantic.get('items',semantic.get('records',semantic.get('rows',[])))
if records:
 keys=list(records[0]);sheet('153语义复核',[keys]+[[r.get(k)for k in keys]for r in records])
path=root/'本轮来源与工程审计矩阵.xlsx';wb.save(path);verify=load_workbook(path,read_only=True,data_only=False)
assert verify['252来源条目'].max_row==253 and verify['80工程任务'].max_row==81 and verify['17关系表达'].max_row==18 and verify['296页范围清单'].max_row==297
assert all(c.data_type!='f'for ws in verify for row in ws for c in row)
print(json.dumps({'file':str(path),'sheets':{ws.title:ws.max_row-1 for ws in verify},'formulaCells':0},ensure_ascii=False))
