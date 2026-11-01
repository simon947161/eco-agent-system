"""One-cell July 2000 AWRA empirical check; never admits a cross-source join.

Offline by default. --fetch explicitly captures a small, fixed public NCI batch.
Only standard-library dependencies; DAP2 binary arrays preserve Float32 values.
"""
import argparse
import hashlib
import json
import math
import re
import struct
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/tasks/climateos_regional_public_os_001/evidence/p04_awra_20261031'
HOST = 'https://thredds.nci.org.au/thredds/'
COLLECTION = 'iu04/australian-water-outlook/'
MODEL = COLLECTION + 'historical/v1/AWRALv7/'
PRODUCTS = {
    'day-sm_pct': MODEL + 'processed/values/day/sm_pct_2000.nc',
    'month-sm_pct': MODEL + 'processed/values/month/sm_pct.nc',
    'day-rain_day': MODEL + 'rain_day_2000.nc',  # README convention; absent from catalogue at capture
    'month-rain_day': MODEL + 'processed/values/month/rain_day.nc',
}
START = (date(2000, 7, 1) - date(1900, 1, 1)).days
END = (date(2000, 8, 1) - date(1900, 1, 1)).days
CELL = {'latitude_index': 525, 'longitude_index': 742, 'latitude': -36.25, 'longitude': 149.1}
MAX_BYTES = 2 * 1024 * 1024
MAX_REQUESTS = 32
SAFE_HEADERS = ('date', 'last-modified', 'etag', 'content-length', 'content-type', 'content-description')


def query(key):
    period, var = key.split('-', 1)
    times = '[182:1:212]' if period == 'day' else '[1074:1:1074]'
    value = f'{var}{times}[525:1:525][742:1:742]'
    if period == 'month':
        value += ',time_bounds[1074:1:1074][0:1:1]'
    return urllib.parse.quote(value, safe=':,')


def plan():
    result = {
        'awral-catalog.xml': (HOST + 'catalog/' + MODEL + 'catalog.xml', 'GET', 262144),
        'day-catalog.xml': (HOST + 'catalog/' + MODEL + 'processed/values/day/catalog.xml', 'GET', 262144),
        'month-catalog.xml': (HOST + 'catalog/' + MODEL + 'processed/values/month/catalog.xml', 'GET', 65536),
        'license.txt': (HOST + 'fileServer/' + COLLECTION + 'license.txt', 'GET', 4096),
        'official-readme.md': (HOST + 'fileServer/' + COLLECTION + 'historical/v1/README.md', 'GET', 16384),
    }
    for key, path in PRODUCTS.items():
        dap = HOST + 'dodsC/' + path
        for ext in ('dds', 'das'):
            result[key + '.' + ext] = (dap + '.' + ext, 'GET', 16384)
        result[key + '.dods'] = (dap + '.dods?' + query(key), 'GET', 16384)
        for when in ('before', 'after'):
            result[key + '-' + when + '.head'] = (HOST + 'fileServer/' + path, 'HEAD', 0)
    return result


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Redirect refused')


