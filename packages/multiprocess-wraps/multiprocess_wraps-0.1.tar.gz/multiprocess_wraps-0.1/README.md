# Multiprocess V0.0

## What is it?

It is a package for easily using multiprocess.

## Usage

One can use this package as the **decorator** of you function, which is much easier than to implement the multiprocess pool or process. For example:

```python
def original_version_function(x, y=0, z=0):
    return x + y + z

import multiprocess
@multiprocess.multiprocess()
def multiprocess_version_function(x, y=0, z=0):
    return x + y + z
```

To call the function, simply using

```python
# original version
# return value: 1
origigal_version_function(1)

# multiprocessing version
# return value: [1, 2, 3]
multiprocess_version_function([1, 2, 3])
```

One can also specify the number of workers or whether to involvo CUDA by

```python
# use `min(8, cpu_count())` workers, 
@multiprocess.multiprocess(8)

# print some information for understanding or debugging
@multiprocess.multiprocess(verbose=True)

# involve CUDA
@multiprocess.multiprocess(cuda=True)
```

Notice that the input parameters are iterators with the same length, so when using `torch.Tensor` you may need to adjust the output or the input, e.g.,

```python
@multiprocess.multiprocess()
def func(x, y=0, z=0):
    return x + y + z

print(func(torch.ones(2, 3)))
# return value: [tensor([1., 1., 1.]), tensor([1., 1., 1.])]
# i.e,. [torch.ones(3), torch.ones(3)]
```
## TODOs:

- [ ] Setting `gpu_ids`for multiprocessing with CUDA involved.