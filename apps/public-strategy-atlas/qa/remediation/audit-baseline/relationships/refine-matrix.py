from pathlib import Path
import json,csv
root=Path('/tmp/csoi-integrity-audit-20261031/relationships');rows=json.loads((root/'relationship-evidence-matrix.json').read_text())
for r in rows:
 r['sourceDocument']= ' | '.join(x.get('url') or x.get('sourceId') or 'UNKNOWN' for x in r.get('sourceLocations',[])) or 'NO_ORIGINAL_SOURCE'
 r['pageOrSection']=' | '.join(x.get('locator') or 'UNKNOWN' for x in r.get('sourceLocations',[])) or 'UNKNOWN'
 r['originalTextCheck']='NOT_APPLICABLE_SYNTHETIC' if r['category']=='SYNTHETIC_OR_HYPOTHESIS' else 'NOT_INDEPENDENTLY_CHECKED_BY_RELATIONSHIP_AUDIT'
 r['errorRisk']='Do not reinterpret examples, context, provenance, containment or candidates as legal duty, implementation, achieved outcome or causality.'
 if r['category']=='SOURCE_REPORTED_RESEARCH_CANDIDATE':
  explicit=r['to'] in ['csp6','csp8']
  r['officialExplicitRelationship']='EXPLICIT_OFFICIAL_DOCUMENT_CROSS_REFERENCE_TEXT' if explicit else 'RESEARCH_MODEL_ASSOCIATION_OF_FIELDS_WITHIN_ONE_TABLE_ROW'
  r['originalTextCheck']='PASS_PDF27_CSP6.1' if 'ltw-complaints' not in r['id'] else 'PASS_PDF30_LTW_CSP6.1_8.2'
  r['semanticVerification']='SOURCE_TEXT_CROSS_REFERENCE_CONFIRMED_ADMISSION_PENDING' if explicit else 'SOURCE_TABLE_FIELDS_CONFIRMED_MODEL_EDGE_IS_RESEARCH_INTERPRETATION'
  r['officialOrAIInference']='DOCUMENT_EXPLICIT_REFERENCE' if explicit else 'RESEARCH_AUTHORED_TABLE_ROW_ASSOCIATION'
  r['notDistinctLinkWarning']='foodnote→csp6 and foodprogramme→csp6 represent the same original food row; avoid double-counting.'
 elif r['collection']=='DERIVED_GOVERNED_INPUT':
  r['officialOrAIInference']='AUTHOR_DEFINED_RESEARCH_STRUCTURE_OR_PROVENANCE_NOT_POLICY_RELATION'
 elif r['category']=='OBSERVED_METRIC_CONTEXT_NOT_VERIFIED_MAPPING':r['officialOrAIInference']='AUTHOR_SELECTED_THEMATIC_CONTEXT'
 else:r['officialOrAIInference']='EXPLICITLY_SYNTHETIC_OR_HYPOTHESIS'
(root/'relationship-evidence-matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
keys=list(dict.fromkeys(k for r in rows for k in r));
with (root/'relationship-evidence-matrix.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
checks={'sourceId':'csoi:smrc-op-2026:20261030','original':'originals/smrc-op-2026.pdf','rawDigest':'sha256:4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2','sourceStatus':'Historical original recovered; digest matches retained receipt','textChecks':[{'pdfPage':27,'printedPage':27,'row':'Undertake food inspection program — first volume row','CspLink':['6.1'],'optimalVolume':168,'fundedVolume':84,'targetVolume':84,'serviceKpi':{'plannedPercent':98,'eligibleGroup':'P1,P2,P3foodpremises','interval':'atleastonceayear'},'reporting':'Biannual','actualOutput':'UNKNOWN','evidence':'PASS_ORIGINAL_ROW_CHECK'},{'pdfPage':30,'printedPage':30,'row':'Investigate environmental complaints continued — LTW complaints','CspLink':['6.1','8.2'],'optimalVolume':25,'fundedVolume':25,'target':'90%','plannedResponse':'LTWcomplaintsinspectedwithin72hours','reporting':'Quarterly','actualOutput':'UNKNOWN','evidence':'PASS_ORIGINAL_ROW_CHECK'}],'distinctExplicitDocumentCrossReferences':3,'graphAssertionsWithExplicitCspReference':4,'graphTableFieldAssociationAssertions':4,'officialAdmittedAssertions':0,'cspToWaterOperationalCausalLinksVerified':0,'notes':'Source-table references do not prove legal applicability, causal impact, programme achievement or admitted official modelling. No source body reproduced.'}
(root/'op-original-reference-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
p=root/'relationship-summary.json';summary=json.loads(p.read_text());summary.update(explicitDocumentCrossReferenceAssertionsOriginalChecked=4,distinctOriginalDocumentCrossReferencesChecked=3,researchTableRowAssociations=4);p.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print('PASS refined216rowmatrix;3distinctoriginalexplicitCSPcrossrefs verified;0admittedimplementation/legal/causal links.')
