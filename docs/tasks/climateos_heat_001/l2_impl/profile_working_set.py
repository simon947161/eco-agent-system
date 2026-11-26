#!/usr/bin/env python3
"""Read-only Windows working-set sampler for one no-write L2 workload probe."""
import ctypes, json, subprocess, sys, time
from ctypes import wintypes

class PMC(ctypes.Structure):
    _fields_=[("cb",wintypes.DWORD),("PageFaultCount",wintypes.DWORD),("PeakWorkingSetSize",ctypes.c_size_t),
              ("WorkingSetSize",ctypes.c_size_t),("QuotaPeakPagedPoolUsage",ctypes.c_size_t),("QuotaPagedPoolUsage",ctypes.c_size_t),
              ("QuotaPeakNonPagedPoolUsage",ctypes.c_size_t),("QuotaNonPagedPoolUsage",ctypes.c_size_t),
              ("PagefileUsage",ctypes.c_size_t),("PeakPagefileUsage",ctypes.c_size_t)]

p=subprocess.Popen([sys.executable,"-B","run_l2.py","L","60","25","--no-write"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
k32=ctypes.WinDLL("kernel32",use_last_error=True); psapi=ctypes.WinDLL("psapi",use_last_error=True)
h=k32.OpenProcess(0x0400|0x0010,False,p.pid)
peak=0; samples=0; started=time.perf_counter()
if not h: raise OSError(ctypes.get_last_error(),"OpenProcess denied")
try:
    while p.poll() is None:
        m=PMC(); m.cb=ctypes.sizeof(m)
        if not psapi.GetProcessMemoryInfo(h,ctypes.byref(m),m.cb): raise OSError(ctypes.get_last_error(),"GetProcessMemoryInfo failed")
        peak=max(peak,int(m.PeakWorkingSetSize),int(m.WorkingSetSize)); samples+=1
        time.sleep(.05)
    out,err=p.communicate()
finally: k32.CloseHandle(h)
print(json.dumps({"tag":"SYNTHETIC","probe":"no-write L 8760-hour case; OS working-set sampling","exit_code":p.returncode,"wall_runtime_s":time.perf_counter()-started,"peak_working_set_bytes":peak,"samples":samples,"stdout":out.strip(),"stderr":err.strip()},sort_keys=True))
