"""Bounded semantic regression checks grounded in the original CSP rows, not a completeness claim."""
from pathlib import Path
import argparse,copy,datetime,importlib.util,json,re
APP=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('original_csp',APP/'tools/verify-csp-knowledge.py');original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
def need(ok,reason):
 if not ok:raise ValueError(reason)
def verify(source,bundle):
 source.verify(bundle)
 rows={n['code']:n for n in bundle['records']if n['category']=='CSP_INDICATOR'}
 # These expectations were selected from the original table during independent reading.
 required={
 '29-community-07':['至少一个','one or more'], '29-community-08':['出生时','all persons'],
 '29-community-09':['总人口'], '29-community-10':['总人口'], '29-community-11':['all persons'],
 '29-community-14':['>30%'], '29-community-15':['>30%'], '29-community-23':['reticulated water supplies'],
 '29-community-24':['100,000'], '30-economy-01':['2024','全州'], '30-economy-03':['2022','NSW'],
 '30-economy-04':['15—64','Certificate III','非学校'], '30-economy-07':['找工作'],
 '30-economy-08':['regional NSW'], '30-economy-09':['净储蓄','regional NSW'],
 '30-environment-04':['平均','lodgement'], '30-environment-05':['平均','assessment'],
 '30-environment-06':['满意度','community values'], '30-environment-08':['关键'],
 '31-infrastructure-01':['每人'], '31-infrastructure-04':['供水','污水','100 公里'],
 '31-infrastructure-05':['供水','污水','合计'], '31-infrastructure-11':['潮汐','岩石'],
 '31-infrastructure-12':['Council','令人满意'], '31-civic-02':['平均'],
 '31-civic-03':['典型','sewerage'], '31-civic-06':['having a say','being heard']}
 for suffix,tokens in required.items():
  f=rows['CSP-KPI-'+suffix]['facts'];need(all(t in f['definition']for t in tokens),'DEFINITION_QUALIFIER:'+suffix)
 crime=rows['CSP-KPI-29-community-24']['facts'];need('100000'in crime['denominator']['normalisationReference']and '100-unit'not in crime['denominator']['label'],'CRIME_NORMALISATION_100000')
 for n in rows.values():
  f=n['facts'];r=f['semanticReview'];need(r['method']=='INDEPENDENT_AI_SOURCE_REVIEW_NOT_OFFICIAL'and r['sourceRevision']==source.sha,'REVIEW_NOT_OFFICIAL')
  need(f['target']['value']=='UNKNOWN_NOT_STATED'and f['target']['due']=='UNKNOWN_NOT_STATED','NO_NUMERIC_TARGET_OR_DEADLINE')
  need(f['timeInterval']['from']=='UNKNOWN'and f['timeInterval']['to']=='UNKNOWN','NO_INFERRED_EXACT_PERIOD')
  if f['measurementYearLabel'].startswith('UNKNOWN'):need(f['referencePeriod']['label']=='UNKNOWN_NOT_STATED_IN_MEASURE','SOURCE_DATE_IS_NOT_MEASUREMENT_PERIOD')
  else:need(f['referencePeriod']['label']==f['measurementYearLabel'],'MEASURE_PERIOD_PRESERVED')
  need(f['responsibleRole']=='UNKNOWN'and f['officialRelationship']=='UNKNOWN_NOT_ADMITTED','NO_INFERRED_ACCOUNTABLE_ROLE')
  need(f['baseline']['currency']in ['UNKNOWN','UNKNOWN_DOLLAR_CURRENCY_NOT_STATED_IN_ROW'],'NO_INFERRED_CURRENCY_CODE')
  need(len(f['formula']['requiredInputs'])>=3 and len(r['calculation'])>30,'ROW_SPECIFIC_CALCULATION_LIMITS')
 for suffix in ['31-infrastructure-05','31-infrastructure-06','31-civic-01','31-civic-04','30-economy-08']:need(rows['CSP-KPI-'+suffix]['facts']['baseline']['unit']=='UNKNOWN','NO_INVENTED_UNIT:'+suffix)
 need(rows['CSP-KPI-30-economy-02']['facts']['sourceYear']=='2024'and rows['CSP-KPI-30-economy-02']['facts']['referencePeriod']['label']=='2023','BUSINESS_MEASURE_2023_SOURCE_2024')
 return {'status':'PASS_BOUNDED_SEMANTIC_REGRESSIONS','indicators':63,'definitionQualifierRows':len(required),'sourceColumnsChecked':252,'sourceRevision':source.sha,'humanSemanticAdmission':'PENDING','rawDataRecalculation':'NOT_COMPUTABLE','limits':'Selected regression assertions supplement the63-row independent reading/readback; neither checks nor hashes prove full-document understanding.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);p.add_argument('bundle',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=original.Source(a.pdf);b=json.loads(a.bundle.read_text());result=verify(source,b);cases=[]
 def reject(label,mutate):
  x=copy.deepcopy(b);by={n['code']:n for n in x['records']};mutate(x,by)
  try:verify(source,x)
  except (ValueError,KeyError)as e:cases.append({'case':label,'status':'REJECTED_EXPECTED','reason':str(e)});return
  raise AssertionError('SEMANTIC_NEGATIVE_ACCEPTED:'+label)
 reject('crime100instead100000',lambda x,r:r['CSP-KPI-29-community-24']['facts']['denominator'].update(normalisationReference='100-unit normalisation'))
 reject('missing-child-one-or-more',lambda x,r:r['CSP-KPI-29-community-07']['facts'].update(definition='儿童发展脆弱比例'))
 reject('missing-qualification-age',lambda x,r:r['CSP-KPI-30-economy-04']['facts'].update(definition='学历比例'))
 reject('mortgage-threshold-nonstrict',lambda x,r:r['CSP-KPI-29-community-14']['facts'].update(definition='按揭费用 >=30% 的比例'))
 reject('source2024-as-business-measure',lambda x,r:r['CSP-KPI-30-economy-02']['facts']['referencePeriod'].update(label='2024'))
 reject('source2021-as-survey-measure',lambda x,r:r['CSP-KPI-29-community-01']['facts']['referencePeriod'].update(label='2021'))
 reject('invented-numeric-target',lambda x,r:r['CSP-KPI-29-community-01']['facts']['target'].update(value=100))
 reject('invented2035-deadline',lambda x,r:r['CSP-KPI-29-community-01']['facts']['target'].update(due='2035-12-31'))
 reject('invented-council-responsibility',lambda x,r:r['CSP-KPI-29-community-01']['facts'].update(responsibleRole='Council'))
 reject('invented-AUD-currency',lambda x,r:r['CSP-KPI-29-community-04']['facts']['baseline'].update(currency='AUD'))
 reject('recycling48.3-as-percent',lambda x,r:r['CSP-KPI-31-infrastructure-06']['facts']['baseline'].update(unit='%'))
 reject('water7519-as-tonnes',lambda x,r:r['CSP-KPI-31-infrastructure-05']['facts']['baseline'].update(unit='tonnes'))
 reject('independent-review-as-approval',lambda x,r:r['CSP-KPI-29-community-01']['facts']['semanticReview'].update(method='COUNCIL_APPROVED'))
 reject('promote-baseline-to-actual',lambda x,r:r['CSP-KPI-29-community-01']['facts'].update(actualValue=72.5))
 result.update(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),negativeCases=cases);a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='negativeCases'},ensure_ascii=False));print('PASS:',len(cases),'semantic negative cases rejected')
if __name__=='__main__':main()
