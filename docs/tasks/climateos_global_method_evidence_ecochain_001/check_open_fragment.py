"""Parse original XLSX with stdlib; only 23 dissolved-mass unit conversions.

No flow integration, ideal-gas conversion, regression or emission estimation.
"""
from pathlib import Path
import csv, hashlib, io, json, zipfile
from decimal import Decimal
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta

T=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
MEMBER='Data for Network SL1/Measured_Methane_Data_SL1.xlsx'
EXPECTED='d559b1c81e31090c7563accea4091b215c4a0d533d0a23d79b251dd83b9cb589'

def read_rows(raw):
    assert hashlib.sha256(raw).hexdigest()==EXPECTED,'RAW_SHA'
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        workbook=archive.read(MEMBER)
    with zipfile.ZipFile(io.BytesIO(workbook)) as book:
        strings=[''.join(x.itertext()) for x in ET.fromstring(book.read('xl/sharedStrings.xml'))]
        root=ET.fromstring(book.read('xl/worksheets/sheet1.xml'))
        rows=[]
        for row in root.findall('.//s:sheetData/s:row',NS):
            vals={}
            for cell in row.findall('s:c',NS):
                value=cell.find('s:v',NS)
                if value is not None:
                    vals[cell.attrib['r'].rstrip('0123456789')]=strings[int(value.text)] if cell.attrib.get('t')=='s' else value.text
            if vals: rows.append((int(row.attrib['r']),vals))
    assert rows[0][1]=={'A':'Date and Time','B':'CH4 Concentration (mg/L)'},'HEADER'
    return workbook,rows[1:]

def main():
    receipt=json.loads((T/'evidence/open-case-acquisition.json').read_text(encoding='utf-8'))
    if receipt['status']!='RAW_BYTES_VERIFIED': raise SystemExit('OPEN_CASE_DATA_NOT_READY')
    raw=(T/'evidence/raw/SL1.zip').read_bytes(); workbook,rows=read_rows(raw)
    prior=list(csv.DictReader((T.parent/'climateos_local_case_method_intake_001/evidence/measured-transcription.csv').open(encoding='utf-8')))
    assert len(rows)==len(prior)==23,'ROW_COUNT'
    output=[]
    for (row,v),old in zip(rows,prior):
        # Excel naive serial; not silently assigned to UTC or Australia.
        stamp=(datetime(1899,12,30)+timedelta(days=float(v['A']))).replace(microsecond=0).isoformat()
        x=Decimal(v['B']); y=x*Decimal('0.001')
        assert x.is_finite() and x>=0
        assert row==int(old['source_row_1_based']) and stamp==old['time_as_stored_no_timezone']
        assert abs(x-Decimal(old['dissolved_ch4_mg_per_l']))<Decimal('1e-12'),'PR139_CROSSCHECK'
        assert y/Decimal('0.001')==x,'REVERSE_CONVERSION'
        output.append({'row':row,'time_naive':stamp,'original_mg_L':str(x),'derived_kg_m3':str(y)})
    result={'status':'OPEN_FRAGMENT_RECALCULATED_WITH_LIMITS','source':'Li, Jiuling (2025), Sewer CH4, v1, doi:10.5281/zenodo.17718964',
      'licence':'CC-BY-4.0','raw_sha256':EXPECTED,'xlsx_member':MEMBER,'xlsx_sha256':hashlib.sha256(workbook).hexdigest(),
      'formula':'kg/m3 = mg/L * (1e-6 kg/mg)/(1e-3 m3/L) = mg/L * 0.001',
      'phase':'dissolved_CH4','row_count':23,'missing_selected_cells':0,'crosscheck_PR139':'23/23 within 1e-12 mg/L',
      'quality_flags':'NOT_PROVIDED_IN_SELECTED_SHEET','timezone':'UNKNOWN','calibration':'UNKNOWN',
      'spatial_support':'published SL1 sewer network; coordinates and representativeness UNKNOWN',
      'measurement_method':'workbook observations; instrument and uncertainty not established by this fragment',
      'uncertainty':'unit conversion exact, measured concentration uncertainty UNKNOWN',
      'full_landfill_case':'OPEN_CASE_DATA_NOT_READY','effect':'NOT_ASSESSED',
      'rows':output}
    (T/'evidence/open-fragment-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(result['status'],len(output),'rows')

if __name__=='__main__': main()