class Capture:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        self.receipts = []
        self.bytes = 0
        self.opener = urllib.request.build_opener(NoRedirect())

    def get(self, name):
        url, method, limit = plan()[name]  # no arbitrary caller URL or physical whole-file GET
        if len(self.receipts) >= MAX_REQUESTS or self.bytes + limit + 1 > MAX_BYTES:
            raise ValueError('Batch request/byte budget exhausted')
        record = {'file': name, 'url': url, 'method': method,
                  'started_at_utc': datetime.now(timezone.utc).isoformat()}
        body = b''
        try:
            request = urllib.request.Request(url, method=method, headers={'Accept-Encoding': 'identity'})
            try:
                response = self.opener.open(request, timeout=25)
            except urllib.error.HTTPError as error:
                response = error  # retain exact bounded 404 body, status and receipt
            with response:
                record['http_status'] = response.status
                record['headers'] = {k: response.headers[k] for k in SAFE_HEADERS if k in response.headers}
                if method == 'GET':
                    length = response.headers.get('Content-Length')
                    if length and int(length) > limit:
                        raise ValueError('Response Content-Length exceeds cap')
                    body = response.read(limit + 1)
                    if len(body) > limit:
                        raise ValueError('Response body exceeds cap')
            record['complete'] = True
        except (OSError, ValueError) as error:
            record.update(complete=False, error=type(error).__name__ + ': ' + str(error))
        self.bytes += len(body)
        record.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                      completed_at_utc=datetime.now(timezone.utc).isoformat())
        (self.directory / name).write_bytes(body)
        self.receipts.append(record)
        return record.get('complete') and record.get('http_status') == 200

    def finish(self):
        manifest = {
            'schema': 'climateos.p04.awra_single_cell_capture.v1',
            'baseline_commit': '67bc471ebeaab02cd09b0ee9dd8edd917483f3fc',
            'month': '2000-07', 'cell': CELL, 'files': self.receipts,
            'attribution': 'Bureau of Meteorology, Australian Landscape Water Balance AWRA-L; NCI distribution; ClimateOS extraction and calculations.',
            'licence': 'CC BY 4.0; see captured license.txt',
            'budget': {'max_requests': MAX_REQUESTS, 'max_body_bytes': MAX_BYTES,
                       'actual_requests': len(self.receipts), 'actual_body_bytes': self.bytes,
                       'external_spending_aud': 0, 'credentials_used': False},
            'representation': 'Exact bounded HTTP response bodies; .dods is a DAP2 subset, not a whole NetCDF file. HEAD files are empty bodies; source headers are in receipts.',
            'revision_limit': 'Last-Modified/size compared before and after each subset. No immutable publisher revision or whole-file hash; HTTP Date is retrieval, not observation time.',
        }
        (self.directory / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


def fetch(directory):
    capture = Capture(directory)
    try:
        for name in ('awral-catalog.xml', 'day-catalog.xml', 'month-catalog.xml', 'license.txt', 'official-readme.md'):
            capture.get(name)
        for key in PRODUCTS:
            # Missing daily rain is a recorded negative result, never a fabricated daily series.
            if not capture.get(key + '.dds'):
                continue
            if not capture.get(key + '-before.head'):
                continue
            capture.get(key + '.das')
            capture.get(key + '.dods')
            capture.get(key + '-after.head')
    finally:
        capture.finish()


def load(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text())
    data, receipts = {}, {}
    for record in manifest['files']:
        name = record['file']
        if name not in plan() or name in receipts:
            raise ValueError('Unexpected or duplicate evidence file')
        if (record['url'], record['method']) != plan()[name][:2]:
            raise ValueError('Source identity mismatch')
        body = (directory / name).read_bytes()
        if len(body) != record['bytes'] or hashlib.sha256(body).hexdigest() != record['sha256']:
            raise ValueError('Evidence checksum/size mismatch: ' + name)
        if len(body) > plan()[name][2] + 1:
            raise ValueError('Evidence exceeds response budget')
        data[name], receipts[name] = body, record
    if len(receipts) > MAX_REQUESTS or sum(map(len, data.values())) > MAX_BYTES:
        raise ValueError('Evidence exceeds batch budget')
    return manifest, data, receipts


def attributes(body, variable):
    text = body.decode('ascii')
    match = re.search(r'\b' + re.escape(variable) + r'\s*\{([^{}]*)\}', text)
    if not match:
        raise ValueError('Missing variable attributes: ' + variable)
    result = {}
    for type_, key, value in re.findall(r'\b(String|Float32|Float64|Int32|UInt32|Int16|UInt16|Byte)\s+(\w+)\s+([^;]+);', match[1]):
        if key in result:
            raise ValueError('Duplicate metadata attribute')
        if type_ == 'String':
            result[key] = value.strip('"')
        else:
            numbers = [float(v.strip()) for v in value.split(',')]
            result[key] = numbers[0] if len(numbers) == 1 else numbers
    return result


def decode(body, key):
    """Strict DAP2 decoder for this one grid + optional monthly bounds only."""
    header, payload = body.split(b'\nData:\n', 1)
    header = header.decode('ascii')
    if not header.rstrip().endswith('} ' + PRODUCTS[key] + ';'):
        raise ValueError('Wrong DAP dataset identity')
    declarations = re.findall(r'(Float32|Float64|Int32)\s+(\w+)((?:\[\w+\s*=\s*\d+\])+);', header)
    period, var = key.split('-', 1)
    n = 31 if period == 'day' else 1
    expected = [('Float32', var, [n, 1, 1]), ('Int32', 'time', [n]),
                ('Float64', 'latitude', [1]), ('Float64', 'longitude', [1])]
    if period == 'month':
        expected.insert(0, ('Int32', 'time_bounds', [1, 2]))
    actual = [(t, name, list(map(int, re.findall(r'=\s*(\d+)', dims)))) for t, name, dims in declarations]
    if actual != expected:
        raise ValueError('Unreviewed DAP types, shapes or variable order')
    result, pos = {}, 0
    for type_, name, dims in actual:
        count = math.prod(dims)
        if struct.unpack_from('>II', payload, pos) != (count, count):
            raise ValueError('DAP element counts do not match descriptor')
        pos += 8
        fmt = '>' + str(count) + {'Float32': 'f', 'Float64': 'd', 'Int32': 'i'}[type_]
        result[name] = list(struct.unpack_from(fmt, payload, pos))
        pos += struct.calcsize(fmt)
    if pos != len(payload):
        raise ValueError('Unexpected trailing DAP bytes')
    return result


def validate_sample(sample, metadata, key):
    period, var = key.split('-', 1)
    time = attributes(metadata, 'time')
    attrs = attributes(metadata, var)
    units = {'rain_day': 'mm', 'sm_pct': 'fraction of fullness'}[var]
    if time.get('units') != 'days since 1900-01-01' or time.get('calendar') != 'gregorian':
        raise ValueError('Unreviewed time unit/calendar')
    if attrs.get('units') != units or attrs.get('_FillValue') != -999:
        raise ValueError('Unreviewed unit/fill contract')
    if any(x in attrs for x in ('scale_factor', 'add_offset', 'missing_value', 'valid_range')):
        raise ValueError('New packing/mask contract requires review')
    if attributes(metadata, 'latitude').get('units') != 'degrees_north' or attributes(metadata, 'longitude').get('units') != 'degrees_east':
        raise ValueError('Unreviewed coordinate units')
    if sample['latitude'] != [CELL['latitude']] or sample['longitude'] != [CELL['longitude']]:
        raise ValueError('Wrong grid cell')
    expected_time = list(range(START, END)) if period == 'day' else [END - 1]
    if sample['time'] != expected_time:
        raise ValueError('Incomplete, duplicate or shifted calendar labels')
    if period == 'month' and (sample.get('time_bounds') != [START, END] or time.get('bounds') != 'time_bounds'):
        raise ValueError('Wrong monthly bounds')
    values = sample[var]
    if len(values) != len(expected_time):
        raise ValueError('Incomplete physical sample')
    masked = sum(not math.isfinite(v) or v == attrs['_FillValue'] for v in values)
    if masked:
        raise ValueError(f'Masked/nonfinite samples: {masked}; no dropping, zero filling or interpolation')
    if any(v < 0 or (var == 'sm_pct' and v > 1) for v in values):
        raise ValueError('Out-of-domain value; no automatic scale conversion')
    return {'units': units, 'fill_value': -999, 'valid_samples': len(values),
            'masked_samples': 0, 'global_attributes': attributes(metadata, 'NC_GLOBAL')}


def comparison(observed, reference, absolute):
    # Predeclared allowance for Float32 storage/reduction rounding, not scientific uncertainty.
    tolerance = max(absolute, abs(reference) * 2e-6)
    return {'observed': observed, 'reference': reference, 'difference': observed - reference,
            'absolute_tolerance': tolerance, 'agrees': abs(observed - reference) <= tolerance}


def analyse(data, receipts):
    samples, metadata, failures = {}, {}, {}
    for key in PRODUCTS:
        names = [key + x for x in ('.dds', '.das', '.dods', '-before.head', '-after.head')]
        if not all(n in receipts and receipts[n].get('complete') and receipts[n].get('http_status') == 200 for n in names):
            failed = [n for n in names if n not in receipts or not receipts[n].get('complete') or receipts[n].get('http_status') != 200]
            failures[key] = 'Missing or unsuccessful official product capture: ' + ', '.join(
                n + ' (HTTP ' + str(receipts.get(n, {}).get('http_status', 'not captured')) + ')' for n in failed)
            continue
        try:
            before, after = [receipts[key + '-' + x + '.head']['headers'] for x in ('before', 'after')]
            if not before.get('last-modified') or not before.get('content-length'):
                raise ValueError('Missing source revision/size headers')
            if any(before.get(x) != after.get(x) for x in ('last-modified', 'content-length', 'etag')):
                raise ValueError('Source revision changed during capture')
            sample = decode(data[key + '.dods'], key)
            metadata[key] = validate_sample(sample, data[key + '.das'], key)
            samples[key] = sample
        except (ValueError, KeyError, struct.error) as error:
            failures[key] = str(error)
    result = {'schema': 'climateos.p04.awra_empirical_reproduction.v1',
              'status': 'PARTIAL', 'month': '2000-07', 'cell': CELL,
              'source_products': PRODUCTS, 'unverified_candidate_products': ['day-rain_day'],
              'metadata': metadata, 'failures': failures,
              'cross_source_numeric_join': 'BLOCKED', 'scientific_admission': False,
              'provider_general_semantics_proven': False,
              'time_basis': 'Product calendar labels only; no UTC, local-time or HRS interval alignment inferred.',
              'samples': samples, 'comparisons': {}}
    for var in ('rain_day', 'sm_pct'):
        day, month = 'day-' + var, 'month-' + var
        if day not in samples or month not in samples:
            result['comparisons'][var] = {'status': 'BLOCKED_MISSING_MATCHED_DAILY_MONTHLY_SAMPLE'}
            continue
        daily, monthly = samples[day][var], samples[month][var][0]
        if var == 'rain_day':
            match = comparison(monthly, math.fsum(daily), 1e-5)
            result['comparisons'][var] = {'status': 'EMPIRICAL_AGREEMENT' if match['agrees'] else 'EMPIRICAL_DISAGREEMENT', 'daily_sum': match}
        else:
            mean = comparison(monthly, math.fsum(daily) / len(daily), 1e-7)
            last = comparison(monthly, daily[-1], 1e-7)
            result['comparisons'][var] = {'status': 'PASS_EMPIRICAL_COMPARISON', 'daily_mean': mean, 'final_day': last,
                                          'minimum_daily': min(daily), 'maximum_daily': max(daily)}
    if not failures:
        result['status'] = 'PASS_BOUNDED_REPRODUCTION_ONLY'
    return result


def reproduce(directory=EVIDENCE):
    _, data, receipts = load(directory)
    return analyse(data, receipts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='explicit zero-cost fixed public-data acquisition')
    parser.add_argument('--directory', type=Path, default=EVIDENCE)
    parser.add_argument('--result', type=Path)
    args = parser.parse_args()
    if args.fetch:
        fetch(args.directory)
    result = reproduce(args.directory)
    output = json.dumps(result, indent=2, allow_nan=False) + '\n'
    if args.result:
        args.result.write_text(output)
    print(json.dumps({'status': result['status'], 'comparisons': result['comparisons'], 'failures': result['failures']}, indent=2))
