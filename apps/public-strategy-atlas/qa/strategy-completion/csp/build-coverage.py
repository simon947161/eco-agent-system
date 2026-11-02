"""Rebuild source/core-item matrix and preserve authored page-review scope; no source bodies emitted."""
from pathlib import Path
import argparse,csv,hashlib,json,datetime
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent;APP=HERE.parents[2]
REVIEW={
1:('Cover and revision identity','EXTRACTED_METADATA','2025 revision and document identity retained; current controlled version not inferred.'),
2:('Acknowledgement, contents and public contact context','REVIEWED_CONTEXT_NOT_STRUCTURED','Contents reviewed against page sequence. Contact details and acknowledgement prose not republished. Contents lists SDGs at15; actual15 is photograph.'),
3:('Welcome and plan purpose','REVIEWED_CONTEXT_NOT_STRUCTURED','Community-wide custodial/partnership purpose reviewed. Source wording says next18years despite2025 revision and2035 horizon; conflict retained, no date repair inferred.'),
4:('Vision and definition of welcoming/environment','REVIEWED_CONTEXT_NOT_STRUCTURED','Vision/context reviewed; no separate graph of definitions or complete prose reproduction.'),
5:('Photographic interlude','VISUALLY_REVIEWED_NOT_APPLICABLE_CORE_ITEM','Photograph, visually checked; no objective/strategy/indicator extraction applicable.'),
6:('Plan overview and five themes','REVIEWED_CONTEXT_WITH_THEME_LINKS','Five-theme census cross-check; pillar records anchored at their detailed sections rather than duplicate overview records.'),
7:('Community ownership and integrated planning/reporting framework','REVIEWED_CONTEXT_NOT_STRUCTURED','Described CSP/DP/OP framework is context, not evidence that each current operational activity implements a given strategy. Statute references not admitted current law.'),
8:('Regional profile and headline demographics','REVIEWED_CONTEXT_NOT_STRUCTURED','Population22132 andSEIFA1020 reviewed as profile context; not used as an unqualified denominator for2021–22 emissions.'),
9:('Population infographic','VISUALLY_REVIEWED_CONTEXT_NOT_STRUCTURED','Demographic percentages and source footer reviewed visually; not among the63progress-measure rows; no independent demographic dataset reconstructed.'),
10:('Engagement questions, methods and participation','REVIEWED_CONTEXT_NOT_STRUCTURED','Participation699 and1February–15March2024 context reviewed; questionnaire and raw responses not extracted.'),
11:('Engagement-channel counts','REVIEWED_CONTEXT_NOT_STRUCTURED','Five channel counts reviewed as publication context. Not summed into distinct participants; duplicates/definitions are not established.'),
12:('Engagement themes','REVIEWED_CONTEXT_NOT_STRUCTURED','Themes about environment, lifestyle, community, infrastructure, finance, housing and roads reviewed; no raw-response inference.'),
13:('Children’s drawings and engagement photograph','REVIEWED_CONTEXT_NOT_STRUCTURED','Artworks, named personal credits and photograph are not republished or converted into policy records.'),
14:('Council role definitions','REVIEWED_CONTEXT_WITH_ROLE_FIELDS','Provide/Collaborate/Advocate definitions reviewed;44strategy rows retain their own role labels and listed partners. Labels are not current staff assignments.'),
15:('Photographic interlude; contents mismatch','VISUALLY_REVIEWED_SOURCE_GAP','Contents names Sustainable Development Goals here, but visiblepage15 is photograph only. No SDG mapping fabricated; locate correct authoritative content if needed.'),
16:('Resilience approach','REVIEWED_CONTEXT_NOT_STRUCTURED','Source names South East NSW Resilience Blueprint; its specific version and implementation evidence are not resolved by this statement.'),
17:('Photographic interlude','VISUALLY_REVIEWED_NOT_APPLICABLE_CORE_ITEM','Photograph visually checked; no core-item extraction applicable.'),
18:('Community outcome; objective1 and strategies1.1–1.2','CORE_ITEMS_AND_ROLE_PARTNER_COLUMNS_EXTRACTED','Outcome/numbereditems/roles/partners structured with anchors; surrounding narrative is reviewed context, not a complete sentence-level graph.'),
19:('Objectives2–3, strategies2.1–3.5 and supporting documents','CORE_ITEMS_AND_SUPPORT_REFERENCES_EXTRACTED','All printed numbered strategies, role/partner columns and three supporting-document names represented; supporting versions/implementation UNKNOWN.'),
20:('Economy outcome and narrative','PILLAR_EXTRACTED_NARRATIVE_REVIEWED','Authored economic outcome summary retained; economic causal statements are not admitted actual outcomes.'),
21:('Objectives4–5, strategies4.1–5.3 and supporting document','CORE_ITEMS_AND_SUPPORT_REFERENCES_EXTRACTED','Numbereditems, roles/partners and named destination plan represented; no current execution assignments inferred.'),
22:('Environment outcome, objective6, strategies6.1–6.3','CORE_ITEMS_AND_ROLE_PARTNER_COLUMNS_EXTRACTED','Monitoring, remediation/biodiversity and shared stewardship preserved as source proposals, not scientific or legal admission.'),
23:('Objective7, strategies7.1–7.4 and supporting documents','CORE_ITEMS_AND_SUPPORT_REFERENCES_EXTRACTED','All four strategies and five supporting-document names represented, including LSPS/OSSM and regional-plan references; no source-listed reference becomes an automatic obligation.'),
24:('Infrastructure outcome, objective8, strategies8.1–8.3','CORE_ITEMS_AND_ROLE_PARTNER_COLUMNS_EXTRACTED','Health, water/wastewater and waste strategy rows represented with source-specific role labels; capacity/growth condition retained.'),
25:('Objectives9–11, strategies9.1–11.4 and supporting documents','CORE_ITEMS_AND_SUPPORT_REFERENCES_EXTRACTED','Transport/digital/public infrastructure strategies and six support names represented; source regional-plan spelling differs frompage23 and is retained.'),
26:('Civic leadership outcome, objective12, strategies12.1–12.3','CORE_ITEMS_AND_ROLE_PARTNER_COLUMNS_EXTRACTED','Leadership access, service standards and governance represented; organisational role labels do not authorise this software.'),
27:('Objectives13–14, strategies13.1–14.1 and supporting documents','CORE_ITEMS_AND_SUPPORT_REFERENCES_EXTRACTED','Engagement, communication and strategy currency represented with three support names.'),
28:('Progress, review, reporting and meaning of measures','REVIEWED_CRITICAL_MEASUREMENT_BOUNDARY','Source explicitly distinguishes community progress measures from Council performance. This governs all63baseline records; four-year review is document context, not a new automated duty.'),
29:('Community progress measures','ALL_24_PRINTED_ROWS_STRUCTURED','24rows; all4columns independently checked. Underlying methods, source microdata, denominators and current values remain unverified.'),
30:('Economy and environment progress measures','ALL_19_PRINTED_ROWS_STRUCTURED','11economy+8environment rows.29.9 is per-person regional emissions with2021–22 source label; no Council actual or independent recalculation.'),
31:('Infrastructure and civic progress measures','ALL_20_PRINTED_ROWS_STRUCTURED','12infrastructure+8civic rows.7519CO2eq has no complete mass unit. Public-transport2.1/3.1 conflict retained. Ratios lacking printedpercent unit remain UNKNOWN.'),
32:('Consolidated partner directory','REVIEWED_CONTEXT_NOT_STRUCTURED','Directory reviewed; actual strategy-cell partner names retained separately. Directory entries are not automatically assigned to all strategies; no current agency-name remapping.'),
33:('Abbreviations','REVIEWED_CONTEXT_NOT_STRUCTURED','Abbreviation glossary reviewed as source context; no new statutory definitions or current agency registry generated.'),
34:('Acknowledgements','REVIEWED_CONTEXT_NOT_STRUCTURED','Authorship/collaboration acknowledgement reviewed; no new implementation relationship inferred.'),
35:('Version history and controlled-document notice','EXTRACTED_VERSION_METADATA','v3.0,1May2025,resolution73/25 observed. Source directs controlled copies to intranet; no intranet accessed and current-version status stays UNKNOWN.'),
36:('Further information and contacts','REVIEWED_CONTEXT_NOT_STRUCTURED','Public document/contact directions reviewed; no contact details copied into operational records or outbound messages.')}
def main():
 p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);a=p.parse_args();b=json.loads((APP/'sources/csp-public-knowledge.json').read_text());r=PdfReader(a.pdf);assert len(r.pages)==len(REVIEW)==36
 rows=[]
 for n in b['records']:
  cat=n['category'];row={'recordId':n['id'],'category':cat,'code':n['code'],'sourceId':b['sourceId'],'sourceRevision':b['sourceRevision'],'sourceVersion':'CSP2035 2025revision; v3.0/1May2025/73-25 observed PDF35; current version UNKNOWN','pdfPage':n['anchor']['pdfPage'],'printedPage':n['anchor']['pdfPage'],'normalizedPageDigest':n['anchor']['normalizedPageDigest'],'bbox':n['anchor']['bbox'],'extraction':'BOUNDED_STRUCTURED_FACTS_AND_AUTHORED_PARAPHRASE','implementation':'PENDING_PARENT_INTEGRATION','verification':'PASS_ORIGINAL_COLUMNS_AND_CENSUS'if cat in ['CSP_INDICATOR','CSP_STRATEGY']else'PASS_ORIGINAL_IDENTITY_HIERARCHY_AND_PAGE_REVIEW','semanticReview':'AI_ASSISTED_BOUNDED_PARAPHRASE_REVIEW_NOT_FORMAL_ADMISSION','evidence':'qa/strategy-completion/csp/original-verification.json','gap':'Current source version, authorised admission and actual outcome remain UNKNOWN/PENDING; full-document semantics not claimed.'}
  if cat=='CSP_INDICATOR':row['gap']+=' Raw calculation inputs/denominators/methods not ingested; NOT_COMPUTABLE.'
  if cat=='CSP_STRATEGY':row['gap']+=' Source roles/partners are historical labels; actual individual assignment, budget and execution dates not established.'
  rows.append(row)
 (HERE/'item-coverage.json').write_text(json.dumps({'sourceId':b['sourceId'],'sourceRevision':b['sourceRevision'],'rows':rows},ensure_ascii=False,indent=2)+'\n')
 with (HERE/'item-coverage.csv').open('w',encoding='utf-8-sig',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([{**x,'bbox':json.dumps(x['bbox'])}for x in rows])
 pages=[]
 for page,(section,status,gap)in REVIEW.items():
  text=' '.join((r.pages[page-1].extract_text(extraction_mode='layout')or'').split());items=[x['recordId']for x in rows if x['pdfPage']==page];pages.append({'pdfPage':page,'section':section,'reviewStatus':status,'normalizedPageDigest':'sha256:'+hashlib.sha256(text.encode()).hexdigest(),'primaryRecordIds':items,'primaryRecordCount':len(items),'scopeAndRemainingGap':gap,'legalApplicability':'UNKNOWN','wholePageSemanticExtraction':'NOT_CLAIMED'})
 (HERE/'page-coverage.json').write_text(json.dumps({'sourceId':b['sourceId'],'sourceRevision':b['sourceRevision'],'pageCount':36,'coreItemCount':127,'definition':'Every page reviewed for document structure/context; core numbered objectives/strategies and measure tables are bounded structured extraction. This is not every-sentence semantic ingestion or legal review.','pages':pages},ensure_ascii=False,indent=2)+'\n')
 with (HERE/'page-coverage.csv').open('w',encoding='utf-8-sig',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(pages[0]));w.writeheader();w.writerows([{**x,'primaryRecordIds':' | '.join(x['primaryRecordIds'])}for x in pages])
 print('CSP coverage:127 coreitem rows and36 page-scope rows; implementation pending integration')
if __name__=='__main__':main()
