"""Build and read back a lossless authored OP/80-task evidence workbook.

No original PDF body is copied. All inputs are committed-style authored research
and task records. Long values are split to an explicit continuation sheet before
openpyxl can truncate them. Every saved cell is read back and reconstructed.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO
import hashlib
import json
import os
import tempfile
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

APP=Path(__file__).resolve().parents[1]
OUT=APP/'qa/op-completion-20261102'
TARGET=OUT/'OP与工程验收矩阵.xlsx'
RECEIPT=OUT/'workbook-readback-receipt.json'
SOURCE_SHA='sha256:4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
INPUTS=['sources/op-completion-review.json','qa/op-completion-20261102/services/services-author.json','qa/op-completion-20261102/finance/finance-author.json','COI_TASK_REGISTRY_V1_7.json','qa/op-completion-20261102/independent/initial-source-findings.json']
raw={}
for name in INPUTS:
    p=APP/name
    if not p.is_file():raise SystemExit('PENDING_REQUIRED_FINAL_INPUT: '+name+'; no workbook published')
    raw[name]=p.read_bytes()
parsed={k:json.loads(v) for k,v in raw.items()}
r=parsed[INPUTS[0]];services=parsed[INPUTS[1]];finance=parsed[INPUTS[2]];registry=parsed[INPUTS[3]];independent=parsed[INPUTS[4]]
def digest(b):return 'sha256:'+hashlib.sha256(b if isinstance(b,bytes) else b.encode()).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def string(v):return canon(v) if isinstance(v,(dict,list)) else v
def clean(v):
    if isinstance(v,dict):return {k:clean(x) for k,x in v.items() if k not in ['localOnlyCrop','localCropPath']}
    if isinstance(v,list):return [clean(x) for x in v]
    return v
assert r['sourceRevision']==services['sourceRevision']==finance['sourceRevision']==SOURCE_SHA
assert len(r['pages'])==142 and sorted(p['pdfPage'] for p in r['pages'])==list(range(1,143))
units=[u for n in r['records'] for u in n['facts'].get('units',[])]
assert len({u['id'] for u in units})==len(units)==r['counts']['semanticUnits']
author_units=clean(services['units']+finance['units'])
assert {u['id']:u for u in units}=={u['id']:u for u in author_units},'RUNTIME_AUTHOR_UNIT_PROJECTION_DIFFERS'
for name in INPUTS[1:3]:assert r['sourceAuthorHashes'][name]==digest(raw[name]),'STALE_COMPILED_AUTHOR_HASH: '+name
tasks=registry['tasks'];assert len(tasks)==80 and {t['id'] for t in tasks}=={f'COI-{i:03d}' for i in range(1,81)}
references=r['referenceIndex'];assert len(references)==r['counts']['allPrintedCspReferenceOccurrences']
formal_refs=[ref for ref in references if ref['unitCategory'] in ['SERVICE_ACTION','PROJECT','IMPROVEMENT_ACTION']]
assert len(formal_refs)==r['counts']['formalPrintedCspReferenceOccurrences']
unit_ids={u['id'] for u in units};assert all(ref['unitId'] in unit_ids for ref in references)
# A continued row is navigable from every source page, but stored/counts once.
for p in r['pages']:assert set(p['unitIds'])=={u['id'] for u in units if p['pdfPage'] in u.get('pages',[u['pdfPage']])}

wb=Workbook();wb.remove(wb.active)
expected={};long_rows=[];split_references={};id_columns={}
MAX_UNITS=30000  # below Excel's 32767 UTF-16 code-unit cell limit
def utf16length(v):return len(v.encode('utf-16-le'))//2
def chunks(v):
    out=[];part=[];length=0
    for char in v:
        n=2 if ord(char)>0xffff else 1
        if length+n>MAX_UNITS:out.append(''.join(part));part=[];length=0
        part.append(char);length+=n
    if part:out.append(''.join(part))
    assert ''.join(out)==v and all(utf16length(s)<=MAX_UNITS for s in out)
    return out

def make_sheet(name,headers,rows,id_column=None):
    rows=[[string(c) for c in row] for row in rows]
    assert all(len(row)==len(headers) for row in rows),name
    expected[name]=[headers,*rows]
    ws=wb.create_sheet(name);ws.append(headers)
    if id_column is not None:
        ids=[row[id_column] for row in rows]
        assert len(set(ids))==len(ids),'DUPLICATE_SHEET_ROW_ID: '+name
        id_columns[name]=id_column
    for ri,row in enumerate(rows,2):
        encoded=[]
        for ci,value in enumerate(row,1):
            if isinstance(value,str) and utf16length(value)>MAX_UNITS:
                key=f'{name}!R{ri}C{ci}'
                parts=chunks(value);marker=f'LONG_TEXT:{key}; parts={len(parts)}; sha256={digest(value)}'
                split_references[(name,ri,ci)]=(key,len(parts),digest(value))
                for k,part in enumerate(parts,1):long_rows.append([key,name,ri,headers[ci-1],k,len(parts),part,digest(value)])
                encoded.append(marker)
            else:encoded.append(value)
        ws.append(encoded)
    ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions;ws.sheet_view.zoomScale=85
    for row in ws:
        for cell in row:
            if isinstance(cell.value,str):cell.data_type='s'  # never reinterpret source strings as formulas
            cell.alignment=Alignment(vertical='top',wrap_text=True)
    for cell in ws[1]:cell.fill=PatternFill('solid',fgColor='163F47');cell.font=Font(color='FFFFFF',bold=True)
    for index,head in enumerate(headers,1):
        letter=openpyxl.utils.get_column_letter(index)
        ws.column_dimensions[letter].width=14 if 'PDF页' in head else (34 if index<=3 else 52)
    for row in range(2,ws.max_row+1):ws.row_dimensions[row].height=54
    return ws

state_counts=dict(Counter(t['status'] for t in tasks))
make_sheet('说明',['项目','实际范围与限制'],[
 ['研究对象','同一登记 OP 2026–27 原件，142 页；没有扩展其他年份、另建系统或导入私人数据。'],
 ['原件SHA256',SOURCE_SHA],['来源ID',r['sourceId']],
 ['阅读单元分母',r['counts']],
 ['CSP引用出现口径',{'formalTableOccurrences':len(formal_refs),'guideExampleOccurrences':sum(x['unitCategory']=='GUIDE_EXAMPLE' for x in references),'overviewOccurrences':sum(x['unitCategory']=='FRONT_MATTER' for x in references),'meaning':'正式表内出现、教学示例、概览单列；均只证明文档印刷关系，不是已完成行动或官方准入。'}],
 ['计数含义','每单元包括作者定义的正文、行动/KPI子行、预算行、版本、术语、图与地图等；数量不等于项目数或理解百分比。'],
 ['80任务含义','原 80 项工程任务，与 Council 项目数及来源阅读单元数分开；原状态/证据和本轮边界完整保存。'],
 ['80项登记状态',state_counts],
 ['研究与实际区别','计划目标、预算金额、来源引用、作者研究与当前实际执行/产出/支出/效果分开，未核实的实际均UNKNOWN。'],
 ['版本限制',finance['sourceVersionBoundaries']],
 ['金额与单位','保留原文 $、$000、$\'000、M、年份、负括号、空白、破折号及N/A；不推断AUD，不跨不同预算口径相加。'],
 ['正式边界','独立AI原件复核不构成Council审批、现行法律意见、地块准入或真实履职证明。'],
 ['旧资料恢复','Phase1已恢复的原档与离线未提交Phase2分开；当前成果是登记官方原件补做，不称找回未访问的旧文件。'],
 ['实际验收','本表仅证明输入投影、工作簿完整读回和明确范围。应用/浏览器/线上发布以主任务对应源码的验收回执为准。'],
 ['长文本','超出安全单元长度时写入“长文本续页”；原单元保留指针和SHA，读回逐段复原比较，禁止截断。'],
 ['原件版权与位置','不包含原PDF、完整正文或原图；所有内容为自写摘要、短事实格、来源坐标与指纹。'],
 ['当前范围',r['scope']]])
make_sheet('输入指纹',['相对路径','SHA256','字节数'],[[k,digest(v),len(v)] for k,v in raw.items()],0)
make_sheet('142页覆盖',['PDF页','章节','页面状态','原页文字SHA','源记录ID','单元ID','剩余边界','完整页面覆盖记录'],[
 [p['pdfPage'],p['section'],p['status'],p['pageDigest'],p['recordIds'],p['unitIds'],p['gap'],p] for p in r['pages']],0)
make_sheet('全部阅读单元',['ID','PDF页','类别','章节','标题','自写摘要','事实与原单位','条件','限定','逐字段原件位置','印刷CSP引用','印刷LSPS引用','原有记录ID','原件SHA','完整单元JSON'],[
 [u['id'],u['pdfPage'],u['category'],u['section'],u['title'],u['summary'],u['facts'],u['conditions'],u['qualifiers'],u['sourceAnchors'],u['cspReferences'],u['lspsReferences'],u['existingRecordIds'],SOURCE_SHA,u] for u in units],0)

numeric_rows=[]
def numeric_objects(v,path):
    if isinstance(v,dict):
        if 'display' in v and 'unit' in v:yield path,v
        for k,x in v.items():yield from numeric_objects(x,path+'.'+k)
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from numeric_objects(x,f'{path}[{i}]')
for u in units:
    for path,v in numeric_objects(u['facts'],'facts'):
        anchors=[a for a in u['sourceAnchors'] if a['field']==path or a['field'].startswith(path+'.')]
        numeric_rows.append([u['id']+'::'+path,u['id'],u['pdfPage'],path,v.get('column'),v['display'],v['unit'],v.get('currency'),v.get('period'),v.get('numericValue'),v.get('status'),v.get('signConvention'),v.get('meaning'),anchors or u['sourceAnchors'],v])
make_sheet('数字与单位',['定位ID','单元ID','PDF页','事实字段','列','印刷值','印刷单位','币种状态','期间','数值解释','空白或值状态','符号约定','含义','来源锚','完整数值对象'],numeric_rows,0)
make_sheet('CSP印刷关系',['出现ID','单元ID','PDF页','单元类别','引用计数口径','原代码','解析目标ID','关系边界','来源锚与完整引用'],[
 [f'CSPREF-{i:04d}',ref['unitId'],ref['pdfPage'],ref['unitCategory'],'FORMAL_TABLE' if ref['unitCategory'] in ['SERVICE_ACTION','PROJECT','IMPROVEMENT_ACTION'] else ('GUIDE_EXAMPLE' if ref['unitCategory']=='GUIDE_EXAMPLE' else 'OVERVIEW'),ref['code'],ref.get('targetId'),'PRINTED_SOURCE_REFERENCE_ONLY; NOT_EXECUTION_CAUSALITY_OR_ACTUAL_ASSIGNMENT',ref] for i,ref in enumerate(references,1)],0)
make_sheet('源内诊断',['诊断ID','类型','PDF页','相关单元','完整诊断'],[
 [f'DIAG-{i:04d}',d.get('type',d.get('category')),d.get('pdfPages',d.get('pdfPage')),d.get('sourceUnitIds',d.get('unitIds',[])),d] for i,d in enumerate(r['diagnostics'],1)],0)
make_sheet('独立原件疑点',['疑点ID','PDF页','完整原件发现'],[
 [f'INDEPENDENT-{i:04d}',d.get('pdfPages',d.get('pdfPage')),d] for i,d in enumerate(independent['findings'],1)],0)
make_sheet('80原任务',['ID','原Pack','状态','原任务范围','代码文件','测试命令','已有证据','登记源码SHA','阻塞','下一步','来源准入状态','完整原登记行'],[
 [t['id'],t.get('pack'),t['status'],t['title_and_scope'],t.get('actual_code_files',[]),t.get('actual_test_commands',[]),t.get('evidence_links',[]),t.get('remote_sha'),t.get('blocker'),t.get('next_action'),t.get('source_admission_status'),t] for t in tasks],0)
make_sheet('80项分层验收',['ID','本轮有限实现','剩余缺口','缺口类型','可自主下一步','完成判据','软件能力','公开证据','人工准入边界','现在需Founder动作','最终外部依赖','完整分层记录'],[
 [t['id'],t.get('closureBaseline',{}).get('actualBoundedImplementation'),t.get('closureBaseline',{}).get('remainingGap'),t.get('closureBaseline',{}).get('gapTypes'),t.get('closureBaseline',{}).get('independentlyExecutableNextAction'),t.get('closureBaseline',{}).get('completionCriterion'),t.get('closureBaseline',{}).get('softwareCapabilityAssessment'),t.get('closureBaseline',{}).get('publicEvidenceAssessment'),t.get('closureBaseline',{}).get('humanAdmissionAssessment'),t.get('closureBaseline',{}).get('founderActionNeededNow'),t.get('closureBaseline',{}).get('eventualDependency'),t.get('closureBaseline',{})] for t in tasks],0)
make_sheet('长文本续页',['续页ID','源工作表','源行','源字段','段号','段数','完整段内容','原值SHA256'],long_rows)

# A real overflow exercise is independent of whether today's data has long cells.
probe='段😀'+('x'*29998)+'中'+('y'*35000)
probe_chunks=chunks(probe)
assert len(probe_chunks)>=3 and ''.join(probe_chunks)==probe
assert all(utf16length(s)<=MAX_UNITS for s in probe_chunks)
probe_wb=Workbook();probe_ws=probe_wb.active
for i,chunk in enumerate(probe_chunks,1):probe_ws.append([i,chunk])
probe_bytes=BytesIO();probe_wb.save(probe_bytes);probe_bytes.seek(0)
probe_saved=openpyxl.load_workbook(probe_bytes,read_only=True,data_only=False)
assert ''.join(row[1] for row in probe_saved.active.iter_rows(values_only=True))==probe
probe_saved.close()

with tempfile.NamedTemporaryFile(prefix='.op-review-workbook-',suffix='.xlsx',dir=OUT,delete=False) as temp:temp_path=Path(temp.name)
try:
    wb.save(temp_path)
    saved=openpyxl.load_workbook(temp_path,read_only=True,data_only=False)
    assert saved.sheetnames==wb.sheetnames
    saved_long=list(saved['长文本续页'].iter_rows(min_row=2,values_only=True))
    reassembled={}
    for row in saved_long:
        if row[0] is not None:reassembled.setdefault(row[0],[]).append(row)
    cell_count=0;max_units=0;sheet_receipts=[]
    for name,rows in expected.items():
        ws=saved[name];got=list(ws.iter_rows(values_only=True))
        assert len(got)==len(rows),f'ROW_COUNT_CHANGED:{name}'
        logical=[]
        for ri,(want_row,got_row) in enumerate(zip(rows,got),1):
            assert len(want_row)==len(got_row),f'COLUMN_COUNT_CHANGED:{name}'
            restored=[]
            for ci,(wanted,actual) in enumerate(zip(want_row,got_row),1):
                if isinstance(actual,str):max_units=max(max_units,utf16length(actual));assert utf16length(actual)<=32767
                key=(name,ri,ci)
                if key in split_references:
                    ref,n,h=split_references[key];parts=sorted(reassembled[ref],key=lambda x:x[4])
                    assert len(parts)==n and [p[4] for p in parts]==list(range(1,n+1))
                    actual=''.join(p[6] for p in parts)
                    assert digest(actual)==h
                assert actual==wanted or (actual is None and wanted==''),f'CELL_READBACK_DIFFERS:{name}!R{ri}C{ci}'
                restored.append(wanted);cell_count+=1
            logical.append(restored)
        if name in id_columns:
            idx=id_columns[name];assert [row[idx] for row in logical[1:]]==[row[idx] for row in rows[1:]]
        sheet_receipts.append({'name':name,'dataRows':len(rows)-1,'columns':len(rows[0]),'logicalContentSha256':digest(canon(rows)),'allCellsExactlyReadBack':True})
    assert sum(1 for _ in saved['142页覆盖'].iter_rows(min_row=2,values_only=True))==142
    assert sum(1 for _ in saved['80原任务'].iter_rows(min_row=2,values_only=True))==80
    saved.close()
    # Inputs must not change during generation; mutation requires a fresh rebuild.
    for k,v in raw.items():assert (APP/k).read_bytes()==v,'INPUT_CHANGED_DURING_BUILD: '+k
    os.replace(temp_path,TARGET)
except Exception:
    temp_path.unlink(missing_ok=True)
    raise

receipt={'format':'csoi-op-review-workbook-readback-1','status':'PASS_WORKBOOK_CONTENT_AND_AUTHOR_PROJECTION_READBACK_ONLY','createdAt':datetime.now(timezone.utc).isoformat(),'workbook':str(TARGET.relative_to(APP)),'workbookSha256':digest(TARGET.read_bytes()),'openpyxlVersion':openpyxl.__version__,'sourceRevision':SOURCE_SHA,'inputSha256':{k:digest(v) for k,v in raw.items()},'sourceCounts':r['counts'],'registryStateCountsAsRead':state_counts,'exactCellsReadBack':cell_count,'maxSavedCellUtf16Units':max_units,'splitLogicalValues':len(split_references),'continuationRows':len(long_rows),'syntheticOverflowProbe':{'utf16Units':utf16length(probe),'parts':len(probe_chunks),'reassembledExactly':True,'actualXlsxRoundTrip':True},'sheets':sheet_receipts,'limitations':['This verifies the exported authored records and task registry; it does not prove source semantics independently.','No app/native/browser/deployment result is inferred from this workbook check.','80 engineering tasks are not 80 Council projects.','Currentness/legal/parcel/actual execution remain bounded by original source records.']}
receipt['retainedPriorRejectedBuilds']=[
 {'sequence':1,'date':'2026-11-02','stage':'author/runtime equality before workbook writing','outcome':'REJECTED_NO_WORKBOOK_PUBLISHED','reason':'RUNTIME_AUTHOR_UNIT_PROJECTION_DIFFERS: 47 service section values differed while service author was still being corrected.','resolution':'Waited for corrected final author input and rebuilt compiler output; equality check retained.'},
 {'sequence':2,'date':'2026-11-02','stage':'author/runtime equality after first final-source notification','outcome':'REJECTED_NO_WORKBOOK_PUBLISHED','reason':'RUNTIME_AUTHOR_UNIT_PROJECTION_DIFFERS: only P142 public-contact.summary differed; compiled unit had earlier summary while sourceAuthorHashes already referred to new finance bytes.','resolution':'Root confirmed input-read race, changed compiler to snapshot input bytes, hash those same bytes and verify unchanged inputs before writing; strict equality retained.'},
 {'sequence':3,'date':'2026-11-02','stage':'final row-count assertion after successful individual-cell reads','outcome':'REJECTED_NO_WORKBOOK_PUBLISHED','reason':'Workbook author used unsupported ReadOnlyWorksheet column indexing; AttributeError iter_cols.','resolution':'Changed final row counting to supported iter_rows and reran complete export/readback.'},
 {'sequence':4,'date':'2026-11-02','stage':'atomic output rename after successful workbook readback','outcome':'REJECTED_NO_WORKBOOK_PUBLISHED','reason':'Temporary /tmp and final /workspace are different filesystems; os.replace raised EXDEV.','resolution':'Create transient workbook in final output directory, retain same readback and atomic rename, remove temporary file on failure.'}
]
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'unitRows':len(units),'pageRows':142,'cspRows':len(references),'taskRows':80,'exactCellsReadBack':cell_count,'splitValues':len(split_references),'workbookSha256':receipt['workbookSha256']},ensure_ascii=False))
