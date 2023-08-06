from .multiprocess_no_cuda import multiprocess_no_cuda
from .multiprocess_enable_cuda import multiprocess_enable_cuda
from .base_multiprocess import _func_to_src_dict


def multiprocess(n_workers=4, **multi_kwargs):
    use_cuda = multi_kwargs.get('cuda', False)
    if not use_cuda:
        return multiprocess_no_cuda(n_workers, **multi_kwargs)
    return multiprocess_enable_cuda(n_workers, **multi_kwargs)
