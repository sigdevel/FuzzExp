"""Module cma implements the CMA-ES (Covariance Matrix Adaptation
Evolution Strategy).

CMA-ES is a stochastic optimizer for robust non-linear non-convex
derivative- and function-value-free numerical optimization.

This implementation can be used with Python versions >= 2.6, namely
2.6, 2.7, 3.3, 3.4.

CMA-ES searches for a minimizer (a solution x in :math:`R^n`) of an
objective function f (cost function), such that f(x) is minimal.
Regarding f, only a passably reliable ranking of the candidate
solutions in each iteration is necessary. Neither the function values
itself, nor the gradient of f need to be available or do matter (like
in the downhill simplex Nelder-Mead algorithm). Some termination
criteria however depend on actual f-values.

Two interfaces are provided:

  - function `fmin(func, x0, sigma0,...)`
        runs a complete minimization
        of the objective function func with CMA-ES.

  - class `CMAEvolutionStrategy`
      allows for minimization such that the control of the iteration
      loop remains with the user.


Used packages:

    - unavoidable: `numpy` (see `barecmaes2.py` if `numpy` is not
      available),
    - avoidable with small changes: `time`, `sys`
    - optional: `matplotlib.pyplot` (for `plot` etc., highly
      recommended), `pprint` (pretty print), `pickle` (in class
      `Sections`), `doctest`, `inspect`, `pygsl` (never by default)

Install
-------
The file ``cma.py`` only needs to be visible in the python path (e.g. in
the current working directory).

The preferred way of (system-wide) installation is calling

    pip install cma

from the command line.

The ``cma.py`` file can also be installed from the
system shell terminal command line by::

    python cma.py --install

which solely calls the ``setup`` function from the standard
``distutils.core`` package for installation. If the ``setup.py``
file is been provided with ``cma.py``, the standard call is

    python setup.py cma

Both calls need to see ``cma.py`` in the current working directory and
might need to be preceded with ``sudo``.

To upgrade the currently installed version from the Python Package Index,
and also for first time installation, type in the system shell::

    pip install --upgrade cma

Testing
-------
From the system shell::

    python cma.py --test

or from the Python shell ``ipython``::

    run cma.py --test

or from any python shell

    import cma
    cma.main('--test')

runs ``doctest.testmod(cma)`` showing only exceptions (and not the
tests that fail due to small differences in the output) and should
run without complaints in about between 20 and 100 seconds.

Example
-------
From a python shell::

    import cma
    help(cma)  "this" help message, use cma? in ipython
    help(cma.fmin)
    help(cma.CMAEvolutionStrategy)
    help(cma.CMAOptions)
    cma.CMAOptions('tol')  
    cma.CMAOptions('verb') 
    res = cma.fmin(cma.Fcts.tablet, 15 * [1], 1)
    res[0]  
    res[5]  

:See: `fmin()`, `CMAOptions`, `CMAEvolutionStrategy`

:Author: Nikolaus Hansen, 2008-2015
:Contributor: Petr Baudis, 2014

:License: BSD 3-Clause, see below.

"""























"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT














































"pure"













"exact"?
"signals" from a file, see import ConfigParser


































"stop now" in file cmaes_signals.par





















"unicode" removed (was incompatible to 3.x)
































































import sys
if not sys.version.startswith('2'):  
    xrange = range
    raw_input = input
    str = str
else:
    input = raw_input  

import time  
import collections
import numpy as np


from numpy import inf, array, dot, exp, log, sqrt, sum, isscalar, isfinite


try:
    from matplotlib import pyplot
    savefig = pyplot.savefig  
    closefig = pyplot.close
    def show():
        
        pyplot.ion()
        pyplot.show()
        
        
    pyplot.ion()  
except:
    pyplot = None
    savefig = None
    closefig = None
    def show():
        print('pyplot.show() is not available')
    print('Could not import matplotlib.pyplot, therefore ``cma.plot()``" +'
          ' etc. is not available')

__author__ = 'Nikolaus Hansen'
__version__ = "1.1.06  $Revision: 4129 $ $Date: 2015-01-23 20:13:51 +0100 (Fri, 23 Jan 2015) $"




__docformat__ = "reStructuredText"  
__all__ = (
        'main',
        'fmin',
        'fcts',
        'Fcts',
        'felli',
        'rotate',
        'pprint',
        'plot',
        'disp',
        'show',
        'savefig',
        'closefig',
        'use_archives',
        'is_feasible',
        'unitdoctest',
        'DerivedDictBase',
        'SolutionDict',
        'CMASolutionDict',
        'BestSolution',

        'BoundNone',
        'BoundTransform',
        'BoundPenalty',


        'GenoPheno',
        'OOOptimizer',
        'CMAEvolutionStrategy',
        'CMAOptions',
        'CMASolutionDict',
        'CMAAdaptSigmaBase',
        'CMAAdaptSigmaNone',
        'CMAAdaptSigmaDistanceProportional',
        'CMAAdaptSigmaCSA',
        'CMAAdaptSigmaTPA',
        'CMAAdaptSigmaMedianImprovement',
        'BaseDataLogger',
        'CMADataLogger',
        'NoiseHandler',
        'Sections',
        'Misc',
        'Mh',
        'ElapsedTime',
        'Rotation',
        'fcts',
        'FFWrappers',
        )
use_archives = True  
"""speed up for very large population size. `use_archives` prevents the
need for an inverse gp-transformation, relies on collections module,
not sure what happens if set to ``False``. """

class MetaParameters(object):
    """meta parameters are either "modifiable constants" or refer to
    options from ``CMAOptions`` or are arguments to ``fmin`` or to the
    ``NoiseHandler`` class constructor.

    Details
    -------
    This code contains a single class instance `meta_parameters`

    Some interfaces rely on parameters being either `int` or
    `float` only. More sophisticated choices are implemented via
    ``choice_value = {1: 'this', 2: 'or that'}[int_param_value]`` here.

    CAVEAT
    ------
    ``meta_parameters`` should not be used to determine default
    arguments, because these are assigned only once and for all during
    module import.

    """
    def __init__(self):
        self.sigma0 = None  

        
        self.CMA_cmean = 1.0  
        self.c1_multiplier = 1.0  
        self.cmu_multiplier = 2.0  
        self.CMA_active = 1.0  
        self.cc_multiplier = 1.0  
        self.cs_multiplier = 1.0 
        self.CSA_dampfac = 1.0  
        self.CMA_dampsvec_fac = None  
        self.CMA_dampsvec_fade = 0.1  

        
        self.c1_exponent = 2.0  
        self.cmu_exponent = 2.0  
        self.cact_exponent = 1.5  
        self.cc_exponent = 1.0  
        self.cs_exponent = 1.0  

        
        self.lambda_exponent = 0.0  
        self.parent_fraction = 0.5  
        self.CMA_elitist = 0  
        self.CMA_mirrors = 0.0  

        
        self.CMA_sample_on_sphere_surface = 0  
        self.mean_shift_line_samples = 0  
        self.pc_line_samples = 0  

        
        self.CSA_damp_mueff_exponent = 0.5  
        self.CSA_disregard_length = 0  
        self.CSA_squared = 0  
        self.CSA_clip_length_value = None  

        
        self.noise_reeval_multiplier = 1.0  
        self.noise_choose_reeval = 1  
        self.noise_theta = 0.5  
        self.noise_alphasigma = 2.0  
        self.noise_alphaevals = 2.0  
        self.noise_alphaevalsdown_exponent = -0.25  
        self.noise_aggregate = None  
        

        
        self.restarts = 0  
        self.restart_from_best = 0  
        self.incpopsize = 2.0  

        
        self.maxiter_multiplier = 1.0  
        self.mindx = 0.0  
        self.minstd = 0.0  
        self.maxstd = None  
        self.tolfacupx = 1e3  
        self.tolupsigma = 1e20  "creeping behavior" with usually minor improvements',
        self.tolx = 1e-11  
        self.tolfun = 1e-11  
        self.tolfunhist = 1e-12  
        self.tolstagnation_multiplier = 1.0  

        
        
        
        
        
        
        

meta_parameters = MetaParameters()









"x in emptysets" cannot be well replaced by "not x"







def rglen(ar):
    """shortcut for the iterator ``xrange(len(ar))``"""
    return range(len(ar))

def is_feasible(x, f):
    """default to check feasibility, see also ``cma_default_options``"""
    return f is not None and f is not np.NaN

global_verbosity = 1
def _print_warning(msg, method_name=None, class_name=None, iteration=None,
                   verbose=None):
    if verbose is None:
        verbose = global_verbosity
    if verbose > 0:
        print('WARNING (module=' + __name__ +
              (', class=' + str(class_name) if class_name else '') +
              (', method=' + str(method_name) if method_name else '') +
              (', iteration=' + str(iteration) if iteration else '') +
              '): ', msg)




def unitdoctest():
    """is used to describe test cases and might in future become helpful
    as an experimental tutorial as well. The main testing feature at the
    moment is by doctest with ``cma._test()`` or conveniently by
    ``python cma.py --test``. With the ``--verbose`` option added, the
    results will always slightly differ and many "failed" test cases
    might be reported.

    A simple first overall test:
        >>> import cma
        >>> res = cma.fmin(cma.fcts.elli, 3*[1], 1,
        ...                {'CMA_diagonal':2, 'seed':1, 'verb_time':0})
        (3_w,7)-CMA-ES (mu_w=2.3,w_1=58%) in dimension 3 (seed=1)
           Covariance matrix is diagonal for 2 iterations (1/ccov=7.0)
        Iterat 
            1       7 1.453161670768570e+04 1.2e+00 1.08e+00  1e+00  1e+00
            2      14 3.281197961927601e+04 1.3e+00 1.22e+00  1e+00  2e+00
            3      21 1.082851071704020e+04 1.3e+00 1.24e+00  1e+00  2e+00
          100     700 8.544042012075362e+00 1.4e+02 3.18e-01  1e-03  2e-01
          200    1400 5.691152415221861e-12 1.0e+03 3.82e-05  1e-09  1e-06
          220    1540 3.890107746209078e-15 9.5e+02 4.56e-06  8e-11  7e-08
        termination on tolfun : 1e-11
        final/bestever f-value = 3.89010774621e-15 2.52273602735e-15
        mean solution:  [ -4.63614606e-08  -3.42761465e-10   1.59957987e-11]
        std deviation: [  6.96066282e-08   2.28704425e-09   7.63875911e-11]

    Test on the Rosenbrock function with 3 restarts. The first trial only
    finds the local optimum, which happens in about 20% of the cases.

        >>> import cma
        >>> res = cma.fmin(cma.fcts.rosen, 4*[-1], 1,
        ...                options={'ftarget':1e-6, 'verb_time':0,
        ...                    'verb_disp':500, 'seed':3},
        ...                restarts=3)
        (4_w,8)-CMA-ES (mu_w=2.6,w_1=52%) in dimension 4 (seed=3)
        Iterat 
            1       8 4.875315645656848e+01 1.0e+00 8.43e-01  8e-01  8e-01
            2      16 1.662319948123120e+02 1.1e+00 7.67e-01  7e-01  8e-01
            3      24 6.747063604799602e+01 1.2e+00 7.08e-01  6e-01  7e-01
          184    1472 3.701428610430019e+00 4.3e+01 9.41e-07  3e-08  5e-08
        termination on tolfun : 1e-11
        final/bestever f-value = 3.70142861043 3.70142861043
        mean solution:  [-0.77565922  0.61309336  0.38206284  0.14597202]
        std deviation: [  2.54211502e-08   3.88803698e-08   4.74481641e-08   3.64398108e-08]
        (8_w,16)-CMA-ES (mu_w=4.8,w_1=32%) in dimension 4 (seed=4)
        Iterat 
            1    1489 2.011376859371495e+02 1.0e+00 8.90e-01  8e-01  9e-01
            2    1505 4.157106647905128e+01 1.1e+00 8.02e-01  7e-01  7e-01
            3    1521 3.548184889359060e+01 1.1e+00 1.02e+00  8e-01  1e+00
          111    3249 6.831867555502181e-07 5.1e+01 2.62e-02  2e-04  2e-03
        termination on ftarget : 1e-06
        final/bestever f-value = 6.8318675555e-07 1.18576673231e-07
        mean solution:  [ 0.99997004  0.99993938  0.99984868  0.99969505]
        std deviation: [ 0.00018973  0.00038006  0.00076479  0.00151402]
        >>> assert res[1] <= 1e-6

    Notice the different termination conditions. Termination on the target
    function value ftarget prevents further restarts.

    Test of scaling_of_variables option

        >>> import cma
        >>> opts = cma.CMAOptions()
        >>> opts['seed'] = 456
        >>> opts['verb_disp'] = 0
        >>> opts['CMA_active'] = 1
        >>> 
        >>> 
        >>> opts['scaling_of_variables'] = [1, 1, 1e3, 1]
        >>> res = cma.fmin(cma.fcts.rosen, 4 * [0.1], 0.1, opts)
        termination on tolfun : 1e-11
        final/bestever f-value = 2.68096173031e-14 1.09714829146e-14
        mean solution:  [ 1.00000001  1.00000002  1.00000004  1.00000007]
        std deviation: [  3.00466854e-08   5.88400826e-08   1.18482371e-07   2.34837383e-07]

    The printed std deviations reflect the actual value in the parameters
    of the function (not the one in the internal representation which 
    can be different).

    Test of CMA_stds scaling option.

        >>> import cma
        >>> opts = cma.CMAOptions()
        >>> s = 5 * [1]
        >>> s[0] = 1e3
        >>> opts.set('CMA_stds', s)
        >>> opts.set('verb_disp', 0)
        >>> res = cma.fmin(cma.fcts.cigar, 5 * [0.1], 0.1, opts)
        >>> assert res[1] < 1800

    :See: cma.main(), cma._test()

    """

    pass

class _BlancClass(object):
    """blanc container class for having a collection of attributes,
    that might/should at some point become a more tailored class"""

if use_archives:

    class DerivedDictBase(collections.MutableMapping):
        """for conveniently adding "features" to a dictionary. The actual
        dictionary is in ``self.data``. Copy-paste
        and modify setitem, getitem, and delitem, if necessary.

        Details: This is the clean way to subclass build-in dict.

        """
        def __init__(self, *args, **kwargs):
            
            super(DerivedDictBase, self).__init__()
            
            self.data = dict()
            self.data.update(dict(*args, **kwargs))
        def __len__(self):
            return len(self.data)
        def __contains__(self, key):
            return key in self.data
        def __iter__(self):
            return iter(self.data)
        def __setitem__(self, key, value):
            """defines self[key] = value"""
            self.data[key] = value
        def __getitem__(self, key):
            """defines self[key]"""
            return self.data[key]
        def __delitem__(self, key):
            del self.data[key]

    class SolutionDict(DerivedDictBase):
        """dictionary with computation of an hash key.

        The hash key is generated from the inserted solution and a stack of
        previously inserted same solutions is provided. Each entry is meant
        to store additional information related to the solution.

            >>> import cma, numpy as np
            >>> d = cma.SolutionDict()
            >>> x = np.array([1,2,4])
            >>> d[x] = {'f': sum(x**2), 'iteration': 1}
            >>> assert d[x]['iteration'] == 1
            >>> assert d.get(x) == (d[x] if d.key(x) in d.keys() else None)

        TODO: data_with_same_key behaves like a stack (see setitem and
        delitem), but rather should behave like a queue?! A queue is less
        consistent with the operation self[key] = ..., if
        self.data_with_same_key[key] is not empty.

        TODO: iteration key is used to clean up without error management

        """
        def __init__(self, *args, **kwargs):
            
            super(SolutionDict, self).__init__(*args, **kwargs)
            self.data_with_same_key = {}
            self.last_iteration = 0
        def key(self, x):
            try:
                return tuple(x)
                
            except TypeError:
                return x
        def __setitem__(self, key, value):
            """defines self[key] = value"""
            key = self.key(key)
            if key in self.data_with_same_key:
                self.data_with_same_key[key] += [self.data[key]]
            elif key in self.data:
                self.data_with_same_key[key] = [self.data[key]]
            self.data[key] = value
        def __getitem__(self, key):  
            """defines self[key]"""
            return self.data[self.key(key)]
        def __delitem__(self, key):
            """remove only most current key-entry"""
            key = self.key(key)
            if key in self.data_with_same_key:
                if len(self.data_with_same_key[key]) == 1:
                    self.data[key] = self.data_with_same_key.pop(key)[0]
                else:
                    self.data[key] = self.data_with_same_key[key].pop(-1)
            else:
                del self.data[key]
        def truncate(self, max_len, min_iter):
            if len(self) > max_len:
                for k in list(self.keys()):
                    if self[k]['iteration'] < min_iter:
                        del self[k]
                        

    class CMASolutionDict(SolutionDict):
        def __init__(self, *args, **kwargs):
            
            super(CMASolutionDict, self).__init__(*args, **kwargs)
            self.last_solution_index = 0

        
        
        def insert(self, key, geno=None, iteration=None, fitness=None, value=None):
            """insert an entry with key ``key`` and value
            ``value if value is not None else {'geno':key}`` and
            ``self[key]['kwarg'] = kwarg if kwarg is not None`` for the further kwargs.

            """
            
            if iteration is not None and iteration > self.last_iteration and (iteration % 10) < 1:
                self.truncate(300, iteration - 3)
            elif value is not None and value.get('iteration'):
                iteration = value['iteration']
                if (iteration % 10) < 1:
                    self.truncate(300, iteration - 3)

            self.last_solution_index += 1
            if value is not None:
                try:
                    iteration = value['iteration']
                except:
                    pass
            if iteration is not None:
                if iteration > self.last_iteration:
                    self.last_solution_index = 0
                self.last_iteration = iteration
            else:
                iteration = self.last_iteration + 0.5  
            if value is not None:
                self[key] = value
            else:
                self[key] = {'pheno': key}
            if geno is not None:
                self[key]['geno'] = geno
            if iteration is not None:
                self[key]['iteration'] = iteration
            if fitness is not None:
                self[key]['fitness'] = fitness
            return self[key]

if not use_archives:
    class CMASolutionDict(dict):
        """a hack to get most code examples running"""
        def insert(self, *args, **kwargs):
            pass
        def get(self, key):
            return None
        def __getitem__(self, key):
            return None
        def __setitem__(self, key, value):
            pass

class BestSolution(object):
    """container to keep track of the best solution seen"""
    def __init__(self, x=None, f=np.inf, evals=None):
        """initialize the best solution with `x`, `f`, and `evals`.
        Better solutions have smaller `f`-values.

        """
        self.x = x
        self.x_geno = None
        self.f = f if f is not None and f is not np.nan else np.inf
        self.evals = evals
        self.evalsall = evals
        self.last = _BlancClass()
        self.last.x = x
        self.last.f = f
    def update(self, arx, xarchive=None, arf=None, evals=None):
        """checks for better solutions in list `arx`.

        Based on the smallest corresponding value in `arf`,
        alternatively, `update` may be called with a `BestSolution`
        instance like ``update(another_best_solution)`` in which case
        the better solution becomes the current best.

        `xarchive` is used to retrieve the genotype of a solution.

        """
        if isinstance(arx, BestSolution):
            if self.evalsall is None:
                self.evalsall = arx.evalsall
            elif arx.evalsall is not None:
                self.evalsall = max((self.evalsall, arx.evalsall))
            if arx.f is not None and arx.f < np.inf:
                self.update([arx.x], xarchive, [arx.f], arx.evals)
            return self
        assert arf is not None
        
        minidx = np.nanargmin(arf)
        if minidx is np.nan:
            return
        minarf = arf[minidx]
        
        
        if minarf < np.inf and (minarf < self.f or self.f is None):
            self.x, self.f = arx[minidx], arf[minidx]
            if xarchive is not None and xarchive.get(self.x) is not None:
                self.x_geno = xarchive[self.x].get('geno')
            else:
                self.x_geno = None
            self.evals = None if not evals else evals - len(arf) + minidx + 1
            self.evalsall = evals
        elif evals:
            self.evalsall = evals
        self.last.x = arx[minidx]
        self.last.f = minarf
    def get(self):
        """return ``(x, f, evals)`` """
        return self.x, self.f, self.evals  





class BoundaryHandlerBase(object):
    """hacked base class """
    def __init__(self, bounds):
        """bounds are not copied, but possibly modified and
        put into a normalized form: ``bounds`` can be ``None``
        or ``[lb, ub]`` where ``lb`` and ``ub`` are
        either None or a vector (which can have ``None`` entries).

        Generally, the last entry is recycled to compute bounds
        for any dimension.

        """
        if not bounds:
            self.bounds = None
        else:
            l = [None, None]  
            for i in [0, 1]:
                try:
                    l[i] = len(bounds[i])
                except TypeError:
                    bounds[i] = [bounds[i]]
                    l[i] = 1
                if all([bounds[i][j] is None or not isfinite(bounds[i][j])
                        for j in rglen(bounds[i])]):
                    bounds[i] = None
                if bounds[i] is not None and any([bounds[i][j] == (-1)**i * np.inf
                                                  for j in rglen(bounds[i])]):
                    raise ValueError('lower/upper is +inf/-inf and ' +
                                     'therefore no finite feasible solution is available')
            self.bounds = bounds

    def __call__(self, solutions, *args, **kwargs):
        """return penalty or list of penalties, by default zero(s).

        This interface seems too specifically tailored to the derived
        BoundPenalty class, it should maybe change.

        """
        if isscalar(solutions[0]):
            return 0.0
        else:
            return len(solutions) * [0.0]

    def update(self, *args, **kwargs):
        return self

    def repair(self, x, copy_if_changed=True, copy_always=False):
        """projects infeasible values on the domain bound, might be
        overwritten by derived class """
        if copy_always:
            x = array(x, copy=True)
            copy = False
        else:
            copy = copy_if_changed
        if self.bounds is None:
            return x
        for ib in [0, 1]:
            if self.bounds[ib] is None:
                continue
            for i in rglen(x):
                idx = min([i, len(self.bounds[ib]) - 1])
                if self.bounds[ib][idx] is not None and \
                        (-1)**ib * x[i] < (-1)**ib * self.bounds[ib][idx]:
                    if copy:
                        x = array(x, copy=True)
                        copy = False
                    x[i] = self.bounds[ib][idx]

    def inverse(self, y, copy_if_changed=True, copy_always=False):
        return y if not copy_always else array(y, copy=True)

    def get_bounds(self, which, dimension):
        """``get_bounds('lower', 8)`` returns the lower bounds in 8-D"""
        if which == 'lower' or which == 0:
            return self._get_bounds(0, dimension)
        elif which == 'upper' or which == 1:
            return self._get_bounds(1, dimension)
        else:
            raise ValueError("argument which must be 'lower' or 'upper'")

    def _get_bounds(self, ib, dimension):
        """ib == 0/1 means lower/upper bound, return a vector of length
        `dimension` """
        sign_ = 2 * ib - 1
        assert sign_**2 == 1
        if self.bounds is None or self.bounds[ib] is None:
            return array(dimension * [sign_ * np.Inf])
        res = []
        for i in range(dimension):
            res.append(self.bounds[ib][min([i, len(self.bounds[ib]) - 1])])
            if res[-1] is None:
                res[-1] = sign_ * np.Inf
        return array(res)

    def has_bounds(self):
        """return True, if any variable is bounded"""
        bounds = self.bounds
        if bounds in (None, [None, None]):
            return False
        for ib, bound in enumerate(bounds):
            if bound is not None:
                sign_ = 2 * ib - 1
                for bound_i in bound:
                    if bound_i is not None and sign_ * bound_i < np.inf:
                        return True
        return False

    def is_in_bounds(self, x):
        """not yet tested"""
        if self.bounds is None:
            return True
        for ib in [0, 1]:
            if self.bounds[ib] is None:
                continue
            for i in rglen(x):
                idx = min([i, len(self.bounds[ib]) - 1])
                if self.bounds[ib][idx] is not None and \
                        (-1)**ib * x[i] < (-1)**ib * self.bounds[ib][idx]:
                    return False
        return True

    def to_dim_times_two(self, bounds):
        """return boundaries in format ``[[lb0, ub0], [lb1, ub1], ...]``,
        as used by ``BoxConstraints...`` class.

        """
        if not bounds:
            b = [[None, None]]
        else:
            l = [None, None]  
            for i in [0, 1]:
                try:
                    l[i] = len(bounds[i])
                except TypeError:
                    bounds[i] = [bounds[i]]
                    l[i] = 1
            b = []  
            try:
                for i in range(max(l)):
                    b.append([bounds[0][i] if i < l[0] else None,
                              bounds[1][i] if i < l[1] else None])
            except (TypeError, IndexError):
                print("boundaries must be provided in the form " +
                      "[scalar_of_vector, scalar_or_vector]")
                raise
        return b




class BoundNone(BoundaryHandlerBase):
    def __init__(self, bounds=None):
        if bounds is not None:
            raise ValueError()
        
        super(BoundNone, self).__init__(None)
    def is_in_bounds(self, x):
        return True




class BoundTransform(BoundaryHandlerBase):
    """Handles boundary by a smooth, piecewise linear and quadratic
    transformation into the feasible domain.

    >>> import cma
    >>> veq = cma.Mh.vequals_approximately
    >>> b = cma.BoundTransform([None, 1])
    >>> assert b.bounds == [[None], [1]]
    >>> assert veq(b.repair([0, 1, 1.2]), array([ 0., 0.975, 0.975]))
    >>> assert b.is_in_bounds([0, 0.5, 1])
    >>> assert veq(b.transform([0, 1, 2]), [ 0.   ,  0.975,  0.2  ])
    >>> o=cma.fmin(cma.fcts.sphere, 6 * [-2], 0.5, options={
    ...    'boundary_handling': 'BoundTransform ',
    ...    'bounds': [[], 5 * [-1] + [inf]] })
    >>> assert o[1] < 5 + 1e-8
    >>> import numpy as np
    >>> b = cma.BoundTransform([-np.random.rand(120), np.random.rand(120)])
    >>> for i in range(100):
    ...     x = (-i-1) * np.random.rand(120) + i * np.random.randn(120)
    ...     x_to_b = b.repair(x)
    ...     x2 = b.inverse(x_to_b)
    ...     x2_to_b = b.repair(x2)
    ...     x3 = b.inverse(x2_to_b)
    ...     x3_to_b = b.repair(x3)
    ...     assert veq(x_to_b, x2_to_b)
    ...     assert veq(x2, x3)
    ...     assert veq(x2_to_b, x3_to_b)

    Details: this class uses ``class BoxConstraintsLinQuadTransformation``

    """
    def __init__(self, bounds=None):
        """Argument bounds can be `None` or ``bounds[0]`` and ``bounds[1]``
        are lower and upper domain boundaries, each is either `None` or
        a scalar or a list or array of appropriate size.

        """
        
        super(BoundTransform, self).__init__(bounds)
        self.bounds_tf = BoxConstraintsLinQuadTransformation(self.to_dim_times_two(bounds))

    def repair(self, x, copy_if_changed=True, copy_always=False):
        """transforms ``x`` into the bounded domain.

        ``copy_always`` option might disappear.

        """
        copy = copy_if_changed
        if copy_always:
            x = array(x, copy=True)
            copy = False
        if self.bounds is None or (self.bounds[0] is None and
                                   self.bounds[1] is None):
            return x
        return self.bounds_tf(x, copy)

    def transform(self, x):
        return self.repair(x)

    def inverse(self, x, copy_if_changed=True, copy_always=False):
        """inverse transform of ``x`` from the bounded domain.

        """
        copy = copy_if_changed
        if copy_always:
            x = array(x, copy=True)
            copy = False
        if self.bounds is None or (self.bounds[0] is None and
                                   self.bounds[1] is None):
            return x
        return self.bounds_tf.inverse(x, copy)  




