import random
import torch
import numpy as np

def manual_seed(seed:int):
    """Sets the seed for the random number generator (PyTorch, Numpy and Python).
    """
    if not seed:
        return
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)