#!/usr/bin/env python3
from pynvml import *

try:
    nvmlInit()
    NVML = True
except:
    NVML = False

def enabled():
    return NVML

#get mem stats
def mem(dev=0):
    h = nvmlDeviceGetHandleByIndex(dev)
    info = nvmlDeviceGetMemoryInfo(h)
    return info.used, info.free, info.total

#get # of gpu's
def gpu_count():
    return nvmlDeviceGetCount()

#opine on least-used aka best to use
def least_used():
    devs = nvmlDeviceGetCount()
    best = None
    freest = -1
    for dev in range(devs):
        used, free, tot = mem(dev)
        if free > freest:
            freest = free
            best = dev
    return best, freest

if __name__ == "__main__":
    if not NVML:
        print ("NVML driver not available (no gpu?)")
    else:
        best, free = least_used()
        print (f"dev {best} has most free memory: {free/1000000:.3f}mb")
        devs = nvmlDeviceGetCount()
        print (f"{devs} GPU devices found")
        for dev in range(devs):
            used, free, tot = mem(dev)
            print (f"device: {dev} used: {used/tot:.3%} {used/1000000:.3f}mb out of {tot/1000000:.3f}mb free: {free/1000000:.3f}mb")
