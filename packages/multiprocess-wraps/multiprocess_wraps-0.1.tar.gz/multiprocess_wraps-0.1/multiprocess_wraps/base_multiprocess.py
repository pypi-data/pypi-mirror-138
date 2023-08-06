"""A package of decorators to use multiprocessing easily."""

import json
import inspect
import functools
import multiprocessing as mp


_func_to_src_dict = dict()    # {module: src, ...}


class _BaseMultiprocess():
    def __init__(self, n_workers=4, **multi_kwargs):
        """Initialization function of base class of multiprocessing.
        
        Args:
            n_workers:     How many workers for multiprocessing. (default: 4)
            multi_kwargs:  Other configs for multiprocessing. (default: None)

        Raises:
            ValueError: An error occurred when `self._n_workers` less than 0.
        """

        # Set worker number.
        self._n_workers = min(n_workers, mp.cpu_count())
        if self._n_workers <= 0:
            raise ValueError(f'The number of workers must be positive, '
                            f'however, n_workers={n_workers} received.')

        # Whether to print infos.
        self.verbose = multi_kwargs.get('verbose', False)

        # Update and save the configs.
        multiprocess_type = self.__class__.__name__
        multi_kwargs.update(
            n_workers=n_workers,
            multiprocess_type=multiprocess_type)
        self.multi_kwargs = multi_kwargs

        if self.verbose:
            infos = ''
            infos += '=====================Configs=====================\n'
            infos += json.dumps(multi_kwargs, indent=4).replace('"', '\'') + '\n'
            infos += '=====================Configs=====================\n'
            print(infos)

    @property
    def n_workers(self):
        return self._n_workers

    @staticmethod
    def _func_to_src(func):
        """Query the source code of a given Python function.
        
        Args:
            func:  The function to query source code.

        Return:
            The source code of the function.
        """

        src = _func_to_src_dict.get(func, None)
        if src is None:
            src = inspect.getsource(func)
            src = src.split('\n')
            for i, line in enumerate(src):
                # Remove all the decorators.
                if line[0] != '@':
                    src = '\n'.join(src[i:])
                    break
            # Save to the global dict.
            _func_to_src_dict[func] = src
        return src

    @staticmethod
    def _check_args(*args, **kwargs):
        """Check whether all input configs are of the same length."""
        all_args = list(args) + list(kwargs.values())
        length = list(set(map(len, all_args)))

        # Illegal configs.
        if len(length) > 1:
            return -1, False

        return length[0], True

    @staticmethod
    def _parameter_wraps(func):
        """Wrappers to re-organize parameters of functions.

        Since `multiprocessing.Pool.imap` receives only one parameter as input,
        one has to re-organize the parameters to a tuple of (args, kwargs).

        E.g.: For the following function:

        >>> def original_function(x, y, z=1, w=2):
        >>>     print(x, y, z, w)
        >>> args, kwargs = [1, 2], dict(z=5)
        >>> original_function(*args, **kwargs)
        >>> # (1, 2, 5, 2)  # output

        one can rewrite it using this decorator by

        >>> @parameter_wraps
        >>> def rewrited_function(x, y, z=1, w=2):
        >>>     print(x, y, z, w)
        >>> args, kwargs = [1, 2], dict(z=5)
        >>> packaged_params = (arg, kwargs)
        >>> rewrited_function(packaged_params)
        >>> # (1, 2, 5, 2)  # output
        """

        @functools.wraps(func)
        def _func(tuple_dict_params):
            args, kwargs = tuple_dict_params
            return func(*args, **kwargs)
        return _func

    @staticmethod
    def _exec(src, func_name, args, kwargs):
        """Executing the function by its source code."""
        scope = dict()
        exec(src, scope)
        return scope[func_name](*args, **kwargs)

    def __call__(self, func):
        """The main function to decorate the input function."""
        if self.verbose:
            print(f'Decorating function `{func.__name__}`.')

        # We need to first re-organize the input parameters of the function.
        func = self._parameter_wraps(func)
        return func
