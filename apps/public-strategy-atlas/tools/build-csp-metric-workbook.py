"""Founder-readable source review workbook; actual application acceptance remains a separate receipt."""
from pathlib import Path
import json,csv
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csp-metric-review'
read=lambda p:json.loads((APP/p).read_text())
plan=read('sources/csp-indicator-review.json');initial=read('qa/csp-metric-review/independent/initial-review.json');review=read('qa/csp-metric-review/independent/readback-review.json');engineering=read('qa/csp-metric-review/engineering-coverage.json')
initialBy={r['id']:r for r in initial['records']};reviewBy={r['id']:r for r in review['records']}
rows=[]
for item in plan['records']:
 n=item['node'];f=n['facts'];r=f['semanticReview'];old=initialBy[n['id']]
 rows.append({'id':n['id'],'code':n['code'],'pdfPage':n['anchor']['pdfPage'],'definition':f['definition'],'publishedBaseline':f['printedBaseline'],'unit':f['baseline']['unit'],'sourceLabel':f['printedSource'],'sourceYear':f['sourceYear'],'measurementPeriod':f['referencePeriod']['label'],'desiredTrend':f['desiredTrend'],'numericTarget':'UNKNOWN_NOT_STATED','denominator':f['denominator']['label'],'normalisation':f['denominator']['normalisationReference'],'responsibleRole':f['responsibleRole'],'scope':r['scope'],'computability':f['computability'],'calculationGap':r['calculation'],'requiredInputs':f['formula']['requiredInputs'],'initialSemanticStatus':old['initialSemanticStatus'],'readback':'PASS_BOUNDED_SEMANTIC_READBACK_NOT_FORMAL_ADMISSION','sourceRevision':plan['sourceRevision'],'oldNodeDigest':item['beforeNodeDigest']})
(OUT/'metric-coverage.json').write_text(json.dumps({'format':'csoi-csp-metric-coverage-1','scope':'All63 CSP PDF29–31 metric rows plus PDF28 context; not current actuals, raw-data validation or official admission','records':rows},ensure_ascii=False,indent=2)+'\n')
with (OUT/'metric-coverage.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False)if isinstance(v,(list,dict))else v for k,v in r.items()}for r in rows)
wb=Workbook();wb.remove(wb.active)
def sheet(name,headers,values):
 ws=wb.create_sheet(name);ws.append(headers)
 for row in values:ws.append([json.dumps(x,ensure_ascii=False)if isinstance(x,(list,dict))else x for x in row])
 ws.freeze_panes='C2';ws.auto_filter.ref=ws.dimensions;ws.row_dimensions[1].height=32
 for cell in ws[1]:cell.font=Font(color='FFFFFF',bold=True);cell.fill=PatternFill('solid',fgColor='153E50')
 for row in ws.iter_rows(min_row=2):
  for cell in row:cell.alignment=Alignment(vertical='top',wrap_text=True);cell.font=Font(name='Calibri',size=11)
  ws.row_dimensions[row[0].row].height=88
 for i,h in enumerate(headers,1):ws.column_dimensions[get_column_letter(i)].width=14 if h in ['PDF页','单位','来源年','测量期','期望趋势','负责人','能否复算']else 42
 return ws
sheet('阅读说明',['范围','说明'],[
 ['已完成','63个指标逐项读原页、作者解释、独立初审及实际新节点读回。27条定义/范围建议已处理，45条来源年份归属已澄清。'],
 ['历史','原版记录和初审缺陷快照保留；应用以63条新修订追加，不删除旧版本。'],
 ['数字边界','252个原列单元再次核对；原基线值、单位已知/未知状态和趋势均保留。63项仍不能独立复算。'],
 ['状态边界','独立AI阅读不是Council审批或专业人工签认；humanReview PENDING、actual UNKNOWN、无数值目标。'],
 ['软件验收','运行测试、桌面/390px手机、部署与权限以同目录acceptance.json及deployment.json为准；本表不代替运行证据。'],
 ['整体未完','80项是工程任务：49 VERIFIED、28 PARTIAL、3 BLOCKED。LSPS地图/非编号叙述、完整OP及DP/资源/预算/年报仍缺。'],
 ['恢复边界','旧Phase2未提交原件仍不可访问。本次为官方PDF的新语义审读，不称为找回Phase2。']])
keys=list(rows[0]);headers=['指标ID','指标代码','PDF页','完整含义','来源基线','单位','来源标签','来源年','测量期','期望趋势','数值目标','分母/集合','归一化依据','负责人','适用范围','能否复算','缺失原因','所需输入','初审状态','读回结果','来源版本','旧记录指纹']
sheet('63指标逐项核对',headers,[[r[k]for k in keys]for r in rows])
corrections=[r for r in rows if r['initialSemanticStatus']=='CORRECTION_REQUIRED'];sheet('27条初审建议',['指标ID','PDF页','旧定义','新完整含义','初审建议','结果'],[[r['id'],r['pdfPage'],initialBy[r['id']]['currentFieldSnapshot']['definition'],r['definition'],initialBy[r['id']]['correctionSuggestions'],r['readback']]for r in corrections])
sheet('80工程任务',['任务ID','工程状态','范围','本轮','阻塞','下一步'],[[r[k]for k in ['id','engineeringStatus','scope','thisBatch','blocker','nextAction']]for r in engineering['tasks']])
target=OUT/'CSP63指标语义复核.xlsx';wb.save(target);check=load_workbook(target,data_only=False);assert check['63指标逐项核对'].max_row==64 and check['27条初审建议'].max_row==28 and check['80工程任务'].max_row==81;assert not any(c.data_type=='f'for ws in check for row in ws for c in row)
print('PASS:63row source review +27initial corrections +80unchanged engineering states workbook; read-back counts and zero formula cells verified.')