class BoundPenalty(BoundaryHandlerBase):
    """Computes the boundary penalty. Must be updated each iteration,
    using the `update` method.

    Details
    -------
    The penalty computes like ``sum(w[i] * (x[i]-xfeas[i])**2)``,
    where `xfeas` is the closest feasible (in-bounds) solution from `x`.
    The weight `w[i]` should be updated during each iteration using
    the update method.

    Example:

    >>> import cma
    >>> cma.fmin(cma.felli, 6 * [1], 1,
    ...          {
    ...              'boundary_handling': 'BoundPenalty',
    ...              'bounds': [-1, 1],
    ...              'fixed_variables': {0: 0.012, 2:0.234}
    ...          })

    Reference: Hansen et al 2009, A Method for Handling Uncertainty...
    IEEE TEC, with addendum, see
    http://www.lri.fr/~hansen/TEC2009online.pdf

    """
    def __init__(self, bounds=None):
        """Argument bounds can be `None` or ``bounds[0]`` and ``bounds[1]``
        are lower  and upper domain boundaries, each is either `None` or
        a scalar or a list or array of appropriate size.
        """
        
        
        
        super(BoundPenalty, self).__init__(bounds)

        self.gamma = 1  
        self.weights_initialized = False  
        self.hist = []  

    def repair(self, x, copy_if_changed=True, copy_always=False):
        """sets out-of-bounds components of ``x`` on the bounds.

        """
        
        
        copy = copy_if_changed
        if copy_always:
            x = array(x, copy=True)
        bounds = self.bounds
        if bounds not in (None, [None, None], (None, None)):  
            x = array(x, copy=True) if copy and not copy_always else x
            if bounds[0] is not None:
                if isscalar(bounds[0]):
                    for i in rglen(x):
                        x[i] = max((bounds[0], x[i]))
                else:
                    for i in rglen(x):
                        j = min([i, len(bounds[0]) - 1])
                        if bounds[0][j] is not None:
                            x[i] = max((bounds[0][j], x[i]))
            if bounds[1] is not None:
                if isscalar(bounds[1]):
                    for i in rglen(x):
                        x[i] = min((bounds[1], x[i]))
                else:
                    for i in rglen(x):
                        j = min((i, len(bounds[1]) - 1))
                        if bounds[1][j] is not None:
                            x[i] = min((bounds[1][j], x[i]))
        return x

    
    
    def __call__(self, x, archive, gp):
        """returns the boundary violation penalty for `x` ,where `x` is a
        single solution or a list or array of solutions.

        """
        if x in (None, (), []):
            return x
        if self.bounds in (None, [None, None], (None, None)):
            return 0.0 if isscalar(x[0]) else [0.0] * len(x)  

        x_is_single_vector = isscalar(x[0])
        x = [x] if x_is_single_vector else x

        
        try:
            gamma = list(self.gamma)  
            for i in sorted(gp.fixed_values):  
                gamma.insert(i, 0.0)
            gamma = array(gamma, copy=False)
        except TypeError:
            gamma = self.gamma
        pen = []
        for xi in x:
            
            
            
            xpheno = gp.pheno(archive[xi]['geno'])
            
            xinbounds = self.repair(xpheno)
            
            fac = 1  
            pen.append(sum(gamma * ((xinbounds - xpheno) / fac)**2) / len(xi))
        return pen[0] if x_is_single_vector else pen

    
    
    def feasible_ratio(self, solutions):
        """counts for each coordinate the number of feasible values in
        ``solutions`` and returns an array of length ``len(solutions[0])``
        with the ratios.

        `solutions` is a list or array of repaired ``Solution``
        instances,

        """
        raise NotImplementedError('Solution class disappeared')
        count = np.zeros(len(solutions[0]))
        for x in solutions:
            count += x.unrepaired == x
        return count / float(len(solutions))

    
    
    def update(self, function_values, es):
        """updates the weights for computing a boundary penalty.

        Arguments
        ---------
        `function_values`
            all function values of recent population of solutions
        `es`
            `CMAEvolutionStrategy` object instance, in particular
            mean and variances and the methods from the attribute
            `gp` of type `GenoPheno` are used.

        """
        if self.bounds is None or (self.bounds[0] is None and
                                   self.bounds[1] is None):
            return self

        N = es.N
        
        
        varis = es.sigma**2 * array(N * [es.C] if isscalar(es.C) else (
                                es.C if isscalar(es.C[0]) else  
                                [es.C[i][i] for i in range(N)]))  

        
        dmean = (es.mean - es.gp.geno(self.repair(es.gp.pheno(es.mean)))) / varis**0.5

        
        fvals = sorted(function_values)
        l = 1 + len(fvals)
        val = fvals[3 * l // 4] - fvals[l // 4]  
        val = val / np.mean(varis)  
        
        if isfinite(val) and val > 0:
            self.hist.insert(0, val)
        elif val == inf and len(self.hist) > 1:
            self.hist.insert(0, max(self.hist))
        else:
            pass  
        if len(self.hist) > 20 + (3 * N) / es.popsize:
            self.hist.pop()

        
        dfit = np.median(self.hist)  
        damp = min(1, es.sp.mueff / 10. / N)

        
        
        if len(self.hist) == 0:
            raise _Error('wrongful initialization, no feasible solution sampled. ' +
                'Reasons can be mistakenly set bounds (lower bound not smaller than upper bound) or a too large initial sigma0 or... ' +
                'See description of argument func in help(cma.fmin) or an example handling infeasible solutions in help(cma.CMAEvolutionStrategy). ')
        
        if dmean.any() and (not self.weights_initialized or es.countiter == 2):  
            self.gamma = array(N * [2 * dfit])  
            self.weights_initialized = True
        
        if self.weights_initialized:
            edist = array(abs(dmean) - 3 * max(1, N**0.5 / es.sp.mueff))
            if 1 < 3:  
                
                
                self.gamma *= exp((edist > 0) * np.tanh(edist / 3) / 2.)**damp
                
                
                self.gamma[self.gamma > 5 * dfit] *= exp(-1. / 3)**damp
                
        es.more_to_write += list(self.gamma) if self.weights_initialized else N * [1.0]
        
        
        return self  




class BoxConstraintsTransformationBase(object):
    """Implements a transformation into boundaries and is used for
    boundary handling::

        tf = BoxConstraintsTransformationAnyDerivedClass([[1, 4]])
        x = [3, 2, 4.4]
        y = tf(x)  "repaired" solution
        print(tf([2.5]))  
        [2.5]

    :See: ``BoundaryHandler``

    """
    def __init__(self, bounds):
        try:
            if len(bounds[0]) != 2:
                raise ValueError
        except:
            raise ValueError(' bounds must be either [[lb0, ub0]] or [[lb0, ub0], [lb1, ub1],...], \n where in both cases the last entry is reused for all remaining dimensions')
        self.bounds = bounds
        self.initialize()

    def initialize(self):
        """initialize in base class"""
        self._lb = [b[0] for b in self.bounds]  
        self._ub = [b[1] for b in self.bounds]

    def _lowerupperval(self, a, b, c):
        return np.max([np.max(a), np.min([np.min(b), c])])
    def bounds_i(self, i):
        """return ``[ith_lower_bound, ith_upper_bound]``"""
        return self.bounds[self._index(i)]
    def __call__(self, solution_in_genotype):
        res = [self._transform_i(x, i) for i, x in enumerate(solution_in_genotype)]
        return res
    transform = __call__
    def inverse(self, solution_in_phenotype, copy_if_changed=True, copy_always=True):
        return [self._inverse_i(y, i) for i, y in enumerate(solution_in_phenotype)]
    def _index(self, i):
        return min((i, len(self.bounds) - 1))
    def _transform_i(self, x, i):
        raise NotImplementedError('this is an abstract method that should be implemented in the derived class')
    def _inverse_i(self, y, i):
        raise NotImplementedError('this is an abstract method that should be implemented in the derived class')
    def shift_or_mirror_into_invertible_domain(self, solution_genotype):
        """return the reference solution that has the same ``box_constraints_transformation(solution)``
        value, i.e. ``tf.shift_or_mirror_into_invertible_domain(x) = tf.inverse(tf.transform(x))``.
        This is an idempotent mapping (leading to the same result independent how often it is
        repeatedly applied).

        """
        return self.inverse(self(solution_genotype))
        raise NotImplementedError('this is an abstract method that should be implemented in the derived class')

class _BoxConstraintsTransformationTemplate(BoxConstraintsTransformationBase):
    """copy/paste this template to implement a new boundary handling transformation"""
    def __init__(self, bounds):
        
        super(_BoxConstraintsTransformationTemplate, self).__init__(bounds)
    def initialize(self):
        BoxConstraintsTransformationBase.initialize(self)  
    def _transform_i(self, x, i):
        raise NotImplementedError('this is an abstract method that should be implemented in the derived class')
    def _inverse_i(self, y, i):
        raise NotImplementedError('this is an abstract method that should be implemented in the derived class')
    __doc__ = BoxConstraintsTransformationBase.__doc__ + __doc__

class BoxConstraintsLinQuadTransformation(BoxConstraintsTransformationBase):
    """implements a bijective, monotonous transformation between [lb - al, ub + au]
    and [lb, ub] which is the identity (and therefore linear) in [lb + al, ub - au]
    (typically about 90% of the interval) and quadratic in [lb - 3*al, lb + al]
    and in [ub - au, ub + 3*au]. The transformation is periodically
    expanded beyond the limits (somewhat resembling the shape sin(x-pi/2))
    with a period of ``2 * (ub - lb + al + au)``.

    Details
    =======
    Partly due to numerical considerations depend the values ``al`` and ``au``
    on ``abs(lb)`` and ``abs(ub)`` which makes the transformation non-translation
    invariant. In contrast to sin(.), the transformation is robust to "arbitrary"
    values for boundaries, e.g. a lower bound of ``-1e99`` or ``np.Inf`` or
    ``None``.

    Examples
    ========
    Example to use with cma:

    >>> import cma
    >>> 
    >>> tf = cma.BoxConstraintsLinQuadTransformation([[1,2], [1,None]]) 
    >>> cma.fmin(cma.felli, 9 * [2], 1, {'transformation': [tf.transform, tf.inverse], 'verb_disp': 0})
    >>> 
    >>> es = cma.CMAEvolutionStrategy(9 * [2], 1)
    >>> while not es.stop():
    ...     X = es.ask()
    ...     f = [cma.felli(tf(x)) for x in X]  
    ...     es.tell(X, f)

    Example of the internal workings:

    >>> import cma
    >>> tf = cma.BoxConstraintsLinQuadTransformation([[1,2], [1,11], [1,11]])
    >>> tf.bounds
    [[1, 2], [1, 11], [1, 11]]
    >>> tf([1.5, 1.5, 1.5])
    [1.5, 1.5, 1.5]
    >>> tf([1.52, -2.2, -0.2, 2, 4, 10.4])
    [1.52, 4.0, 2.0, 2.0, 4.0, 10.4]
    >>> res = np.round(tf._au, 2)
    >>> assert list(res[:4]) == [ 0.15, 0.6, 0.6, 0.6]
    >>> res = [round(x, 2) for x in tf.shift_or_mirror_into_invertible_domain([1.52, -12.2, -0.2, 2, 4, 10.4])]
    >>> assert res == [1.52, 9.2, 2.0, 2.0, 4.0, 10.4]
    >>> tmp = tf([1])  

    """
    def __init__(self, bounds):
        """``x`` is defined in ``[lb - 3*al, ub + au + r - 2*al]`` with ``r = ub - lb + al + au``,
        and ``x == transformation(x)`` in ``[lb + al, ub - au]``.
        ``beta*x - alphal = beta*x - alphau`` is then defined in ``[lb, ub]``,

        ``alphal`` and ``alphau`` represent the same value, but respectively numerically
        better suited for values close to lb and ub.

        """
        
        super(BoxConstraintsLinQuadTransformation, self).__init__(bounds)
        
        

    def initialize(self, length=None):
        """see ``__init__``"""
        if length is None:
            length = len(self.bounds)
        max_i = min((len(self.bounds) - 1, length - 1))
        self._lb = array([self.bounds[min((i, max_i))][0]
                          if self.bounds[min((i, max_i))][0] is not None
                          else -np.Inf
                          for i in range(length)], copy=False)
        self._ub = array([self.bounds[min((i, max_i))][1]
                          if self.bounds[min((i, max_i))][1] is not None
                          else np.Inf
                          for i in range(length)], copy=False)
        lb = self._lb
        ub = self._ub
        
        self._al = array([min([(ub[i] - lb[i]) / 2, (1 + np.abs(lb[i])) / 20])
                             if isfinite(lb[i]) else 1 for i in rglen(lb)], copy=False)
        self._au = array([min([(ub[i] - lb[i]) / 2, (1 + np.abs(ub[i])) / 20])
                             if isfinite(ub[i]) else 1 for i in rglen(ub)], copy=False)

    def __call__(self, solution_genotype, copy_if_changed=True, copy_always=False):
        
        
        
        if len(self._lb) != len(solution_genotype):
            self.initialize(len(solution_genotype))
        lb = self._lb
        ub = self._ub
        al = self._al
        au = self._au

        if copy_always or not isinstance(solution_genotype[0], float):
            
            y = np.array(solution_genotype, copy=True, dtype=float)
            
            copy = False
        else:
            y = solution_genotype
            copy = copy_if_changed
        idx = (y < lb - 2 * al - (ub - lb) / 2.0) | (y > ub + 2 * au + (ub - lb) / 2.0)
        if idx.any():
            r = 2 * (ub[idx] - lb[idx] + al[idx] + au[idx])  
            s = lb[idx] - 2 * al[idx] - (ub[idx] - lb[idx]) / 2.0  
            if copy:
                y = np.array(y, copy=True)
                copy = False
            y[idx] -= r * ((y[idx] - s) // r)  
        idx = y > ub + au
        if idx.any():
            if copy:
                y = np.array(y, copy=True)
                copy = False
            y[idx] -= 2 * (y[idx] - ub[idx] - au[idx])
        idx = y < lb - al
        if idx.any():
            if copy:
                y = np.array(y, copy=True)
                copy = False
            y[idx] += 2 * (lb[idx] - al[idx] - y[idx])
        idx = y < lb + al
        if idx.any():
            if copy:
                y = np.array(y, copy=True)
                copy = False
            y[idx] = lb[idx] + (y[idx] - (lb[idx] - al[idx]))**2 / 4 / al[idx]
        idx = y > ub - au
        if idx.any():
            if copy:
                y = np.array(y, copy=True)
                copy = False
            y[idx] = ub[idx] - (y[idx] - (ub[idx] + au[idx]))**2 / 4 / au[idx]
        
        return y
    __call__.doc = BoxConstraintsTransformationBase.__doc__
    transform = __call__
    def idx_infeasible(self, solution_genotype):
        """return indices of "infeasible" variables, that is,
        variables that do not directly map into the feasible domain such that
        ``tf.inverse(tf(x)) == x``.

        """
        res = [i for i, x in enumerate(solution_genotype)
                                if not self.is_feasible_i(x, i)]
        return res
    def is_feasible_i(self, x, i):
        """return True if value ``x`` is in the invertible domain of
        variable ``i``

        """
        lb = self._lb[self._index(i)]
        ub = self._ub[self._index(i)]
        al = self._al[self._index(i)]
        au = self._au[self._index(i)]
        return lb - al < x < ub + au
    def is_loosely_feasible_i(self, x, i):
        """never used"""
        lb = self._lb[self._index(i)]
        ub = self._ub[self._index(i)]
        al = self._al[self._index(i)]
        au = self._au[self._index(i)]
        return lb - 2 * al - (ub - lb) / 2.0 <= x <= ub + 2 * au + (ub - lb) / 2.0

    def shift_or_mirror_into_invertible_domain(self, solution_genotype,
                                               copy=False):
        """Details: input ``solution_genotype`` is changed. The domain is
        [lb - al, ub + au] and in [lb - 2*al - (ub - lb) / 2, lb - al]
        mirroring is applied.

        """
        assert solution_genotype is not None
        if copy:
            y = [val for val in solution_genotype]
        else:
            y = solution_genotype
        if isinstance(y, np.ndarray) and not isinstance(y[0], float):
            y = array(y, dtype=float)
        for i in rglen(y):
            lb = self._lb[self._index(i)]
            ub = self._ub[self._index(i)]
            al = self._al[self._index(i)]
            au = self._au[self._index(i)]
            
            if y[i] < lb - 2 * al - (ub - lb) / 2.0 or y[i] > ub + 2 * au + (ub - lb) / 2.0:
                r = 2 * (ub - lb + al + au)  
                s = lb - 2 * al - (ub - lb) / 2.0  
                y[i] -= r * ((y[i] - s) // r)  
            if y[i] > ub + au:
                y[i] -= 2 * (y[i] - ub - au)
            if y[i] < lb - al:
                y[i] += 2 * (lb - al - y[i])
        return y
    shift_or_mirror_into_invertible_domain.__doc__ = BoxConstraintsTransformationBase.shift_or_mirror_into_invertible_domain.__doc__ + shift_or_mirror_into_invertible_domain.__doc__

    def _shift_or_mirror_into_invertible_i(self, x, i):
        """shift into the invertible domain [lb - ab, ub + au], mirror close to
        boundaries in order to get a smooth transformation everywhere

        """
        assert x is not None
        lb = self._lb[self._index(i)]
        ub = self._ub[self._index(i)]
        al = self._al[self._index(i)]
        au = self._au[self._index(i)]
        
        if x < lb - 2 * al - (ub - lb) / 2.0 or x > ub + 2 * au + (ub - lb) / 2.0:
            r = 2 * (ub - lb + al + au)  
            s = lb - 2 * al - (ub - lb) / 2.0  
            x -= r * ((x - s) // r)  
        if x > ub + au:
            x -= 2 * (x - ub - au)
        if x < lb - al:
            x += 2 * (lb - al - x)
        return x
    def _transform_i(self, x, i):
        """return transform of x in component i"""
        x = self._shift_or_mirror_into_invertible_i(x, i)
        lb = self._lb[self._index(i)]
        ub = self._ub[self._index(i)]
        al = self._al[self._index(i)]
        au = self._au[self._index(i)]
        if x < lb + al:
            return lb + (x - (lb - al))**2 / 4 / al
        elif x < ub - au:
            return x
        elif x < ub + 3 * au:
            return ub - (x - (ub + au))**2 / 4 / au
        else:
            assert False  
            return ub + au - (x - (ub + au))
    def _inverse_i(self, y, i):
        """return inverse of y in component i"""
        lb = self._lb[self._index(i)]
        ub = self._ub[self._index(i)]
        al = self._al[self._index(i)]
        au = self._au[self._index(i)]
        if 1 < 3:
            if not lb <= y <= ub:
                raise ValueError('argument of inverse must be within the given bounds')
        if y < lb + al:
            return (lb - al) + 2 * (al * (y - lb))**0.5
        elif y < ub - au:
            return y
        else:
            return (ub + au) - 2 * (au * (ub - y))**0.5

class GenoPheno(object):
    """Genotype-phenotype transformation.

    Method `pheno` provides the transformation from geno- to phenotype,
    that is from the internal representation to the representation used
    in the objective function. Method `geno` provides the "inverse" pheno-
    to genotype transformation. The geno-phenotype transformation comprises,
    in this order:

       - insert fixed variables (with the phenotypic and therefore quite
         possibly "wrong" values)
       - affine linear transformation (first scaling then shift)
       - user-defined transformation
       - repair (e.g. into feasible domain due to boundaries)
       - assign fixed variables their original phenotypic value

    By default all transformations are the identity. The repair is only applied,
    if the transformation is given as argument to the method `pheno`.

    ``geno`` is only necessary, if solutions have been injected.

    """
    def __init__(self, dim, scaling=None, typical_x=None,
                 fixed_values=None, tf=None):
        """return `GenoPheno` instance with phenotypic dimension `dim`.

        Keyword Arguments
        -----------------
            `scaling`
                the diagonal of a scaling transformation matrix, multipliers
                in the genotyp-phenotyp transformation, see `typical_x`
            `typical_x`
                ``pheno = scaling*geno + typical_x``
            `fixed_values`
                a dictionary of variable indices and values, like ``{0:2.0, 2:1.1}``,
                that are not subject to change, negative indices are ignored
                (they act like incommenting the index), values are phenotypic
                values.
            `tf`
                list of two user-defined transformation functions, or `None`.

                ``tf[0]`` is a function that transforms the internal representation
                as used by the optimizer into a solution as used by the
                objective function. ``tf[1]`` does the back-transformation.
                For example::

                    tf_0 = lambda x: [xi**2 for xi in x]
                    tf_1 = lambda x: [abs(xi)**0.5 fox xi in x]

                or "equivalently" without the `lambda` construct::

                    def tf_0(x):
                        return [xi**2 for xi in x]
                    def tf_1(x):
                        return [abs(xi)**0.5 fox xi in x]

                ``tf=[tf_0, tf_1]`` is a reasonable way to guaranty that only positive
                values are used in the objective function.

        Details
        -------
        If ``tf_0`` is not the identity and ``tf_1`` is ommitted,
        the genotype of ``x0`` cannot be computed consistently and
        "injection" of phenotypic solutions is likely to lead to
        unexpected results.

        """
        self.N = dim
        self.fixed_values = fixed_values
        if tf is not None:
            self.tf_pheno = tf[0]
            self.tf_geno = tf[1]  
            
            
            
            
            _print_warning("in class GenoPheno: user defined transformations have not been tested thoroughly")
        else:
            self.tf_geno = None
            self.tf_pheno = None

        if fixed_values:
            if not isinstance(fixed_values, dict):
                raise _Error("fixed_values must be a dictionary {index:value,...}")
            if max(fixed_values.keys()) >= dim:
                raise _Error("max(fixed_values.keys()) = " + str(max(fixed_values.keys())) +
                    " >= dim=N=" + str(dim) + " is not a feasible index")
            
            for k in list(fixed_values.keys()):
                if k < 0:
                    fixed_values.pop(k)

        def vec_is_default(vec, default_val=0):
            """return True if `vec` has the value `default_val`,
            None or [None] are also recognized as default

            """
            
            
            try:
                if len(vec) == 1:
                    vec = vec[0]  
            except TypeError:
                pass  

            if vec is None or all(vec == default_val):
                return True

            if all([val is None or val == default_val for val in vec]):
                    return True

            return False

        self.scales = array(scaling) if scaling is not None else None
        if vec_is_default(self.scales, 1):
            self.scales = 1  
        elif self.scales.shape is not () and len(self.scales) != self.N:
            raise _Error('len(scales) == ' + str(len(self.scales)) +
                         ' does not match dimension N == ' + str(self.N))

        self.typical_x = array(typical_x) if typical_x is not None else None
        if vec_is_default(self.typical_x, 0):
            self.typical_x = 0
        elif self.typical_x.shape is not () and len(self.typical_x) != self.N:
            raise _Error('len(typical_x) == ' + str(len(self.typical_x)) +
                         ' does not match dimension N == ' + str(self.N))

        if (self.scales is 1 and
                self.typical_x is 0 and
                self.fixed_values is None and
                self.tf_pheno is None):
            self.isidentity = True
        else:
            self.isidentity = False
        if self.tf_pheno is None:
            self.islinear = True
        else:
            self.islinear = False

    def pheno(self, x, into_bounds=None, copy=True, copy_always=False,
              archive=None, iteration=None):
        """maps the genotypic input argument into the phenotypic space,
        see help for class `GenoPheno`

        Details
        -------
        If ``copy``, values from ``x`` are copied if changed under the transformation.

        """
        
        input_type = type(x)
        if into_bounds is None:
            into_bounds = (lambda x, copy=False:
                                x if not copy else array(x, copy=copy))
        if copy_always and not copy:
            raise ValueError('arguments copy_always=' + str(copy_always) +
                             ' and copy=' + str(copy) + ' have inconsistent values')
        if copy_always:
            x = array(x, copy=True)
            copy = False

        if self.isidentity:
            y = into_bounds(x) 
        else:
            if self.fixed_values is None:
                y = array(x, copy=copy)  
            else:  
                y = list(x)  
                for i in sorted(self.fixed_values.keys()):
                    y.insert(i, self.fixed_values[i])
                y = array(y, copy=False)
            copy = False

            if self.scales is not 1:  
                y *= self.scales

            if self.typical_x is not 0:
                y += self.typical_x

            if self.tf_pheno is not None:
                y = array(self.tf_pheno(y), copy=False)

            y = into_bounds(y, copy)  

            if self.fixed_values is not None:
                for i, k in list(self.fixed_values.items()):
                    y[i] = k

        if input_type is np.ndarray:
            y = array(y, copy=False)
        if archive is not None:
            archive.insert(y, geno=x, iteration=iteration)
        return y

    def geno(self, y, from_bounds=None,
             copy_if_changed=True, copy_always=False,
             repair=None, archive=None):
        """maps the phenotypic input argument into the genotypic space,
        that is, computes essentially the inverse of ``pheno``.

        By default a copy is made only to prevent to modify ``y``.

        The inverse of the user-defined transformation (if any)
        is only needed if external solutions are injected, it is not
        applied to the initial solution x0.

        Details
        =======
        ``geno`` searches first in ``archive`` for the genotype of
        ``y`` and returns the found value, typically unrepaired.
        Otherwise, first ``from_bounds`` is applied, to revert a
        projection into the bound domain (if necessary) and ``pheno``
        is reverted. ``repair`` is applied last, and is usually the
        method ``CMAEvolutionStrategy.repair_genotype`` that limits the
        Mahalanobis norm of ``geno(y) - mean``.

        """
        if from_bounds is None:
            from_bounds = lambda x, copy=False: x  

        if archive is not None:
            try:
                x = archive[y]['geno']
            except (KeyError, TypeError):
                x = None
            if x is not None:
                if archive[y]['iteration'] < archive.last_iteration \
                        and repair is not None:
                    x = repair(x, copy_if_changed=copy_always)
                return x

        input_type = type(y)
        x = y
        if copy_always:
            x = array(y, copy=True)
            copy = False
        else:
            copy = copy_if_changed

        x = from_bounds(x, copy)

        if self.isidentity:
            if repair is not None:
                x = repair(x, copy)
            return x

        if copy:  
            x = array(x, copy=True)
            copy = False

        
        if self.tf_geno is not None:
            x = array(self.tf_geno(x), copy=False)
        elif self.tf_pheno is not None:
            raise ValueError('t1 of options transformation was not defined but is needed as being the inverse of t0')

        
        if self.typical_x is not 0:
            x -= self.typical_x
        if self.scales is not 1:  
            x /= self.scales

        
        if self.fixed_values is not None:
            
            
            if 1 < 3:
                keys = sorted(self.fixed_values.keys())
                x = array([x[i] for i in range(len(x)) if i not in keys],
                          copy=False)
        
        if repair is not None:
            x = repair(x, copy)
        if input_type is np.ndarray:
            x = array(x, copy=False)
        return x






class OOOptimizer(object):
    """"abstract" base class for an Object Oriented Optimizer interface.

     Relevant methods are `__init__`, `ask`, `tell`, `stop`, `result`,
     and `optimize`. Only `optimize` is fully implemented in this base
     class.

    Examples
    --------
    All examples minimize the function `elli`, the output is not shown.
    (A preferred environment to execute all examples is ``ipython`` in
    ``%pylab`` mode.)

    First we need::

        from cma import CMAEvolutionStrategy
        
        felli = lambda x: sum(1e3**((i-1.)/(len(x)-1.)*x[i])**2 for i in range(len(x)))

    The shortest example uses the inherited method
    `OOOptimizer.optimize()`::

        es = CMAEvolutionStrategy(8 * [0.1], 0.5).optimize(felli)

    The input parameters to `CMAEvolutionStrategy` are specific to this
    inherited class. The remaining functionality is based on interface
    defined by `OOOptimizer`. We might have a look at the result::

        print(es.result()[0])  
        print(es.result()[1])  

    In order to display more exciting output we do::

        es.logger.plot()  

    Virtually the same example can be written with an explicit loop
    instead of using `optimize()`. This gives the necessary insight into
    the `OOOptimizer` class interface and entire control over the
    iteration loop::

        optim = CMAEvolutionStrategy(9 * [0.5], 0.3)
        

        
        while not optim.stop():  
            X = optim.ask()      
            f = [felli(x) for x in X]  
            
            optim.tell(X, f)     "update" work
            optim.disp(20)       
            optim.logger.add()   "data line"

        
        print('termination by', optim.stop())
        print('best f-value =', optim.result()[1])
        print('best solution =', optim.result()[0])
        optim.logger.plot()  

    Details
    -------
    Most of the work is done in the method `tell(...)`. The method
    `result()` returns more useful output.

    """
    def __init__(self, xstart, **more_args):
        """``xstart`` is a mandatory argument"""
        self.xstart = xstart
        self.more_args = more_args
        self.initialize()
    def initialize(self):
        """(re-)set to the initial state"""
        self.countiter = 0
        self.xcurrent = self.xstart[:]
        raise NotImplementedError('method initialize() must be implemented in derived class')
    def ask(self, gradf=None, **more_args):
        """abstract method, AKA "get" or "sample_distribution", deliver
        new candidate solution(s), a list of "vectors"

        """
        raise NotImplementedError('method ask() must be implemented in derived class')
    def tell(self, solutions, function_values):
        """abstract method, AKA "update", pass f-values and prepare for
        next iteration

        """
        self.countiter += 1
        raise NotImplementedError('method tell() must be implemented in derived class')
    def stop(self):
        """abstract method, return satisfied termination conditions in
        a dictionary like ``{'termination reason': value, ...}``,
        for example ``{'tolfun': 1e-12}``, or the empty dictionary ``{}``.
        The implementation of `stop()` should prevent an infinite
        loop.

        """
        raise NotImplementedError('method stop() is not implemented')
    def disp(self, modulo=None):
        """abstract method, display some iteration infos if
        ``self.iteration_counter % modulo == 0``

        """
        pass  
    def result(self):
        """abstract method, return ``(x, f(x), ...)``, that is, the
        minimizer, its function value, ...

        """
        raise NotImplementedError('method result() is not implemented')

    
    
    
    
    
    def optimize(self, objective_fct, iterations=None, min_iterations=1,
                 args=(), verb_disp=None, logger=None, call_back=None):
        """find minimizer of `objective_fct`.

        CAVEAT: the return value for `optimize` has changed to ``self``.

        Arguments
        ---------

            `objective_fct`
                function be to minimized
            `iterations`
                number of (maximal) iterations, while ``not self.stop()``
            `min_iterations`
                minimal number of iterations, even if ``not self.stop()``
            `args`
                arguments passed to `objective_fct`
            `verb_disp`
                print to screen every `verb_disp` iteration, if ``None``
                the value from ``self.logger`` is "inherited", if
                available.
            ``logger``
                a `BaseDataLogger` instance, which must be compatible
                with the type of ``self``.
            ``call_back``
                call back function called like ``call_back(self)`` or
                a list of call back functions.

        ``return self``, that is, the `OOOptimizer` instance.

        Example
        -------
        >>> import cma
        >>> es = cma.CMAEvolutionStrategy(7 * [0.1], 0.5
        ...              ).optimize(cma.fcts.rosen, verb_disp=100)
        (4_w,9)-CMA-ES (mu_w=2.8,w_1=49%) in dimension 7 (seed=630721393)
        Iterat 
            1       9 3.163954777181882e+01 1.0e+00 4.12e-01  4e-01  4e-01 0:0.0
            2      18 3.299006223906629e+01 1.0e+00 3.60e-01  3e-01  4e-01 0:0.0
            3      27 1.389129389866704e+01 1.1e+00 3.18e-01  3e-01  3e-01 0:0.0
          100     900 2.494847340045985e+00 8.6e+00 5.03e-02  2e-02  5e-02 0:0.3
          200    1800 3.428234862999135e-01 1.7e+01 3.77e-02  6e-03  3e-02 0:0.5
          300    2700 3.216640032470860e-04 5.6e+01 6.62e-03  4e-04  9e-03 0:0.8
          400    3600 6.155215286199821e-12 6.6e+01 7.44e-06  1e-07  4e-06 0:1.1
          438    3942 1.187372505161762e-14 6.0e+01 3.27e-07  4e-09  9e-08 0:1.2
          438    3942 1.187372505161762e-14 6.0e+01 3.27e-07  4e-09  9e-08 0:1.2
        ('termination by', {'tolfun': 1e-11})
        ('best f-value =', 1.1189867885201275e-14)
        ('solution =', array([ 1.        ,  1.        ,  1.        ,  0.99999999,  0.99999998,
                0.99999996,  0.99999992]))
        >>> print(es.result()[0])
        array([ 1.          1.          1.          0.99999999  0.99999998  0.99999996
          0.99999992])

        """
        assert iterations is None or min_iterations <= iterations
        if not hasattr(self, 'logger'):
            self.logger = logger
        logger = self.logger = logger or self.logger
        if not isinstance(call_back, list):
            call_back = [call_back]

        citer = 0
        while not self.stop() or citer < min_iterations:
            if iterations is not None and citer >= iterations:
                return self.result()
            citer += 1

            X = self.ask()  
            fitvals = [objective_fct(x, *args) for x in X]
            self.tell(X, fitvals)  
            self.disp(verb_disp)
            for f in call_back:
                f is None or f(self)
            logger.add(self) if logger else None

        
        
        
        try:
            logger.add(self, modulo=bool(logger.modulo)) if logger else None
        except TypeError:
            print('  suppressing the final call of the logger in ' +
                  'OOOptimizer.optimize (modulo keyword parameter not ' +
                  'available)')
        except AttributeError:
            print('  suppressing the final call of the logger in ' +
                  'OOOptimizer.optimize (modulo attribute not ' +
                  'available)')
        if verb_disp:
            self.disp(1)
        if verb_disp in (1, True):
            print('termination by', self.stop())
            print('best f-value =', self.result()[1])
            print('solution =', self.result()[0])

        return self
        

_experimental = False

class CMAAdaptSigmaBase(object):
    """step-size adaptation base class, implementing hsig functionality
    via an isotropic evolution path.

    """
    def __init__(self, *args, **kwargs):
        self.is_initialized_base = False
        self._ps_updated_iteration = -1
    def initialize_base(self, es):
        """set parameters and state variable based on dimension,
        mueff and possibly further options.

        """
        
        b = 1.0
        
        self.cs = 1.0 * (es.sp.mueff + 2)**b / (es.N**b + (es.sp.mueff + 3)**b)
        self.ps = np.zeros(es.N)
        self.is_initialized_base = True
        return self
    def _update_ps(self, es):
        """update the isotropic evolution path

        :type es: CMAEvolutionStrategy
        """
        if not self.is_initialized_base:
            self.initialize_base(es)
        if self._ps_updated_iteration == es.countiter:
            return
        if es.countiter <= es.itereigenupdated:
            
            assert es.countiter >= es.itereigenupdated
            _print_warning('distribution transformation (B and D) have been updated before ps could be computed',
                          '_update_ps', 'CMAAdaptSigmaBase')
        z = dot(es.B, (1. / es.D) * dot(es.B.T, (es.mean - es.mean_old) / es.sigma_vec))
        z *= es.sp.mueff**0.5 / es.sigma / es.sp.cmean
        self.ps = (1 - self.cs) * self.ps + sqrt(self.cs * (2 - self.cs)) * z
        self._ps_updated_iteration = es.countiter
    def hsig(self, es):
        """return "OK-signal" for rank-one update, `True` (OK) or `False`
        (stall rank-one update), based on the length of an evolution path

        """
        self._update_ps(es)
        if self.ps is None:
            return True
        squared_sum = sum(self.ps**2) / (1 - (1 - self.cs)**(2 * es.countiter))
        
        
        return squared_sum / es.N - 1 < 1 + 4. / (es.N + 1)
    def update(self, es, **kwargs):
        """update ``es.sigma``"""
        self._update_ps(es)
        raise NotImplementedError('must be implemented in a derived class')


class CMAAdaptSigmaNone(CMAAdaptSigmaBase):
    def update(self, es, **kwargs):
        """no update, ``es.sigma`` remains constant.

        :param es: ``CMAEvolutionStrategy`` class instance
        :param kwargs: whatever else is needed to update ``es.sigma``

        """
        pass


class CMAAdaptSigmaDistanceProportional(CMAAdaptSigmaBase):
    """artificial setting of ``sigma`` for test purposes, e.g.
    to simulate optimal progress rates.

    """
    def __init__(self, coefficient=1.2):
        super(CMAAdaptSigmaDistanceProportional, self).__init__() 
        self.coefficient = coefficient
        self.is_initialized = True
    def update(self, es, **kwargs):
        
        es.sigma = self.coefficient * es.sp.mueff * sum(es.mean**2)**0.5 / es.N / es.sp.cmean


class CMAAdaptSigmaCSA(CMAAdaptSigmaBase):
    def __init__(self):
        """postpone initialization to a method call where dimension and mueff should be known.

        """
        self.is_initialized = False
    def initialize(self, es):
        """set parameters and state variable based on dimension,
        mueff and possibly further options.

        """
        self.disregard_length_setting = True if es.opts['CSA_disregard_length'] else False
        if es.opts['CSA_clip_length_value'] is not None:
            try:
                if len(es.opts['CSA_clip_length_value']) == 0:
                    es.opts['CSA_clip_length_value'] = [-np.Inf, np.Inf]
                elif len(es.opts['CSA_clip_length_value']) == 1:
                    es.opts['CSA_clip_length_value'] = [-np.Inf, es.opts['CSA_clip_length_value'][0]]
                elif len(es.opts['CSA_clip_length_value']) == 2:
                    es.opts['CSA_clip_length_value'] = np.sort(es.opts['CSA_clip_length_value'])
                else:
                    raise ValueError('option CSA_clip_length_value should be a number of len(.) in [1,2]')
            except TypeError:  
                es.opts['CSA_clip_length_value'] = [-np.Inf, es.opts['CSA_clip_length_value']]
            es.opts['CSA_clip_length_value'] = list(np.sort(es.opts['CSA_clip_length_value']))
            if es.opts['CSA_clip_length_value'][0] > 0 or es.opts['CSA_clip_length_value'][1] < 0:
                raise ValueError('option CSA_clip_length_value must be a single positive or a negative and a positive number')
        
        b = 1.0
        
        self.cs = 1.0 * (es.sp.mueff + 2)**b / (es.N + (es.sp.mueff + 3)**b)
        self.damps = es.opts['CSA_dampfac'] * (0.5 +
                                          0.5 * min([1, (es.sp.lam_mirr / (0.159 * es.sp.popsize) - 1)**2])**1 +
                                          2 * max([0, ((es.sp.mueff - 1) / (es.N + 1))**es.opts['CSA_damp_mueff_exponent'] - 1]) +
                                          self.cs
                                          )
        self.max_delta_log_sigma = 1  

        if self.disregard_length_setting:
            es.opts['CSA_clip_length_value'] = [0, 0]
            
            b = 1.0 * 0.5
            
            self.cs = 1.0 * (es.sp.mueff + 1)**b / (es.N**b + 2 * es.sp.mueff**b)
            self.damps = es.opts['CSA_dampfac'] * 1  
        if es.opts['verbose'] > 1 or self.disregard_length_setting or 11 < 3:
            print('SigmaCSA Parameters')
            for k, v in list(self.__dict__.items()):
                print('  ', k, ':', v)
        self.ps = np.zeros(es.N)
        self._ps_updated_iteration = -1
        self.is_initialized = True

    def _update_ps(self, es):
        if not self.is_initialized:
            self.initialize(es)
        if self._ps_updated_iteration == es.countiter:
            return
        z = dot(es.B, (1. / es.D) * dot(es.B.T, (es.mean - es.mean_old) / es.sigma_vec))
        z *= es.sp.mueff**0.5 / es.sigma / es.sp.cmean
        
        if es.opts['CSA_clip_length_value'] is not None:
            vals = es.opts['CSA_clip_length_value']
            min_len = es.N**0.5 + vals[0] * es.N / (es.N + 2)
            max_len = es.N**0.5 + vals[1] * es.N / (es.N + 2)
            act_len = sum(z**2)**0.5
            new_len = Mh.minmax(act_len, min_len, max_len)
            if new_len != act_len:
                z *= new_len / act_len
                
                
        self.ps = (1 - self.cs) * self.ps + sqrt(self.cs * (2 - self.cs)) * z
        self._ps_updated_iteration = es.countiter
    def update(self, es, **kwargs):
        self._update_ps(es)  
        if es.opts['CSA_squared']:
            s = (sum(self.ps**2) / es.N - 1) / 2
            
            
        else:
            s = sum(self.ps**2)**0.5 / es.const.chiN - 1
            if es.opts['vv'] == 'pc for ps':
                s = sum((es.D**-1 * dot(es.B.T, es.pc))**2)**0.5 / es.const.chiN - 1
                s = (sum((es.D**-1 * dot(es.B.T, es.pc))**2) / es.N - 1) / 2
        s *= self.cs / self.damps
        s_clipped = Mh.minmax(s, -self.max_delta_log_sigma, self.max_delta_log_sigma)
        es.sigma *= np.exp(s_clipped)
        "error" handling
        if s_clipped != s:
            _print_warning('sigma change exp(' + str(s) + ') = ' + str(np.exp(s)) +
                          ' clipped to exp(+-' + str(self.max_delta_log_sigma) + ')',
                          'update',
                          'CMAAdaptSigmaCSA',
                          es.countiter, es.opts['verbose'])
class CMAAdaptSigmaMedianImprovement(CMAAdaptSigmaBase):
    """Compares median fitness against a fitness percentile of the previous iteration,
    see Ait ElHara et al, GECCO 2013.

    """
    def __init__(self):
        
        super(CMAAdaptSigmaMedianImprovement, self).__init__() 
    def initialize(self, es):
        r = es.sp.mueff / es.popsize
        self.index_to_compare = 0.5 * (r**0.5 + 2.0 * (1 - r**0.5) / log(es.N + 9)**2) * (es.popsize)  
        self.index_to_compare = (0.30 if not es.opts['vv']
                                 else es.opts['vv']) * es.popsize  
        self.damp = 2 - 2 / es.N  
        self.c = 0.3  
        self.s = 0  
    def update(self, es, **kwargs):
        if es.countiter < 2:
            self.initialize(es)
            self.fit = es.fit.fit
        else:
            ft1, ft2 = self.fit[int(self.index_to_compare)], self.fit[int(np.ceil(self.index_to_compare))]
            ftt1, ftt2 = es.fit.fit[(es.popsize - 1) // 2], es.fit.fit[int(np.ceil((es.popsize - 1) / 2))]
            pt2 = self.index_to_compare - int(self.index_to_compare)
            
            s = 0
            if 1 < 3:
                s += pt2 * sum(es.fit.fit <= self.fit[int(np.ceil(self.index_to_compare))])
                s += (1 - pt2) * sum(es.fit.fit < self.fit[int(self.index_to_compare)])
                s -= es.popsize / 2.
                s *= 2. / es.popsize  
            self.s = (1 - self.c) * self.s + self.c * s
            es.sigma *= exp(self.s / self.damp)
        

        
        
        
        self.fit = es.fit.fit
class CMAAdaptSigmaTPA(CMAAdaptSigmaBase):
    """two point adaptation for step-size sigma. Relies on a specific
    sampling of the first two offspring, whose objective function
    value ranks are used to decide on the step-size change.

    Example
    =======

    >>> import cma
    >>> cma.CMAOptions('adapt').pprint()
    >>> es = cma.CMAEvolutionStrategy(10 * [0.2], 0.1, {'AdaptSigma': cma.CMAAdaptSigmaTPA, 'ftarget': 1e-8})
    >>> es.optimize(cma.fcts.rosen)
    >>> assert 'ftarget' in es.stop()
    >>> assert es.result()[1] <= 1e-8
    >>> assert es.result()[2] < 6500  

    References: loosely based on Hansen 2008, CMA-ES with Two-Point
    Step-Size Adaptation, more tightly based on an upcoming paper by
    Hansen et al.

    """
    def __init__(self, dimension=None, opts=None):
        super(CMAAdaptSigmaTPA, self).__init__() 
        
        self.initialized = False
        self.dimension = dimension
        self.opts = opts
    def initialize(self, N=None, opts=None):
        if N is None:
            N = self.dimension
        if opts is None:
            opts = self.opts
        try:
            damp_fac = opts['CSA_dampfac']  
        except (TypeError, KeyError):
            damp_fac = 1

        self.sp = _BlancClass()  
        try:
            self.sp.damp = damp_fac * eval('N')**0.5  
            
        except:
            self.sp.damp = 4  
            _print_warning("dimension not known, damping set to 4",
                'initialize', 'CMAAdaptSigmaTPA')
        try:
            if opts['vv'][0] == 'TPA_damp':
                self.sp.damp = opts['vv'][1]
                print('damp set to %d' % self.sp.damp)
        except (TypeError):
            pass

        self.sp.dampup = 0.5**0.0 * 1.0 * self.sp.damp  
        self.sp.dampdown = 2.0**0.0 * self.sp.damp
        if self.sp.dampup != self.sp.dampdown:
            print('TPA damping is asymmetric')
        self.sp.c = 0.3  
        self.sp.z_exponent = 0.5  
        self.sp.sigma_fac = 1.0  
        self.sp.relative_to_delta_mean = True  
        self.s = 0  
        self.last = None
        self.initialized = True
        return self
    def update(self, es, function_values, **kwargs):
        """the first and second value in ``function_values``
        must reflect two mirrored solutions sampled
        in direction / in opposite direction of
        the previous mean shift, respectively.

        """
        
        
        
        
        
        if not self.initialized:
            self.initialize(es.N, es.opts)
        if 1 < 3:
            
            
            z = np.where(es.fit.idx == 1)[0][0] - np.where(es.fit.idx == 0)[0][0]
            z /= es.popsize - 1  
        self.s = (1 - self.sp.c) * self.s + self.sp.c * np.sign(z) * np.abs(z)**self.sp.z_exponent
        if self.s > 0:
            es.sigma *= exp(self.s / self.sp.dampup)
        else:
            es.sigma *= exp(self.s / self.sp.dampdown)
        

new_injections = True




class CMAEvolutionStrategy(OOOptimizer):
    """CMA-ES stochastic optimizer class with ask-and-tell interface.

    Calling Sequences
    =================

        es = CMAEvolutionStrategy(x0, sigma0)

        es = CMAEvolutionStrategy(x0, sigma0, opts)

        es = CMAEvolutionStrategy(x0, sigma0).optimize(objective_fct)

        res = CMAEvolutionStrategy(x0, sigma0,
                                opts).optimize(objective_fct).result()

    Arguments
    =========
        `x0`
            initial solution, starting point. `x0` is given as "phenotype"
            which means, if::

                opts = {'transformation': [transform, inverse]}

            is given and ``inverse is None``, the initial mean is not
            consistent with `x0` in that ``transform(mean)`` does not
            equal to `x0` unless ``transform(mean)`` equals ``mean``.
        `sigma0`
            initial standard deviation.  The problem variables should
            have been scaled, such that a single standard deviation
            on all variables is useful and the optimum is expected to
            lie within about `x0` +- ``3*sigma0``. See also options
            `scaling_of_variables`. Often one wants to check for
            solutions close to the initial point. This allows,
            for example, for an easier check of consistency of the
            objective function and its interfacing with the optimizer.
            In this case, a much smaller `sigma0` is advisable.
        `opts`
            options, a dictionary with optional settings,
            see class `CMAOptions`.

    Main interface / usage
    ======================
    The interface is inherited from the generic `OOOptimizer`
    class (see also there). An object instance is generated from

        es = cma.CMAEvolutionStrategy(8 * [0.5], 0.2)

    The least verbose interface is via the optimize method::

        es.optimize(objective_func)
        res = es.result()

    More verbosely, the optimization is done using the
    methods ``stop``, ``ask``, and ``tell``::

        while not es.stop():
            solutions = es.ask()
            es.tell(solutions, [cma.fcts.rosen(s) for s in solutions])
            es.disp()
        es.result_pretty()


    where ``ask`` delivers new candidate solutions and ``tell`` updates
    the ``optim`` instance by passing the respective function values
    (the objective function ``cma.fcts.rosen`` can be replaced by any
    properly defined objective function, see ``cma.fcts`` for more
    examples).

    To change an option, for example a termination condition to
    continue the optimization, call

        es.opts.set({'tolfacupx': 1e4})

    The class `CMAEvolutionStrategy` also provides::

        (solutions, func_values) = es.ask_and_eval(objective_func)

    and an entire optimization can also be written like::

        while not es.stop():
            es.tell(*es.ask_and_eval(objective_func))

    Besides for termination criteria, in CMA-ES only the ranks of the
    `func_values` are relevant.

    Attributes and Properties
    =========================
        - `inputargs` -- passed input arguments
        - `inopts` -- passed options
        - `opts` -- actually used options, some of them can be changed any
          time via ``opts.set``, see class `CMAOptions`
        - `popsize` -- population size lambda, number of candidate
           solutions returned by `ask()`
        - `logger` -- a `CMADataLogger` instance utilized by `optimize`

    Examples
    ========
    Super-short example, with output shown:

    >>> import cma
    >>> 
    >>> es = cma.CMAEvolutionStrategy(4 * [1], 1, {'seed':234})
    (4_w,8)-CMA-ES (mu_w=2.6,w_1=52%) in dimension 4 (seed=234)
    >>>
    >>> 
    >>> es.optimize(cma.fcts.elli, verb_disp=1)
    Iterat 
        1       8 2.093015112685775e+04 1.0e+00 9.27e-01  9e-01  9e-01 0:0.0
        2      16 4.964814235917688e+04 1.1e+00 9.54e-01  9e-01  1e+00 0:0.0
        3      24 2.876682459926845e+05 1.2e+00 1.02e+00  9e-01  1e+00 0:0.0
      100     800 6.809045875281943e-01 1.3e+02 1.41e-02  1e-04  1e-02 0:0.2
      200    1600 2.473662150861846e-10 8.0e+02 3.08e-05  1e-08  8e-06 0:0.5
      233    1864 2.766344961865341e-14 8.6e+02 7.99e-07  8e-11  7e-08 0:0.6
    >>>
    >>> cma.pprint(es.result())
    (array([ -1.98546755e-09,  -1.10214235e-09,   6.43822409e-11,
            -1.68621326e-11]),
     4.5119610261406537e-16,
     1666,
     1672,
     209,
     array([ -9.13545269e-09,  -1.45520541e-09,  -6.47755631e-11,
            -1.00643523e-11]),
     array([  3.20258681e-08,   3.15614974e-09,   2.75282215e-10,
             3.27482983e-11]))
    >>> assert es.result()[1] < 1e-9
    >>> help(es.result)
    Help on method result in module cma:

    result(self) method of cma.CMAEvolutionStrategy instance
        return ``(xbest, f(xbest), evaluations_xbest, evaluations, iterations, pheno(xmean), effective_stds)``


    The optimization loop can also be written explicitly.

    >>> import cma
    >>> es = cma.CMAEvolutionStrategy(4 * [1], 1)
    >>> while not es.stop():
    ...    X = es.ask()
    ...    es.tell(X, [cma.fcts.elli(x) for x in X])
    ...    es.disp()
    <output omitted>

    achieving the same result as above.

    An example with lower bounds (at zero) and handling infeasible
    solutions:

    >>> import cma
    >>> import numpy as np
    >>> es = cma.CMAEvolutionStrategy(10 * [0.2], 0.5, {'bounds': [0, np.inf]})
    >>> while not es.stop():
    ...     fit, X = [], []
    ...     while len(X) < es.popsize:
    ...         curr_fit = None
    ...         while curr_fit in (None, np.NaN):
    ...             x = es.ask(1)[0]
    ...             curr_fit = cma.fcts.somenan(x, cma.fcts.elli) 
    ...         X.append(x)
    ...         fit.append(curr_fit)
    ...     es.tell(X, fit)
    ...     es.logger.add()
    ...     es.disp()
    <output omitted>
    >>>
    >>> assert es.result()[1] < 1e-9
    >>> assert es.result()[2] < 9000  
    >>> 
    >>> 

    An example with user-defined transformation, in this case to realize
    a lower bound of 2.

    >>> es = cma.CMAEvolutionStrategy(5 * [3], 1,
    ...                 {"transformation": [lambda x: x**2+2, None]})
    >>> es.optimize(cma.fcts.rosen)
    <output omitted>
    >>> assert cma.fcts.rosen(es.result()[0]) < 1e-6 + 5.530760944396627e+02
    >>> assert es.result()[2] < 3300

    The inverse transformation is (only) necessary if the `BoundPenalty`
    boundary handler is used at the same time.

    The ``CMAEvolutionStrategy`` class also provides a default logger
    (cave: files are overwritten when the logger is used with the same
    filename prefix):

    >>> import cma
    >>> es = cma.CMAEvolutionStrategy(4 * [0.2], 0.5, {'verb_disp': 0})
    >>> es.logger.disp_header()  
    Iterat Nfevals  function value    axis ratio maxstd   minstd
    >>> while not es.stop():
    ...     X = es.ask()
    ...     es.tell(X, [cma.fcts.sphere(x) for x in X])
    ...     es.logger.add()  
    ...     es.logger.disp([-1])  
    1      8 2.72769793021748e+03 1.0e+00 4.05e-01 3.99e-01
    2     16 6.58755537926063e+03 1.1e+00 4.00e-01 3.39e-01
    <output ommitted>
    193   1544 3.15195320957214e-15 1.2e+03 3.70e-08 3.45e-11
    >>> es.logger.disp_header()
    Iterat Nfevals  function value    axis ratio maxstd   minstd
    >>> 

    Example implementing restarts with increasing popsize (IPOP), output
    is not displayed:

    >>> import cma, numpy as np
    >>>
    >>> 
    >>> bestever = cma.BestSolution()
    >>> for lam in 10 * 2**np.arange(8):  
    ...     es = cma.CMAEvolutionStrategy('6 - 8 * np.random.rand(9)',  
    ...                                   5,  
    ...                                   {'popsize': lam,  
    ...                                    'verb_append': bestever.evalsall})
    ...     logger = cma.CMADataLogger().register(es, append=bestever.evalsall)
    ...     while not es.stop():
    ...         X = es.ask()    
    ...         fit = [cma.fcts.rastrigin(x) for x in X]  
    ...         es.tell(X, fit) 
    ...
    ...         
    ...         logger.add()  "data point" to the log, writing in files
    ...         es.disp()  
    ...
    ...     print('termination:', es.stop())
    ...     cma.pprint(es.best.__dict__)
    ...
    ...     bestever.update(es.best)
    ...
    ...     
    ...     
    ...     if bestever.f < 1e-8:  
    ...         break
    <output omitted>
    >>> assert es.result()[1] < 1e-8

    On the Rastrigin function, usually after five restarts the global
    optimum is located.

    Using the ``multiprocessing`` module, we can evaluate the function in
    parallel with a simple modification of the example (however
    multiprocessing seems not always reliable)::

        try:
            import multiprocessing as mp
            import cma
            es = cma.CMAEvolutionStrategy(22 * [0.0], 1.0, {'maxiter':10})
            pool = mp.Pool(es.popsize)
            while not es.stop():
                X = es.ask()
                f_values = pool.map_async(cma.felli, X).get()
                
                es.tell(X, f_values)
                es.disp()
                es.logger.add()
        except ImportError:
            pass

    The final example shows how to resume:

    >>> import cma, pickle
    >>>
    >>> es = cma.CMAEvolutionStrategy(12 * [0.1],  
    ...                               0.5)         
    >>> es.optimize(cma.fcts.rosen, iterations=100)
    >>> pickle.dump(es, open('saved-cma-object.pkl', 'wb'))
    >>> print('saved')
    >>> del es  
    >>>
    >>> es = pickle.load(open('saved-cma-object.pkl', 'rb'))
    >>> print('resumed')
    >>> es.optimize(cma.fcts.rosen, verb_disp=200)
    >>> assert es.result()[2] < 15000
    >>> cma.pprint(es.result())

    Details
    =======
    The following two enhancements are implemented, the latter is turned
    on by default only for very small population size.

    *Active CMA* is implemented with option ``CMA_active`` and
    conducts an update of the covariance matrix with negative weights.
    The negative update is implemented, such that positive definiteness
    is guarantied. The update is applied after the default update and
    only before the covariance matrix is decomposed, which limits the
    additional computational burden to be at most a factor of three
    (typically smaller). A typical speed up factor (number of
    f-evaluations) is between 1.1 and two.

    References: Jastrebski and Arnold, CEC 2006, Glasmachers et al, GECCO 2010.

    *Selective mirroring* is implemented with option ``CMA_mirrors``
    in the method ``get_mirror()``. Only the method `ask_and_eval()`
    (used by `fmin`) will then sample selectively mirrored vectors. In
    selective mirroring, only the worst solutions are mirrored. With
    the default small number of mirrors, *pairwise selection* (where at
    most one of the two mirrors contribute to the update of the
    distribution mean) is implicitly guarantied under selective
    mirroring and therefore not explicitly implemented.

    References: Brockhoff et al, PPSN 2010, Auger et al, GECCO 2011.

    :See: `fmin()`, `OOOptimizer`, `CMAOptions`, `plot()`, `ask()`,
        `tell()`, `ask_and_eval()`

    """
    @property  
    def popsize(self):
        """number of samples by default returned by` ask()`
        """
        return self.sp.popsize

    @popsize.setter
    def popsize(self, p):
        """popsize cannot be set (this might change in future)
        """
        raise _Error("popsize cannot be changed")

    def stop(self, check=True):
        """return a dictionary with the termination status.
        With ``check==False``, the termination conditions are not checked
        and the status might not reflect the current situation.

        """
        if (check and self.countiter > 0 and self.opts['termination_callback'] and
                self.opts['termination_callback'] != str(self.opts['termination_callback'])):
            self.callbackstop = self.opts['termination_callback'](self)

        return self._stopdict(self, check)  

    def copy_constructor(self, es):
        raise NotImplementedError("")

    def __init__(self, x0, sigma0, inopts={}):
        """see class `CMAEvolutionStrategy`

        """
        if isinstance(x0, CMAEvolutionStrategy):
            self.copy_constructor(x0)
            return
        self.inputargs = dict(locals())  
        del self.inputargs['self']  
        self.inopts = inopts
        opts = CMAOptions(inopts).complement()  
        global_verbosity = opts.eval('verbose')
        if global_verbosity < -8:
            opts['verb_disp'] = 0
            opts['verb_log'] = 0
            opts['verb_plot'] = 0

        if 'noise_handling' in opts and opts.eval('noise_handling'):
            raise ValueError('noise_handling not available with class CMAEvolutionStrategy, use function fmin')
        if 'restarts' in opts and opts.eval('restarts'):
            raise ValueError('restarts not available with class CMAEvolutionStrategy, use function fmin')

        self._set_x0(x0)  
        self.N_pheno = len(self.x0)

        self.sigma0 = sigma0
        if isinstance(sigma0, str):
        
            self.sigma0 = eval(sigma0)  
        if np.size(self.sigma0) != 1 or np.shape(self.sigma0):
            raise _Error('input argument sigma0 must be (or evaluate to) a scalar')
        self.sigma = self.sigma0  

        
        N = self.N_pheno
        assert isinstance(opts['fixed_variables'], (str, dict)) \
            or opts['fixed_variables'] is None
        
        if isinstance(opts['fixed_variables'], dict):
            N = self.N_pheno - len(opts['fixed_variables'])
        opts.evalall(locals())  
        self.opts = opts

        self.randn = opts['randn']
        self.gp = GenoPheno(self.N_pheno, opts['scaling_of_variables'], opts['typical_x'],
            opts['fixed_variables'], opts['transformation'])
        self.boundary_handler = opts.eval('boundary_handling')(opts.eval('bounds'))
        if not self.boundary_handler.has_bounds():
            self.boundary_handler = BoundNone()  
        elif not self.boundary_handler.is_in_bounds(self.x0):
            if opts['verbose'] >= 0:
                _print_warning('initial solution is out of the domain boundaries:')
                print('  x0   = ' + str(self.gp.pheno(self.x0)))
                print('  ldom = ' + str(self.boundary_handler.bounds[0]))
                print('  udom = ' + str(self.boundary_handler.bounds[1]))

        
        tf_geno_backup = self.gp.tf_geno
        if self.gp.tf_pheno and self.gp.tf_geno is None:
            self.gp.tf_geno = lambda x: x  
            _print_warning("""
                computed initial point is likely to be wrong, because
                no inverse was found of user provided phenotype
                transformation""")
        self.mean = self.gp.geno(self.x0,
                            from_bounds=self.boundary_handler.inverse,
                            copy_always=True)
        self.gp.tf_geno = tf_geno_backup
        
        
        self.N = len(self.mean)
        assert N == self.N
        self.fmean = np.NaN  
        self.fmean_noise_free = 0.  

        self.adapt_sigma = opts['AdaptSigma']
        if self.adapt_sigma is False:
            self.adapt_sigma = CMAAdaptSigmaNone
        self.adapt_sigma = self.adapt_sigma()  

        self.sp = _CMAParameters(N, opts)
        self.sp0 = self.sp  

        
        self.countiter = 0
        self.countevals = max((0, opts['verb_append'])) \
            if not isinstance(opts['verb_append'], bool) else 0
        self.pc = np.zeros(N)
        self.pc_neg = np.zeros(N)
        def eval_scaling_vector(in_):
            res = 1
            if np.all(in_):
                res = array(in_, dtype=float)
                if np.size(res) not in (1, N):
                    raise ValueError("""CMA_stds option must have dimension %d
                                 instead of %d""" %
                                 (str(N), np.size(res)))
            return res
        self.sigma_vec = eval_scaling_vector(self.opts['CMA_stds'])
        if isfinite(self.opts['CMA_dampsvec_fac']):
            self.sigma_vec *= np.ones(N)  
        self.sigma_vec0 = self.sigma_vec if isscalar(self.sigma_vec) \
                                        else self.sigma_vec.copy()
        stds = eval_scaling_vector(self.opts['CMA_teststds'])
        if self.opts['CMA_diagonal']:  
            
            self.B = array(1)  
            self.C = stds**2 * np.ones(N)  
            self.dC = self.C
        else:
            self.B = np.eye(N)  
            
            
            self.C = np.diag(stds**2 * exp((1e-4 / N) * np.arange(N)))
            self.dC = np.diag(self.C).copy()
            self._Yneg = np.zeros((N, N))

        self.D = self.dC**0.5  

        
        relative_stds = ((self.gp.pheno(self.mean + self.sigma * self.sigma_vec * self.D)
                          - self.gp.pheno(self.mean - self.sigma * self.sigma_vec * self.D)) / 2.0
                         / (self.boundary_handler.get_bounds('upper', self.N_pheno)
                            - self.boundary_handler.get_bounds('lower', self.N_pheno)))
        if np.any(relative_stds > 1):
            raise ValueError('initial standard deviations larger than the bounded domain size in variables '
                         + str(np.where(relative_stds > 1)[0]))
        self._flgtelldone = True
        self.itereigenupdated = self.countiter
        self.count_eigen = 0
        self.noiseS = 0  "signal"
        self.hsiglist = []

        if not opts['seed']:
            np.random.seed()
            six_decimals = (time.time() - 1e6 * (time.time() // 1e6))
            opts['seed'] = 1e5 * np.random.rand() + six_decimals + 1e5 * (time.time() % 1)
        opts['seed'] = int(opts['seed'])
        np.random.seed(opts['seed'])  

        self.sent_solutions = CMASolutionDict()
        self.archive = CMASolutionDict()
        self.best = BestSolution()

        self.const = _BlancClass()
        self.const.chiN = N**0.5 * (1 - 1. / (4.*N) + 1. / (21.*N**2))  

        self.logger = CMADataLogger(opts['verb_filenameprefix'], modulo=opts['verb_log']).register(self)

        
        self._stopdict = _CMAStopDict()
        self.callbackstop = 0

        self.fit = _BlancClass()
        self.fit.fit = []  
        self.fit.hist = []  
        self.fit.histbest = []  
        self.fit.histmedian = []  

        self.more_to_write = []  

        
        if opts['verb_disp'] > 0 and opts['verbose'] >= 0:
            sweighted = '_w' if self.sp.mu > 1 else ''
            smirr = 'mirr%d' % (self.sp.lam_mirr) if self.sp.lam_mirr else ''
            print('(%d' % (self.sp.mu) + sweighted + ',%d' % (self.sp.popsize) + smirr +
                  ')-' + ('a' if opts['CMA_active'] else '') + 'CMA-ES' +
                  ' (mu_w=%2.1f,w_1=%d%%)' % (self.sp.mueff, int(100 * self.sp.weights[0])) +
                  ' in dimension %d (seed=%d, %s)' % (N, opts['seed'], time.asctime()))  
            if opts['CMA_diagonal'] and self.sp.CMA_on:
                s = ''
                if opts['CMA_diagonal'] is not True:
                    s = ' for '
                    if opts['CMA_diagonal'] < np.inf:
                        s += str(int(opts['CMA_diagonal']))
                    else:
                        s += str(np.floor(opts['CMA_diagonal']))
                    s += ' iterations'
                    s += ' (1/ccov=' + str(round(1. / (self.sp.c1 + self.sp.cmu))) + ')'
                print('   Covariance matrix is diagonal' + s)

    def _set_x0(self, x0):
        if x0 == str(x0):
            x0 = eval(x0)
        self.x0 = array(x0)  
        if self.x0.ndim == 2:
            if self.opts.eval('verbose') >= 0:
                _print_warning('input x0 should be a list or 1-D array, trying to flatten ' +
                        str(self.x0.shape) + '-array')
            if self.x0.shape[0] == 1:
                self.x0 = self.x0[0]
            elif self.x0.shape[1] == 1:
                self.x0 = array([x[0] for x in self.x0])
        if self.x0.ndim != 1:
            raise _Error('x0 must be 1-D array')
        if len(self.x0) <= 1:
            raise _Error('optimization in 1-D is not supported (code was never tested)')
        self.x0.resize(self.x0.shape[0])  

    
    
    def ask(self, number=None, xmean=None, sigma_fac=1,
            gradf=None, args=()):
        """get new candidate solutions, sampled from a multi-variate
        normal distribution and transformed to f-representation
        (phenotype) to be evaluated.

        Arguments
        ---------
            `number`
                number of returned solutions, by default the
                population size ``popsize`` (AKA ``lambda``).
            `xmean`
                distribution mean, phenotyp?
            `sigma_fac`
                multiplier for internal sample width (standard
                deviation)
            `gradf`
                gradient, ``len(gradf(x)) == len(x)``, if
                ``gradf is not None`` the third solution in the
                returned list is "sampled" in supposedly Newton
                direction ``dot(C, gradf(xmean, *args))``.
            `args`
                additional arguments passed to gradf

        Return
        ------
        A list of N-dimensional candidate solutions to be evaluated

        Example
        -------
        >>> import cma
        >>> es = cma.CMAEvolutionStrategy([0,0,0,0], 0.3)
        >>> while not es.stop() and es.best.f > 1e-6:  
        ...     X = es.ask()  
        ...     fit = [cma.fcts.rosen(x) for x in X]  
        ...     es.tell(X, fit)  

        :See: `ask_and_eval`, `ask_geno`, `tell`

        """
        pop_geno = self.ask_geno(number, xmean, sigma_fac)

        
        
        
        
        
        pop_pheno = [self.gp.pheno(x, copy=True, into_bounds=self.boundary_handler.repair) for x in pop_geno]

        if gradf is not None:
            
            if not self.gp.islinear:
                _print_warning("""
                using the gradient (option ``gradf``) with a non-linear
                coordinate-wise transformation (option ``transformation``)
                has never been tested.""")
                
            def grad_numerical_of_coordinate_map(x, map, epsilon=None):
                """map is a coordinate-wise independent map, return
                the estimated diagonal of the Jacobian.
                """
                eps = 1e-8 * (1 + abs(x)) if epsilon is None else epsilon
                return (list(map(x + eps)) - list(map(x - eps))) / (2 * eps)
            def grad_numerical_sym(x, func, epsilon=None):
                """return symmetric numerical gradient of func : R^n -> R.
                """
                eps = 1e-8 * (1 + abs(x)) if epsilon is None else epsilon
                grad = np.zeros(len(x))
                ei = np.zeros(len(x))  
                for i in rglen(x):
                    ei[i] = eps[i]
                    grad[i] = (func(x + ei) - func(x - ei)) / (2*eps[i])
                    ei[i] = 0
                return grad
            try:
                if self.last_iteration_with_gradient == self.countiter:
                    _print_warning('gradient is used several times in ' +
                            'this iteration', iteration=self.countiter)
                self.last_iteration_with_gradient = self.countiter
            except AttributeError:
                pass
            index_for_gradient = min((2, len(pop_pheno)-1))
            xmean = self.mean if xmean is None else xmean
            xpheno = self.gp.pheno(xmean, copy=True,
                                into_bounds=self.boundary_handler.repair)
            grad_at_mean = gradf(xpheno, *args)
            
            if not self.gp.isidentity or (self.boundary_handler is not None
                    and self.boundary_handler.has_bounds()):
                boundary_repair = None
                gradpen = 0
                if isinstance(self.boundary_handler, BoundTransform):
                    boundary_repair = self.boundary_handler.repair
                elif isinstance(self.boundary_handler, BoundPenalty):
                    fpenalty = lambda x: self.boundary_handler.__call__(
                        x, SolutionDict({tuple(x): {'geno': x}}), self.gp)
                    gradpen = grad_numerical_sym(
                        xmean, fpenalty)
                elif self.boundary_handler is None or \
                        isinstance(self.boundary_handler, BoundNone):
                    pass
                else:
                    raise NotImplementedError(
                        "unknown boundary handling method" +
                        str(self.boundary_handler) +
                        " when using gradf")
                gradgp = grad_numerical_of_coordinate_map(
                    xmean,
                    lambda x: self.gp.pheno(x, copy=True,
                            into_bounds=boundary_repair))
                grad_at_mean = grad_at_mean * gradgp + gradpen

            
            if len(grad_at_mean) != self.N and self.opts['fixed_variables']:
                NotImplementedError("""
                gradient with fixed variables is not yet implemented""")
            v = self.D * dot(self.B.T, self.sigma_vec * grad_at_mean)
            
            
            q = sum(v**2)
            if q:
                
                pop_geno[index_for_gradient] = xmean - self.sigma \
                            * (self.N / q)**0.5 \
                            * (self.sigma_vec * dot(self.B, self.D * v))
            else:
                pop_geno[index_for_gradient] = xmean
                _print_warning('gradient zero observed',
                               iteration=self.countiter)

            pop_pheno[index_for_gradient] = self.gp.pheno(
                pop_geno[index_for_gradient], copy=True,
                into_bounds=self.boundary_handler.repair)

        
        for i in rglen((pop_geno)):
            self.sent_solutions.insert(pop_pheno[i], geno=pop_geno[i], iteration=self.countiter)
        return pop_pheno

    
    
    def ask_geno(self, number=None, xmean=None, sigma_fac=1):
        """get new candidate solutions in genotyp, sampled from a
        multi-variate normal distribution.

        Arguments are
            `number`
                number of returned solutions, by default the
                population size `popsize` (AKA lambda).
            `xmean`
                distribution mean
            `sigma_fac`
                multiplier for internal sample width (standard
                deviation)

        `ask_geno` returns a list of N-dimensional candidate solutions
        in genotyp representation and is called by `ask`.

        Details: updates the sample distribution and might change
        the geno-pheno transformation during this update.

        :See: `ask`, `ask_and_eval`

        """

        if number is None or number < 1:
            number = self.sp.popsize

        
        if self.sp.CMA_on and (
                (self.opts['updatecovwait'] is None and
                 self.countiter >=
                     self.itereigenupdated + 1. / (self.sp.c1 + self.sp.cmu) / self.N / 10
                 ) or
                (self.opts['updatecovwait'] is not None and
                 self.countiter > self.itereigenupdated + self.opts['updatecovwait']
                 ) or
                (self.sp.neg.cmuexp * (self.countiter - self.itereigenupdated) > 0.5
                )  "the right" criterion
            ):
            self.updateBD()
        if xmean is None:
            xmean = self.mean
        else:
            try:
                xmean = self.archive[xmean]['geno']
                
            except KeyError:
                try:
                    xmean = self.sent_solutions[xmean]['geno']
                    
                except KeyError:
                    pass

        if self.countiter == 0:
            self.tic = time.clock()  
            self.elapsed_time = ElapsedTime()

        sigma = sigma_fac * self.sigma

        
        
        
        
        
        
        
        
        
        

        
        if self._flgtelldone:  
            self._flgtelldone = False
            self.ary = []

        
        arinj = []
        if hasattr(self, 'pop_injection_directions'):
            if self.countiter < 4 and \
                    len(self.pop_injection_directions) > self.popsize - 2:
                _print_warning('  %d special injected samples with popsize %d, '
                                  % (len(self.pop_injection_directions), self.popsize)
                               + "popsize %d will be used" % (len(self.pop_injection_directions) + 2)
                               + (" and the warning is suppressed in the following" if self.countiter == 3 else ""))
            while self.pop_injection_directions:
                y = self.pop_injection_directions.pop(0)
                if self.opts['CMA_sample_on_sphere_surface']:
                    y *= (self.N**0.5 if self.opts['CSA_squared'] else
                          self.const.chiN) / self.mahalanobis_norm(y)
                    arinj.append(y)
                else:
                    y *= self.random_rescaling_factor_to_mahalanobis_size(y) / self.sigma
                    arinj.append(y)
        
        "pure" adaptive encoding
        arz = self.randn((max([1, (number - len(arinj))]), self.N))
        if self.opts['CMA_sample_on_sphere_surface']:  
            for i in rglen((arz)):
                ss = sum(arz[i]**2)
                if 1 < 3 or ss > self.N + 10.1:
                    arz[i] *= (self.N**0.5 if self.opts['CSA_squared']
                                           else self.const.chiN) / ss**0.5
            
            

        
        
        

        
        if len(arz):  
            
            if new_injections and self.sp.lam_mirr and self.opts['CMA_mirrormethod'] == 0:
                for i in range(self.sp.lam_mirr):
                    if 2 * (i + 1) > len(arz):
                        if self.countiter < 4:
                            _print_warning("fewer mirrors generated than given in parameter setting (%d<%d)"
                                            % (i, self.sp.lam_mirr))
                        break
                    arz[-1 - 2 * i] = -arz[-2 - 2 * i]
            ary = self.sigma_vec * np.dot(self.B, (self.D * arz).T).T
            if len(arinj):
                ary = np.vstack((arinj, ary))
        else:
            ary = array(arinj)

        
        if not new_injections and number > 2 and self.countiter > 2:
            if (isinstance(self.adapt_sigma, CMAAdaptSigmaTPA) or
                self.opts['mean_shift_line_samples'] or
                self.opts['pc_line_samples']):
                ys = []
                if self.opts['pc_line_samples']:
                    ys.append(self.pc[:])  
                if self.opts['mean_shift_line_samples']:
                    ys.append(self.mean - self.mean_old)
                if not len(ys):
                    ys.append(self.mean - self.mean_old)
                
                for i, y in enumerate(ys):
                    if len(arz) > 2 * i + 1:  
                        assert y is not self.pc
                        
                        y *= self.random_rescaling_factor_to_mahalanobis_size(y)
                        
                        ary[2*i] = y / self.sigma
                        ary[2*i + 1] = y / -self.sigma
                    else:
                        _print_warning('line samples omitted due to small popsize',
                            method_name='ask_geno', iteration=self.countiter)

        
        pop = xmean + sigma * ary
        self.evaluations_per_f_value = 1
        self.ary = ary
        return pop

    def random_rescale_to_mahalanobis(self, x):
        """change `x` like for injection, all on genotypic level"""
        x -= self.mean
        if any(x):
            x *= sum(self.randn(len(x))**2)**0.5 / self.mahalanobis_norm(x)
        x += self.mean
        return x
    def random_rescaling_factor_to_mahalanobis_size(self, y):
        """``self.mean + self.random_rescaling_factor_to_mahalanobis_size(y)``
        is guarantied to appear like from the sample distribution.
        """
        if len(y) != self.N:
            raise ValueError('len(y)=%d != %d=dimension' % (len(y), self.N))
        if not any(y):
            _print_warning("input was all-zeros, which is probably a bug",
                           "random_rescaling_factor_to_mahalanobis_size",
                           iteration=self.countiter)
            return 1.0
        return sum(self.randn(len(y))**2)**0.5 / self.mahalanobis_norm(y)


    def get_mirror(self, x, preserve_length=False):
        """return ``pheno(self.mean - (geno(x) - self.mean))``.

        >>> import cma
        >>> es = cma.CMAEvolutionStrategy(cma.np.random.randn(3), 1)
        >>> x = cma.np.random.randn(3)
        >>> assert cma.Mh.vequals_approximately(es.mean - (x - es.mean), es.get_mirror(x, preserve_length=True))
        >>> x = es.ask(1)[0]
        >>> vals = (es.get_mirror(x) - es.mean) / (x - es.mean)
        >>> assert cma.Mh.equals_approximately(sum(vals), len(vals) * vals[0])

        TODO: this implementation is yet experimental.

        TODO: this implementation includes geno-pheno transformation,
        however in general GP-transformation should be separated from
        specific code.

        Selectively mirrored sampling improves to a moderate extend but
        overadditively with active CMA for quite understandable reasons.

        Optimal number of mirrors are suprisingly small: 1,2,3 for
        maxlam=7,13,20 where 3,6,10 are the respective maximal possible
        mirrors that must be clearly suboptimal.

        """
        try:
            dx = self.sent_solutions[x]['geno'] - self.mean
        except:  
            dx = self.gp.geno(x, from_bounds=self.boundary_handler.inverse,
                              copy_if_changed=True) - self.mean

        if not preserve_length:
            
            dx *= self.random_rescaling_factor_to_mahalanobis_size(dx)
        x = self.mean - dx
        y = self.gp.pheno(x, into_bounds=self.boundary_handler.repair)
        
        self.sent_solutions.insert(y, geno=x, iteration=self.countiter)
        return y

    def _mirror_penalized(self, f_values, idx):
        """obsolete and subject to removal (TODO),
        return modified f-values such that for each mirror one becomes worst.

        This function is useless when selective mirroring is applied with no
        more than (lambda-mu)/2 solutions.

        Mirrors are leading and trailing values in ``f_values``.

        """
        assert len(f_values) >= 2 * len(idx)
        m = np.max(np.abs(f_values))
        for i in len(idx):
            if f_values[idx[i]] > f_values[-1 - i]:
                f_values[idx[i]] += m
            else:
                f_values[-1 - i] += m
        return f_values

    def _mirror_idx_cov(self, f_values, idx1):  
        """obsolete and subject to removal (TODO),
        return indices for negative ("active") update of the covariance matrix
        assuming that ``f_values[idx1[i]]`` and ``f_values[-1-i]`` are
        the corresponding mirrored values

        computes the index of the worse solution sorted by the f-value of the
        better solution.

        TODO: when the actual mirror was rejected, it is better
        to return idx1 instead of idx2.

        Remark: this function might not be necessary at all: if the worst solution
        is the best mirrored, the covariance matrix updates cancel (cave: weights
        and learning rates), which seems what is desirable. If the mirror is bad,
        as strong negative update is made, again what is desirable.
        And the fitness--step-length correlation is in part addressed by
        using flat weights.

        """
        idx2 = np.arange(len(f_values) - 1, len(f_values) - 1 - len(idx1), -1)
        f = []
        for i in rglen((idx1)):
            f.append(min((f_values[idx1[i]], f_values[idx2[i]])))
            
        return idx2[np.argsort(f)][-1::-1]

    def eval_mean(self, func, args=()):
        """evaluate the distribution mean, this is not (yet) effective
        in terms of termination or display"""
        self.fmean = func(self.mean, *args)
        return self.fmean

    
    
    
    def ask_and_eval(self, func, args=(), gradf=None, number=None, xmean=None, sigma_fac=1,
                     evaluations=1, aggregation=np.median, kappa=1):
        """samples `number` solutions and evaluates them on `func`, where
        each solution `s` is resampled until ``self.is_feasible(s, func(s)) is True``.

        Arguments
        ---------
            `func`
                objective function, ``func(x)`` returns a scalar
            `args`
                additional parameters for `func`
            `gradf`
                gradient of objective function, ``g = gradf(x, *args)``
                must satisfy ``len(g) == len(x)``
            `number`
                number of solutions to be sampled, by default
                population size ``popsize`` (AKA lambda)
            `xmean`
                mean for sampling the solutions, by default ``self.mean``.
            `sigma_fac`
                multiplier for sampling width, standard deviation, for example
                to get a small perturbation of solution `xmean`
            `evaluations`
                number of evaluations for each sampled solution
            `aggregation`
                function that aggregates `evaluations` values to
                as single value.
            `kappa`
                multiplier used for the evaluation of the solutions, in
                that ``func(m + kappa*(x - m))`` is the f-value for x.

        Return
        ------
        ``(X, fit)``, where
            X -- list of solutions
            fit -- list of respective function values

        Details
        -------
        While ``not self.is_feasible(x, func(x))``new solutions are sampled. By
        default ``self.is_feasible == cma.feasible == lambda x, f: f not in (None, np.NaN)``.
        The argument to `func` can be freely modified within `func`.

        Depending on the ``CMA_mirrors`` option, some solutions are not sampled
        independently but as mirrors of other bad solutions. This is a simple
        derandomization that can save 10-30% of the evaluations in particular
        with small populations, for example on the cigar function.

        Example
        -------
        >>> import cma
        >>> x0, sigma0 = 8*[10], 1  
        >>> es = cma.CMAEvolutionStrategy(x0, sigma0)
        >>> while not es.stop():
        ...     X, fit = es.ask_and_eval(cma.fcts.elli)  
        ...     es.tell(X, fit)  
        ...     es.disp(20) 
        >>> print('terminated on ' + str(es.stop()))
        <output omitted>

        A single iteration step can be expressed in one line, such that
        an entire optimization after initialization becomes
        ::

            while not es.stop():
                es.tell(*es.ask_and_eval(cma.fcts.elli))

        """
        
        popsize = self.sp.popsize
        if number is not None:
            popsize = number

        selective_mirroring = self.opts['CMA_mirrormethod'] > 0
        nmirrors = self.sp.lam_mirr
        if popsize != self.sp.popsize:
            nmirrors = Mh.sround(popsize * self.sp.lam_mirr / self.sp.popsize)
            
        assert new_injections or self.opts['CMA_mirrormethod'] < 2 
        if new_injections and self.opts['CMA_mirrormethod'] != 1: 
            nmirrors = 0
        assert nmirrors <= popsize // 2
        self.mirrors_idx = np.arange(nmirrors)  
        self.mirrors_rejected_idx = []  
        is_feasible = self.opts['is_feasible']

        
        fit = []  
        X_first = self.ask(popsize, xmean=xmean, gradf=gradf, args=args)
        if xmean is None:
            xmean = self.mean  
        X = []
        for k in range(int(popsize)):
            x, f = X_first.pop(0), None
            rejected = -1
            while rejected < 0 or not is_feasible(x, f):  
                rejected += 1
                if rejected:  
                    x = self.ask(1, xmean, sigma_fac)[0]
                elif k >= popsize - nmirrors:  
                    if k == popsize - nmirrors and selective_mirroring:
                        self.mirrors_idx = np.argsort(fit)[-1:-1 - nmirrors:-1]
                    x = self.get_mirror(X[self.mirrors_idx[popsize - 1 - k]])
                if rejected == 1 and k >= popsize - nmirrors:
                    self.mirrors_rejected_idx.append(k)

                
                length_normalizer = 1
                
                f = func(x, *args) if kappa == 1 else \
                    func(xmean + kappa * length_normalizer * (x - xmean),
                         *args)
                if is_feasible(x, f) and evaluations > 1:
                    f = aggregation([f] + [(func(x, *args) if kappa == 1 else
                                            func(xmean + kappa * length_normalizer * (x - xmean), *args))
                                           for _i in range(int(evaluations - 1))])
                if rejected + 1 % 1000 == 0:
                    print('  %d solutions rejected (f-value NaN or None) at iteration %d' %
                          (rejected, self.countiter))
            fit.append(f)
            X.append(x)
        self.evaluations_per_f_value = int(evaluations)
        return X, fit

    def prepare_injection_directions(self):
        """provide genotypic directions for TPA and selective mirroring,
        with no specific length normalization, to be used in the
        coming iteration.

        Details:
        This method is called in the end of `tell`. The result is
        assigned to ``self.pop_injection_directions`` and used in
        `ask_geno`.

        TODO: should be rather appended?

        """
        
        if hasattr(self, 'pop_injection_directions') and self.pop_injection_directions:
            ValueError("Looks like a bug in calling order/logics")
        ary = []
        if (isinstance(self.adapt_sigma, CMAAdaptSigmaTPA) or
                self.opts['mean_shift_line_samples']):
            ary.append(self.mean - self.mean_old)
            ary.append(self.mean_old - self.mean)  
            if ary[-1][0] == 0.0:
                _print_warning('zero mean shift encountered which ',
                               'prepare_injection_directions',
                               'CMAEvolutionStrategy', self.countiter)
        if self.opts['pc_line_samples']: 
            ary.append(self.pc.copy())
        if self.sp.lam_mirr and self.opts['CMA_mirrormethod'] == 2:
            if self.pop_sorted is None:
                _print_warning('pop_sorted attribute not found, mirrors obmitted',
                               'prepare_injection_directions',
                               iteration=self.countiter)
            else:
                ary += self.get_selective_mirrors()
        self.pop_injection_directions = ary
        return ary

    def get_selective_mirrors(self, number=None, pop_sorted=None):
        """get mirror genotypic directions of the `number` worst
        solution, based on ``pop_sorted`` attribute (from last
        iteration).

        Details:
        Takes the last ``number=sp.lam_mirr`` entries in
        ``pop_sorted=self.pop_sorted`` as solutions to be mirrored.

        """
        if pop_sorted is None:
            if hasattr(self, 'pop_sorted'):
                pop_sorted = self.pop_sorted
            else:
                return None
        if number is None:
            number = self.sp.lam_mirr
        res = []
        for i in range(1, number + 1):
            res.append(self.mean_old - pop_sorted[-i])
        return res

    
    def tell(self, solutions, function_values, check_points=None,
             copy=False):
        """pass objective function values to prepare for next
        iteration. This core procedure of the CMA-ES algorithm updates
        all state variables, in particular the two evolution paths, the
        distribution mean, the covariance matrix and a step-size.

        Arguments
        ---------
            `solutions`
                list or array of candidate solution points (of
                type `numpy.ndarray`), most presumably before
                delivered by method `ask()` or `ask_and_eval()`.
            `function_values`
                list or array of objective function values
                corresponding to the respective points. Beside for termination
                decisions, only the ranking of values in `function_values`
                is used.
            `check_points`
                If ``check_points is None``, only solutions that are not generated
                by `ask()` are possibly clipped (recommended). ``False`` does not clip
                any solution (not recommended).
                If ``True``, clips solutions that realize long steps (i.e. also
                those that are unlikely to be generated with `ask()`). `check_points`
                can be a list of indices to be checked in solutions.
            `copy`
                ``solutions`` can be modified in this routine, if ``copy is False``

        Details
        -------
        `tell()` updates the parameters of the multivariate
        normal search distribution, namely covariance matrix and
        step-size and updates also the attributes ``countiter`` and
        ``countevals``. To check the points for consistency is quadratic
        in the dimension (like sampling points).

        Bugs
        ----
        The effect of changing the solutions delivered by `ask()`
        depends on whether boundary handling is applied. With boundary
        handling, modifications are disregarded. This is necessary to
        apply the default boundary handling that uses unrepaired
        solutions but might change in future.

        Example
        -------
        ::

            import cma
            func = cma.fcts.elli  
            es = cma.CMAEvolutionStrategy(cma.np.random.rand(10), 1)
            while not es.stop():
               X = es.ask()
               es.tell(X, [func(x) for x in X])
            es.result()  

        :See: class `CMAEvolutionStrategy`, `ask()`, `ask_and_eval()`, `fmin()`

        """
        if self._flgtelldone:
            raise _Error('tell should only be called once per iteration')

        lam = len(solutions)
        if lam != array(function_values).shape[0]:
            raise _Error('for each candidate solution '
                        + 'a function value must be provided')
        if lam + self.sp.lam_mirr < 3:
            raise _Error('population size ' + str(lam) + ' is too small when option CMA_mirrors * popsize < 0.5')

        if not isscalar(function_values[0]):
            if isscalar(function_values[0][0]):
                if self.countiter <= 1:
                    _print_warning('function values are not a list of scalars (further warnings are suppressed)')
                function_values = [val[0] for val in function_values]
            else:
                raise _Error('objective function values must be a list of scalars')


        
        N = self.N
        sp = self.sp
        if lam < sp.mu:  
            raise _Error('not enough solutions passed to function tell (mu>lambda)')

        self.countiter += 1  
        self.countevals += sp.popsize * self.evaluations_per_f_value
        self.best.update(solutions, self.sent_solutions, function_values, self.countevals)

        flg_diagonal = self.opts['CMA_diagonal'] is True \
                       or self.countiter <= self.opts['CMA_diagonal']
        if not flg_diagonal and len(self.C.shape) == 1:  
            
            self.C = np.diag(self.C)
            if 1 < 3:
                self.B = np.eye(N)  
                idx = np.argsort(self.D)
                self.D = self.D[idx]
                self.B = self.B[:, idx]
            self._Yneg = np.zeros((N, N))

        
        fit = self.fit  

        
        fit.bndpen = self.boundary_handler.update(function_values, self)(solutions, self.sent_solutions, self.gp)
        
        
        fit.idx = np.argsort(array(fit.bndpen) + array(function_values))
        fit.fit = array(function_values, copy=False)[fit.idx]

        
        
        
        

        
        fit.hist.insert(0, fit.fit[0])
        
        if ((self.countiter % 5) == 0):  
            fit.histbest.insert(0, fit.fit[0])
            fit.histmedian.insert(0, np.median(fit.fit) if len(fit.fit) < 21
                                    else fit.fit[self.popsize // 2])
        if len(fit.histbest) > 2e4:  
            fit.histbest.pop()
            fit.histmedian.pop()
        if len(fit.hist) > 10 + 30 * N / sp.popsize:
            fit.hist.pop()

        
        
        pop = self.pop_sorted = []  
        for k, s in enumerate(solutions):  
            if 1 < 3:
                pop += [self.gp.geno(s,
                            from_bounds=self.boundary_handler.inverse,
                            repair=(self.repair_genotype if check_points not in (False, 0, [], ()) else None),
                            archive=self.sent_solutions)]  
                try:
                    self.archive.insert(s, value=self.sent_solutions.pop(s), fitness=function_values[k])
                    
                except KeyError:
                    pass
        
        if isinstance(self.adapt_sigma, CMAAdaptSigmaTPA) and self.countiter > 3 and not (self.countiter % 3):
            dm = self.mean[0] - self.mean_old[0]
            dx0 = pop[0][0] - self.mean_old[0]
            dx1 = pop[1][0] - self.mean_old[0]
            for i in np.random.randint(1, self.N, 1):
                try:
                    if not Mh.equals_approximately(
                                (self.mean[i] - self.mean_old[i])
                                    / (pop[0][i] - self.mean_old[i]),
                                 dm / dx0, 1e-8) or \
                        not Mh.equals_approximately(
                                (self.mean[i] - self.mean_old[i])
                                    / (pop[1][i] - self.mean_old[i]),
                                dm / dx1, 1e-8):
                        _print_warning('TPA error with mirrored samples', 'tell',
                                       'CMAEvolutionStrategy', self.countiter)
                except ZeroDivisionError:
                    _print_warning('zero division encountered in TPA check\n which should be very rare and is likely a bug',
                                   'tell', 'CMAEvolutionStrategy', self.countiter)

        try:
            moldold = self.mean_old
        except:
            pass
        self.mean_old = self.mean
        mold = self.mean_old  

        
        
        
        if check_points not in (None, False, 0, [], ()):  
            try:
                if len(check_points):
                    idx = check_points
            except:
                idx = range(sp.popsize)

            for k in idx:
                self.repair_genotype(pop[k])

        
        pop = array(pop, copy=False)

        
        pop = pop[fit.idx]

        
        if self.opts['CMA_elitist'] and self.best.f < fit.fit[0]:
            if self.best.x_geno is not None:
                xp = [self.best.x_geno]
                
                
                
            else:
                xp = [self.gp.geno(array(self.best.x, copy=True),
                                   self.boundary_handler.inverse,
                                   copy_if_changed=False)]
                print('genotype for elitist not found')
            self.clip_or_fit_solutions(xp, [0])
            pop = array([xp[0]] + list(pop))
        elif self.opts['CMA_elitist'] == 'initial':  
            self.opts['CMA_elitist'] = False

        self.pop_sorted = pop
        
        self.mean = mold + self.sp.cmean * \
                    (sum(sp.weights * pop[0:sp.mu].T, 1) - mold)


        
        
        
        
        
        if 1 < 3:
            cmean = self.sp.cmean

        
        
        cc, c1, cmu = sp.cc, sp.c1, sp.cmu
        if flg_diagonal:
            cc, c1, cmu = sp.cc_sep, sp.c1_sep, sp.cmu_sep

        

        hsig = self.adapt_sigma.hsig(self) 

        
        
        
        
        c1a = c1 - (1 - hsig**2) * c1 * cc * (2 - cc)  

        self.pc = (1 - cc) * self.pc + \
                  hsig * (sqrt(cc * (2 - cc) * sp.mueff) / self.sigma / cmean) * \
                  (self.mean - mold) / self.sigma_vec

        
        if sp.CMA_on:
            
            assert c1 + cmu <= 1

            
            if not flg_diagonal:
                Y = (pop[0:sp.mu] - mold) / (self.sigma * self.sigma_vec)
                Y = dot((cmu * sp.weights) * Y.T, Y)  
                if self.sp.neg.cmuexp:
                    tmp = (pop[-sp.neg.mu:] - mold) / (self.sigma * self.sigma_vec)
                    
                    for i in range(tmp.shape[0]):
                        tmp[i, :] *= N**0.5 / self.mahalanobis_norm(
                                 self.sigma_vec * tmp[i, :]) / self.sigma
                    self._Yneg *= 1 - self.sp.neg.cmuexp  
                    self._Yneg += dot(sp.neg.weights * tmp.T, tmp) - self.C
                    

                self.C *= 1 - c1a - cmu
                self.C += np.outer(c1 * self.pc, self.pc) + Y
                self.dC[:] = np.diag(self.C)  

            else:  
                assert(c1 + cmu <= 1)
                Z = np.zeros(N)
                for k in range(sp.mu):
                    z = (pop[k] - mold) / (self.sigma * self.sigma_vec)  
                    Z += sp.weights[k] * z * z  
                self.C = (1 - c1a - cmu) * self.C + c1 * self.pc * self.pc + cmu * Z
                
                self.dC = self.C
                self.D = sqrt(self.C)  
                self.itereigenupdated = self.countiter

                

        
        
        self.adapt_sigma.update(self, function_values=function_values)

        if self.sigma * min(self.sigma_vec * self.dC**0.5) < self.opts['minstd']:
            self.sigma = self.opts['minstd'] / min(self.sigma_vec * self.dC**0.5)
        if self.sigma * max(self.sigma_vec * self.dC**0.5) > self.opts['maxstd']:
            self.sigma = self.opts['maxstd'] / max(self.sigma_vec * self.dC**0.5)
        
        
        
        
        if self.sigma * min(self.D) < self.opts['mindx']:  
            self.sigma = self.opts['mindx'] / min(self.D)

        if self.sigma > 1e9 * self.sigma0:
            alpha = self.sigma / max(self.D)
            self.multiplyC(alpha)
            self.sigma /= alpha**0.5
            self.opts['tolupsigma'] /= alpha**0.5  

        

        

        "feasible preimage", leads to weird behavior on
        
        
        if new_injections:
            self.pop_injection_directions = self.prepare_injection_directions()
        self.pop_sorted = []  
        self._flgtelldone = True
    

    def inject(self, solutions):
        """inject a genotypic solution. The solution is used as direction
        relative to the distribution mean to compute a new candidate
        solution returned in method `ask_geno` which in turn is used in
        method `ask`.

        >>> import cma
        >>> es = cma.CMAEvolutionStrategy(4 * [1], 2)
        >>> while not es.stop():
        ...     es.inject([4 * [0.0]])
        ...     X = es.ask()
        ...     break
        >>> assert X[0][0] == X[0][1]

        """
        if not hasattr(self, 'pop_injection_directions'):
            self.pop_injection_directions = []
        for solution in solutions:
            if len(solution) != self.N:
                raise ValueError('method `inject` needs a list or array'
                    + (' each el with dimension (`len`) %d' % self.N))
            self.pop_injection_directions.append(
                array(solution, copy=False, dtype=float) - self.mean)

    def result(self):
        """return::

             (xbest, f(xbest), evaluations_xbest, evaluations, iterations,
                 pheno(xmean), effective_stds)

        """
        
        return self.best.get() + (
            self.countevals, self.countiter, self.gp.pheno(self.mean),
            self.gp.scales * self.sigma * self.sigma_vec * self.dC**0.5)
    def result_pretty(self, number_of_runs=0, time_str=None,
                      fbestever=None):
        """pretty print result.

        Returns ``self.result()``

        """
        if fbestever is None:
            fbestever = self.best.f
        s = (' after %i restart' + ('s' if number_of_runs > 1 else '')) \
            % number_of_runs if number_of_runs else ''
        for k, v in list(self.stop().items()):
            print('termination on %s=%s%s' % (k, str(v), s +
                  (' (%s)' % time_str if time_str else '')))

        print('final/bestever f-value = %e %e' % (self.best.last.f,
                                                  fbestever))
        if self.N < 9:
            print('incumbent solution: ' + str(list(self.gp.pheno(self.mean, into_bounds=self.boundary_handler.repair))))
            print('std deviation: ' + str(list(self.sigma * self.sigma_vec * sqrt(self.dC) * self.gp.scales)))
        else:
            print('incumbent solution: %s ...]' % (str(self.gp.pheno(self.mean, into_bounds=self.boundary_handler.repair)[:8])[:-1]))
            print('std deviations: %s ...]' % (str((self.sigma * self.sigma_vec * sqrt(self.dC) * self.gp.scales)[:8])[:-1]))
        return self.result()

    def clip_or_fit_solutions(self, pop, idx):
        """make sure that solutions fit to sample distribution, this interface will probably change.

        In particular the frequency of long vectors appearing in pop[idx] - self.mean is limited.

        """
        for k in idx:
            self.repair_genotype(pop[k])

    def repair_genotype(self, x, copy_if_changed=False):
        """make sure that solutions fit to the sample distribution, this interface will probably change.

        In particular the frequency of x - self.mean being long is limited.

        """
        x = array(x, copy=False)
        mold = array(self.mean, copy=False)
        if 1 < 3:  
            upper_length = self.N**0.5 + 2 * self.N / (self.N + 2)  
            fac = self.mahalanobis_norm(x - mold) / upper_length

            if fac > 1:
                if copy_if_changed:
                    x = (x - mold) / fac + mold
                else:  
                    x -= mold
                    x /= fac
                    x += mold
                
                
        else:
            if 'checktail' not in self.__dict__:  
                raise NotImplementedError
                
                
                
            fac = self.checktail.addchin(self.mahalanobis_norm(x - mold))

            if fac < 1:
                x = fac * (x - mold) + mold

        return x

    def decompose_C(self):
        """eigen-decompose self.C and update self.dC, self.C, self.B.

        Known bugs: this might give a runtime error with
        CMA_diagonal / separable option on.

        """
        if self.opts['CMA_diagonal']:
            _print_warning("this might fail with CMA_diagonal option on",
                       iteration=self.countiter)
            print(self.opts['CMA_diagonal'])

        
        self.C = (self.C + self.C.T) / 2
        self.dC = np.diag(self.C).copy()
        self.D, self.B = self.opts['CMA_eigenmethod'](self.C)
 
 
 
 
 
        
        
        if any(self.D <= 0):
            _print_warning("ERROR", iteration=self.countiter)
            raise ValueError("covariance matrix was not positive definite," +
            " this must be considered as a bug")
        self.D = self.D**0.5
        assert all(isfinite(self.D))
        idx = np.argsort(self.D)
        self.D = self.D[idx]
        self.B = self.B[:, idx]  
        self.count_eigen += 1
    def updateBD(self):
        """update internal variables for sampling the distribution with the
        current covariance matrix C. This method is O(N^3), if C is not diagonal.

        """
        
        
        if self.itereigenupdated == self.countiter:
            return
        if self.opts['CMA_diagonal'] >= self.countiter:
            _print_warning("updateBD called in CMA_diagonal mode, " +
                           "this should be considered a bug", "updateBD",
                           iteration=self.countiter)
        
        if self.sp.neg.cmuexp:
            C_shrunken = (1 - self.sp.cmu - self.sp.c1)**(self.countiter - self.itereigenupdated)
            clip_fac = 0.60  
            if hasattr(self.opts['vv'], '__getitem__') and self.opts['vv'][0] == 'sweep_ccov_neg':
                clip_fac = 0.98
            if (self.countiter - self.itereigenupdated) * self.sp.neg.cmuexp * self.N \
                < clip_fac * C_shrunken:
                
                self.C -= self.sp.neg.cmuexp * self._Yneg
            else:
                max_warns = 1
                try:
                    self._updateBD_warnings += 1
                except AttributeError:
                    self._updateBD_warnings = 1
                if self.opts['verbose'] > 1 and \
                                self._updateBD_warnings <= max_warns:
                    _print_warning('doing two additional eigen' +
                                   'decompositions to guarantee pos.def.',
                                   'updateBD', 'CMAEvolutionStrategy')
                    if self._updateBD_warnings == max_warns:
                        _print_warning('further warnings are surpressed',
                                       'updateBD')
                self.decompose_C()
                _tmp_inverse_root_C = dot(self.B / self.D, self.B.T)
                _tmp_inverse_root_C = (_tmp_inverse_root_C + _tmp_inverse_root_C.T) / 2
                Zneg = dot(dot(_tmp_inverse_root_C, self._Yneg), _tmp_inverse_root_C)
                eigvals, eigvecs = self.opts['CMA_eigenmethod'](Zneg)
                self.count_eigen += 1
                if max(eigvals) * self.sp.neg.cmuexp <= clip_fac:
                   self.C -= self.sp.neg.cmuexp * self._Yneg
                elif 1 < 3:
                    self.C -= (clip_fac / max(eigvals)) * self._Yneg
                    _print_warning(
                        'clipped learning rate for negative weights, ' +
                        'maximal eigenvalue = %f, maxeig * ccov = %f > %f'
                         % (max(eigvals), max(eigvals) * self.sp.neg.cmuexp, clip_fac),
                        iteration=self.countiter)
                    if 1 < 3: 
                        eigvals, eigvecs = self.opts['CMA_eigenmethod'](self.C)
                        self.count_eigen += 1
                        print('new min eigenval = %e, old = %e'
                              % (min(eigvals), min(self.D)**2))
                        if min(eigvals) > 0:
                            print('new cond = %e, old = %e'
                                  % (max(eigvals) / min(eigvals),
                                     (max(self.D) / min(self.D))**2))
                else: 
                    _print_warning('exponential update for negative weights (internally more expensive)',
                                   iteration=self.countiter)
                    self.update_exponential(self._Yneg, -self.sp.neg.cmuexp)
                    
            
            self._Yneg = np.zeros((self.N, self.N))

        if hasattr(self.opts['vv'], '__getitem__') and self.opts['vv'][0].startswith('sweep_ccov'):
            self.opts['CMA_const_trace'] = True
        if self.opts['CMA_const_trace'] in (True, 1, 2):  
            if self.opts['CMA_const_trace'] == 2:
                s = np.exp(2 * np.mean(np.log(self.D)))  
            else:
                s = np.mean(np.diag(self.C))
            self.C /= s

        dC = np.diag(self.C)
        if max(dC) / min(dC) > 1e8:
            
            self.sigma_vec *= np.diag(self.C)**0.5
            self.C = self.correlation_matrix()
            _print_warning('condition in coordinate system exceeded 1e8' +
                ', rescaled to 1')

        
        

        self.decompose_C()
        
        
        
        

        
        
        

        if 1 < 3 and max(self.D) / min(self.D) > 1e6 and self.gp.isidentity:
            
            
            self.gp._tf_matrix = (self.sigma_vec * dot(self.B * self.D, self.B.T).T).T
            self.gp._tf_matrix_inv = (dot(self.B / self.D, self.B.T).T / self.sigma_vec).T
            self.gp.tf_pheno = lambda x: dot(self.gp._tf_matrix, x)
            self.gp.tf_geno = lambda x: dot(self.gp._tf_matrix_inv, x)  
            self.gp.isidentity = False
            assert self.mean is not self.mean_old
            self.mean = self.gp.geno(self.mean)  
            self.mean_old = self.gp.geno(self.mean_old)  
            self.pc = self.gp.geno(self.pc)
            self.D[:] = 1.0
            self.B = np.eye(self.N)
            self.C = np.eye(self.N)
            self.dC[:] = 1.0
            self.sigma_vec = 1
            
            
            _print_warning('\n geno-pheno transformation introduced based on current C,\n injected solutions become "invalid" in this iteration',
                           'updateBD', 'CMAEvolutionStrategy', self.countiter)

        self.itereigenupdated = self.countiter

    def multiplyC(self, alpha):
        """multiply C with a scalar and update all related internal variables (dC, D,...)"""
        self.C *= alpha
        if self.dC is not self.C:
            self.dC *= alpha
        self.D *= alpha**0.5
    def update_exponential(self, Z, eta, BDpair=None):
        """exponential update of C that guarantees positive definiteness, that is,
        instead of the assignment ``C = C + eta * Z``,
        we have ``C = C**.5 * exp(eta * C**-.5 * Z * C**-.5) * C**.5``.

        Parameter `Z` should have expectation zero, e.g. sum(w[i] * z[i] * z[i].T) - C
        if E z z.T = C.

        Parameter `eta` is the learning rate, for ``eta == 0`` nothing is updated.

        This function conducts two eigendecompositions, assuming that
        B and D are not up to date, unless `BDpair` is given. Given BDpair,
        B is the eigensystem and D is the vector of sqrt(eigenvalues), one
        eigendecomposition is omitted.

        Reference: Glasmachers et al 2010, Exponential Natural Evolution Strategies

        """
        if eta == 0:
            return
        if BDpair:
            B, D = BDpair
        else:
            D, B = self.opts['CMA_eigenmethod'](self.C)
            self.count_eigen += 1
            D **= 0.5
        Cs = dot(B, (B * D).T)   
        Csi = dot(B, (B / D).T)  
        self.C = dot(Cs, dot(Mh.expms(eta * dot(Csi, dot(Z, Csi)),
                                      self.opts['CMA_eigenmethod']), Cs))
        self.count_eigen += 1

    
    
    def feedForResume(self, X, function_values):
        """Given all "previous" candidate solutions and their respective
        function values, the state of a `CMAEvolutionStrategy` object
        can be reconstructed from this history. This is the purpose of
        function `feedForResume`.

        Arguments
        ---------
            `X`
              (all) solution points in chronological order, phenotypic
              representation. The number of points must be a multiple
              of popsize.
            `function_values`
              respective objective function values

        Details
        -------
        `feedForResume` can be called repeatedly with only parts of
        the history. The part must have the length of a multiple
        of the population size.
        `feedForResume` feeds the history in popsize-chunks into `tell`.
        The state of the random number generator might not be
        reconstructed, but this would be only relevant for the future.

        Example
        -------
        ::

            import cma

            
            (x0, sigma0) = ... 
            X = ... 
            f = ... 

            
            es = cma.CMAEvolutionStrategy(x0, sigma0)
            es.feedForResume(X, f)

            
            while not es.stop():
               X = es.ask()
               es.tell(X, [func(x) for x in X])

        Credits to Dirk Bueche and Fabrice Marchal for the feeding idea.

        :See: class `CMAEvolutionStrategy` for a simple dump/load to resume

        """
        if self.countiter > 0:
            _print_warning('feed should generally be used with a new object instance')
        if len(X) != len(function_values):
            raise _Error('number of solutions ' + str(len(X)) +
                ' and number function values ' +
                str(len(function_values)) + ' must not differ')
        popsize = self.sp.popsize
        if (len(X) % popsize) != 0:
            raise _Error('number of solutions ' + str(len(X)) +
                    ' must be a multiple of popsize (lambda) ' +
                    str(popsize))
        for i in rglen((X) / popsize):
            
            self.ask()  
                        
            self.tell(X[i * popsize:(i + 1) * popsize], function_values[i * popsize:(i + 1) * popsize])

    
    
    def readProperties(self):
        """reads dynamic parameters from property file (not implemented)
        """
        print('not yet implemented')

    
    
    def correlation_matrix(self):
        if len(self.C.shape) <= 1:
            return None
        c = self.C.copy()
        for i in range(c.shape[0]):
            fac = c[i, i]**0.5
            c[:, i] /= fac
            c[i, :] /= fac
        c = (c + c.T) / 2.0
        return c
    def mahalanobis_norm(self, dx):
        """compute the Mahalanobis norm that is induced by the adapted
        sample distribution, covariance matrix ``C`` times ``sigma**2``,
        including ``sigma_vec``. The expected Mahalanobis distance to
        the sample mean is about ``sqrt(dimension)``.

        Argument
        --------
        A *genotype* difference `dx`.

        Example
        -------
        >>> import cma, numpy
        >>> es = cma.CMAEvolutionStrategy(numpy.ones(10), 1)
        >>> xx = numpy.random.randn(2, 10)
        >>> d = es.mahalanobis_norm(es.gp.geno(xx[0]-xx[1]))

        `d` is the distance "in" the true sample distribution,
        sampled points have a typical distance of ``sqrt(2*es.N)``,
        where ``es.N`` is the dimension, and an expected distance of
        close to ``sqrt(N)`` to the sample mean. In the example,
        `d` is the Euclidean distance, because C = I and sigma = 1.

        """
        return sqrt(sum((self.D**-1. * np.dot(self.B.T, dx / self.sigma_vec))**2)) / self.sigma

    def _metric_when_multiplied_with_sig_vec(self, sig):
        """return D^-1 B^T diag(sig) B D as a measure for
        C^-1/2 diag(sig) C^1/2

        :param sig: a vector "used" as diagonal matrix
        :return:

        """
        return dot((self.B * self.D**-1.).T * sig, self.B * self.D)

    def disp_annotation(self):
        """print annotation for `disp()`"""
        print('Iterat 
        sys.stdout.flush()

    def disp(self, modulo=None):  
        """prints some single-line infos according to `disp_annotation()`,
        if ``iteration_counter % modulo == 0``

        """
        if modulo is None:
            modulo = self.opts['verb_disp']

        
        if modulo:
            if (self.countiter - 1) % (10 * modulo) < 1:
                self.disp_annotation()
            if self.countiter > 0 and (self.stop() or self.countiter < 4
                              or self.countiter % modulo < 1):
                if self.opts['verb_time']:
                    toc = self.elapsed_time()
                    stime = str(int(toc // 60)) + ':' + str(round(toc % 60, 1))
                else:
                    stime = ''
                print(' '.join((repr(self.countiter).rjust(5),
                                repr(self.countevals).rjust(6),
                                '%.15e' % (min(self.fit.fit)),
                                '%4.1e' % (self.D.max() / self.D.min()),
                                '%6.2e' % self.sigma,
                                '%6.0e' % (self.sigma * min(self.sigma_vec * sqrt(self.dC))),
                                '%6.0e' % (self.sigma * max(self.sigma_vec * sqrt(self.dC))),
                                stime)))
                
                sys.stdout.flush()
        return self
    def plot(self):
        try:
            self.logger.plot()
        except AttributeError:
            _print_warning('plotting failed, no logger attribute found')
        except:
            _print_warning(('plotting failed with:', sys.exc_info()[0]),
                           'plot', 'CMAEvolutionStrategy')
        return self

cma_default_options = {
    "filename"
    'AdaptSigma': 'CMAAdaptSigmaCSA  
    'CMA_active': 'True  

    'CMA_cmean': '1  
    'CMA_const_trace': 'False  
    'CMA_diagonal': '0*100*N/sqrt(popsize)  
    'CMA_eigenmethod': 'np.linalg.eigh  
    'CMA_elitist': 'False  "initial" or True, elitism likely impairs global search performance',
    'CMA_mirrors': 'popsize < 6  
    'CMA_mirrormethod': '1  
    'CMA_mu': 'None  
    'CMA_on': 'True  
    'CMA_sample_on_sphere_surface': 'False  
    'CMA_rankmu': 'True  
    'CMA_rankmualpha': '0.3  
    'CMA_dampsvec_fac': 'np.Inf  "default" damping for sigma vector update',
    'CMA_dampsvec_fade': '0.1  
    'CMA_teststds': 'None  
    'CMA_stds': 'None  
    
    'CSA_dampfac': '1  
    'CSA_damp_mueff_exponent': '0.5  
    'CSA_disregard_length': 'False  
    'CSA_clip_length_value': 'None  
    'CSA_squared': 'False  
    'boundary_handling': 'BoundTransform  
    'bounds': '[None, None]  
     "processes": None, "timeout": 12, "is_feasible": lambda x: True} 
    'fixed_variables': 'None  
    'ftarget': '-inf  
    'is_feasible': 'is_feasible  
    'maxfevals': 'inf  
    'maxiter': '100 + 50 * (N+3)**2 // popsize**0.5  
    'mean_shift_line_samples': 'False 
    'mindx': '0  
    'minstd': '0  
    'maxstd': 'inf  
    'pc_line_samples': 'False 
    'popsize': '4+int(3*log(N))  
    'randn': 'np.random.standard_normal  
    'scaling_of_variables': 'None  
    'seed': 'None  
    'signals_filename': 'cmaes_signals.par  "stop now"',
    'termination_callback': 'None  
    'tolfacupx': '1e3  
    'tolupsigma': '1e20  "creeping behavior" with usually minor improvements',
    'tolfun': '1e-11  
    'tolfunhist': '1e-12  
    'tolstagnation': 'int(100 + 100 * N**1.5 / popsize)  
    'tolx': '1e-11  
    'transformation': 'None  
    'typical_x': 'None  
    'updatecovwait': 'None  
    'verbose': '1  
    'verb_append': '0  
    'verb_disp': '100  
    'verb_filenameprefix': 'outcmaes  
    'verb_log': '1  
    'verb_plot': '0  
    'verb_time': 'True  
    'vv': '0  "vv"]'
}
class CMAOptions(dict):
    """``CMAOptions()`` returns a dictionary with the available options
    and their default values for class ``CMAEvolutionStrategy``.

    ``CMAOptions('pop')`` returns a subset of recognized options that
    contain 'pop' in there keyword name or (default) value or description.

    ``CMAOptions(opts)`` returns the subset of recognized options in
    ``dict(opts)``.

    Option values can be "written" in a string and, when passed to fmin
    or CMAEvolutionStrategy, are evaluated using "N" and "popsize" as
    known values for dimension and population size (sample size, number
    of new solutions per iteration). All default option values are such
    a string.

    Details
    -------
    ``CMAOptions`` entries starting with ``tol`` are termination
    "tolerances".

    For `tolstagnation`, the median over the first and the second half
    of at least `tolstagnation` iterations are compared for both, the
    per-iteration best and per-iteration median function value.

    Example
    -------
    ::

        import cma
        cma.CMAOptions('tol')

    is a shortcut for cma.CMAOptions().match('tol') that returns all options
    that contain 'tol' in their name or description.

    To set an option

        import cma
        opts = cma.CMAOptions()
        opts.set('tolfun', 1e-12)
        opts['tolx'] = 1e-11

    :See: `fmin`(), `CMAEvolutionStrategy`, `_CMAParameters`

    """

    
    
    
    """returns all options with defaults"""
    

    @staticmethod
    def defaults():
        """return a dictionary with default option values and description"""
        return dict((str(k), str(v)) for k, v in list(cma_default_options.items()))
        "name" by str(u"name")
        

    @staticmethod
    def versatile_options():
        """return list of options that can be changed at any time (not
        only be initialized), however the list might not be entirely up
        to date.

        The string ' 
        option that can be changed any time.

        """
        return tuple(sorted(i[0] for i in list(CMAOptions.defaults().items()) if i[1].find(' 
    def check(self, options=None):
        """check for ambiguous keys and move attributes into dict"""
        self.check_values(options)
        self.check_attributes(options)
        self.check_values(options)
        return self
    def check_values(self, options=None):
        corrected_key = CMAOptions().corrected_key  
        validated_keys = []
        original_keys = []
        if options is None:
            options = self
        for key in options:
            correct_key = corrected_key(key)
            if correct_key is None:
                raise ValueError("""%s is not a valid option""" % key)
            if correct_key in validated_keys:
                if key == correct_key:
                    key = original_keys[validated_keys.index(key)]
                raise ValueError("%s was not a unique key for %s option"
                    % (key, correct_key))
            validated_keys.append(correct_key)
            original_keys.append(key)
        return options
    def check_attributes(self, opts=None):
        """check for attributes and moves them into the dictionary"""
        if opts is None:
            opts = self
        if 1 < 3:
        
        
        
            if hasattr(opts, '__dict__'):
                for key in list(opts.__dict__):
                    if key in self._attributes:
                        continue
                    _print_warning(
                        """
        An option attribute has been merged into the dictionary,
        thereby possibly overwriting the dictionary value, and the
        attribute has been removed. Assign options with

            ``opts['%s'] = value``  

        or use

            ``opts.set('%s', value)  

        instead of

            ``opts.%s = value``  
                        """ % (key, key, key), 'check', 'CMAOptions')

                    opts[key] = opts.__dict__[key]  
                    delattr(opts, key)  
                    
                    
            return opts

    @staticmethod
    def merge(self, dict_=None):
        """not is use so far, see check()"""
        if dict_ is None and hasattr(self, '__dict__'):
            dict_ = self.__dict__  
            
        if dict_ is None:
            return self
        self.update(dict_)
        return self

    def __init__(self, s=None, unchecked=False):
        """return an `CMAOptions` instance, either with the default
        options, if ``s is None``, or with all options whose name or
        description contains `s`, if `s` is a string (case is
        disregarded), or with entries from dictionary `s` as options,
        not complemented with default options or settings

        Returns: see above.

        """
        
        
        if s is None:
            super(CMAOptions, self).__init__(CMAOptions.defaults())  
            
        elif isinstance(s, str):
            super(CMAOptions, self).__init__(CMAOptions().match(s))
            
        else:
            super(CMAOptions, self).__init__(s)

        if not unchecked and s is not None:
            self.check()  
            for key in list(self.keys()):
                correct_key = self.corrected_key(key)
                if correct_key not in CMAOptions.defaults():
                    _print_warning('invalid key ``' + str(key) +
                                   '`` removed', '__init__', 'CMAOptions')
                    self.pop(key)
                elif key != correct_key:
                    self[correct_key] = self.pop(key)
        
        self._lock_setting = False
        self._attributes = self.__dict__.copy()  
        self._attributes['_attributes'] = len(self._attributes)

    def init(self, dict_or_str, val=None, warn=True):
        """initialize one or several options.

        Arguments
        ---------
            `dict_or_str`
                a dictionary if ``val is None``, otherwise a key.
                If `val` is provided `dict_or_str` must be a valid key.
            `val`
                value for key

        Details
        -------
        Only known keys are accepted. Known keys are in `CMAOptions.defaults()`

        """
        
        self.check(dict_or_str)
        dic = dict_or_str
        if val is not None:
            dic = {dict_or_str:val}

        for key, val in list(dic.items()):
            key = self.corrected_key(key)
            if key not in CMAOptions.defaults():
                
                if warn:
                    print('Warning in cma.CMAOptions.init(): key ' +
                        str(key) + ' ignored')
            else:
                self[key] = val

        return self

    def set(self, dic, val=None, force=False):
        """set can assign versatile options from
        `CMAOptions.versatile_options()` with a new value, use `init()`
        for the others.

        Arguments
        ---------
            `dic`
                either a dictionary or a key. In the latter
                case, `val` must be provided
            `val`
                value for `key`, approximate match is sufficient
            `force`
                force setting of non-versatile options, use with caution

        This method will be most probably used with the ``opts`` attribute of
        a `CMAEvolutionStrategy` instance.

        """
        if val is not None:  
            dic = {dic:val}  
        for key_original, val in list(dict(dic).items()):
            key = self.corrected_key(key_original)
            if not self._lock_setting or \
                            key in CMAOptions.versatile_options():
                self[key] = val
            else:
                _print_warning('key ' + str(key_original) +
                      ' ignored (not recognized as versatile)',
                               'set', 'CMAOptions')
        return self  

    def complement(self):
        """add all missing options with their default values"""

        
        self.check()
        for key in CMAOptions.defaults():
            if key not in self:
                self[key] = CMAOptions.defaults()[key]
        return self

    def settable(self):
        """return the subset of those options that are settable at any
        time.

        Settable options are in `versatile_options()`, but the
        list might be incomplete.

        """
        return CMAOptions([i for i in list(self.items())
                                if i[0] in CMAOptions.versatile_options()])

    def __call__(self, key, default=None, loc=None):
        """evaluate and return the value of option `key` on the fly, or
        returns those options whose name or description contains `key`,
        case disregarded.

        Details
        -------
        Keys that contain `filename` are not evaluated.
        For ``loc==None``, `self` is used as environment
        but this does not define ``N``.

        :See: `eval()`, `evalall()`

        """
        try:
            val = self[key]
        except:
            return self.match(key)

        if loc is None:
            loc = self  
        try:
            if isinstance(val, str):
                val = val.split('
                if isinstance(val, str) and \
                        key.find('filename') < 0:
                        
                    val = eval(val, globals(), loc)
            
            
            
            elif val is None and default is not None:
                val = eval(str(default), globals(), loc)
        except:
            pass  
        return val

    def corrected_key(self, key):
        """return the matching valid key, if ``key.lower()`` is a unique
        starting sequence to identify the valid key, ``else None``

        """
        matching_keys = []
        for allowed_key in CMAOptions.defaults():
            if allowed_key.lower() == key.lower():
                return allowed_key
            if allowed_key.lower().startswith(key.lower()):
                matching_keys.append(allowed_key)
        return matching_keys[0] if len(matching_keys) == 1 else None

    def eval(self, key, default=None, loc=None, correct_key=True):
        """Evaluates and sets the specified option value in
        environment `loc`. Many options need ``N`` to be defined in
        `loc`, some need `popsize`.

        Details
        -------
        Keys that contain 'filename' are not evaluated.
        For `loc` is None, the self-dict is used as environment

        :See: `evalall()`, `__call__`

        """
        
        if correct_key:
            
            key = self.corrected_key(key)
        self[key] = self(key, default, loc)
        return self[key]

    def evalall(self, loc=None, defaults=None):
        """Evaluates all option values in environment `loc`.

        :See: `eval()`

        """
        self.check()
        if defaults is None:
            defaults = cma_default_options
        
        if 'N' in loc:  
            popsize = self('popsize', defaults['popsize'], loc)
            for k in list(self.keys()):
                k = self.corrected_key(k)
                self.eval(k, defaults[k],
                          {'N':loc['N'], 'popsize':popsize})
        self._lock_setting = True
        return self

    def match(self, s=''):
        """return all options that match, in the name or the description,
        with string `s`, case is disregarded.

        Example: ``cma.CMAOptions().match('verb')`` returns the verbosity
        options.

        """
        match = s.lower()
        res = {}
        for k in sorted(self):
            s = str(k) + '=\'' + str(self[k]) + '\''
            if match in s.lower():
                res[k] = self[k]
        return CMAOptions(res, unchecked=True)

    def pp(self):
        pprint(self)

    def pprint(self, linebreak=80):
        for i in sorted(self.items()):
            s = str(i[0]) + "='" + str(i[1]) + "'"
            a = s.split(' ')

            
            l = ''  
            while a:
                while a and len(l) + len(a[0]) < linebreak:
                    l += ' ' + a.pop(0)
                print(l)
                l = '        '  
    print_ = pprint  
    printme = pprint



class _CMAStopDict(dict):
    """keep and update a termination condition dictionary, which is
    "usually" empty and returned by `CMAEvolutionStrategy.stop()`.
    The class methods entirely depend on `CMAEvolutionStrategy` class
    attributes.

    Details
    -------
    This class is not relevant for the end-user and could be a nested
    class, but nested classes cannot be serialized.

    Example
    -------
    >>> import cma
    >>> es = cma.CMAEvolutionStrategy(4 * [1], 1, {'verbose':-1})
    >>> print(es.stop())
    {}
    >>> es.optimize(cma.fcts.sphere, verb_disp=0)
    >>> print(es.stop())
    {'tolfun': 1e-11}

    :See: `OOOptimizer.stop()`, `CMAEvolutionStrategy.stop()`

    """
    def __init__(self, d={}):
        update = isinstance(d, CMAEvolutionStrategy)
        super(_CMAStopDict, self).__init__({} if update else d)
        self._stoplist = []  
        self.lastiter = 0  
        if isinstance(d, _CMAStopDict):  
            self._stoplist = d._stoplist  
            self.lastiter = d.lastiter    
        if update:
            self._update(d)

    def __call__(self, es=None, check=True):
        """update and return the termination conditions dictionary

        """
        if not check:
            return self
        if es is None and self.es is None:
            raise ValueError('termination conditions need an optimizer to act upon')
        self._update(es)
        return self

    def _update(self, es):
        """Test termination criteria and update dictionary

        """
        if es is None:
            es = self.es
        assert es is not None

        if es.countiter == 0:  
            self.__init__()
            return self

        self.lastiter = es.countiter
        self.es = es

        self.clear()  

        N = es.N
        opts = es.opts
        self.opts = opts  

        
        self._addstop('ftarget',
                      es.best.f < opts['ftarget'])
        
        self._addstop('maxfevals',
                      es.countevals - 1 >= opts['maxfevals'])
        self._addstop('maxiter',
                      
                      es.countiter >= 1.0 * opts['maxiter'])
        
        
        self._addstop('tolx',
                      all([es.sigma * xi < opts['tolx'] for xi in es.sigma_vec * es.pc]) and
                      all([es.sigma * xi < opts['tolx'] for xi in es.sigma_vec * sqrt(es.dC)]))
        self._addstop('tolfacupx',
                      any(es.sigma * es.sigma_vec * sqrt(es.dC) >
                          es.sigma0 * es.sigma_vec0 * opts['tolfacupx']))
        self._addstop('tolfun',
                      es.fit.fit[-1] - es.fit.fit[0] < opts['tolfun'] and
                      max(es.fit.hist) - min(es.fit.hist) < opts['tolfun'])
        self._addstop('tolfunhist',
                      len(es.fit.hist) > 9 and
                      max(es.fit.hist) - min(es.fit.hist) < opts['tolfunhist'])

        
        
        
        
        
        l = int(max(( 1.0 * opts['tolstagnation'] / 5. / 2, len(es.fit.histbest) / 10)))
        
        
        
        self._addstop('tolstagnation',  
                      1 < 3 and opts['tolstagnation'] and es.countiter > N * (5 + 100 / es.popsize) and
                      len(es.fit.histbest) > 100 and 2 * l < len(es.fit.histbest) and
                      np.median(es.fit.histmedian[:l]) >= np.median(es.fit.histmedian[l:2 * l]) and
                      np.median(es.fit.histbest[:l]) >= np.median(es.fit.histbest[l:2 * l]))
        

        self._addstop('tolupsigma', opts['tolupsigma'] and
                      es.sigma / np.max(es.D) > es.sigma0 * opts['tolupsigma'])

        if 1 < 3:
            
            
            idx = np.where(es.mean == es.mean + 0.2 * es.sigma *
                                    es.sigma_vec * es.dC**0.5)[0]
            self._addstop('noeffectcoord', any(idx), idx)





            if opts['CMA_diagonal'] is not True and es.countiter > opts['CMA_diagonal']:
                i = es.countiter % N
                self._addstop('noeffectaxis',
                             sum(es.mean == es.mean + 0.1 * es.sigma * es.D[i] * es.B[:, i]) == N)
            self._addstop('conditioncov',
                         es.D[-1] > 1e7 * es.D[0], 1e14)  

            self._addstop('callback', es.callbackstop)  
        try:
            with open(self.opts['signals_filename'], 'r') as f:
                for line in f.readlines():
                    words = line.split()
                    if len(words) < 2 or words[0].startswith(('
                        continue
                    if words[0] == 'stop' and words[1] == 'now':
                        if len(words) > 2 and not words[2].startswith(
                                self.opts['verb_filenameprefix']):
                            continue
                        self._addstop('file_signal', True, "stop now")
                        break
        except IOError:
            pass

        if len(self):
            self._addstop('flat fitness: please (re)consider how to compute the fitness more elaborate',
                         len(es.fit.hist) > 9 and
                         max(es.fit.hist) == min(es.fit.hist))
        return self

    def _addstop(self, key, cond, val=None):
        if cond:
            self.stoplist.append(key)  
            self[key] = val if val is not None \
                            else self.opts.get(key, None)

    def clear(self):
        for k in list(self):
            self.pop(k)
        self.stoplist = []



class _CMAParameters(object):
    """strategy parameters like population size and learning rates.

    Note:
        contrary to `CMAOptions`, `_CMAParameters` is not (yet) part of the
        "user-interface" and subject to future changes (it might become
        a `collections.namedtuple`)

    Example
    -------
    >>> import cma
    >>> es = cma.CMAEvolutionStrategy(20 * [0.1], 1)
    (6_w,12)-CMA-ES (mu_w=3.7,w_1=40%) in dimension 20 (seed=504519190)  "random" by default
    >>>
    >>> type(es.sp)  
    <class 'cma._CMAParameters'>
    >>>
    >>> es.sp.disp()
    {'CMA_on': True,
     'N': 20,
     'c1': 0.004181139918745593,
     'c1_sep': 0.034327992810300939,
     'cc': 0.17176721127681213,
     'cc_sep': 0.25259494835857677,
     'cmean': 1.0,
     'cmu': 0.0085149624979034746,
     'cmu_sep': 0.057796356229390715,
     'cs': 0.21434997799189287,
     'damps': 1.2143499779918929,
     'mu': 6,
     'mu_f': 6.0,
     'mueff': 3.7294589343030671,
     'popsize': 12,
     'rankmualpha': 0.3,
     'weights': array([ 0.40240294,  0.25338908,  0.16622156,  0.10437523,  0.05640348,
            0.01720771])}
    >>>
    >> es.sp == cma._CMAParameters(20, 12, cma.CMAOptions().evalall({'N': 20}))
    True

    :See: `CMAOptions`, `CMAEvolutionStrategy`

    """
    def __init__(self, N, opts, ccovfac=1, verbose=True):
        """Compute strategy parameters, mainly depending on
        dimension and population size, by calling `set`

        """
        self.N = N
        if ccovfac == 1:
            ccovfac = opts['CMA_on']  
        self.popsize = None  
        self.set(opts, ccovfac=ccovfac, verbose=verbose)

    def set(self, opts, popsize=None, ccovfac=1, verbose=True):
        """Compute strategy parameters as a function
        of dimension and population size """

        alpha_cc = 1.0  

        def conedf(df, mu, N):
            """used for computing separable learning rate"""
            return 1. / (df + 2.*sqrt(df) + float(mu) / N)

        def cmudf(df, mu, alphamu):
            """used for computing separable learning rate"""
            return (alphamu + mu - 2. + 1. / mu) / (df + 4.*sqrt(df) + mu / 2.)

        sp = self
        N = sp.N
        if popsize:
            opts.evalall({'N':N, 'popsize':popsize})
        else:
            popsize = opts.evalall({'N':N})['popsize']  
        
        popsize = int(popsize + N** 0.0 - 1)
        sp.popsize = popsize
        if opts['CMA_mirrors'] < 0.5:
            sp.lam_mirr = int(0.5 + opts['CMA_mirrors'] * popsize)
        elif opts['CMA_mirrors'] > 1:
            sp.lam_mirr = int(0.5 + opts['CMA_mirrors'])
        else:
            sp.lam_mirr = int(0.5 + 0.16 * min((popsize, 2 * N + 2)) + 0.29)  
            
            
            
            
            
        
        sp.mu_f = 0.5 * sp.popsize  
        if opts['CMA_mu'] is not None:
            sp.mu_f = opts['CMA_mu']
        sp.mu = int(sp.mu_f + 0.499999)  
        sp.mu = max((sp.mu, 1))
        
        
        if sp.mu > sp.popsize - 2 * sp.lam_mirr + 1:
            _print_warning("pairwise selection is not implemented, therefore " +
                  " mu = %d > %d = %d - 2*%d + 1 = popsize - 2*mirr + 1 can produce a bias" % (
                    sp.mu, sp.popsize - 2 * sp.lam_mirr + 1, sp.popsize, sp.lam_mirr))
        if sp.lam_mirr > sp.popsize // 2:
            raise _Error("fraction of mirrors in the population as read from option CMA_mirrors cannot be larger 0.5, " +
                         "theoretically optimal is 0.159")
        sp.weights = log(max([sp.mu, sp.popsize / 2.0]) + 0.5) - log(1 + np.arange(sp.mu))
        sp.weights /= sum(sp.weights)
        sp.mueff = 1 / sum(sp.weights**2)
        
        
        b = 1.0
        
        sp.cs = 1.0 * (sp.mueff + 2)**b / (N + (sp.mueff + 3)**b)  
        
        
        b = 1.0
        
        sp.cc = 1.0 * \
                (4 + alpha_cc * sp.mueff / N)**b / \
                (N**b + (4 + alpha_cc * 2 * sp.mueff / N)**b)
        sp.cc_sep = (1 + 1 / N + alpha_cc * sp.mueff / N) / (N**0.5 + 1 / N + alpha_cc * 2 * sp.mueff / N)  
        if hasattr(opts['vv'], '__getitem__') and opts['vv'][0] == 'sweep_ccov1':
            
            sp.cc = 1.0 * (4 + sp.mueff / N)**0.5 / ((N + 4)**0.5 + (2 * sp.mueff / N)**0.5)
        sp.rankmualpha = opts['CMA_rankmualpha']
        
        
        sp.c1 = ( 1.0 * ccovfac * min(1, sp.popsize / 6) *
                 
                 2 / ((N + 1.3)** 2.0 + sp.mueff))
        
        sp.c1_sep = ccovfac * conedf(N, sp.mueff, N)
        if opts['CMA_rankmu'] != 0:  
            
            alphacov, mu = 2.0 , sp.mueff
            sp.cmu = min(1 - sp.c1, ccovfac * alphacov *
                         
                         (sp.rankmualpha + mu - 2 + 1 / mu) / ((N + 2)** 2.0 + alphacov * mu / 2))
            if hasattr(opts['vv'], '__getitem__') and opts['vv'][0] == 'sweep_ccov':
                sp.cmu = opts['vv'][1]
            sp.cmu_sep = min(1 - sp.c1_sep, ccovfac * cmudf(N, sp.mueff, sp.rankmualpha))
        else:
            sp.cmu = sp.cmu_sep = 0
        if hasattr(opts['vv'], '__getitem__') and opts['vv'][0] == 'sweep_ccov1':
            sp.c1 = opts['vv'][1]

        sp.neg = _BlancClass()
        if opts['CMA_active'] and opts['CMA_on']:
            
            
            if 1 < 3: 
                sp.neg.mu_f = popsize // 2  
                sp.neg.weights = array([log(k) - log(popsize/2 + 1/2) for k in np.arange(np.ceil(popsize/2 + 1.1/2), popsize + .1)])
            sp.neg.mu = len(sp.neg.weights)
            sp.neg.weights /= sum(sp.neg.weights)
            sp.neg.mueff = 1 / sum(sp.neg.weights**2)
            
            sp.neg.cmuexp = opts['CMA_active'] * 0.3 * sp.neg.mueff / ((N + 2)** 1.5 + 1.0 * sp.neg.mueff)
            if hasattr(opts['vv'], '__getitem__') and opts['vv'][0] == 'sweep_ccov_neg':
                sp.neg.cmuexp = opts['vv'][1]
            
            
            
            assert sp.neg.mu >= sp.lam_mirr  
            
        else:
            sp.neg.cmuexp = 0

        sp.CMA_on = sp.c1 + sp.cmu > 0
        

        if not opts['CMA_on'] and opts['CMA_on'] not in (None, [], (), ''):
            sp.CMA_on = False
            
        mueff_exponent = 0.5
        if 1 < 3:
            mueff_exponent = opts['CSA_damp_mueff_exponent']
        
        sp.damps = opts['CSA_dampfac'] * (0.5 +
                                          0.5 * min([1, (sp.lam_mirr / (0.159 * sp.popsize) - 1)**2])**1 +
                                          2 * max([0, ((sp.mueff - 1) / (N + 1))**mueff_exponent - 1]) + sp.cs
                                          )
        sp.cmean = float(opts['CMA_cmean'])
        
                        
        if verbose:
            if not sp.CMA_on:
                print('covariance matrix adaptation turned off')
            if opts['CMA_mu'] != None:
                print('mu = %f' % (sp.mu_f))

        

    def disp(self):
        pprint(self.__dict__)

def fmin(objective_function, x0, sigma0,
         options=None,
         args=(),
         gradf=None,
         restarts=0,
         restart_from_best='False',
         incpopsize=2,
         eval_initial_x=False,
         noise_handler=None,
         noise_change_sigma_exponent=1,
         noise_kappa_exponent=0,  
         bipop=False):
    """functional interface to the stochastic optimizer CMA-ES
    for non-convex function minimization.

    Calling Sequences
    =================
        ``fmin(objective_function, x0, sigma0)``
            minimizes `objective_function` starting at `x0` and with standard deviation
            `sigma0` (step-size)
        ``fmin(objective_function, x0, sigma0, options={'ftarget': 1e-5})``
            minimizes `objective_function` up to target function value 1e-5, which
            is typically useful for benchmarking.
        ``fmin(objective_function, x0, sigma0, args=('f',))``
            minimizes `objective_function` called with an additional argument ``'f'``.
        ``fmin(objective_function, x0, sigma0, options={'ftarget':1e-5, 'popsize':40})``
            uses additional options ``ftarget`` and ``popsize``
        ``fmin(objective_function, esobj, None, options={'maxfevals': 1e5})``
            uses the `CMAEvolutionStrategy` object instance `esobj` to optimize
            `objective_function`, similar to `esobj.optimize()`.

    Arguments
    =========
        `objective_function`
            function to be minimized. Called as ``objective_function(x,
            *args)``. `x` is a one-dimensional `numpy.ndarray`.
            `objective_function` can return `numpy.NaN`,
            which is interpreted as outright rejection of solution `x`
            and invokes an immediate resampling and (re-)evaluation
            of a new solution not counting as function evaluation.
        `x0`
            list or `numpy.ndarray`, initial guess of minimum solution
            before the application of the geno-phenotype transformation
            according to the ``transformation`` option.  It can also be
            a string holding a Python expression that is evaluated
            to yield the initial guess - this is important in case
            restarts are performed so that they start from different
            places.  Otherwise `x0` can also be a `cma.CMAEvolutionStrategy`
            object instance, in that case `sigma0` can be ``None``.
        `sigma0`
            scalar, initial standard deviation in each coordinate.
            `sigma0` should be about 1/4th of the search domain width
            (where the optimum is to be expected). The variables in
            `objective_function` should be scaled such that they
            presumably have similar sensitivity.
            See also option `scaling_of_variables`.
        `options`
            a dictionary with additional options passed to the constructor
            of class ``CMAEvolutionStrategy``, see ``cma.CMAOptions()``
            for a list of available options.
        ``args=()``
            arguments to be used to call the `objective_function`
        ``gradf``
            gradient of f, where ``len(gradf(x, *args)) == len(x)``.
            `gradf` is called once in each iteration if
            ``gradf is not None``.
        ``restarts=0``
            number of restarts with increasing population size, see also
            parameter `incpopsize`, implementing the IPOP-CMA-ES restart
            strategy, see also parameter `bipop`; to restart from
            different points (recommended), pass `x0` as a string.
        ``restart_from_best=False``
            which point to restart from
        ``incpopsize=2``
            multiplier for increasing the population size `popsize` before
            each restart
        ``eval_initial_x=None``
            evaluate initial solution, for `None` only with elitist option
        ``noise_handler=None``
            a ``NoiseHandler`` instance or ``None``, a simple usecase is
            ``cma.fmin(f, 6 * [1], 1, noise_handler=cma.NoiseHandler(6))``
            see ``help(cma.NoiseHandler)``.
        ``noise_change_sigma_exponent=1``
            exponent for sigma increment for additional noise treatment
        ``noise_evaluations_as_kappa``
            instead of applying reevaluations, the "number of evaluations"
            is (ab)used as scaling factor kappa (experimental).
        ``bipop``
            if True, run as BIPOP-CMA-ES; BIPOP is a special restart
            strategy switching between two population sizings - small
            (like the default CMA, but with more focused search) and
            large (progressively increased as in IPOP). This makes the
            algorithm perform well both on functions with many regularly
            or irregularly arranged local optima (the latter by frequently
            restarting with small populations).  For the `bipop` parameter
            to actually take effect, also select non-zero number of
            (IPOP) restarts; the recommended setting is ``restarts<=9``
            and `x0` passed as a string.  Note that small-population
            restarts do not count into the total restart count.

    Optional Arguments
    ==================
    All values in the `options` dictionary are evaluated if they are of
    type `str`, besides `verb_filenameprefix`, see class `CMAOptions` for
    details. The full list is available via ``cma.CMAOptions()``.

    >>> import cma
    >>> cma.CMAOptions()

    Subsets of options can be displayed, for example like
    ``cma.CMAOptions('tol')``, or ``cma.CMAOptions('bound')``,
    see also class `CMAOptions`.

    Return
    ======
    Return the list provided by `CMAEvolutionStrategy.result()` appended
    with termination conditions, an `OOOptimizer` and a `BaseDataLogger`::

        res = es.result() + (es.stop(), es, logger)

    where
        - ``res[0]`` (``xopt``) -- best evaluated solution
        - ``res[1]`` (``fopt``) -- respective function value
        - ``res[2]`` (``evalsopt``) -- respective number of function evaluations
        - ``res[3]`` (``evals``) -- number of overall conducted objective function evaluations
        - ``res[4]`` (``iterations``) -- number of overall conducted iterations
        - ``res[5]`` (``xmean``) -- mean of the final sample distribution
        - ``res[6]`` (``stds``) -- effective stds of the final sample distribution
        - ``res[-3]`` (``stop``) -- termination condition(s) in a dictionary
        - ``res[-2]`` (``cmaes``) -- class `CMAEvolutionStrategy` instance
        - ``res[-1]`` (``logger``) -- class `CMADataLogger` instance

    Details
    =======
    This function is an interface to the class `CMAEvolutionStrategy`. The
    latter class should be used when full control over the iteration loop
    of the optimizer is desired.

    Examples
    ========
    The following example calls `fmin` optimizing the Rosenbrock function
    in 10-D with initial solution 0.1 and initial step-size 0.5. The
    options are specified for the usage with the `doctest` module.

    >>> import cma
    >>> 
    >>> options = {'CMA_diagonal':100, 'seed':1234, 'verb_time':0}
    >>>
    >>> res = cma.fmin(cma.fcts.rosen, [0.1] * 10, 0.5, options)
    (5_w,10)-CMA-ES (mu_w=3.2,w_1=45%) in dimension 10 (seed=1234)
       Covariance matrix is diagonal for 10 iterations (1/ccov=29.0)
    Iterat 
        1      10 1.264232686260072e+02 1.1e+00 4.40e-01  4e-01  4e-01
        2      20 1.023929748193649e+02 1.1e+00 4.00e-01  4e-01  4e-01
        3      30 1.214724267489674e+02 1.2e+00 3.70e-01  3e-01  4e-01
      100    1000 6.366683525319511e+00 6.2e+00 2.49e-02  9e-03  3e-02
      200    2000 3.347312410388666e+00 1.2e+01 4.52e-02  8e-03  4e-02
      300    3000 1.027509686232270e+00 1.3e+01 2.85e-02  5e-03  2e-02
      400    4000 1.279649321170636e-01 2.3e+01 3.53e-02  3e-03  3e-02
      500    5000 4.302636076186532e-04 4.6e+01 4.78e-03  3e-04  5e-03
      600    6000 6.943669235595049e-11 5.1e+01 5.41e-06  1e-07  4e-06
      650    6500 5.557961334063003e-14 5.4e+01 1.88e-07  4e-09  1e-07
    termination on tolfun : 1e-11
    final/bestever f-value = 5.55796133406e-14 2.62435631419e-14
    mean solution:  [ 1.          1.00000001  1.          1.
        1.          1.00000001  1.00000002  1.00000003 ...]
    std deviation: [ 3.9193387e-09  3.7792732e-09  4.0062285e-09  4.6605925e-09
        5.4966188e-09   7.4377745e-09   1.3797207e-08   2.6020765e-08 ...]
    >>>
    >>> print('best solutions fitness = %f' % (res[1]))
    best solutions fitness = 2.62435631419e-14
    >>> assert res[1] < 1e-12

    The above call is pretty much equivalent with the slightly more
    verbose call::

        es = cma.CMAEvolutionStrategy([0.1] * 10, 0.5,
                    options=options).optimize(cma.fcts.rosen)

    The following example calls `fmin` optimizing the Rastrigin function
    in 3-D with random initial solution in [-2,2], initial step-size 0.5
    and the BIPOP restart strategy (that progressively increases population).
    The options are specified for the usage with the `doctest` module.

    >>> import cma
    >>> 
    >>> options = {'seed':12345, 'verb_time':0, 'ftarget': 1e-8}
    >>>
    >>> res = cma.fmin(cma.fcts.rastrigin, '2. * np.random.rand(3) - 1', 0.5,
    ...                options, restarts=9, bipop=True)
    (3_w,7)-aCMA-ES (mu_w=2.3,w_1=58%) in dimension 3 (seed=12345)
    Iterat 
        1       7 1.633489455763566e+01 1.0e+00 4.35e-01  4e-01  4e-01
        2      14 9.762462950258016e+00 1.2e+00 4.12e-01  4e-01  4e-01
        3      21 2.461107851413725e+01 1.4e+00 3.78e-01  3e-01  4e-01
      100     700 9.949590571272680e-01 1.7e+00 5.07e-05  3e-07  5e-07
      123     861 9.949590570932969e-01 1.3e+00 3.93e-06  9e-09  1e-08
    termination on tolfun=1e-11
    final/bestever f-value = 9.949591e-01 9.949591e-01
    mean solution: [  9.94958638e-01  -7.19265205e-10   2.09294450e-10]
    std deviation: [  8.71497860e-09   8.58994807e-09   9.85585654e-09]
    [...]
    (4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 3 (seed=12349)
    Iterat 
        1  5342.0 2.114883315350800e+01 1.0e+00 3.42e-02  3e-02  4e-02
        2  5351.0 1.810102940125502e+01 1.4e+00 3.79e-02  3e-02  4e-02
        3  5360.0 1.340222457448063e+01 1.4e+00 4.58e-02  4e-02  6e-02
       50  5783.0 8.631491965616078e-09 1.6e+00 2.01e-04  8e-06  1e-05
    termination on ftarget=1e-08 after 4 restarts
    final/bestever f-value = 8.316963e-09 8.316963e-09
    mean solution: [ -3.10652459e-06   2.77935436e-06  -4.95444519e-06]
    std deviation: [  1.02825265e-05   8.08348144e-06   8.47256408e-06]

    In either case, the method::

        cma.plot();

    (based on `matplotlib.pyplot`) produces a plot of the run and, if
    necessary::

        cma.show()

    shows the plot in a window. Finally::

        cma.savefig('myfirstrun')  

    will save the figure in a png.

    We can use the gradient like

    >>> import cma
    >>> res = cma.fmin(cma.fcts.rosen, np.zeros(10), 0.1,
    ...             options = {'ftarget':1e-8,},
    ...             gradf=cma.fcts.grad_rosen,
    ...         )
    >>> assert cma.fcts.rosen(res[0]) < 1e-8
    >>> assert res[2] < 3600  
    >>> assert res[3] < 3600  

    :See: `CMAEvolutionStrategy`, `OOOptimizer.optimize(), `plot()`,
        `CMAOptions`, `scipy.optimize.fmin()`

    """  
    if 1 < 3:  
        if not objective_function:  
            return CMAOptions()  

        fmin_options = locals().copy()  
        del fmin_options['objective_function']
        del fmin_options['x0']
        del fmin_options['sigma0']
        del fmin_options['options']
        del fmin_options['args']

        if options is None:
            options = cma_default_options
        CMAOptions().check_attributes(options)  
        
        opts = CMAOptions(options.copy()).complement()

        
        runs_with_small = 0
        small_i = []
        large_i = []
        popsize0 = None  
        maxiter0 = None  
        base_evals = 0

        irun = 0
        best = BestSolution()
        while True:  
            sigma_factor = 1

            
            if not bipop:
                
                
                if irun > 0:
                    popsize_multiplier = fmin_options['incpopsize'] ** (irun - runs_with_small)
                    opts['popsize'] = popsize0 * popsize_multiplier

            elif irun == 0:
                "normal" population size; it is
                
                
                
                poptype = 'small'

            elif sum(small_i) < sum(large_i):
                
                poptype = 'small'
                runs_with_small += 1  

                sigma_factor = 0.01 ** np.random.uniform()  
                popsize_multiplier = fmin_options['incpopsize'] ** (irun - runs_with_small)
                opts['popsize'] = np.floor(popsize0 * popsize_multiplier ** (np.random.uniform() ** 2))
                opts['maxiter'] = min(maxiter0, 0.5 * sum(large_i) / opts['popsize'])
                

            else:
                
                
                poptype = 'large'

                popsize_multiplier = fmin_options['incpopsize'] ** (irun - runs_with_small)
                opts['popsize'] = popsize0 * popsize_multiplier
                opts['maxiter'] = maxiter0
                

            
            if irun == 0 and isinstance(x0, CMAEvolutionStrategy):
                es = x0
                x0 = es.inputargs['x0']  
                if isscalar(sigma0) and isfinite(sigma0) and sigma0 > 0:
                    es.sigma = sigma0
                
                sigma0 = es.inputargs['sigma0']  
                if options is not None:
                    es.opts.set(options)
                
            else:  
                if irun and eval(str(fmin_options['restart_from_best'])):
                    print_warning('CAVE: restart_from_best is often not useful',
                                  verbose=opts['verbose'])
                    es = CMAEvolutionStrategy(best.x, sigma_factor * sigma0, opts)
                else:
                    es = CMAEvolutionStrategy(x0, sigma_factor * sigma0, opts)
                if eval_initial_x or es.opts['CMA_elitist'] == 'initial' \
                   or (es.opts['CMA_elitist'] and eval_initial_x is None):
                    x = es.gp.pheno(es.mean,
                                    into_bounds=es.boundary_handler.repair,
                                    archive=es.sent_solutions)
                    es.best.update([x], es.sent_solutions,
                                   [objective_function(x, *args)], 1)
                    es.countevals += 1

            opts = es.opts  
            
            fmin_opts = CMAOptions(fmin_options.copy(), unchecked=True)
            for k in fmin_opts:
                
                
                fmin_opts.eval(k, loc={'N': es.N,
                                       'popsize': opts['popsize']},
                               correct_key=False)

            append = opts['verb_append'] or es.countiter > 0 or irun > 0
            "the same" logger, because the "identity"
            
            logger = CMADataLogger(opts['verb_filenameprefix'],
                                   opts['verb_log'])
            logger.register(es, append).add()  
            es.logger = logger

            if noise_handler:
                noisehandler = noise_handler
                noise_handling = True
                if fmin_opts['noise_change_sigma_exponent'] > 0:
                    es.opts['tolfacupx'] = inf
            else:
                noisehandler = NoiseHandler(es.N, 0)
                noise_handling = False
            es.noise_handler = noisehandler

            
            
            if 1 < 3:
                while not es.stop():  
                    
                    X, fit = es.ask_and_eval(objective_function, args, gradf=gradf,
                                             evaluations=noisehandler.evaluations,
                                             aggregation=np.median)  
                    

                    es.tell(X, fit)  
                    if noise_handling:  
                        es.sigma *= noisehandler(X, fit, objective_function, es.ask,
                                                 args=args)**fmin_opts['noise_change_sigma_exponent']

                        es.countevals += noisehandler.evaluations_just_done  
                        
                        if noisehandler.maxevals > noisehandler.minevals:
                            es.more_to_write.append(noisehandler.get_evaluations())
                        if 1 < 3:
                            es.sp.cmean *= exp(-noise_kappa_exponent * np.tanh(noisehandler.noiseS))
                            if es.sp.cmean > 1:
                                es.sp.cmean = 1

                    es.disp()
                    logger.add(
                               modulo=1 if es.stop() and logger.modulo else None)
                    if (opts['verb_log'] and opts['verb_plot'] and
                          (es.countiter % max(opts['verb_plot'], opts['verb_log']) == 0 or es.stop())):
                        logger.plot(324)

            
            mean_pheno = es.gp.pheno(es.mean, into_bounds=es.boundary_handler.repair, archive=es.sent_solutions)
            fmean = objective_function(mean_pheno, *args)
            es.countevals += 1

            es.best.update([mean_pheno], es.sent_solutions, [fmean], es.countevals)
            best.update(es.best, es.sent_solutions)  
            

            this_evals = es.countevals - base_evals
            base_evals = es.countevals

            

            if irun == 0:
                popsize0 = opts['popsize']
                maxiter0 = opts['maxiter']
                
                

            if bipop:
                if poptype == 'small':
                    small_i.append(this_evals)
                else:  
                    large_i.append(this_evals)

            
            if opts['verb_disp']:
                es.result_pretty(irun, time.asctime(time.localtime()),
                                 best.f)

            irun += 1
            
            
            if irun - runs_with_small > fmin_opts['restarts'] or 'ftarget' in es.stop() \
                    or 'maxfevals' in es.stop(check=False):
                break
            opts['verb_append'] = es.countevals
            opts['popsize'] = fmin_opts['incpopsize'] * es.sp.popsize  
            opts['seed'] += 1

        

        
        if 1 < 3:
            if irun:
                es.best.update(best)
                
            return es.result() + (es.stop(), es, logger)

        else:  
            return (best.x.copy(), best.f, es.countevals,
                    dict((('stopdict', _CMAStopDict(es._stopdict))
                          , ('mean', es.gp.pheno(es.mean))
                          , ('std', es.sigma * es.sigma_vec * sqrt(es.dC) * es.gp.scales)
                          , ('out', es.out)
                          , ('opts', es.opts)  
                          , ('cma', es)
                          , ('inputargs', es.inputargs)
                          ))
                   )
        
        
    else:  
        if eval(str(options['verb_disp'])) > 0:
            print(' in/outcomment ``raise`` in last line of cma.fmin to prevent/restore KeyboardInterrupt exception')
        raise  




class BaseDataLogger(object):
    """"abstract" base class for a data logger that can be used with an `OOOptimizer`

    Details: attribute `modulo` is used in ``OOOptimizer.optimize``

    """
    def add(self, optim=None, more_data=[]):
        """abstract method, add a "data point" from the state of `optim` into the
        logger, the argument `optim` can be omitted if it was `register()`-ed before,
        acts like an event handler"""
        raise NotImplementedError
    def register(self, optim):
        """abstract method, register an optimizer `optim`, only needed if `add()` is
        called without a value for the `optim` argument"""
        self.optim = optim
    def disp(self):
        """display some data trace (not implemented)"""
        print('method BaseDataLogger.disp() not implemented, to be done in subclass ' + str(type(self)))
    def plot(self):
        """plot data (not implemented)"""
        print('method BaseDataLogger.plot() is not implemented, to be done in subclass ' + str(type(self)))
    def data(self):
        """return logged data in a dictionary (not implemented)"""
        print('method BaseDataLogger.data() is not implemented, to be done in subclass ' + str(type(self)))




class CMADataLogger(BaseDataLogger):
    """data logger for class `CMAEvolutionStrategy`. The logger is
    identified by its name prefix and (over-)writes or reads according
    data files. Therefore, the logger must be considered as *global* variable
    with unpredictable side effects, if two loggers with the same name
    and on the same working folder are used at the same time.

    Examples
    ========
    ::

        import cma
        es = cma.CMAEvolutionStrategy(...)
        logger = cma.CMADataLogger().register(es)
        while not es.stop():
            ...
            logger.add()  

        logger.plot() 
        cma.plot()  


        logger2 = cma.CMADataLogger('just_another_filename_prefix').load()
        logger2.plot()
        logger2.disp()

    ::

        import cma
        from matplotlib.pylab import *
        res = cma.fmin(cma.Fcts.sphere, rand(10), 1e-0)
        logger = res[-1]  
        logger.load()  "default" data are on disk
        semilogy(logger.f[:,0], logger.f[:,5])  
        show()

    Details
    =======
    After loading data, the logger has the attributes `xmean`, `xrecent`,
    `std`, `f`, `D` and `corrspec` corresponding to ``xmean``,
    ``xrecentbest``, ``stddev``, ``fit``, ``axlen`` and ``axlencorr``
    filename trails.

    :See: `disp()`, `plot()`

    """
    default_prefix = 'outcmaes'
    
    

    def __init__(self, name_prefix=default_prefix, modulo=1, append=False):
        """initialize logging of data from a `CMAEvolutionStrategy`
        instance, default ``modulo=1`` means logging with each call

        """
        
        
        
        self.name_prefix = name_prefix if name_prefix \
            else CMADataLogger.default_prefix
        if isinstance(self.name_prefix, CMAEvolutionStrategy):
            self.name_prefix = self.name_prefix.opts.eval(
                'verb_filenameprefix')
        self.file_names = ('axlen', 'axlencorr', 'fit', 'stddev', 'xmean',
                'xrecentbest')
        """used in load, however hard-coded in add"""
        self.key_names = ('D', 'corrspec', 'f', 'std', 'xmean', 'xrecent')
        """used in load, however hard-coded in plot"""
        self._key_names_with_annotation = ('std', 'xmean', 'xrecent')
        """used in load to add one data row to be modified in plot"""
        self.modulo = modulo
        """how often to record data, allows calling `add` without args"""
        self.append = append
        """append to previous data"""
        self.counter = 0
        """number of calls to `add`"""
        self.last_iteration = 0
        self.registered = False
        self.last_correlation_spectrum = None
        self._eigen_counter = 1  
    def data(self):
        """return dictionary with data.

        If data entries are None or incomplete, consider calling
        ``.load().data()`` to (re-)load the data from files first.

        """
        d = {}
        for name in self.key_names:
            d[name] = self.__dict__.get(name, None)
        return d
    def register(self, es, append=None, modulo=None):
        """register a `CMAEvolutionStrategy` instance for logging,
        ``append=True`` appends to previous data logged under the same name,
        by default previous data are overwritten.

        """
        if not isinstance(es, CMAEvolutionStrategy):
            raise TypeError("only class CMAEvolutionStrategy can be " +
                            "registered for logging")
        self.es = es
        if append is not None:
            self.append = append
        if modulo is not None:
            self.modulo = modulo
        self.registered = True
        return self

    def initialize(self, modulo=None):
        """reset logger, overwrite original files, `modulo`: log only every modulo call"""
        if modulo is not None:
            self.modulo = modulo
        try:
            es = self.es  
        except AttributeError:
            pass  
            raise _Error('call register() before initialize()')

        self.counter = 0  
        self.last_iteration = 0  

        
        fn = self.name_prefix + 'fit.dat'
        strseedtime = 'seed=%d, %s' % (es.opts['seed'], time.asctime())

        try:
            with open(fn, 'w') as f:
                f.write('% "iteration, evaluation, sigma, axis ratio, ' +
                        'bestever, best, median, worst objective function value, ' +
                        'further objective values of best", ' +
                        strseedtime +
                        "%Y/%m/%d %H:%M:%S", localtime()) + 
                        '\n')
        except (IOError, OSError):
            print('could not open file ' + fn)

        fn = self.name_prefix + 'axlen.dat'
        try:
            with open(fn, 'w') as f:
                f.write('%  columns="iteration, evaluation, sigma, ' +
                        'max axis length, ' +
                        ' min axis length, all principle axes lengths ' +
                        ' (sorted square roots of eigenvalues of C)", ' +
                        strseedtime +
                        '\n')
        except (IOError, OSError):
            print('could not open/write file ' + fn)
        fn = self.name_prefix + 'axlencorr.dat'
        try:
            with open(fn, 'w') as f:
                f.write('%  columns="iteration, evaluation, min max(neg(.)) min(pos(.))' +
                        ' max correlation, correlation matrix principle axes lengths ' +
                        ' (sorted square roots of eigenvalues of correlation matrix)", ' +
                        strseedtime +
                        '\n')
        except (IOError, OSError):
            print('could not open file ' + fn)
        fn = self.name_prefix + 'stddev.dat'
        try:
            with open(fn, 'w') as f:
                f.write('% "iteration, evaluation, sigma, void, void, ' +
                        ' stds==sigma*sqrt(diag(C))", ' +
                        strseedtime +
                        '\n')
        except (IOError, OSError):
            print('could not open file ' + fn)

        fn = self.name_prefix + 'xmean.dat'
        try:
            with open(fn, 'w') as f:
                f.write('% "iteration, evaluation, void, void, void, xmean", ' +
                        strseedtime)
                f.write(' 
                if np.size(es.gp.scales) > 1:
                    f.write(' '.join(map(str, es.gp.scales)))
                else:
                    f.write(str(es.gp.scales))
                f.write(', typical_x: ')
                if np.size(es.gp.typical_x) > 1:
                    f.write(' '.join(map(str, es.gp.typical_x)))
                else:
                    f.write(str(es.gp.typical_x))
                f.write('\n')
        except (IOError, OSError):
            print('could not open/write file ' + fn)

        fn = self.name_prefix + 'xrecentbest.dat'
        try:
            with open(fn, 'w') as f:
                f.write('% 
                        strseedtime +
                        '\n')
        except (IOError, OSError):
            print('could not open/write file ' + fn)

        return self
    

    def load(self, filenameprefix=None):
        """load (or reload) data from output files, `load()` is called in
        `plot()` and `disp()`.

        Argument `filenameprefix` is the filename prefix of data to be
        loaded (six files), by default ``'outcmaes'``.

        Return self with (added) attributes `xrecent`, `xmean`,
        `f`, `D`, `std`, 'corrspec'

        """
        if not filenameprefix:
            filenameprefix = self.name_prefix
        assert len(self.file_names) == len(self.key_names)
        for i in rglen((self.file_names)):
            fn = filenameprefix + self.file_names[i] + '.dat'
            try:
                self.__dict__[self.key_names[i]] = _fileToMatrix(fn)
            except:
                _print_warning('reading from file "' + fn + '" failed',
                               'load', 'CMADataLogger')
            try:
                if self.key_names[i] in self._key_names_with_annotation:
                    
                    self.__dict__[self.key_names[i]].append(
                        self.__dict__[self.key_names[i]][-1])
                self.__dict__[self.key_names[i]] = \
                    array(self.__dict__[self.key_names[i]], copy=False)
            except:
                _print_warning('no data for %s' % fn, 'load',
                               'CMADataLogger')
        return self

    def add(self, es=None, more_data=[], modulo=None):
        """append some logging data from `CMAEvolutionStrategy` class instance `es`,
        if ``number_of_times_called % modulo`` equals to zero, never if ``modulo==0``.

        The sequence ``more_data`` must always have the same length.

        When used for a different optimizer class, this function can be
        (easily?) adapted by changing the assignments under INTERFACE
        in the implemention.

        """
        mod = modulo if modulo is not None else self.modulo
        self.counter += 1
        if mod == 0 or (self.counter > 3 and (self.counter - 1) % mod):
            return
        if es is None:
            try:
                es = self.es  
            except AttributeError :
                raise _Error('call `add` with argument `es` or ``register(es)`` before ``add()``')
        elif not self.registered:
            self.register(es)

        if 1 < 3:
            if self.counter == 1 and not self.append and self.modulo != 0:
                self.initialize()  
                self.counter = 1

        
        if not isinstance(es, CMAEvolutionStrategy):  
            _print_warning('type CMAEvolutionStrategy expected, found '
                           + str(type(es)), 'add', 'CMADataLogger')
        evals = es.countevals
        iteration = es.countiter
        eigen_decompositions = es.count_eigen
        sigma = es.sigma
        axratio = es.D.max() / es.D.min()
        xmean = es.mean  
        fmean_noise_free = es.fmean_noise_free
        fmean = es.fmean
        
        try:
            besteverf = es.best.f
            bestf = es.fit.fit[0]
            worstf = es.fit.fit[-1]
            medianf = es.fit.fit[es.sp.popsize // 2]
        except:
            if iteration > 0:  
                raise
        try:
            xrecent = es.best.last.x
        except:
            xrecent = None
        maxD = es.D.max()
        minD = es.D.min()
        diagD = es.D
        diagC = es.sigma * es.sigma_vec * sqrt(es.dC)
        more_to_write = es.more_to_write
        es.more_to_write = []
        

        try:
            
            if iteration > self.last_iteration:
                fn = self.name_prefix + 'fit.dat'
                with open(fn, 'a') as f:
                    f.write(str(iteration) + ' '
                            + str(evals) + ' '
                            + str(sigma) + ' '
                            + str(axratio) + ' '
                            + str(besteverf) + ' '
                            + '%.16e' % bestf + ' '
                            + str(medianf) + ' '
                            + str(worstf) + ' '
                            
                            
                            
                            + ' '.join(str(i) for i in more_to_write) + ' '
                            + ' '.join(str(i) for i in more_data) + ' '
                            + '\n')
            
            fn = self.name_prefix + 'axlen.dat'
            if 1 < 3:
                with open(fn, 'a') as f:  
                    f.write(str(iteration) + ' '
                            + str(evals) + ' '
                            + str(sigma) + ' '
                            + str(maxD) + ' '
                            + str(minD) + ' '
                            + ' '.join(map(str, diagD))
                            + '\n')
            
            if 1 < 3:
                fn = self.name_prefix + 'axlencorr.dat'
                c = es.correlation_matrix()
                if c is not None:
                    
                    if self._eigen_counter < eigen_decompositions / 2:
                        self.last_correlation_spectrum = \
                            sorted(es.opts['CMA_eigenmethod'](c)[0]**0.5)
                        self._eigen_counter += 1
                    if self.last_correlation_spectrum is None:
                        self.last_correlation_spectrum = len(diagD) * [1]
                    c = c[c < 1 - 1e-14]  
                    c[c > 1 - 1e-14] = 1 - 1e-14
                    c[c < -1 + 1e-14] = -1 + 1e-14
                    c_min = np.min(c)
                    c_max = np.max(c)
                    if np.min(abs(c)) == 0:
                        c_medminus = 0  "is negative"
                        c_medplus = 0  "is positive"
                    else:
                        c_medminus = c[np.argmin(1/c)]  
                        c_medplus = c[np.argmax(1/c)]  

                    with open(fn, 'a') as f:
                        f.write(str(iteration) + ' '
                                + str(evals) + ' '
                                + str(c_min) + ' '
                                + str(c_medminus) + ' ' 
                                + str(c_medplus) + ' ' 
                                + str(c_max) + ' '
                                + ' '.join(map(str,
                                        self.last_correlation_spectrum))
                                + '\n')

            
            fn = self.name_prefix + 'stddev.dat'
            with open(fn, 'a') as f:
                f.write(str(iteration) + ' '
                        + str(evals) + ' '
                        + str(sigma) + ' '
                        + '0 0 '
                        + ' '.join(map(str, diagC))
                        + '\n')
            
            fn = self.name_prefix + 'xmean.dat'
            with open(fn, 'a') as f:
                f.write(str(iteration) + ' '
                        + str(evals) + ' '
                        
                        + '0 '
                        + str(fmean_noise_free) + ' '
                        + str(fmean) + ' '  
                        
                        + ' '.join(map(str, xmean))
                        + '\n')
            
            fn = self.name_prefix + 'xrecentbest.dat'
            if iteration > 0 and xrecent is not None:
                with open(fn, 'a') as f:
                    f.write(str(iteration) + ' '
                            + str(evals) + ' '
                            + str(sigma) + ' '
                            + '0 '
                            + str(bestf) + ' '
                            + ' '.join(map(str, xrecent))
                            + '\n')
        except (IOError, OSError):
            if iteration <= 1:
                _print_warning(('could not open/write file %s: ' % fn,
                                sys.exc_info()))
        self.last_iteration = iteration

    def closefig(self):
        pyplot.close(self.fighandle)

    def save_to(self, nameprefix, switch=False):
        """saves logger data to a different set of files, for
        ``switch=True`` also the loggers name prefix is switched to
        the new value

        """
        if not nameprefix or not isinstance(nameprefix, str):
            raise _Error('filename prefix must be a nonempty string')

        if nameprefix == self.default_prefix:
            raise _Error('cannot save to default name "' + nameprefix + '...", chose another name')

        if nameprefix == self.name_prefix:
            return

        for name in self.file_names:
            open(nameprefix + name + '.dat', 'w').write(open(self.name_prefix + name + '.dat').read())

        if switch:
            self.name_prefix = nameprefix
    def select_data(self, iteration_indices):
        """keep only data of `iteration_indices`"""
        dat = self
        iteridx = iteration_indices
        dat.f = dat.f[np.where([x in iteridx for x in dat.f[:, 0]])[0], :]
        dat.D = dat.D[np.where([x in iteridx for x in dat.D[:, 0]])[0], :]
        try:
            iteridx = list(iteridx)
            iteridx.append(iteridx[-1])  
        except:
            pass
        dat.std = dat.std[np.where([x in iteridx
                                    for x in dat.std[:, 0]])[0], :]
        dat.xmean = dat.xmean[np.where([x in iteridx
                                        for x in dat.xmean[:, 0]])[0], :]
        try:
            dat.xrecent = dat.x[np.where([x in iteridx for x in
                                          dat.xrecent[:, 0]])[0], :]
        except AttributeError:
            pass
        try:
            dat.corrspec = dat.x[np.where([x in iteridx for x in
                                           dat.corrspec[:, 0]])[0], :]
        except AttributeError:
            pass
    def plot(self, fig=None, iabscissa=1, iteridx=None,
             plot_mean=False, 
             foffset=1e-19, x_opt=None, fontsize=9):
        """plot data from a `CMADataLogger` (using the files written 
        by the logger).

        Arguments
        ---------
            `fig`
                figure number, by default 325
            `iabscissa`
                ``0==plot`` versus iteration count,
                ``1==plot`` versus function evaluation number
            `iteridx`
                iteration indices to plot

        Return `CMADataLogger` itself.

        Examples
        --------
        ::

            import cma
            logger = cma.CMADataLogger()  
            "default logging" data (e.g.
            
            
            logger.plot()
            cma.savefig('fig325.png')  
            logger.closefig()

        Dependencies: matlabplotlib/pyplot.

        """
        try:
            
            from matplotlib.pyplot import figure, subplot, hold, gcf
        except ImportError:
            ImportError('could not find matplotlib.pyplot module, function plot() is not available')
            return

        if fig is None:
            fig = 325
        if iabscissa not in (0, 1):
            iabscissa = 1

        self.load()  
        dat = self
        dat.x = dat.xmean  
        if not plot_mean:
            if len(dat.x) < 2:
                print('not enough data to plot recent x')
            else:
                dat.x = dat.xrecent

        
        if iteridx is not None:
            self.select_data(iteridx)

        if len(dat.f) <= 1:
            print('nothing to plot')
            return

        
        

        

        
        

        figure(fig)
        self._enter_plotting(fontsize)
        self.fighandle = gcf()  

        subplot(2, 2, 1)
        self.plot_divers(iabscissa, foffset)
        pyplot.xlabel('')

        
        subplot(2, 2, 3)
        self.plot_axes_scaling(iabscissa)

        
        figure(fig)

        subplot(2, 2, 2)
        if plot_mean:
            self.plot_mean(iabscissa, x_opt)
        else:
            self.plot_xrecent(iabscissa, x_opt)
        pyplot.xlabel('')
        

        
        subplot(2, 2, 4)
        self.plot_stds(iabscissa)
        self._finalize_plotting()
        return self
    def plot_all(self, fig=None, iabscissa=1, iteridx=None,
             foffset=1e-19, x_opt=None, fontsize=9):
        """
        plot data from a `CMADataLogger` (using the files written by the logger).

        Arguments
        ---------
            `fig`
                figure number, by default 425
            `iabscissa`
                ``0==plot`` versus iteration count,
                ``1==plot`` versus function evaluation number
            `iteridx`
                iteration indices to plot

        Return `CMADataLogger` itself.

        Examples
        --------
        ::

            import cma
            logger = cma.CMADataLogger()  
            "default logging" data (e.g.
            
            
            logger.plot_all()
            cma.savefig('fig425.png')  
            logger.closefig()

        Dependencies: matlabplotlib/pyplot.

        """
        try:
            
            from  matplotlib.pyplot import figure, subplot, gcf
        except ImportError:
            ImportError('could not find matplotlib.pyplot module, function plot() is not available')
            return

        if fig is None:
            fig = 426
        if iabscissa not in (0, 1):
            iabscissa = 1

        self.load()
        dat = self

        
        if iteridx is not None:
            self.select_data(iteridx)

        if len(dat.f) == 0:
            print('nothing to plot')
            return

        
        

        

        

        figure(fig)
        self._enter_plotting(fontsize)
        self.fighandle = gcf()  

        if 1 < 3:
            subplot(2, 3, 1)
            self.plot_divers(iabscissa, foffset)
            pyplot.xlabel('')

            
            subplot(2, 3, 4)
            self.plot_stds(iabscissa)

            
            subplot(2, 3, 2)
            self.plot_axes_scaling(iabscissa)
            pyplot.xlabel('')

            
            subplot(2, 3, 5)
            self.plot_correlations(iabscissa)

            
            subplot(2, 3, 3)
            self.plot_xrecent(iabscissa, x_opt)
            pyplot.xlabel('')

            subplot(2, 3, 6)
            self.plot_mean(iabscissa, x_opt)

        self._finalize_plotting()
        return self
    def plot_axes_scaling(self, iabscissa=1):
        if not hasattr(self, 'D'):
            self.load()
        dat = self
        self._enter_plotting()
        pyplot.semilogy(dat.D[:, iabscissa], dat.D[:, 5:], '-b')
        pyplot.hold(True)
        pyplot.grid(True)
        ax = array(pyplot.axis())
        
        pyplot.axis(ax)
        pyplot.title('Principle Axes Lengths')
        
        self._xlabel(iabscissa)
        self._finalize_plotting()
        return self
    def plot_stds(self, iabscissa=1):
        if not hasattr(self, 'std'):
            self.load()
        dat = self
        self._enter_plotting()
        
        dat.std[:, 5:] = np.transpose(dat.std[:, 5:].T / dat.std[:, 2].T)
        
        
        
        if 1 < 2 and dat.std.shape[1] < 100:
            
            minxend = int(1.06 * dat.std[-2, iabscissa])
            
            dat.std[-1, iabscissa] = minxend  
            idx = np.argsort(dat.std[-2, 5:])
            idx2 = np.argsort(idx)
            dat.std[-1, 5 + idx] = np.logspace(np.log10(np.min(dat.std[:, 5:])),
                            np.log10(np.max(dat.std[:, 5:])), dat.std.shape[1] - 5)

            dat.std[-1, iabscissa] = minxend  
            pyplot.semilogy(dat.std[:, iabscissa], dat.std[:, 5:], '-')
            pyplot.hold(True)
            ax = array(pyplot.axis())

            yy = np.logspace(np.log10(ax[2]), np.log10(ax[3]), dat.std.shape[1] - 5)
            
            idx = np.argsort(dat.std[-1, 5:])
            idx2 = np.argsort(idx)
            
            
            pyplot.plot(np.dot(dat.std[-2, iabscissa], [1, 1]),
                        array([ax[2] + 1e-6, ax[3] - 1e-6]),
                        
                        'k-')
            pyplot.hold(True)
            
            for i in rglen((idx)):
                
                pyplot.text(dat.std[-1, iabscissa], dat.std[-1, 5 + i], ' ' + str(i))
        else:
            pyplot.semilogy(dat.std[:, iabscissa], dat.std[:, 5:], '-')
        pyplot.hold(True)
        pyplot.grid(True)
        pyplot.title(r'Standard Deviations $\times$ $\sigma^{-1}$ in All Coordinates')
        
        self._xlabel(iabscissa)
        self._finalize_plotting()
        return self
    def plot_mean(self, iabscissa=1, x_opt=None, annotations=None):
        if not hasattr(self, 'xmean'):
            self.load()
        self.x = self.xmean
        self._plot_x(iabscissa, x_opt, 'mean', annotations=annotations)
        self._xlabel(iabscissa)
        return self
    def plot_xrecent(self, iabscissa=1, x_opt=None, annotations=None):
        if not hasattr(self, 'xrecent'):
            self.load()
        self.x = self.xrecent
        self._plot_x(iabscissa, x_opt, 'curr best', annotations=annotations)
        self._xlabel(iabscissa)
        return self
    def plot_correlations(self, iabscissa=1):
        """spectrum of correlation matrix and largest correlation"""
        if not hasattr(self, 'corrspec'):
            self.load()
        if len(self.corrspec) < 2:
            return self
        x = self.corrspec[:, iabscissa]
        y = self.corrspec[:, 6:]  
        ys = self.corrspec[:, :6]  "special" values

        from matplotlib.pyplot import semilogy, hold, text, grid, axis, title
        self._enter_plotting()
        semilogy(x, y, '-c')
        hold(True)
        semilogy(x[:], np.max(y, 1) / np.min(y, 1), '-r')
        text(x[-1], np.max(y[-1, :]) / np.min(y[-1, :]), 'axis ratio')
        if ys is not None:
            semilogy(x, 1 + ys[:, 2], '-b')
            text(x[-1], 1 + ys[-1, 2], '1 + min(corr)')
            semilogy(x, 1 - ys[:, 5], '-b')
            text(x[-1], 1 - ys[-1, 5], '1 - max(corr)')
            semilogy(x[:], 1 + ys[:, 3], '-k')
            text(x[-1], 1 + ys[-1, 3], '1 + max(neg corr)')
            semilogy(x[:], 1 - ys[:, 4], '-k')
            text(x[-1], 1 - ys[-1, 4], '1 - min(pos corr)')
        grid(True)
        ax = array(axis())
        
        axis(ax)
        title('Spectrum (roots) of correlation matrix')
        
        self._xlabel(iabscissa)
        self._finalize_plotting()
        return self
    def plot_divers(self, iabscissa=1, foffset=1e-19):
        """plot fitness, sigma, axis ratio...

        :param iabscissa: 0 means vs evaluations, 1 means vs iterations
        :param foffset: added to f-value

        :See: `plot()`

        """
        from matplotlib.pyplot import semilogy, hold, grid, \
            axis, title, text
        fontsize = pyplot.rcParams['font.size']

        if not hasattr(self, 'f'):
            self.load()
        dat = self

        minfit = min(dat.f[:, 5])
        dfit = dat.f[:, 5] - minfit  
        dfit[dfit < 1e-98] = np.NaN

        self._enter_plotting()
        if dat.f.shape[1] > 7:
            
            semilogy(dat.f[:, iabscissa], abs(dat.f[:, [6, 7]]) + foffset, '-k')
            hold(True)

        
        if dat.f.shape[1] > 8:
            
            
            semilogy(dat.f[:, iabscissa], np.abs(dat.f[:, 8:]) + 10 * foffset, 'y')
            hold(True)

        idx = np.where(dat.f[:, 5] > 1e-98)[0]  
        semilogy(dat.f[idx, iabscissa], dat.f[idx, 5] + foffset, '.b')
        hold(True)
        grid(True)


        semilogy(dat.f[:, iabscissa], abs(dat.f[:, 5]) + foffset, '-b')
        text(dat.f[-1, iabscissa], abs(dat.f[-1, 5]) + foffset,
             r'$|f_\mathsf{best}|$', fontsize=fontsize + 2)

        
        sgn = np.sign(dat.f[:, 5])
        sgn[np.abs(dat.f[:, 5]) < 1e-98] = 0
        idx = np.where(sgn < 0)[0]
        semilogy(dat.f[idx, iabscissa], abs(dat.f[idx, 5]) + foffset,
                 '.m')  

        
        dsgn = np.diff(sgn)
        start_idx = 1 + np.where((dsgn < 0) * (sgn[1:] < 0))[0]
        stop_idx = 1 + np.where(dsgn > 0)[0]
        if sgn[0] < 0:
            start_idx = np.concatenate(([0], start_idx))
        for istart in start_idx:
            istop = stop_idx[stop_idx > istart]
            istop = istop[0] if len(istop) else 0
            idx = range(istart, istop if istop else dat.f.shape[0])
            if len(idx) > 1:
                semilogy(dat.f[idx, iabscissa], abs(dat.f[idx, 5]) + foffset,
                        'm')  
            
            
            if istart > 0:  
                semilogy(dat.f[istart-1:istart+1, iabscissa],
                         abs(dat.f[istart-1:istart+1, 5]) +
                         foffset, '--m')
            if istop:  
                semilogy(dat.f[istop-1:istop+1, iabscissa],
                         abs(dat.f[istop-1:istop+1, 5]) +
                         foffset, '--m')
                
                semilogy(dat.f[istop, iabscissa], abs(dat.f[istop, 5]) +
                         foffset, '.b', markersize=7)
            
            semilogy(dat.f[istart, iabscissa], abs(dat.f[istart, 5]) +
                     foffset, '.r', markersize=7)

        
        semilogy(dat.std[:-1, iabscissa],
                 np.vstack([list(map(max, dat.std[:-1, 5:])),
                            list(map(min, dat.std[:-1, 5:]))]).T,
                     '-m', linewidth=2)
        text(dat.std[-2, iabscissa], max(dat.std[-2, 5:]), 'max std',
             fontsize=fontsize)
        text(dat.std[-2, iabscissa], min(dat.std[-2, 5:]), 'min std',
             fontsize=fontsize)

        
        idx = isfinite(dfit)
        if 1 < 3:
            idx_nan = np.where(idx == False)[0]  
            if not len(idx_nan):  
                semilogy(dat.f[:, iabscissa][idx], dfit[idx], '-c')
            else:
                i_start = 0
                for i_end in idx_nan:
                    if i_end > i_start:
                        semilogy(dat.f[:, iabscissa][i_start:i_end],
                                                dfit[i_start:i_end], '-c')
                i_start = i_end + 1
                if len(dfit) > idx_nan[-1] + 1:
                    semilogy(dat.f[:, iabscissa][idx_nan[-1]+1:],
                                            dfit[idx_nan[-1]+1:], '-c')
            text(dat.f[idx, iabscissa][-1], dfit[idx][-1],
                 r'$f_\mathsf{best} - \min(f)$', fontsize=fontsize + 2)

        
        i = np.argmin(dat.f[:, 5])
        semilogy(dat.f[i, iabscissa], np.abs(dat.f[i, 5]), 'ro',
                 markersize=9)
        semilogy(dat.f[i, iabscissa], dfit[idx][np.argmin(dfit[idx])]
                 + 1e-98, 'ro', markersize=9)
        

        
        semilogy(dat.f[:, iabscissa], dat.f[:, 3], '-r')  
        semilogy(dat.f[:, iabscissa], dat.f[:, 2], '-g')  
        text(dat.f[-1, iabscissa], dat.f[-1, 3], r'axis ratio',
             fontsize=fontsize)
        text(dat.f[-1, iabscissa], dat.f[-1, 2] / 1.5, r'$\sigma$',
             fontsize=fontsize+3)
        ax = array(axis())
        
        axis(ax)
        text(ax[0] + 0.01, ax[2],  
             '.min($f$)=' + repr(minfit))
             

        
        
        
        title(r'$|f_{\mathrm{best},\mathrm{med},\mathrm{worst}}|$, $f - \min(f)$, $\sigma$, axis ratio')

        
        self._xlabel(iabscissa)
        self._finalize_plotting()
        return self
    def _enter_plotting(self, fontsize=9):
        """assumes that a figure is open """
        
        self.original_fontsize = pyplot.rcParams['font.size']
        pyplot.rcParams['font.size'] = fontsize
        pyplot.hold(False)  
        pyplot.ioff()
    def _finalize_plotting(self):
        pyplot.ion()
        pyplot.draw()  "screen"
        pyplot.show()  
        
        pyplot.rcParams['font.size'] = self.original_fontsize
    def _xlabel(self, iabscissa=1):
        pyplot.xlabel('iterations' if iabscissa == 0
                      else 'function evaluations')
    def _plot_x(self, iabscissa=1, x_opt=None, remark=None,
                annotations=None):
        """If ``x_opt is not None`` the difference to x_opt is plotted
        in log scale

        """
        if not hasattr(self, 'x'):
            _print_warning('no x-attributed found, use methods ' +
                           'plot_xrecent or plot_mean', 'plot_x',
                           'CMADataLogger')
            return
        from matplotlib.pyplot import plot, semilogy, hold, text, grid, axis, title
        dat = self  
        
        if dat.x.shape[1] < 100:
            minxend = int(1.06 * dat.x[-2, iabscissa])
            
            dat.x[-1, iabscissa] = minxend  
            if x_opt is None:
                idx = np.argsort(dat.x[-2, 5:])
                idx2 = np.argsort(idx)
                dat.x[-1, 5 + idx] = np.linspace(np.min(dat.x[:, 5:]),
                            np.max(dat.x[:, 5:]), dat.x.shape[1] - 5)
            else: 
                xdat = np.abs(dat.x[:, 5:] - np.array(x_opt, copy=False))
                idx = np.argsort(xdat[-2, :])
                idx2 = np.argsort(idx)
                xdat[-1, idx] = np.logspace(np.log10(np.min(abs(xdat[xdat!=0]))),
                            np.log10(np.max(np.abs(xdat))),
                            dat.x.shape[1] - 5)
        else:
            minxend = 0
        self._enter_plotting()
        if x_opt is not None:  
            semilogy(dat.x[:, iabscissa], abs(xdat), '-')
        else:
            plot(dat.x[:, iabscissa], dat.x[:, 5:], '-')
        hold(True)
        grid(True)
        ax = array(axis())
        
        axis(ax)
        ax[1] -= 1e-6  
        if dat.x.shape[1] < 100:
            yy = np.linspace(ax[2] + 1e-6, ax[3] - 1e-6, dat.x.shape[1] - 5)
            
            if x_opt is not None:
                
                semilogy(np.dot(dat.x[-2, iabscissa], [1, 1]),
                         array([ax[2] * (1+1e-6), ax[3] / (1+1e-6)]), 'k-')
            else:
                
                plot(np.dot(dat.x[-2, iabscissa], [1, 1]),
                     array([ax[2] + 1e-6, ax[3] - 1e-6]), 'k-')
            
            
            for i in rglen(idx):
                
                

                text(dat.x[-1, iabscissa], dat.x[-1, 5 + i]
                            if x_opt is None else np.abs(xdat[-1, i]),
                     ('x(' + str(i) + ')=' if annotations is None
                        else str(i) + ':' + annotations[i] + "=")
                     + str(dat.x[-2, 5 + i]))
        i = 2  
        while i < len(dat.f) and dat.f[-i][0] == dat.f[-1][0]:
            i += 1
        title('Object Variables (' +
                (remark + ', ' if remark is not None else '') +
                str(dat.x.shape[1] - 5) + '-D, popsize~' +
                (str(int((dat.f[-1][1] - dat.f[-i][1]) / (dat.f[-1][0] - dat.f[-i][0])))
                    if len(dat.f.T[0]) > 1 and dat.f[-1][0] > dat.f[-i][0] else 'NA')
                + ')')
        self._finalize_plotting()
    def downsampling(self, factor=10, first=3, switch=True, verbose=True):
        """
        rude downsampling of a `CMADataLogger` data file by `factor`,
        keeping also the first `first` entries. This function is a
        stump and subject to future changes. Return self.

        Arguments
        ---------
           - `factor` -- downsampling factor
           - `first` -- keep first `first` entries
           - `switch` -- switch the new logger to the downsampled logger
                original_name+'down'

        Details
        -------
        ``self.name_prefix+'down'`` files are written

        Example
        -------
        ::

            import cma
            cma.downsampling()  
            cma.plot('outcmaesdown')

        """
        newprefix = self.name_prefix + 'down'
        for name in self.file_names:
            f = open(newprefix + name + '.dat', 'w')
            iline = 0
            cwritten = 0
            for line in open(self.name_prefix + name + '.dat'):
                if iline < first or iline % factor == 0:
                    f.write(line)
                    cwritten += 1
                iline += 1
            f.close()
            if verbose and iline > first:
                print('%d' % (cwritten) + ' lines written in ' + newprefix + name + '.dat')
        if switch:
            self.name_prefix += 'down'
        return self

    
    
    
    def disp(self, idx=100):  
        """displays selected data from (files written by) the class `CMADataLogger`.

        Arguments
        ---------
           `idx`
               indices corresponding to rows in the data file;
               if idx is a scalar (int), the first two, then every idx-th,
               and the last three rows are displayed. Too large index values are removed.

        Example
        -------
        >>> import cma, numpy as np
        >>> res = cma.fmin(cma.fcts.elli, 7 * [0.1], 1, {'verb_disp':1e9})  
        >>> assert res[1] < 1e-9
        >>> assert res[2] < 4400
        >>> l = cma.CMADataLogger()  "points to" above data
        >>> l.disp([0,-1])  
        >>> l.disp(20)  
        >>> l.disp(np.r_[0:999999:100, -1]) 
        >>> l.disp(np.r_[0, -10:0]) 
        >>> cma.disp(l.name_prefix, np.r_[0::100, -10:])  

        Details
        -------
        The data line with the best f-value is displayed as last line.

        :See: `disp()`

        """

        filenameprefix = self.name_prefix

        def printdatarow(dat, iteration):
            """print data of iteration i"""
            i = np.where(dat.f[:, 0] == iteration)[0][0]
            j = np.where(dat.std[:, 0] == iteration)[0][0]
            print('%5d' % (int(dat.f[i, 0])) + ' %6d' % (int(dat.f[i, 1])) + ' %.14e' % (dat.f[i, 5]) +
                  ' %5.1e' % (dat.f[i, 3]) +
                  ' %6.2e' % (max(dat.std[j, 5:])) + ' %6.2e' % min(dat.std[j, 5:]))

        dat = CMADataLogger(filenameprefix).load()
        ndata = dat.f.shape[0]

        
        
        
        if idx is None:
            idx = 100
        if isscalar(idx):
            
            if idx:
                idx = np.r_[0, 1, idx:ndata - 3:idx, -3:0]
            else:
                idx = np.r_[0, 1, -3:0]

        idx = array(idx)
        idx = idx[idx < ndata]
        idx = idx[-idx <= ndata]
        iters = dat.f[idx, 0]
        idxbest = np.argmin(dat.f[:, 5])
        iterbest = dat.f[idxbest, 0]

        if len(iters) == 1:
            printdatarow(dat, iters[0])
        else:
            self.disp_header()
            for i in iters:
                printdatarow(dat, i)
            self.disp_header()
            printdatarow(dat, iterbest)
        sys.stdout.flush()
    def disp_header(self):
        heading = 'Iterat Nfevals  function value    axis ratio maxstd  minstd'
        print(heading)







last_figure_number = 324
def plot(name=None, fig=None, abscissa=1, iteridx=None,
         plot_mean=False,
         foffset=1e-19, x_opt=None, fontsize=9):
    """
    plot data from files written by a `CMADataLogger`,
    the call ``cma.plot(name, **argsdict)`` is a shortcut for
    ``cma.CMADataLogger(name).plot(**argsdict)``

    Arguments
    ---------
        `name`
            name of the logger, filename prefix, None evaluates to
            the default 'outcmaes'
        `fig`
            filename or figure number, or both as a tuple (any order)
        `abscissa`
            0==plot versus iteration count,
            1==plot versus function evaluation number
        `iteridx`
            iteration indices to plot

    Return `None`

    Examples
    --------
    ::

       cma.plot();  
                    
       cma.savefig('fig325.png')
       cma.closefig()

       cdl = cma.CMADataLogger().downsampling().plot()
       

    Details
    -------
    Data from codes in other languages (C, Java, Matlab, Scilab) have the same
    format and can be plotted just the same.

    :See: `CMADataLogger`, `CMADataLogger.plot()`

    """
    global last_figure_number
    if not fig:
        last_figure_number += 1
        fig = last_figure_number
    if isinstance(fig, (int, float)):
        last_figure_number = fig
    CMADataLogger(name).plot(fig, abscissa, iteridx, plot_mean, foffset,
                             x_opt, fontsize)

def disp(name=None, idx=None):
    """displays selected data from (files written by) the class `CMADataLogger`.

    The call ``cma.disp(name, idx)`` is a shortcut for ``cma.CMADataLogger(name).disp(idx)``.

    Arguments
    ---------
        `name`
            name of the logger, filename prefix, `None` evaluates to
            the default ``'outcmaes'``
        `idx`
            indices corresponding to rows in the data file; by
            default the first five, then every 100-th, and the last
            10 rows. Too large index values are removed.

    Examples
    --------
    ::

       import cma, numpy
       
       cma.disp(None,numpy.r_[0,-1])  
       cma.disp(None,numpy.r_[0:1e9:100,-1]) 
       cma.disp(idx=numpy.r_[0,-10:0]) 
       cma.disp(idx=numpy.r_[0:1e9:1e3,-10:0])

    :See: `CMADataLogger.disp()`

    """
    return CMADataLogger(name if name else CMADataLogger.default_prefix
                         ).disp(idx)


def _fileToMatrix(file_name):
    """rudimentary method to read in data from a file"""
    
    
    if 1 < 3:
        lres = []
        for line in open(file_name, 'r').readlines():
            if len(line) > 0 and line[0] not in ('%', '
                lres.append(list(map(float, line.split())))
        res = lres
    while res != [] and res[0] == []:  
        del res[0]
    return res
    
    print('could not read file ' + file_name)



class NoiseHandler(object):
    """Noise handling according to [Hansen et al 2009, A Method for
    Handling Uncertainty in Evolutionary Optimization...]

    The interface of this class is yet versatile and subject to changes.

    The noise handling follows closely [Hansen et al 2009] in the
    measurement part, but the implemented treatment is slightly
    different: for ``noiseS > 0``, ``evaluations`` (time) and sigma are
    increased by ``alpha``. For ``noiseS < 0``, ``evaluations`` (time)
    is decreased by ``alpha**(1/4)``.

    The (second) parameter ``evaluations`` defines the maximal number
    of evaluations for a single fitness computation. If it is a list,
    the smallest element defines the minimal number and if the list has
    three elements, the median value is the start value for
    ``evaluations``.

    ``NoiseHandler`` serves to control the noise via steps-size
    increase and number of re-evaluations, for example via ``fmin`` or
    with ``ask_and_eval()``.

    Examples
    --------
    Minimal example together with `fmin` on a non-noisy function:

    >>> import cma
    >>> cma.fmin(cma.felli, 7 * [1], 1, noise_handler=cma.NoiseHandler(7))

    in dimension 7 (which needs to be given tice). More verbose example
    in the optimization loop with a noisy function defined in ``func``:

    >>> import cma, numpy as np
    >>> func = lambda x: cma.fcts.sphere(x) * (1 + 4 * np.random.randn() / len(x))  
    >>> es = cma.CMAEvolutionStrategy(np.ones(10), 1)
    >>> nh = cma.NoiseHandler(es.N, maxevals=[1, 1, 30])
    >>> while not es.stop():
    ...     X, fit_vals = es.ask_and_eval(func, evaluations=nh.evaluations)
    ...     es.tell(X, fit_vals)  
    ...     es.sigma *= nh(X, fit_vals, func, es.ask)  
    ...     es.countevals += nh.evaluations_just_done  
    ...     es.logger.add(more_data = [nh.evaluations, nh.noiseS])  
    ...     es.disp()
    ...     
    >>> print(es.stop())
    >>> print(es.result()[-2])  
    >>> assert sum(es.result()[-2]**2) < 1e-9
    >>> print(X[np.argmin(fit_vals)])  
    >>> 


    The command ``logger.plot()`` will plot the logged data.

    The noise options of `fmin()` control a `NoiseHandler` instance
    similar to this example. The command ``cma.CMAOptions('noise')``
    lists in effect the parameters of `__init__` apart from
    ``aggregate``.

    Details
    -------
    The parameters reevals, theta, c_s, and alpha_t are set differently
    than in the original publication, see method `__init__()`. For a
    very small population size, say popsize <= 5, the measurement
    technique based on rank changes is likely to fail.

    Missing Features
    ----------------
    In case no noise is found, ``self.lam_reeval`` should be adaptive
    and get at least as low as 1 (however the possible savings from this
    are rather limited). Another option might be to decide during the
    first call by a quantitative analysis of fitness values whether
    ``lam_reeval`` is set to zero. More generally, an automatic noise
    mode detection might also set the covariance matrix learning rates
    to smaller values.

    :See: `fmin()`, `CMAEvolutionStrategy.ask_and_eval()`

    """
    
    
    
    def __init__(self, N, maxevals=[1, 1, 1], aggregate=np.median,
                 reevals=None, epsilon=1e-7, parallel=False):
        """parameters are

            `N`
                dimension, (only) necessary to adjust the internal
                "alpha"-parameters
            `maxevals`
                maximal value for ``self.evaluations``, where
                ``self.evaluations`` function calls are aggregated for
                noise treatment. With ``maxevals == 0`` the noise
                handler is (temporarily) "switched off". If `maxevals`
                is a list, min value and (for >2 elements) median are
                used to define minimal and initial value of
                ``self.evaluations``. Choosing ``maxevals > 1`` is only
                reasonable, if also the original ``fit`` values (that
                are passed to `__call__`) are computed by aggregation of
                ``self.evaluations`` values (otherwise the values are
                not comparable), as it is done within `fmin()`.
            `aggregate`
                function to aggregate single f-values to a 'fitness', e.g.
                ``np.median``.
            `reevals`
                number of solutions to be reevaluated for noise
                measurement, can be a float, by default set to ``2 +
                popsize/20``, where ``popsize = len(fit)`` in
                ``__call__``. zero switches noise handling off.
            `epsilon`
                multiplier for perturbation of the reevaluated solutions
            `parallel`
                a single f-call with all resampled solutions

            :See: `fmin()`, `CMAOptions`, `CMAEvolutionStrategy.ask_and_eval()`

        """
        self.lam_reeval = reevals  
        self.epsilon = epsilon
        self.parallel = parallel
        
        self.theta = 0.5  
        self.cum = 0.3  
        
        self.alphasigma = 1 + 2.0 / (N + 10) 
        
        self.alphaevals = 1 + 2.0 / (N + 10)  
        
        self.alphaevalsdown = self.alphaevals** -0.25  
        
        self.evaluations = 1  
        self.minevals = 1
        self.maxevals = int(np.max(maxevals))
        if hasattr(maxevals, '__contains__'):  
            if len(maxevals) > 1:
                self.minevals = min(maxevals)
                self.evaluations = self.minevals
            if len(maxevals) > 2:
                self.evaluations = np.median(maxevals)
        
        self.f_aggregate = aggregate if not None else {1: np.median, 2: np.mean}[ None ]
        self.evaluations_just_done = 0  
        self.noiseS = 0

    def __call__(self, X, fit, func, ask=None, args=()):
        """proceed with noise measurement, set anew attributes ``evaluations``
        (proposed number of evaluations to "treat" noise) and ``evaluations_just_done``
        and return a factor for increasing sigma.

        Parameters
        ----------
            `X`
                a list/sequence/vector of solutions
            `fit`
                the respective list of function values
            `func`
                the objective function, ``fit[i]`` corresponds to ``func(X[i], *args)``
            `ask`
                a method to generate a new, slightly disturbed solution. The argument
                is (only) mandatory if ``epsilon`` is not zero, see `__init__()`.
            `args`
                optional additional arguments to `func`

        Details
        -------
        Calls the methods ``reeval()``, ``update_measure()`` and ``treat()`` in this order.
        ``self.evaluations`` is adapted within the method `treat()`.

        """
        self.evaluations_just_done = 0
        if not self.maxevals or self.lam_reeval == 0:
            return 1.0
        res = self.reeval(X, fit, func, ask, args)
        if not len(res):
            return 1.0
        self.update_measure()
        return self.treat()

    def get_evaluations(self):
        """return ``self.evaluations``, the number of evalutions to get a single fitness measurement"""
        return self.evaluations

    def treat(self):
        """adapt self.evaluations depending on the current measurement value
        and return ``sigma_fac in (1.0, self.alphasigma)``

        """
        if self.noiseS > 0:
            self.evaluations = min((self.evaluations * self.alphaevals, self.maxevals))
            return self.alphasigma
        else:
            self.evaluations = max((self.evaluations * self.alphaevalsdown, self.minevals))
            return 1.0  

    def reeval(self, X, fit, func, ask, args=()):
        """store two fitness lists, `fit` and ``fitre`` reevaluating some
        solutions in `X`.
        ``self.evaluations`` evaluations are done for each reevaluated
        fitness value.
        See `__call__()`, where `reeval()` is called.

        """
        self.fit = list(fit)
        self.fitre = list(fit)
        self.idx = self.indices(fit)
        if not len(self.idx):
            return self.idx
        evals = int(self.evaluations) if self.f_aggregate else 1
        fagg = np.median if self.f_aggregate is None else self.f_aggregate
        for i in self.idx:
            X_i = X[i]
            if self.epsilon:
                if self.parallel:
                    self.fitre[i] = fagg(func(ask(evals, X_i, self.epsilon), *args))
                else:
                    self.fitre[i] = fagg([func(ask(1, X_i, self.epsilon)[0], *args)
                                            for _k in range(evals)])
            else:
                self.fitre[i] = fagg([func(X_i, *args) for _k in range(evals)])
        self.evaluations_just_done = evals * len(self.idx)
        return self.fit, self.fitre, self.idx

    def update_measure(self):
        """updated noise level measure using two fitness lists ``self.fit`` and
        ``self.fitre``, return ``self.noiseS, all_individual_measures``.

        Assumes that `self.idx` contains the indices where the fitness
        lists differ

        """
        lam = len(self.fit)
        idx = np.argsort(self.fit + self.fitre)
        ranks = np.argsort(idx).reshape((2, lam))
        rankDelta = ranks[0] - ranks[1] - np.sign(ranks[0] - ranks[1])

        
        r = np.arange(1, 2 * lam)  
        limits = [0.5 * (Mh.prctile(np.abs(r - (ranks[0, i] + 1 - (ranks[0, i] > ranks[1, i]))),
                                      self.theta * 50) +
                         Mh.prctile(np.abs(r - (ranks[1, i] + 1 - (ranks[1, i] > ranks[0, i]))),
                                      self.theta * 50))
                    for i in self.idx]
        
        
        s = np.abs(rankDelta[self.idx]) - Mh.amax(limits, 1)  
        self.noiseS += self.cum * (np.mean(s) - self.noiseS)
        return self.noiseS, s

    def indices(self, fit):
        """return the set of indices to be reevaluated for noise
        measurement.

        Given the first values are the earliest, this is a useful policy also
        with a time changing objective.

        """
        
        lam_reev = 1.0 * (self.lam_reeval if self.lam_reeval
                            else 2 + len(fit) / 20)
        lam_reev = int(lam_reev) + ((lam_reev % 1) > np.random.rand())
        
        choice = 1
        if choice == 1:
            
            n_first = lam_reev - lam_reev // 2
            sort_idx = np.argsort(array(fit, copy=False)[n_first:]) + n_first
            return np.array(list(range(0, n_first)) +
                            list(sort_idx[0:lam_reev - n_first]), copy=False)
        elif choice == 2:
            idx_sorted = np.argsort(array(fit, copy=False))
            
            linsp = np.linspace(0, len(fit) - len(fit) / lam_reev, lam_reev)
            return idx_sorted[[int(i) for i in linsp]]
        
        elif choice == 3:
            return np.argsort(array(fit, copy=False)[:2 * (lam_reev + 1)])[:lam_reev]
        else:
            raise ValueError('unrecognized choice value %d for noise reev'
                             % choice)



class Sections(object):
    """plot sections through an objective function.

    A first rational thing to do, when facing an (expensive)
    application. By default 6 points in each coordinate are evaluated.
    This class is still experimental.

    Examples
    --------

    >>> import cma, numpy as np
    >>> s = cma.Sections(cma.Fcts.rosen, np.zeros(3)).do(plot=False)
    >>> s.do(plot=False)  
    >> try:
    ...     s.plot()
    ... except:
    ...     print('plotting failed: matplotlib.pyplot package missing?')

    Details
    -------
    Data are saved after each function call during `do()`. The filename
    is attribute ``name`` and by default ``str(func)``, see `__init__()`.

    A random (orthogonal) basis can be generated with
    ``cma.Rotation()(np.eye(3))``.

    CAVEAT: The default name is unique in the function name, but it
    should be unique in all parameters of `__init__()` but `plot_cmd`
    and `load`. If, for example, a different basis is chosen, either
    the name must be changed or the ``.pkl`` file containing the
    previous data must first be renamed or deleted.

    ``s.res`` is a dictionary with an entry for each "coordinate" ``i``
    and with an entry ``'x'``, the middle point. Each entry ``i`` is
    again a dictionary with keys being different dx values and the
    value being a sequence of f-values. For example ``s.res[2][0.1] ==
    [0.01, 0.01]``, which is generated using the difference vector ``s
    .basis[2]`` like

    ``s.res[2][dx] += func(s.res['x'] + dx * s.basis[2])``.

    :See: `__init__()`

    """
    def __init__(self, func, x, args=(), basis=None, name=None,
                 plot_cmd=pyplot.plot if pyplot else None, load=True):
        """
        Parameters
        ----------
            `func`
                objective function
            `x`
                point in search space, middle point of the sections
            `args`
                arguments passed to `func`
            `basis`
                evaluated points are ``func(x + locations[j] * basis[i])
                for i in len(basis) for j in len(locations)``,
                see `do()`
            `name`
                filename where to save the result
            `plot_cmd`
                command used to plot the data, typically matplotlib pyplots `plot` or `semilogy`
            `load`
                load previous data from file ``str(func) + '.pkl'``

        """
        self.func = func
        self.args = args
        self.x = x
        self.name = name if name else str(func).replace(' ', '_').replace('>', '').replace('<', '')
        self.plot_cmd = plot_cmd  
        self.basis = np.eye(len(x)) if basis is None else basis

        try:
            self.load()
            if any(self.res['x'] != x):
                self.res = {}
                self.res['x'] = x  
            else:
                print(self.name + ' loaded')
        except:
            self.res = {}
            self.res['x'] = x

    def do(self, repetitions=1, locations=np.arange(-0.5, 0.6, 0.2), plot=True):
        """generates, plots and saves function values ``func(y)``,
        where ``y`` is 'close' to `x` (see `__init__()`). The data are stored in
        the ``res`` attribute and the class instance is saved in a file
        with (the weired) name ``str(func)``.

        Parameters
        ----------
            `repetitions`
                for each point, only for noisy functions is >1 useful. For
                ``repetitions==0`` only already generated data are plotted.
            `locations`
                coordinated wise deviations from the middle point given in `__init__`

        """
        if not repetitions:
            self.plot()
            return

        res = self.res
        for i in range(len(self.basis)):  
            if i not in res:
                res[i] = {}
            
            
            for dx in locations:
                xx = self.x + dx * self.basis[i]
                xkey = dx  
                if xkey not in res[i]:
                    res[i][xkey] = []
                n = repetitions
                while n > 0:
                    n -= 1
                    res[i][xkey].append(self.func(xx, *self.args))
                    if plot:
                        self.plot()
                    self.save()
        return self

    def plot(self, plot_cmd=None, tf=lambda y: y):
        """plot the data we have, return ``self``"""
        if not plot_cmd:
            plot_cmd = self.plot_cmd
        colors = 'bgrcmyk'
        pyplot.hold(False)
        res = self.res

        flatx, flatf = self.flattened()
        minf = np.inf
        for i in flatf:
            minf = min((minf, min(flatf[i])))
        addf = 1e-9 - minf if minf <= 1e-9 else 0
        for i in sorted(res.keys()):  
            if isinstance(i, int):
                color = colors[i % len(colors)]
                arx = sorted(res[i].keys())
                plot_cmd(arx, [tf(np.median(res[i][x]) + addf) for x in arx], color + '-')
                pyplot.text(arx[-1], tf(np.median(res[i][arx[-1]])), i)
                pyplot.hold(True)
                plot_cmd(flatx[i], tf(np.array(flatf[i]) + addf), color + 'o')
        pyplot.ylabel('f + ' + str(addf))
        pyplot.draw()
        pyplot.ion()
        pyplot.show()
        
        return self

    def flattened(self):
        """return flattened data ``(x, f)`` such that for the sweep through
        coordinate ``i`` we have for data point ``j`` that ``f[i][j] == func(x[i][j])``

        """
        flatx = {}
        flatf = {}
        for i in self.res:
            if isinstance(i, int):
                flatx[i] = []
                flatf[i] = []
                for x in sorted(self.res[i]):
                    for d in sorted(self.res[i][x]):
                        flatx[i].append(x)
                        flatf[i].append(d)
        return flatx, flatf

    def save(self, name=None):
        """save to file"""
        import pickle
        name = name if name else self.name
        fun = self.func
        del self.func  
        pickle.dump(self, open(name + '.pkl', "wb"))
        self.func = fun
        return self

    def load(self, name=None):
        """load from file"""
        import pickle
        name = name if name else self.name
        s = pickle.load(open(name + '.pkl', 'rb'))
        self.res = s.res  
        return self



class _Error(Exception):
    """generic exception of cma module"""
    pass




class ElapsedTime(object):
    """using ``time.clock`` with overflow handling to measure CPU time.

    Example:

    >>> clock = ElapsedTime()  
    >>> t1 = clock()  

    Details: 32-bit C overflows after int(2**32/1e6) == 4294s about 72 min

    """
    def __init__(self):
        self.tic0 = time.clock()
        self.tic = self.tic0
        self.lasttoc = time.clock()
        self.lastdiff = time.clock() - self.lasttoc
        self.time_to_add = 0
        self.messages = 0
    reset = __init__
    def __call__(self):
        toc = time.clock()
        if toc - self.tic >= self.lasttoc - self.tic:
            self.lastdiff = toc - self.lasttoc
            self.lasttoc = toc
        else:  
            if self.messages < 3:
                self.messages += 1
                print('  in cma.ElapsedTime: time measure overflow, last difference estimated from',
                        self.tic0, self.tic, self.lasttoc, toc, toc - self.lasttoc, self.lastdiff)

            self.time_to_add += self.lastdiff + self.lasttoc - self.tic
            self.tic = toc  
            self.lasttoc = toc
        self.elapsedtime = toc - self.tic + self.time_to_add
        return self.elapsedtime

class Misc(object):
    
    
    
    class MathHelperFunctions(object):
        """static convenience math helper functions, if the function name
        is preceded with an "a", a numpy array is returned

        """
        @staticmethod
        def aclamp(x, upper):
            return -Misc.MathHelperFunctions.apos(-x, -upper)
        @staticmethod
        def equals_approximately(a, b, eps=1e-12):
            if a < 0:
                a, b = -1 * a, -1 * b
            return (a - eps < b < a + eps) or ((1 - eps) * a < b < (1 + eps) * a)
        @staticmethod
        def vequals_approximately(a, b, eps=1e-12):
            a, b = array(a), array(b)
            idx = np.where(a < 0)[0]
            if len(idx):
                a[idx], b[idx] = -1 * a[idx], -1 * b[idx]
            return (np.all(a - eps < b) and np.all(b < a + eps)
                    ) or (np.all((1 - eps) * a < b) and np.all(b < (1 + eps) * a))
        @staticmethod
        def expms(A, eig=np.linalg.eigh):
            """matrix exponential for a symmetric matrix"""
            
            
            D, B = eig(A)
            return np.dot(B, (np.exp(D) * B).T)
        @staticmethod
        def amax(vec, vec_or_scalar):
            return array(Misc.MathHelperFunctions.max(vec, vec_or_scalar))
        @staticmethod
        def max(vec, vec_or_scalar):
            b = vec_or_scalar
            if isscalar(b):
                m = [max(x, b) for x in vec]
            else:
                m = [max(vec[i], b[i]) for i in rglen((vec))]
            return m
        @staticmethod
        def minmax(val, min_val, max_val):
            assert min_val <= max_val
            return min((max_val, max((val, min_val))))
        @staticmethod
        def aminmax(val, min_val, max_val):
            return array([min((max_val, max((v, min_val)))) for v in val])
        @staticmethod
        def amin(vec_or_scalar, vec_or_scalar2):
            return array(Misc.MathHelperFunctions.min(vec_or_scalar, vec_or_scalar2))
        @staticmethod
        def min(a, b):
            iss = isscalar
            if iss(a) and iss(b):
                return min(a, b)
            if iss(a):
                a, b = b, a
            
            if iss(b):
                return [min(x, b) for x in a]
            else:  
                return [min(a[i], b[i]) for i in rglen((a))]
        @staticmethod
        def norm(vec, expo=2):
            return sum(vec**expo)**(1 / expo)
        @staticmethod
        def apos(x, lower=0):
            """clips argument (scalar or array) from below at lower"""
            if lower == 0:
                return (x > 0) * x
            else:
                return lower + (x > lower) * (x - lower)
        @staticmethod
        def prctile(data, p_vals=[0, 25, 50, 75, 100], sorted_=False):
            """``prctile(data, 50)`` returns the median, but p_vals can
            also be a sequence.

            Provides for small samples better values than matplotlib.mlab.prctile,
            however also slower.

            """
            ps = [p_vals] if isscalar(p_vals) else p_vals

            if not sorted_:
                data = sorted(data)
            n = len(data)
            d = []
            for p in ps:
                fi = p * n / 100 - 0.5
                if fi <= 0:  
                    d.append(data[0])
                elif fi >= n - 1:
                    d.append(data[-1])
                else:
                    i = int(fi)
                    d.append((i + 1 - fi) * data[i] + (fi - i) * data[i + 1])
            return d[0] if isscalar(p_vals) else d
        @staticmethod
        def sround(nb):  
            """return stochastic round: floor(nb) + (rand()<remainder(nb))"""
            return nb // 1 + (np.random.rand(1)[0] < (nb % 1))

        @staticmethod
        def cauchy_with_variance_one():
            n = np.random.randn() / np.random.randn()
            while abs(n) > 1000:
                n = np.random.randn() / np.random.randn()
            return n / 25
        @staticmethod
        def standard_finite_cauchy(size=1):
            try:
                l = len(size)
            except TypeError:
                l = 0

            if l == 0:
                return array([Mh.cauchy_with_variance_one() for _i in range(size)])
            elif l == 1:
                return array([Mh.cauchy_with_variance_one() for _i in range(size[0])])
            elif l == 2:
                return array([[Mh.cauchy_with_variance_one() for _i in range(size[1])]
                             for _j in range(size[0])])
            else:
                raise _Error('len(size) cannot be large than two')


    @staticmethod
    def likelihood(x, m=None, Cinv=None, sigma=1, detC=None):
        """return likelihood of x for the normal density N(m, sigma**2 * Cinv**-1)"""
        
        
        if m is None:
            dx = x
        else:
            dx = x - m  
        n = len(x)
        s2pi = (2 * np.pi)**(n / 2.)
        if Cinv is None:
            return exp(-sum(dx**2) / sigma**2 / 2) / s2pi / sigma**n
        if detC is None:
            detC = 1. / np.linalg.linalg.det(Cinv)
        return  exp(-np.dot(dx, np.dot(Cinv, dx)) / sigma**2 / 2) / s2pi / abs(detC)**0.5 / sigma**n

    @staticmethod
    def loglikelihood(self, x, previous=False):
        """return log-likelihood of `x` regarding the current sample distribution"""
        
        
        
        
        

        if previous and hasattr(self, 'lastiter'):
            sigma = self.lastiter.sigma
            Crootinv = self.lastiter._Crootinv
            xmean = self.lastiter.mean
            D = self.lastiter.D
        elif previous and self.countiter > 1:
            raise _Error('no previous distribution parameters stored, check options importance_mixing')
        else:
            sigma = self.sigma
            Crootinv = self._Crootinv
            xmean = self.mean
            D = self.D

        dx = array(x) - xmean  
        n = self.N
        logs2pi = n * log(2 * np.pi) / 2.
        logdetC = 2 * sum(log(D))
        dx = np.dot(Crootinv, dx)
        res = -sum(dx**2) / sigma**2 / 2 - logs2pi - logdetC / 2 - n * log(sigma)
        if 1 < 3:  
            s2pi = (2 * np.pi)**(n / 2.)
            detC = np.prod(D)**2
            res2 = -sum(dx**2) / sigma**2 / 2 - log(s2pi * abs(detC)**0.5 * sigma**n)
            assert res2 < res + 1e-8 or res2 > res - 1e-8
        return res

    
    
    
    
    

    
    


    
    @staticmethod
    def eig(C):
        """eigendecomposition of a symmetric matrix, much slower than
        `numpy.linalg.eigh`, return ``(EVals, Basis)``, the eigenvalues
        and an orthonormal basis of the corresponding eigenvectors, where

            ``Basis[i]``
                the i-th row of ``Basis``
            columns of ``Basis``, ``[Basis[j][i] for j in range(len(Basis))]``
                the i-th eigenvector with eigenvalue ``EVals[i]``

        """

    
    

    
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        


        
        

        
        def tred2 (n, V, d, e):
            
            
            
            

            num_opt = False  

            for j in range(n):
                d[j] = V[n - 1][j]  

            

            for i in range(n - 1, 0, -1):
                
                h = 0.0
                if not num_opt:
                    scale = 0.0
                    for k in range(i):
                        scale = scale + abs(d[k])
                else:
                    scale = sum(abs(d[0:i]))

                if scale == 0.0:
                    e[i] = d[i - 1]
                    for j in range(i):
                        d[j] = V[i - 1][j]
                        V[i][j] = 0.0
                        V[j][i] = 0.0
                else:

                    
                    if not num_opt:
                        for k in range(i):
                            d[k] /= scale
                            h += d[k] * d[k]
                    else:
                        d[:i] /= scale
                        h = np.dot(d[:i], d[:i])

                    f = d[i - 1]
                    g = h**0.5

                    if f > 0:
                        g = -g

                    e[i] = scale * g
                    h = h - f * g
                    d[i - 1] = f - g
                    if not num_opt:
                        for j in range(i):
                            e[j] = 0.0
                    else:
                        e[:i] = 0.0

                    

                    for j in range(i):
                        f = d[j]
                        V[j][i] = f
                        g = e[j] + V[j][j] * f
                        if not num_opt:
                            for k in range(j + 1, i):
                                g += V[k][j] * d[k]
                                e[k] += V[k][j] * f
                            e[j] = g
                        else:
                            e[j + 1:i] += V.T[j][j + 1:i] * f
                            e[j] = g + np.dot(V.T[j][j + 1:i], d[j + 1:i])

                    f = 0.0
                    if not num_opt:
                        for j in range(i):
                            e[j] /= h
                            f += e[j] * d[j]
                    else:
                        e[:i] /= h
                        f += np.dot(e[:i], d[:i])

                    hh = f / (h + h)
                    if not num_opt:
                        for j in range(i):
                            e[j] -= hh * d[j]
                    else:
                        e[:i] -= hh * d[:i]

                    for j in range(i):
                        f = d[j]
                        g = e[j]
                        if not num_opt:
                            for k in range(j, i):
                                V[k][j] -= (f * e[k] + g * d[k])
                        else:
                            V.T[j][j:i] -= (f * e[j:i] + g * d[j:i])

                        d[j] = V[i - 1][j]
                        V[i][j] = 0.0

                d[i] = h
            

            

            for i in range(n - 1):
                V[n - 1][i] = V[i][i]
                V[i][i] = 1.0
                h = d[i + 1]
                if h != 0.0:
                    if not num_opt:
                        for k in range(i + 1):
                            d[k] = V[k][i + 1] / h
                    else:
                        d[:i + 1] = V.T[i + 1][:i + 1] / h

                    for j in range(i + 1):
                        if not num_opt:
                            g = 0.0
                            for k in range(i + 1):
                                g += V[k][i + 1] * V[k][j]
                            for k in range(i + 1):
                                V[k][j] -= g * d[k]
                        else:
                            g = np.dot(V.T[i + 1][0:i + 1], V.T[j][0:i + 1])
                            V.T[j][:i + 1] -= g * d[:i + 1]

                if not num_opt:
                    for k in range(i + 1):
                        V[k][i + 1] = 0.0
                else:
                    V.T[i + 1][:i + 1] = 0.0


            if not num_opt:
                for j in range(n):
                    d[j] = V[n - 1][j]
                    V[n - 1][j] = 0.0
            else:
                d[:n] = V[n - 1][:n]
                V[n - 1][:n] = 0.0

            V[n - 1][n - 1] = 1.0
            e[0] = 0.0


        
        
        
        def tql2 (n, d, e, V):

            
            
            
            

            num_opt = False  

            if not num_opt:
                for i in range(1, n):  
                    e[i - 1] = e[i]
            else:
                e[0:n - 1] = e[1:n]
            e[n - 1] = 0.0

            f = 0.0
            tst1 = 0.0
            eps = 2.0**-52.0
            for l in range(n):  

                

                tst1 = max(tst1, abs(d[l]) + abs(e[l]))
                m = l
                while m < n:
                    if abs(e[m]) <= eps * tst1:
                        break
                    m += 1

                
                

                if m > l:
                    iiter = 0
                    while 1:  
                        iiter += 1  

                        

                        g = d[l]
                        p = (d[l + 1] - g) / (2.0 * e[l])
                        r = (p**2 + 1)**0.5  
                        if p < 0:
                            r = -r

                        d[l] = e[l] / (p + r)
                        d[l + 1] = e[l] * (p + r)
                        dl1 = d[l + 1]
                        h = g - d[l]
                        if not num_opt:
                            for i in range(l + 2, n):
                                d[i] -= h
                        else:
                            d[l + 2:n] -= h

                        f = f + h

                        

                        p = d[m]
                        c = 1.0
                        c2 = c
                        c3 = c
                        el1 = e[l + 1]
                        s = 0.0
                        s2 = 0.0

                        
                        for i in range(m - 1, l - 1, -1):  
                            c3 = c2
                            c2 = c
                            s2 = s
                            g = c * e[i]
                            h = c * p
                            r = (p**2 + e[i]**2)**0.5  
                            e[i + 1] = s * r
                            s = e[i] / r
                            c = p / r
                            p = c * d[i] - s * g
                            d[i + 1] = h + s * (c * g + s * d[i])

                            

                            if not num_opt:  
                                for k in range(n):  
                                    h = V[k][i + 1]
                                    V[k][i + 1] = s * V[k][i] + c * h
                                    V[k][i] = c * V[k][i] - s * h
                            else:  
                                hh = V.T[i + 1].copy()
                                
                                V.T[i + 1] = s * V.T[i] + c * hh
                                V.T[i] = c * V.T[i] - s * hh
                                
                                

                        p = -s * s2 * c3 * el1 * e[l] / dl1
                        e[l] = s * p
                        d[l] = c * p

                        
                        if abs(e[l]) <= eps * tst1:
                            break
                    

                d[l] = d[l] + f
                e[l] = 0.0


            
        

        N = len(C[0])
        if 1 < 3:
            V = [[x[i] for i in range(N)] for x in C]  "row"
            d = N * [0.]
            e = N * [0.]

        tred2(N, V, d, e)
        tql2(N, d, e, V)
        return (array(d), array(V))
Mh = Misc.MathHelperFunctions




def pprint(to_be_printed):
    """nicely formated print"""
    try:
        import pprint as pp
        
        
        pp.pprint(to_be_printed)
    except ImportError:
        if isinstance(to_be_printed, dict):
            print('{')
            for k, v in list(to_be_printed.items()):
                print("'" + k + "'" if isinstance(k, str) else k,
                      ': ',
                      "'" + v + "'" if isinstance(k, str) else v,
                      sep="")
            print('}')
        else:
            print('could not import pprint module, appling regular print')
            print(to_be_printed)

pp = pprint

class ConstRandnShift(object):
    """``ConstRandnShift()(x)`` adds a fixed realization of
    ``stddev * randn(len(x))`` to the vector x.

    By default, the realized shift is the same for each instance of
    ``ConstRandnShift``, see ``seed`` argument. This class is used in
    class ``FFWrapper.ShiftedFitness`` as default transformation.

    See: class ``FFWrapper.ShiftedFitness``

    """
    def __init__(self, stddev=3, seed=1):
        """with ``seed=None`` each instance realizes a different shift"""
        self.seed = seed
        self.stddev = stddev
        self._xopt = {}
    def __call__(self, x):
        """return "shifted" ``x - shift``

        """
        try:
            x_opt = self._xopt[len(x)]
        except KeyError:
            if self.seed is None:
                shift = np.random.randn(len(x))
            else:
                rstate = np.random.get_state()
                np.random.seed(self.seed)
                shift = np.random.randn(len(x))
                np.random.set_state(rstate)
            x_opt = self._xopt.setdefault(len(x), self.stddev * shift)
        return array(x, copy=False) - x_opt
    def get(self, dimension):
        """return shift applied to ``zeros(dimension)``

            >>> import numpy as np, cma
            >>> s = cma.ConstRandnShift()
            >>> assert all(s(-s.get(3)) == np.zeros(3))
            >>> assert all(s.get(3) == s(np.zeros(3)))

        """
        return self.__call__(np.zeros(dimension))

class Rotation(object):
    """Rotation class that implements an orthogonal linear transformation,
    one for each dimension.

    By default reach ``Rotation`` instance provides a different "random"
    but fixed rotation. This class is used to implement non-separable
    test functions, most conveniently via `FFWrapper.RotatedFitness`.

    Example:

    >>> import cma, numpy as np
    >>> R = cma.Rotation()
    >>> R2 = cma.Rotation() 
    >>> x = np.array((1,2,3))
    >>> print(R(R(x), inverse=1))
    [ 1.  2.  3.]

    See: `FFWrapper.RotatedFitness`

    """
    dicMatrices = {}  
    def __init__(self, seed=None):
        """by default a random but fixed rotation, different for each instance"""
        self.seed = seed
        self.dicMatrices = {}  
    def __call__(self, x, inverse=False):  
        """Rotates the input array `x` with a fixed rotation matrix
           (``self.dicMatrices['str(len(x))']``)
        """
        x = np.array(x, copy=False)
        N = x.shape[0]  
        if str(N) not in self.dicMatrices:  
            rstate = np.random.get_state()
            np.random.seed(self.seed) if self.seed else np.random.seed()
            B = np.random.randn(N, N)
            for i in range(N):
                for j in range(0, i):
                    B[i] -= np.dot(B[i], B[j]) * B[j]
                B[i] /= sum(B[i]**2)**0.5
            self.dicMatrices[str(N)] = B
            np.random.set_state(rstate)
        if inverse:
            return np.dot(self.dicMatrices[str(N)].T, x)  
        else:
            return np.dot(self.dicMatrices[str(N)], x)  

rotate = Rotation()





class FFWrapper(object):
    """
    A collection of (yet experimental) classes to implement fitness
    transformations and wrappers. Aliased to `FF2` below.

    """
    class FitnessTransformation(object):
        """This class does nothing but serve as an interface template.
        Typical use-case::

          f = FitnessTransformation(f, parameters_if_needed)``

        See: class ``TransformSearchSpace``

        """
        def __init__(self, fitness_function, *args, **kwargs):
            """`fitness_function` must be callable (e.g. a function
            or a callable class instance)"""
            
            self.inner_fitness = fitness_function
            
        def __call__(self, x, *args):
            """identity as default transformation"""
            if hasattr(self, 'x_transformation'):
                x = self.x_transformation(x)
            f = self.inner_fitness(x, *args)
            if hasattr(self, 'f_transformation'):
                f = self.f_transformation(f)
            return f
    class BookKeeping(FitnessTransformation):
        """a stump for experimenting with use-cases and possible
        extensions of book keeping

        use-case:

            f = BookKeeping(f)
            print(f.count_evaluations)

        """
        def __init__(self, callable=None):
            self.count_evaluations = 0
            self.inner_fitness = callable
        def __call__(self, *args):
            
            self.count_evaluations += 1
            return self.inner_fitness(*args)
    class TransformSearchSpace(FitnessTransformation):
        """::

            f = TransformSearchSpace(f, ConstRandnShift())

        constructs the composed function f <- f o shift.

        Details: to some extend this is a nice shortcut for::

            f = lambda x, *args: f_in(ConstRandnShift()(x), *args)

        however the `lambda` definition depends on the value of
        ``f_in`` even after ``f`` has been assigned.

        See: `ShiftedFitness`, `RotatedFitness`

        """
        def __init__(self, fitness_function, transformation):
            """``TransformSearchSpace(f, s)(x) == f(s(x))``

                >>> import cma
                >>> f0 = lambda x: sum(x)
                >>> shift_fct = cma.ConstRandnShift()
                >>> f = cma.FF2.TransformSearchSpace(f0, shift_fct)
                >>> x = [1, 2, 3]
                >>> assert f(x) == f0(shift_fct(x))

            """
            self.inner_fitness = fitness_function
            
            
            self.x_transformation = transformation
            
    class ScaleCoordinates(TransformSearchSpace):
        """define a scaling of each variable
        """
        def __init__(self, fitness_function, multipliers=None):
            """
            :param fitness_function: a callable object
            :param multipliers: recycling is not implemented, i.e.
                 the dimension must fit to the `fitness_function` argument
                 when called
            """
            super(FFWrapper.ScaleCoordinates, self).__init__(
                    fitness_function, self.transformation)
            
            
            self.multiplier = multipliers
            if self.multiplier is not None and hasattr(self.multiplier, 'len'):
                self.multiplier = array(self.multiplier, copy=True)
        def transformation(x, *args):
            if self.multiplier is None:
                return array(x, copy=False)
            return self.multiplier * array(x, copy=False)

    class ShiftedFitness(TransformSearchSpace):
        """``f = cma.ShiftedFitness(cma.fcts.sphere)`` constructs a
        shifted sphere function, by default the shift is computed
        from class ``ConstRandnShift`` with std dev 3.

        """
        def __init__(self, f, shift=None):
            """``shift(x)`` must return a (stable) shift of x.

            Details: this class solely provides as default second
            argument to TransformSearchSpace a shift in search space.
            ``shift=lambda x: x`` would provide "no shift", ``None``
            expands to ``cma.ConstRandnShift()``.

            """
            self.inner_fitness = f
            self.x_transformation = shift if shift else ConstRandnShift()
            
    class RotatedFitness(TransformSearchSpace):
        """``f = cma.RotatedFitness(cma.fcts.elli)`` constructs a
        rotated ellipsoid function

        """
        def __init__(self, f, rotate=rotate):
            """``rotate(x)`` must return a (stable) rotation of x.

            Details: this class solely provides a default second
            argument to TransformSearchSpace, namely a search space
            rotation.

            """
            super(FFWrapper.RotatedFitness, self).__init__(f, rotate)
            
    class FixVariables(TransformSearchSpace):
        """fix variables to given values, thereby reducing the
        dimensionality of the preimage.

        The constructor takes ``index_value_pairs`` as dict or list of
        pairs as input and returns a function with smaller preimage space
        than `f`.

        Details: this might replace the fixed_variables option in
        CMAOptions in future, but hasn't been tested yet.

        """
        def __init__(self, f, index_value_pairs):
            """`f` has """
            super(FFWrapper.FixVariables, self).__init__(f, self.insert_variables)
            
            self.index_value_pairs = dict(index_value_pairs)
        def insert_variables(self, x):
            y = np.zeros(len(x) + len(self.index_value_pairs))
            assert len(y) > max(self.index_value_pairs)
            j = 0
            for i in range(len(y)):
                if i in self.index_value_pairs:
                    y[i] = self.index_value_pairs[i]
                else:
                    y[i] = x[j]
                    j += 1
            return y
    class SomeNaNFitness(FitnessTransformation):
        def __init__(self, fitness_function, probability_of_nan=0.1):
            self.p = probability_of_nan
            self.inner_fitness = fitness_function
        def __call__(self, x, *args):
            if np.random.rand(1) <= self.p:
                return np.NaN
            else:
                return self.inner_fitness(x, *args)
    class NoisyFitness(FitnessTransformation):
        """apply noise via f += rel_noise(dim) * f + abs_noise()"""
        def __init__(self, fitness_function,
                     rel_noise=lambda dim: 1.1 * np.random.randn() / dim,
                     abs_noise=lambda: 1.1 * np.random.randn()):
            self.rel_noise = rel_noise
            self.abs_noise = abs_noise
            self.inner_fitness = fitness_function
        def __call__(self, x, *args):
            f = self.inner_fitness(x, *args)
            if self.rel_noise:
                f += f * self.rel_noise(len(x))
                assert isscalar(f)
            if self.abs_noise:
                f += self.abs_noise()
            return f
    class GlueArguments(FitnessTransformation):
        """``f = cma.FF2.GlueArguments(cma.fcts.elli, cond=1e4)``

            >>> import cma
            >>> f = cma.FF2.GlueArguments(cma.fcts.elli, cond=1e1)
            >>> f([1, 2])  
            41.0

        """
        def __init__(self, fitness_function, *args, **kwargs):
            self.inner_fitness = fitness_function
            self.args = args
            self.kwargs = kwargs
        def __call__(self, x, *args):
            return self.inner_fitness(array(x, copy=False),
                                *(args + self.args), **self.kwargs)
    class UnknownFF(object):
        """search in [-10, 10] for the unknown (optimum)"""
        def __init__(self, seed=2):
            self.seed = seed
            self._x_opt_ = {}
            self.rotate = Rotation(seed)
            self.count_evaluations = 0
        def _x_opt(self, dim):
            rstate = np.random.get_state()
            np.random.seed(self.seed)
            x = self._x_opt_.setdefault(dim,
                                        0 * 3 * np.random.randn(dim))
            np.random.set_state(rstate)
            return x
        def typical_x(self, dim):
            off = self.rotate(np.floor(np.arange(0, 3, 3. / dim)) /
                          np.logspace(0, 1, dim), inverse=True)
            off[np.s_[3:]] += 0.005
            off[-1] *= 1e2
            off[0] /= 2.0e3 if off[0] > 0 else 1e3
            off[2] /= 3.01e4 if off[2] < 0 else 2e4
            return self._x_opt(dim) + off
        def __call__(self, x):
            self.count_evaluations += 1
            N = len(x)
            x = x - self._x_opt(N)
            x[-1] /= 1e2
            x[0] *= 2.0e3 if x[0] > 0 else 1e3
            x[2] *= 3.01e4 if x[2] < 0 else 2e4
            x = np.logspace(0, 1, N) * self.rotate(x)
            return 10 * N - np.e**2 + \
                        sum(x**2 - 10 * np.cos(2 * np.pi * x))

FF2 = FFWrapper

class FitnessFunctions(object):
    """ versatile container for test objective functions """

    def __init__(self):
        self.counter = 0  
    def rot(self, x, fun, rot=1, args=()):
        """returns ``fun(rotation(x), *args)``, ie. `fun` applied to a rotated argument"""
        if len(np.shape(array(x))) > 1:  
            res = []
            for x in x:
                res.append(self.rot(x, fun, rot, args))
            return res

        if rot:
            return fun(rotate(x, *args))
        else:
            return fun(x)
    def somenan(self, x, fun, p=0.1):
        """returns sometimes np.NaN, otherwise fun(x)"""
        if np.random.rand(1) < p:
            return np.NaN
        else:
            return fun(x)
    def rand(self, x):
        """Random test objective function"""
        return np.random.random(1)[0]
    def linear(self, x):
        return -x[0]
    def lineard(self, x):
        if 1 < 3 and any(array(x) < 0):
            return np.nan
        if 1 < 3 and sum([ (10 + i) * x[i] for i in rglen(x)]) > 50e3:
            return np.nan
        return -sum(x)
    def sphere(self, x):
        """Sphere (squared norm) test objective function"""
        
        return sum((x + 0)**2)
    def grad_sphere(self, x, *args):
        return 2*array(x, copy=False)
    def grad_to_one(self, x, *args):
        return array(x, copy=False) - 1
    def sphere_pos(self, x):
        """Sphere (squared norm) test objective function"""
        
        c = 0.0
        if x[0] < c:
            return np.nan
        return -c**2 + sum((x + 0)**2)
    def spherewithoneconstraint(self, x):
        return sum((x + 0)**2) if x[0] > 1 else np.nan
    def elliwithoneconstraint(self, x, idx=[-1]):
        return self.ellirot(x) if all(array(x)[idx] > 1) else np.nan

    def spherewithnconstraints(self, x):
        return sum((x + 0)**2) if all(array(x) > 1) else np.nan
    
    def noisysphere(self, x, noise=2.10e-9, cond=1.0, noise_offset=0.10):
        """noise=10 does not work with default popsize, noise handling does not help """
        return self.elli(x, cond=cond) * (1 + noise * np.random.randn() / len(x)) + noise_offset * np.random.rand()
    def spherew(self, x):
        """Sphere (squared norm) with sum x_i = 1 test objective function"""
        
        
        
        
        return -0.01 * x[0] + abs(x[0])**-2 * sum(x[1:]**2)
    def partsphere(self, x):
        """Sphere (squared norm) test objective function"""
        self.counter += 1
        
        dim = len(x)
        x = array([x[i % dim] for i in range(2 * dim)])
        N = 8
        i = self.counter % dim
        
        f = sum(x[np.random.randint(dim, size=N)]**2)
        return f
    def sectorsphere(self, x):
        """asymmetric Sphere (squared norm) test objective function"""
        return sum(x**2) + (1e6 - 1) * sum(x[x < 0]**2)
    def cornersphere(self, x):
        """Sphere (squared norm) test objective function constraint to the corner"""
        nconstr = len(x) - 0
        if any(x[:nconstr] < 1):
            return np.NaN
        return sum(x**2) - nconstr
    def cornerelli(self, x):
        """ """
        if any(x < 1):
            return np.NaN
        return self.elli(x) - self.elli(np.ones(len(x)))
    def cornerellirot(self, x):
        """ """
        if any(x < 1):
            return np.NaN
        return self.ellirot(x)
    def normalSkew(self, f):
        N = np.random.randn(1)[0]**2
        if N < 1:
            N = f * N  
        return N
    def noiseC(self, x, func=sphere, fac=10, expon=0.8):
        f = func(self, x)
        N = np.random.randn(1)[0] / np.random.randn(1)[0]
        return max(1e-19, f + (float(fac) / len(x)) * f**expon * N)
    def noise(self, x, func=sphere, fac=10, expon=1):
        f = func(self, x)
        
        R = np.log10(f) + expon * abs(10 - np.log10(f)) * np.random.rand(1)[0]
        
        
        
        
        
        return f + 10**R  
    def cigar(self, x, rot=0, cond=1e6, noise=0):
        """Cigar test objective function"""
        if rot:
            x = rotate(x)
        x = [x] if isscalar(x[0]) else x  
        f = [(x[0]**2 + cond * sum(x[1:]**2)) * np.exp(noise * np.random.randn(1)[0] / len(x)) for x in x]
        return f if len(f) > 1 else f[0]  
    def grad_cigar(self, x, *args):
        grad = 2 * 1e6 * np.array(x)
        grad[0] /= 1e6
        return grad
    def diagonal_cigar(self, x, cond=1e6):
        axis = np.ones(len(x)) / len(x)**0.5
        proj = dot(axis, x) * axis
        s = sum(proj**2)
        s += cond * sum((x - proj)**2)
        return s
    def tablet(self, x, rot=0):
        """Tablet test objective function"""
        if rot and rot is not fcts.tablet:
            x = rotate(x)
        x = [x] if isscalar(x[0]) else x  
        f = [1e6 * x[0]**2 + sum(x[1:]**2) for x in x]
        return f if len(f) > 1 else f[0]  
    def grad_tablet(self, x, *args):
        grad = 2 * np.array(x)
        grad[0] *= 1e6
        return grad
    def cigtab(self, y):
        """Cigtab test objective function"""
        X = [y] if isscalar(y[0]) else y
        f = [1e-4 * x[0]**2 + 1e4 * x[1]**2 + sum(x[2:]**2) for x in X]
        return f if len(f) > 1 else f[0]
    def twoaxes(self, y):
        """Cigtab test objective function"""
        X = [y] if isscalar(y[0]) else y
        N2 = len(X[0]) // 2
        f = [1e6 * sum(x[0:N2]**2) + sum(x[N2:]**2) for x in X]
        return f if len(f) > 1 else f[0]
    def ellirot(self, x):
        return fcts.elli(array(x), 1)
    def hyperelli(self, x):
        N = len(x)
        return sum((np.arange(1, N + 1) * x)**2)
    def halfelli(self, x):
        l = len(x) // 2
        felli = self.elli(x[:l])
        return felli + 1e-8 * sum(x[l:]**2)
    def elli(self, x, rot=0, xoffset=0, cond=1e6, actuator_noise=0.0, both=False):
        """Ellipsoid test objective function"""
        if not isscalar(x[0]):  
            return [self.elli(xi, rot) for xi in x]  
        if rot:
            x = rotate(x)
        N = len(x)
        if actuator_noise:
            x = x + actuator_noise * np.random.randn(N)

        ftrue = sum(cond**(np.arange(N) / (N - 1.)) * (x + xoffset)**2)

        alpha = 0.49 + 1. / N
        beta = 1
        felli = np.random.rand(1)[0]**beta * ftrue * \
                max(1, (10.**9 / (ftrue + 1e-99))**(alpha * np.random.rand(1)[0]))
        
        
        if both:
            return (felli, ftrue)
        else:
            
            return ftrue  
    def grad_elli(self, x, *args):
        cond = 1e6
        N = len(x)
        return 2 * cond**(np.arange(N) / (N - 1.)) * array(x, copy=False)
    def fun_as_arg(self, x, *args):
        """``fun_as_arg(x, fun, *more_args)`` calls ``fun(x, *more_args)``.

        Use case::

            fmin(cma.fun_as_arg, args=(fun,), gradf=grad_numerical)

        calls fun_as_args(x, args) and grad_numerical(x, fun, args=args)

        """
        fun = args[0]
        more_args = args[1:] if len(args) > 1 else ()
        return fun(x, *more_args)
    def grad_numerical(self, x, func, epsilon=None):
        """symmetric gradient"""
        eps = 1e-8 * (1 + abs(x)) if epsilon is None else epsilon
        grad = np.zeros(len(x))
        ei = np.zeros(len(x))  
        for i in rglen(x):
            ei[i] = eps[i]
            grad[i] = (func(x + ei) - func(x - ei)) / (2*eps[i])
            ei[i] = 0
        return grad
    def elliconstraint(self, x, cfac=1e8, tough=True, cond=1e6):
        """ellipsoid test objective function with "constraints" """
        N = len(x)
        f = sum(cond**(np.arange(N)[-1::-1] / (N - 1)) * x**2)
        cvals = (x[0] + 1,
                 x[0] + 1 + 100 * x[1],
                 x[0] + 1 - 100 * x[1])
        if tough:
            f += cfac * sum(max(0, c) for c in cvals)
        else:
            f += cfac * sum(max(0, c + 1e-3)**2 for c in cvals)
        return f
    def rosen(self, x, alpha=1e2):
        """Rosenbrock test objective function"""
        x = [x] if isscalar(x[0]) else x  
        f = [sum(alpha * (x[:-1]**2 - x[1:])**2 + (1. - x[:-1])**2) for x in x]
        return f if len(f) > 1 else f[0]  
    def grad_rosen(self, x, *args):
        N = len(x)
        grad = np.zeros(N)
        grad[0] = 2 * (x[0] - 1) + 200 * (x[1] - x[0]**2) * -2 * x[0]
        i = np.arange(1, N - 1)
        grad[i] = 2 * (x[i] - 1) - 400 * (x[i+1] - x[i]**2) * x[i] + 200 * (x[i] - x[i-1]**2)
        grad[N-1] = 200 * (x[N-1] - x[N-2]**2)
        return grad
    def diffpow(self, x, rot=0):
        """Diffpow test objective function"""
        N = len(x)
        if rot:
            x = rotate(x)
        return sum(np.abs(x)**(2. + 4.*np.arange(N) / (N - 1.)))**0.5
    def rosenelli(self, x):
        N = len(x)
        return self.rosen(x[:N / 2]) + self.elli(x[N / 2:], cond=1)
    def ridge(self, x, expo=2):
        x = [x] if isscalar(x[0]) else x  
        f = [x[0] + 100 * np.sum(x[1:]**2)**(expo / 2.) for x in x]
        return f if len(f) > 1 else f[0]  
    def ridgecircle(self, x, expo=0.5):
        """happy cat by HG Beyer"""
        a = len(x)
        s = sum(x**2)
        return ((s - a)**2)**(expo / 2) + s / a + sum(x) / a
    def happycat(self, x, alpha=1. / 8):
        s = sum(x**2)
        return ((s - len(x))**2)**alpha + (s / 2 + sum(x)) / len(x) + 0.5
    def flat(self, x):
        return 1
        return 1 if np.random.rand(1) < 0.9 else 1.1
        return np.random.randint(1, 30)
    def branin(self, x):
        
        y = x[1]
        x = x[0] + 5
        return (y - 5.1 * x**2 / 4 / np.pi**2 + 5 * x / np.pi - 6)**2 + 10 * (1 - 1 / 8 / np.pi) * np.cos(x) + 10 - 0.397887357729738160000
    def goldsteinprice(self, x):
        x1 = x[0]
        x2 = x[1]
        return (1 + (x1 + x2 + 1)**2 * (19 - 14 * x1 + 3 * x1**2 - 14 * x2 + 6 * x1 * x2 + 3 * x2**2)) * (
                30 + (2 * x1 - 3 * x2)**2 * (18 - 32 * x1 + 12 * x1**2 + 48 * x2 - 36 * x1 * x2 + 27 * x2**2)) - 3
    def griewank(self, x):
        
        x = (600. / 5) * x
        return 1 - np.prod(np.cos(x / sqrt(1. + np.arange(len(x))))) + sum(x**2) / 4e3
    def rastrigin(self, x):
        """Rastrigin test objective function"""
        if not isscalar(x[0]):
            N = len(x[0])
            return [10 * N + sum(xi**2 - 10 * np.cos(2 * np.pi * xi)) for xi in x]
            
        N = len(x)
        return 10 * N + sum(x**2 - 10 * np.cos(2 * np.pi * x))
    def schaffer(self, x):
        """ Schaffer function x0 in [-100..100]"""
        N = len(x)
        s = x[0:N - 1]**2 + x[1:N]**2
        return sum(s**0.25 * (np.sin(50 * s**0.1)**2 + 1))

    def schwefelelli(self, x):
        s = 0
        f = 0
        for i in rglen(x):
            s += x[i]
            f += s**2
        return f
    def schwefelmult(self, x, pen_fac=1e4):
        """multimodal Schwefel function with domain -500..500"""
        y = [x] if isscalar(x[0]) else x
        N = len(y[0])
        f = array([418.9829 * N - 1.27275661e-5 * N - sum(x * np.sin(np.abs(x)**0.5))
                + pen_fac * sum((abs(x) > 500) * (abs(x) - 500)**2) for x in y])
        return f if len(f) > 1 else f[0]
    def optprob(self, x):
        n = np.arange(len(x)) + 1
        f = n * x * (1 - x)**(n - 1)
        return sum(1 - f)
    def lincon(self, x, theta=0.01):
        """ridge like linear function with one linear constraint"""
        if x[0] < 0:
            return np.NaN
        return theta * x[1] + x[0]
    def rosen_nesterov(self, x, rho=100):
        """needs exponential number of steps in a non-increasing f-sequence.

        x_0 = (-1,1,...,1)
        See Jarre (2011) "On Nesterov's Smooth Chebyshev-Rosenbrock Function"

        """
        f = 0.25 * (x[0] - 1)**2
        f += rho * sum((x[1:] - 2 * x[:-1]**2 + 1)**2)
        return f
    def powel_singular(self, x):
        
        res = np.sum((x[i - 1] + 10 * x[i])**2 + 5 * (x[i + 1] - x[i + 2])**2 +
                     (x[i] - 2 * x[i + 1])**4 + 10 * (x[i - 1] - x[i + 2])**4
                     for i in range(1, len(x) - 2))
        return 1 + res
    def styblinski_tang(self, x):
        """in [-5, 5]
        """
        
        
        return (39.1661657037714171054273576010019 * len(x))**1 + \
               sum(x**4 - 16*x**2 + 5*x) / 2

    def trid(self, x):
        return sum((x-1)**2) - sum(x[:-1] * x[1:])

    def bukin(self, x):
        """Bukin function from Wikipedia, generalized simplistically from 2-D.

        http://en.wikipedia.org/wiki/Test_functions_for_optimization"""
        s = 0
        for k in range((1+len(x)) // 2):
            z = x[2 * k]
            y = x[min((2*k + 1, len(x)-1))]
            s += 100 * np.abs(y - 0.01 * z**2)**0.5 + 0.01 * np.abs(z + 10)
        return s

fcts = FitnessFunctions()
Fcts = fcts  
FF = fcts

def felli(x):
    """unbound test function, needed to test multiprocessor"""
    return sum(1e6**(np.arange(len(x)) / (len(x) - 1)) * (np.array(x, copy=False))**2)




def _test(module=None):  
    import doctest
    print(doctest.testmod(module))  
def process_doctest_output(stream=None):
    """ """
    import fileinput
    s1 = ""
    s2 = ""
    s3 = ""
    state = 0
    for line in fileinput.input(stream):  
        if 1 < 3:
            s3 += line
            if state < -1 and line.startswith('***'):
                print(s3)
            if line.startswith('***'):
                s3 = ""

        if state == -1:  
            s1 += '\n\n*** Failed Example:' + line
            s2 += '\n\n\n'  
            

        if line.startswith('Expected:'):
            state = 1
            continue
        elif line.startswith('Got:'):
            state = 2
            continue
        elif line.startswith('***'):  
            state = 0
        elif line.startswith('Failed example:'):
            state = -1
        elif line.startswith('Exception raised'):
            state = -2

        
        if state == 1:
            s1 += line + ''
        if state == 2:
            s2 += line + ''




def main(argv=None):
    """to install and/or test from the command line use::

        python cma.py [options | func dim sig0 [optkey optval][optkey optval]...]

    with options being

    ``--test`` (or ``-t``) to run the doctest, ``--test -v`` to get (much) verbosity.

    ``install`` to install cma.py (uses setup from distutils.core).

    ``--doc`` for more infos.

    Or start Python or (even better) ``ipython`` and::

        import cma
        cma.main('--test')
        help(cma)
        help(cma.fmin)
        res = fmin(cma.fcts.rosen, 10 * [0], 1)
        cma.plot()

    Examples
    ========
    Testing with the local python distribution from a command line
    in a folder where ``cma.py`` can be found::

        python cma.py --test

    And a single run on the Rosenbrock function::

        python cma.py rosen 10 1  
        python cma.py plot

    In the python shell::

        import cma
        cma.main('--test')

    """
    if argv is None:
        argv = sys.argv  
    else:
        if isinstance(argv, list):
            argv = ['python'] + argv  
        else:
            argv = ['python'] + [argv]

    
    
    
    if len(argv) >= 1:  
        if len(argv) == 1 or argv[1].startswith('-h') or argv[1].startswith('--help'):
            print(main.__doc__)
            fun = None
        elif argv[1].startswith('-t') or argv[1].startswith('--test'):
            import doctest
            if len(argv) > 2 and (argv[2].startswith('--v') or argv[2].startswith('-v')):  
                print('doctest for cma.py: due to different platforms and python versions')
                print('and in some cases due to a missing unique random seed')
                print('many examples will "fail". This is OK, if they give a similar')
                print('to the expected result and if no exception occurs. ')
                
                doctest.testmod(sys.modules[__name__], report=True)  
            else:  
                print('doctest for cma.py: launching...') 
                fn = '_cma_doctest_.txt'
                stdout = sys.stdout
                try:
                    with open(fn, 'w') as f:
                        sys.stdout = f
                        clock = ElapsedTime()
                        doctest.testmod(sys.modules[__name__], report=True)  
                        t_elapsed = clock()
                finally:
                    sys.stdout = stdout
                process_doctest_output(fn)
                
                try:
                    import os
                    for name in os.listdir('.'):
                        if (name.startswith('bound_method_FitnessFunctions.rosen_of_cma.FitnessFunctions_object_at_')
                            and name.endswith('.pkl')):
                            os.remove(name)
                except:
                    pass
                print('doctest for cma.py: finished (no other output should be seen after launching, more in file _cma_doctest_.txt)')
                print('  elapsed time [s]:', t_elapsed)
            return
        elif argv[1] == '--doc':
            print(__doc__)
            print(CMAEvolutionStrategy.__doc__)
            print(fmin.__doc__)
            fun = None
        elif argv[1] == '--fcts':
            print('List of valid function names:')
            print([d for d in dir(fcts) if not d.startswith('_')])
            fun = None
        elif argv[1] in ('install', '--install'):
            from distutils.core import setup
            setup(name="cma",
                  long_description=__doc__,
                  version=__version__.split()[0],
                  description="CMA-ES, Covariance Matrix Adaptation Evolution Strategy for non-linear numerical optimization in Python",
                  author="Nikolaus Hansen",
                  author_email="hansen at lri.fr",
                  maintainer="Nikolaus Hansen",
                  maintainer_email="hansen at lri.fr",
                  url="https://www.lri.fr/~hansen/cmaes_inmatlab.html",
                  license="BSD",
                  classifiers = [
                    "Intended Audience :: Science/Research",
                    "Intended Audience :: Education",
                    "Intended Audience :: Other Audience",
                    "Topic :: Scientific/Engineering",
                    "Topic :: Scientific/Engineering :: Mathematics",
                    "Topic :: Scientific/Engineering :: Artificial Intelligence",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python :: 2.6",
                    "Programming Language :: Python :: 2.7",
                    "Programming Language :: Python :: 3",
                    "Development Status :: 4 - Beta",
                    "Environment :: Console",
                    "License :: OSI Approved :: BSD License",
                    "License :: OSI Approved :: MIT License",
                  ],
                  keywords=["optimization", "CMA-ES", "cmaes"],
                  py_modules=["cma"],
                  requires=["numpy"],
            )
            fun = None
        elif argv[1] in ('plot',):
            plot(name=argv[2] if len(argv) > 2 else None)
            input('press return')
            fun = None
        elif len(argv) > 3:
            fun = eval('fcts.' + argv[1])
        else:
            print('try -h option')
            fun = None

    if fun is not None:

        if len(argv) > 2:  
            x0 = np.ones(eval(argv[2]))
        if len(argv) > 3:  
            sig0 = eval(argv[3])

        opts = {}
        for i in range(5, len(argv), 2):
            opts[argv[i - 1]] = eval(argv[i])

        
        if fun is not None:
            tic = time.time()
            fmin(fun, x0, sig0, opts)  
            
            
            print('elapsed time [s]: + %.2f', round(time.time() - tic, 2))

    elif not len(argv):
        fmin(fcts.elli, np.ones(6) * 0.1, 0.1, {'ftarget':1e-9})







if __name__ == "__main__":
    
    "cma.py", "rastrigin", "10", "5", "popsize", "200", "maxfevals", "24999", "verb_log", "0"])
    main()