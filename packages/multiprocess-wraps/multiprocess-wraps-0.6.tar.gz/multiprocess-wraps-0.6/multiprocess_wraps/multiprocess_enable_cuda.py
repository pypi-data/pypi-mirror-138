"""Class for multiprocessing WITH CUDA."""

import multiprocessing as mp

from .base_multiprocess import _BaseMultiprocess


class multiprocess_enable_cuda(_BaseMultiprocess):
    def __init__(self, n_workers=4, **multi_kwargs):
        super().__init__(n_workers, **multi_kwargs)
        '''
        if not torch.cuda.is_available():
            raise AssertionError(f'Try to use CUDA while no available CUDA'
                                f'devices.')
        '''

    def __call__(self, func):
        """The main function to decorate the input function."""
        mp.set_start_method('spawn', force=True)
        multiprocess_func = super().__call__(func)
        return multiprocess_func
