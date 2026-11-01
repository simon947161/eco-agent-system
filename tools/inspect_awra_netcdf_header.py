"""Bounded, read-only native NetCDF4 metadata audit; never read flow/rain/soil arrays."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = 'https://thredds.nci.org.au/thredds/fileServer/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/month/'
BLOCK = 8192
MAX_BLOCKS = 64


def validate_range(status, content_range, start, body, expected_total=None):
    match = re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)', content_range or '')
    if status != 206 or not match:
        raise ValueError('Server did not honor byte range; full download refused')
    first, last, total = map(int, match.groups())
    if first != start or last != min(start + BLOCK, total) - 1 or len(body) != last-first+1:
        raise ValueError('Invalid or oversized range response')
    if expected_total is not None and total != expected_total:
        raise ValueError('Remote file size changed during inspection')
    return total


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Redirect refused')


class HeaderRanges(io.RawIOBase):
    def __init__(self, variable):
        if variable not in ('rain_day', 'sm_pct'):
            raise ValueError('Only approved monthly variables permitted')
        self.url = BASE + variable + '.nc'
        self.pos = 0
        self.cache = {}
        self.total = None
        self.modified = None
        self.opener = urllib.request.build_opener(NoRedirect())
        self.block(0)

    def block(self, offset):
        if offset not in self.cache:
            if len(self.cache) >= MAX_BLOCKS:
                raise ValueError('Metadata byte/request budget exceeded')
            headers = {'Range': f'bytes={offset}-{offset+BLOCK-1}', 'Accept-Encoding':'identity'}
            if self.modified: headers['If-Unmodified-Since'] = self.modified
            with self.opener.open(urllib.request.Request(self.url, headers=headers), timeout=25) as response:
                # Refuse a full response BEFORE reading its body.
                if response.status != 206: raise ValueError('Range unsupported')
                body = response.read(BLOCK+1)
                self.total = validate_range(response.status, response.headers.get('Content-Range'), offset, body, self.total)
                modified = response.headers.get('Last-Modified')
                if self.modified and modified != self.modified: raise ValueError('Remote revision changed')
                self.modified = modified
                self.cache[offset] = body
        return self.cache[offset]

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        position = offset if whence==0 else (self.pos if whence==1 else self.total)+offset
        if position < 0: raise ValueError('Negative seek')
        self.pos = position
        return position
    def readinto(self, buffer):
        data = self.read(len(buffer)); buffer[:len(data)] = data; return len(data)
    def read(self, size=-1):
        if size < 0 or size > BLOCK*MAX_BLOCKS: raise ValueError('Unbounded read refused')
        end = min(self.pos+size, self.total)
        chunks = []
        while self.pos < end:
            offset = self.pos//BLOCK*BLOCK; data = self.block(offset)
            take = min(end-self.pos, len(data)-(self.pos-offset))
            chunks.append(data[self.pos-offset:self.pos-offset+take]); self.pos += take
        return b''.join(chunks)


def plain(value):
    if isinstance(value, bytes): return value.decode('utf-8')
    if hasattr(value, 'tolist'): return plain(value.tolist())
    if isinstance(value, (list,tuple)): return [plain(v) for v in value]
    return value


def inspect(variable, output):
    import h5py
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    remote=HeaderRanges(variable)
    result={'source_url':remote.url,'captured_at_utc':datetime.now(timezone.utc).isoformat(),
            'capture_kind':'native_HDF5_metadata_via_bounded_HTTP_ranges',
            'whole_file_sha256':None,'whole_file_downloaded':False,'hydrological_arrays_read':False}
    with h5py.File(remote,'r') as file:
        result['global_attributes']={k:plain(v) for k,v in file.attrs.items() if k!='_NCProperties'}
        result['variables']={}
        for name in ('time','latitude','longitude','time_bounds',variable):
            data=file[name]
            attrs={k:plain(v) for k,v in data.attrs.items() if k not in ('DIMENSION_LIST','REFERENCE_LIST','CLASS','NAME','_Netcdf4Dimid','_Netcdf4Coordinates')}
            result['variables'][name]={'dtype':str(data.dtype),'shape':list(data.shape),'attributes':attrs}
        # Only coordinate metadata, including a leap month. Never index the physical variable.
        result['coordinate_sample']={'time_indices':[1068,1069,1070],
            'time':file['time'][1068:1071].tolist(),'time_bounds':file['time_bounds'][1068:1071].tolist(),
            'latitude':file['latitude'][:2].tolist(),'longitude':file['longitude'][:2].tolist(),
            'last_time':file['time'][-1:].tolist(),'last_time_bounds':file['time_bounds'][-1:].tolist()}
    result.update(remote_size_bytes=remote.total,last_modified=remote.modified,range_requests=len(remote.cache),bytes_received=sum(map(len,remote.cache.values())))
    result['ranges']=[]
    for offset,body in sorted(remote.cache.items()):
        name=f'{variable}-{offset}.bin'; (output/name).write_bytes(body)
        result['ranges'].append({'file':name,'offset':offset,'length':len(body),'sha256':hashlib.sha256(body).hexdigest()})
    (output/(variable+'-native-header.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--variable',choices=['rain_day','sm_pct'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    r=inspect(args.variable,args.output)
    print(json.dumps({k:r[k] for k in ('source_url','bytes_received','range_requests','remote_size_bytes')}))
