import torch
import pynvml
from typing import Optional
from torch.cuda import is_available, device_count


def gpustat():
    """Returns the status of GPUs.
    """
    if not is_available():
        return None
    cnt = device_count()
    stat = {
        'device_count': cnt,
        'gpus': [],
        'error': ''
    }
    try:
        pynvml.nvmlInit()
    except pynvml.nvml.NVMLError as e:
        stat['error'] = e
        return stat
        
    for i in range(cnt):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        n = str(pynvml.nvmlDeviceGetName(handle), encoding='utf-8')
        m = pynvml.nvmlDeviceGetMemoryInfo(handle)
        u = pynvml.nvmlDeviceGetUtilizationRates(handle)
        stat['gpus'].append({
            'index': i,
            'name': n,
            'utilization.gpu': u.gpu,
            'utilization.mem': u.memory,
            'memory.total': m.total,
            'memory.free': m.free,
            'memory.used': m.used,
        })
    
    pynvml.nvmlShutdown()
    return stat


def auto_selection(prefer:Optional[int]=None, min_memory:int=1024) -> torch.device:
    """Returns the best computing device (CPU or CUDA).

    Parameters
    ----------
    prefer : Optional[int], optional
        Preferred CUDA Device ID. If None, the most idle device is returned.
    min_memory : int, optional
        Minimum free memory value allowed (MB), by default 1024. 
        If the available memory is less than this value, the CPU device is returned.

    Returns
    -------
    torch.device
        [description]
    """
    if not is_available() or device_count() < 1:
        return torch.device('cpu')
    
    if prefer in range(device_count()):
        return torch.device(f'cuda:{prefer}')

    stat = gpustat()
    if not stat['gpus']:
        return torch.device('cuda:0')

    mem_free = [i['memory.free'] for i in stat['gpus']]
    max_free = max(mem_free)
    if max_free < (min_memory * 1024 * 1024):
        return torch.device('cpu')
    return torch.device(f'cuda:{mem_free.index(max_free)}')