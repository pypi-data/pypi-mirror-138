![](./logo.svg)

A minimal package for configuring and exploring parameter `comb`inations of machine learning experiments.

`comb` is a small and simplistic library. `comb` is able to

- quickly and cleanly define grid searches and random searches, and handle parameter dependencies
- add configuration options to existing projects. Existing modules and packages can be turned into a registry, enabling python classes to become accessible and searchable via a string name.


For more complicated workflows, configuration packages like [hydra](https://github.com/facebookresearch/hydra) are better suited.

## Installation

Install `comb-py` from [pypi](https://pypi.org/project/comb-py/):

```python
$ pip install comb-py
```

and import it via

```python
import comb
```

`comb` does not have any dependencies beyond the python standard library. It works for `python>=3.7`.

## Defining an experiment (`comb.sweep`)

In your project, create sweeps directly in python ─ create the following file under `sweep/my_first_experiment.py`

```python
from comb import sweep
from comb.types import zipped, grid

@sweep.register("example-sweep")
class MyExperiment(sweep.Sweep):

    @property
    def script(self):
        return "my/exp.py"

    def get_random_args(self):
        return dict(
            # define a method to sample arguments from
            foo = np.random.choice([42, 73])
        )

    def get_fixed_args(self):
        return dict(
            # zip N dependen arguments together
            bar = zipped("hello", "check out"),
            baz = zipped("world", "comb"),
            # define a search grid (1x2 combinations)
            # over two parameters
            blubb  = grid("star"),
            blubb2 = grid("wars", "treck"),
        )
```

and generate a joblist using

```bash
$ python -m comb example-sweep
exp.py --bar hello --baz world --blubb star --blubb2 wars --foo 73
exp.py --bar hello --baz world --blubb star --blubb2 treck --foo 73
exp.py --bar check out --baz comb --blubb star --blubb2 wars --foo 73
exp.py --bar check out --baz comb --blubb star --blubb2 treck --foo 73
```

## Parametrizing an experiment (`comb.registry`)

`comb` makes it very easy to reference design choices within your experiment by names. Suppose you wanted to add a few datasets and loss functions to a machine learning experiment.

Turn your python module packages or packages into registries by a simple call to `comb.registry.add_helper_functions`:

``` python
# datasets.py
from comb import registry
registry.add_helper_functions(__name__)

@register("mnist")
class MNIST(): pass 

@register("svhn")
class SVHN(): pass 


# loss_functions.py
from comb import registry
registry.add_helper_functions(__name__)

@register("mse")
class MeanSquaredError(): pass

@register("infonce")
class InfoNCE(): pass
```

Afterwards, you can easily list and instantiate your functions:

``` python
>>> import datasets
>>> datasets.get_options("*")
mnist svhn
>>> datasets.init("mnist")
MNIST()
```

## Scheduling experiments

`comb` does not attempt to provide ways to actually launch these experiments ─ there are plenty tools better suited for this.
To name a few suggestions, the following workflows are possible:

### Using GNU parallel

Scheduling a maximum of 2 consecutive jobs via [GNU parallel](https://www.gnu.org/software/parallel/) (similar results can be achived via e.g. `xargs`):

``` bash
$ python -m comb bash-example || exit 1 | parallel --jobs 2 'echo Scheduling job {#}; eval {}'
```

### Using SLURM

Scheduling a job array via slurm:

``` bash
mkdir -p submitted
python -m comb bash-example > jobs.lst
num_jobs=$(wc -l jobs.lst)
jobid=$(sbatch -a 1-${num_jobs} --wrap 'job=$(sed -n ${SLURM_ARRAY_TASK_ID}p jobs.lst); srun ${job}')
mv jobs.lst submitted/{jobid}.lst 
```

## License

`comb` is released under an MIT License.