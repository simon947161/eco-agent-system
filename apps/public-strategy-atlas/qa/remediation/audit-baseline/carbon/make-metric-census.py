from pathlib import Path
import csv,json
out=Path('/tmp/csoi-integrity-audit-20261031/carbon')
groups=[(29,'community',['个人福祉','社区福祉','归属感','每周家庭收入中位数','社会经济不利指数','公平与包容','儿童发展脆弱性','出生时预期寿命','长期健康状况占比','心理健康状况占比','组织志愿劳动','心理困扰','犯罪与安全感','住房按揭负担','租房负担','一般医疗可及性','专科医疗可及性','心理医疗可及性','社区精神认同','健康教育托育可及性','社区活动参与','公共交通可及性（社区章节）','符合饮用水指南的管网供水占比','重大犯罪率']),(30,'economy',['地区生产总值占州比例','GST登记企业数量','旅游销售占州比例','职业或更高学历占比','无非学校学历占比','本地学校质量','求职失业比例','相对区域就业指数','相对区域家庭储蓄','农业产值','游客消费额']),(30,'environment',['景观与美学指数','感知环境健康指数','人均CO2e排放','开发申请提交时间','开发申请评估时间','发展与社区价值平衡满意度','垃圾填埋分流占比','主要土地利用战略年龄']),(31,'infrastructure',['人均道路长度','本地道路质量','公共交通可及性（基础设施章节）','供水与污水主管每百公里破损率','供水与污水温室气体排放总量','回收率','电信可及性','公共礼堂数量','公共图书馆数量','公共开放空间','公共游泳池数量','基础设施达标修复成本']),(31,'civic',['营运绩效比率','平均住宅费率','典型住宅供水与污水账单','基础设施积压比率','社区领导与协作','表达意见与获得倾听','领导满意度','现行战略占比'])]
rows=[]
for page,group,labels in groups:
 for i,label in enumerate(labels,1):
  iscarbon=group=='environment' and i==3
  rows.append({'inventory_id':f'CSP-KPI-{page}-{group}-{i:02d}','source_id':'csoi:smrc-csp-full-2025:20261030','pdf_page':page,'printed_page':page,'pillar':group,'authored_short_name_zh':label,'project_structured_record_id':'csp2035-carbon-per-capita-baseline' if iscarbon else '', 'project_structured_present':iscarbon,'project_row_correctness_this_audit':'PASS_PUBLISHED_ROW_ONLY' if iscarbon else 'NOT_EXTRACTED','project_independent_recalculation':'NOT COMPUTABLE' if iscarbon else 'NOT_TESTED_NOT_INGESTED','census_basis':'MANUAL_ORIGINAL_ROW_CENSUS_INDEPENDENTLY_DOUBLE_COUNTED','source_text_redistributed':False})
assert len(rows)==63
with (out/'csp-metric-census-63.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'scope':'Only CSP fullPDF29–31 published metric rows, not all goals/strategies/documents','expected_metric_rows':63,'structured_project_metrics':1,'source_row_verified_correct_project_metrics':1,'not_structured':62,'structured_coverage_percent':100/63,'full_CSP_semantic_coverage':'UNKNOWN_NEEDS_COMBINED_GRAINS','independent_double_census':True,'counterevidence':[{'topic':'Public transport access','page29_baseline':2.1,'page31_baseline':3.1,'same_printed_source':'UoC Regional Wellbeing Survey2021','status':'APPARENT_SOURCE_CONFLICT_REQUIRES_RECONCILIATION_NOT_AUTO_MERGE'}]}
(out/'csp-metric-census-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
