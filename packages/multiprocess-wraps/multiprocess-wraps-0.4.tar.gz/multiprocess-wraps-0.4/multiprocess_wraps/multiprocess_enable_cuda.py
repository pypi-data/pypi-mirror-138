"""Class for multiprocessing WITH CUDA."""

import functools
import torch
import torch.multiprocessing as mp

from .base_multiprocess import _BaseMultiprocess

# TODO: how to set gpu_ids?
class multiprocess_enable_cuda(_BaseMultiprocess):
    def __init__(self, n_workers=4, **multi_kwargs):
        super().__init__(n_workers, **multi_kwargs)

        if not torch.cuda.is_available():
            raise AssertionError(f'Try to use CUDA while no available CUDA'
                                f'devices.')

    def __call__(self, func):
        """The main function to decorate the input function."""
        torch.multiprocessing.set_start_method('spawn', force=True)
        func = super().__call__(func)
        @functools.wraps(func)
        def multiprocess_func(*args, **kwargs):
            # Check the paramters.
            length, legal = self._check_args(*args, **kwargs)
            if not legal:
                raise AssertionError(f'All input parameters should be of the '
                                     f'the same length.')

            # Print infos if needed.
            if self.verbose:
                infos = ''
                infos += '====================Check Arg====================\n'
                infos += f'args: {args}  kwargs: {kwargs}\n'
                infos += f'length: {length}\n'
                infos += '====================Check Arg====================\n'
                print(infos)

            # The main iteration.
            results = []
            with mp.Pool(self.n_workers) as pool:
                for i in range(length):
                    arg = [x[i] for x in args]
                    kwarg = {k: v[i] for k, v in kwargs.items()}
                    func_src = self._func_to_src(func)
                    func_name = func.__name__
                    result = pool.apply_async(
                        self._exec,
                        args=(func_src, func_name, arg, kwarg))
                    results.append(result.get())
            return results
        return multiprocess_func

