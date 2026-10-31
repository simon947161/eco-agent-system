from pathlib import Path
from pypdf import PdfReader
import pypdf,hashlib,json,datetime
base=Path('/tmp/csoi-integrity-audit-20261031');original=base/'originals/smrc-csp-full-2025.pdf';body=original.read_bytes();expected='sha256:dc4fe1fca1d860b3389ea1e5ddca3826efaf5d02a7d029242a45ec20666cf743';actual='sha256:'+hashlib.sha256(body).hexdigest();assert actual==expected and len(body)==24842203
reader=PdfReader(original);assert len(reader.pages)==36
page=lambda n:' '.join((reader.pages[n-1].extract_text(extraction_mode='layout') or '').split())
checks=[(30,'regional-emissions-row',['CO2e emissions per capita','Snapshot Climate','Profiles 2021-22','29.9 tonnes','Decrease']),(31,'omitted-water-sewer-emissions-row',['Greenhouse Gas Emissions - Total water and sewer','NSW Water 2022-23','7,519','CO2eq']),(22,'goal-6.1-is-monitoring-not-carbon-formula',['6.1 Monitor environmental assets','our air, land, and waterways']),(8,'unqualified-headline-population',['Total population','22,132'])]
results=[]
for number,key,tokens in checks:
 text=page(number)
 assert all(token.casefold() in text.casefold() for token in tokens),(number,key)
 results.append({'id':key,'pdfPage':number,'printedPage':number,'parserVersion':'pypdf-'+pypdf.__version__+'-layout-whitespace-1','normalizedPageDigest':'sha256:'+hashlib.sha256(text.encode()).hexdigest(),'factTokens':tokens,'status':'PASS_ORIGINAL_ROW_OBSERVED_NOT_RECOMPUTED'})
result={'auditedCommit':'744ab46b2bec2ad601da0c4ae528694a4c982154','sourceId':'csoi:smrc-csp-full-2025:20261030','originalPdf':str(original),'byteLength':len(body),'rawDigest':actual,'historicalReceiptMatch':True,'pages':len(reader.pages),'checks':results,'rawOriginalRedistributed':False,'independentRegionalPerCapitaRecalculation':'NOT COMPUTABLE','missingInputs':['Raw source inventory emissions total for2021-22','Exact source population denominator/year','Inventory sectors/scopes/accounting method and version','Unrounded numerator/rate precision'],'waterOperationsAttribution':'NOT COMPUTABLE','waterBaselineCandidate':{'sourcePage':31,'printedLabel':'Greenhouse Gas Emissions - Total water and sewer','sourceLabel':'NSW Water 2022-23','printedBaseline':'7,519 CO2eq','fullUnit':'UNKNOWN_FROM_THIS_ROW','underlyingOperationalInputs':'NOT_INGESTED','actualLinkTo29.9':'NOT_ESTABLISHED'},'admission':'NOT_GRANTED_BY_AUDIT'}
(base/'carbon/carbon-original-evidence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'status':'PASS','rawDigest':actual,'pages':36,'rowsVerified':len(results),'recalculation':'NOT COMPUTABLE','waterRelationship':'NOT ESTABLISHED'}))
