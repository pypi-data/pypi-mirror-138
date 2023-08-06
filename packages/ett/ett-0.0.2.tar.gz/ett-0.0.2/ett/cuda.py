import torch
from torch.cuda import is_available, device_count
import pynvml


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
        pynvml.nvmlInit() # 初始化
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
    
    pynvml.nvmlShutdown() # 关闭管理工具
    return stat


def try_gpu(i) -> torch.device:
    """ Return gpu(id) if exists, otherwise return cpu().
    """
    if is_available() and device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')


def get_idle(ths:int=1e9) -> torch.device:
    """
    Returns the most idle device.

    Params:
    ---
    ths: Minimum CUDA memory free value allowed (B).
    """
    if not is_available():
        return torch.device('cpu')
    stat = gpustat()
    if not stat['gpus']:
        return torch.device(f'cuda:{stat["device_count"]-1}')
    mem_free = [i['memory.free'] for i in stat['gpus']]
    max_free = max(mem_free)
    if max_free < ths:
        return torch.device('cpu')
    return torch.device(f'cuda:{mem_free.index(max_free)}')
