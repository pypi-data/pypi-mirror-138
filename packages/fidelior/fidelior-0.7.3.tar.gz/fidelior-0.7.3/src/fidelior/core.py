#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIDELIOR (new interface)
------------------------

A shortened and simplified version of the core FIDELIOR package (for versions >= 0.7).

This file replaces `common.py`, `symbolic_arrays.py`, `extended_arrays.py`,
`fields.py`, `extended_array_operations.py` from version 0.6.

NOTE: some of the interfaces have changed compared to versions <=0.6!
(some interfaces were inspired by FEniCS package).

The most notable changes are listed below. See the examples in the `examples` directory.

Changes regarding extended arrays (`ExtendedArray` in old, `ExtArray` in new FIDELIOR):
    
- `ExtArray` creation interface -- recommend to use `Box` factory:
    Old:
        >>> # Unallocated array
        >>> a = ExtendedArray((5,5), stags=(1,0), nls=(1,1), nus=(2,2))
        >>> a.arr = np.random.rand(*a.nts) # allocation
        >>> # No pre-allocated array interface
        >>> b = a.copy() # ExtendedArray of the same structure
        >>> b.arr = np.zeros(b.nts)
        >>> b = a.view[half:end-half, 0:end] # a smaller ExtendedArray with same elements
    New:
        >>> # Unallocated array
        >>> box = Box((5,5))
        >>> a = box[-half:end+1+half, -1:end+2]
        >>> # - same as
        >>> # a = ExtArray(box, (slice(-half, end+1+half, None), slice(-1, end+2, None)))
        >>> a._arr = np.random.rand(*a.nt) # allocation
        >>> # Allocated array of the same structure
        >>> b = a.as_zeros() # shortcut for box.zeros()[a.spans], fills with zeros by default
        >>> b = a.restrict[half:end-half, 0:end] # was: view
        
- `ExtArray` indexing: colon now denotes what `span` used to be:
    Old:
        >>> a[span] # all of the values
        >>> a[:]    # same as a[0:end] or a[half:end-half], i.e. values inside the box (no ghost cells)
    New:
        >>> a[:]     # all of the values
        >>> a[0:end] # or a[half:end-half] # values inside the box (no ghost cells)
    `Ellipsis` still may be used:
        >>> a[...] # same as a._arr[...]
        
- Assigning values from another `ExtArray`:
    Old:
        >>> a.setv = b
    New:
        >>> a.assign(b) # Does not copy! if b is changes, so is a!)
        >>> a.assign(b, copy=True) # safer
        
- Shift operator:
    Old:
        >>> ea.shifted((half, 1))
        >>> ea.shifted((0, half, 0))
    New:
        >>> ea.at((half, 1))
        >>> ea.shift(half, axis=1)

Changes in symbolic computations and equation solving:

- There is no more `Field` class, use symbolic and numeric `ExtArray` separately:
    Old:
        >>> field = Field('field', (5,5), stags=(1,0), nls=(1,1), nus=(2,2))
    New:
        >>> box = Box((5,5))
        >>> field = box.zeros()[-half:end+1+half, -1:end+2]
        >>> field_sym = field.as_sym('field') # or box.sym('field')[field.spans]
        
- Constraint recording interface:
    Old:
        >>> field.bc.record('name') # optional
        >>> field.bc[0] = 1
    New:
        >>> (field_sym[0] == 1).constraint('name') # must have a name
        >>> # Constraints may be more complicated than in the old FIDELIOR:
        >>> (BCOperator(field_sym) == BCOperator2(field_sym) + rhs).constraint('complicated')
        
- Solving matrix equations:
    Old:
        >>> solver = Solver(field, Oper(field.symb))
        >>> solver.solve_full(field, rhs)
    New:
        >>> # This works when LHS and RHS are either regular arrays or ExtArrays
        >>> field = (Oper(field_sym) == rhs).solve()
        
- Enforcing recorded boundary conditions on a numerical field:
    Old:
        >>> field.bc.apply()
    New:
        >>> # Not so trivial. BC are enforced on a numeric array, while were recorded on symbolic.
        >>> # Need also to specify which variables are dependent/independent
        >>> dep = field.as_zeros('bool') # all elements are independent by default
        >>> dep[end] = True # dependent variables
        >>> field_bc = ConstraintEnforcer(field_sym, dep)
        >>> field_bc.apply(field) # solves the constraint equations from field_sym
        >>> # Maybe it is easier to just apply them manually.

- Changing RHS in equations:
    Old:
        >>> # see 'solver' from above
        >>> solver.solve_full(field, rhs1) # just substitute new rhs1
    New:
        >>> equation = Equation(Oper(field_sym) == rhs)
        >>> field = equation.solve() # solution with rhs
        >>> equation.update_rhs(None, rhs1) # 'None' for a name means the main equation
        >>> field2 = equation.solve() # with rhs1
        
- Changing RHS in boundary conditions:
    Old:
        >>> field.bc.record('bc_name',is_variable=True)
        >>> field.bc[index] = rhs
        >>> # ... solve it ...
        >>> field.bc.update('bc_name')
        >>> field.bc[index] = rhs1
        >>> # ... solve it again ..., 'solver' does not need to change
    New:
        >>> # Can have an arbitrary operator
        >>> (BCOper(field_sym) == rhs).constraint('bc_name')
        >>> equation = Equation(...) # as above
        >>> field = equation.solve() # initial BC
        >>> equation.update_rhs('bc_name', rhs1)
        >>> field1 = equation.solve() # with updated BC
        
Simplifications that lead to some minor inconveniences, but fixing them is too much \
work which is not worth the usefulness:
     
- Slices with negative steps were removed; steps >1 are retained

FIDELIOR (c) by Nikolai G. Lehtinen

FIDELIOR is licensed under a
Creative Commons Attribution-NoDerivatives 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-nd/4.0/>.

"""

#%% Import the needed packages
import sys
import builtins
import functools
import numpy
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg

if not hasattr(numpy.ndarray, '__array_ufunc__'):
    print('Your NumPy is too old')

import warnings
# Suppress complaints -- I don't know why it is so moody
warnings.simplefilter('ignore', scipy.sparse.SparseEfficiencyWarning)

#%% Global management
def make_indented_printable(cls, multiline=True, replace_repr=True):
    "A general-purpose output utility"
    def indented_repr(obj, level=1):
        tabs = '\n' + ('\t' * level) if multiline else ' '
        if not hasattr(obj,'_indented_repr'):
            s=repr(obj).split('\n')
            # if one line, just s
            # if many, <CR>+tabulated output
            return s[0] if len(s)==1 else tabs + tabs.join(s)
        outputs = []
        for key in sorted(obj.__dict__):
            child = obj.__dict__[key]
            s = '<%s>' % (child.__class__.__name__,) if key[0]=='_' else \
                child._indented_repr(level=level+1) if hasattr(child, '_indented_repr') else \
                    indented_repr(child, level+1)
            outputs.append('%s = %s' % (key, s))
        s = (','+tabs).join(outputs)
        breaks = tabs if '\n' in s else ''
        return ('%s(' + breaks + '%s)') % (obj.__class__.__name__, s)
    setattr(cls,'_indented_repr', indented_repr)
    if replace_repr:
        setattr(cls,'__repr__', indented_repr)

def set_sparse(use_sparse):
    "Common names for functions which may be used both with dense and sparse matrices"
    global USE_SPARSE, _eye, _diag, _vstack, _solve, _to_solvable, _to_dense, _zeros
    USE_SPARSE = use_sparse
    if use_sparse:
        def _eye(n):
            return scipy.sparse.eye(n).tocsc()
        def _diag(diagonal):
            return scipy.sparse.diags(diagonal, dtype=diagonal.dtype)
        _vstack = scipy.sparse.vstack
        _solve = scipy.sparse.linalg.spsolve
        def _to_solvable(m): return m.tocsc()
        def _to_dense(m): return m.todense()
        #_zeros = scipy.sparse.lil_matrix # slow to allocate, fast in handling, no warning
        #_zeros = scipy.sparse.dok_matrix # fast to allocate, slow in handling, no warning
        _zeros = scipy.sparse.csc_matrix # fast, but gives a warning
    else:
        def _eye(n):
            return numpy.eye(n)
        _diag = numpy.diag
        _vstack = numpy.vstack
        _solve = scipy.linalg.solve
        def _to_solvable(m): return m
        def _to_dense(m): return m
        _zeros = numpy.zeros
    pass

set_sparse(True)

#%% Operator, Equality and Equation
class Equality:
    "Really, an equation -- but not solving it yet"
    def __init__(self, oper):
        self.oper = oper
    def __and__(self, equality):
        return Equality(self.oper.cat(equality.oper))
    def constraint(self, name):
        self.oper.ref._bc[name] = self.oper
    def solve(self, out=None):
        "Compatibility function"
        return Equation(self).solve(out)

def empty_equality(unknown):
    "Argument: a FieldOperator, symbolic ExtArray or an iterable of these, or EACollection"
    return Equality(FieldOperator(_get_ref(unknown))) # with empty operator

class Equation:
    "Solver of equalities, updater of RHS"
    def __init__(self, equality):
        equality = _unextend(equality) # in case the argument is (ExtArray == something)
        oper = equality.oper
        self.ref = oper.ref
        # Finalize the system
        system = Operator(None, None, self.ref)
        start = 0
        finish = oper.num_eqs
        addr = {None: slice(start, finish)}
        system.cat(oper, in_place=True)
        for name, oper in self.ref._bc.items():
            start = finish
            finish = start + oper.num_eqs
            addr[name] = slice(start, finish)
            system.cat(oper, in_place=True)
        system.M = _to_solvable(system.M)
        # Check for consistency
        if not system.solvable:
            n, m = system.num_vars, system.num_eqs
            msg = 'There are {:d} unknowns, but {:d} equations. '.format(n, m)
            if n > m:
                msg += 'Insufficient constraints, need {:d} more.'.format(n-m)
            else:
                msg += 'Excessive constraints, remove {:d} of them.'.format(m-n)
            raise ValueError(msg)
        self.system = system
        self.addr = addr
    def update_rhs(self, name, arr):
        self.system.V[self.addr[name]] = -_unextend(arr).flatten()
    def solve(self, out=None):
        # Problem with reshaping
        if not self.system.complete:
            raise ValueError('The system has NaNs (not assigned RHS values)')
        res = self.system.solve_system().reshape(self.ref.shape)
        if hasattr(self.ref, 'spans'):
            # An ExtArray equation
            assert hasattr(self.ref, 'box')
            if out is None:
                return ExtArray(self.ref.box, self.ref.spans, res)
            else:
                out._arr = res
                return None
        else:
            # An ndarray equation
            if out is not None:
                out[...] = res
                return None
            else:
                return res

def solve(equation, out=None):
    "Polymorphism without inheritance -- if it solves like a duck ..."
    return equation.solve(out)

class Operator:
    """Operator M*x + V
    M is a 2D np.ndarray (dense) or a sparse matrix (sparse); V is a 1D np.array."""
    def __init__(self, M, V, ref):
        self.M = M
        self.V = V
        self.ref = ref
    @property
    def num_vars(self):
        return self.M.shape[1]
    @property
    def num_eqs(self):
        return 0 if self.M is None else self.M.shape[0]
    @property
    def valid(self):
        return len(self.M.shape)==2 and len(self.V.shape)==1 and self.num_eqs == self.V.shape[0]
    @property
    def complete(self):
        return not numpy.isnan(self.V).any()
    @property
    def solvable(self):
        return self.valid and self.num_vars == self.num_eqs
    def apply(self, x):
        return self.M.dot(x) + self.V
    def __call__(self,x):
        return self.apply(x)
    def solve_system(self):
        return _solve(self.M, -self.V)
    def __getitem__(self, i):
        if isinstance(i, tuple) and len(i)==1:
            i = i[0]
        i = numpy.repeat(numpy.arange(self.num_eqs)[i], 1, axis=0) # so that M does not become a 1d
        return Operator(self.M[i, :], self.V[i], self.ref)
    def __setitem__(self, i, op):
        if isinstance(op, Operator):
            assert self.ref is op.ref
            M, V = op.M, op.V
        else:
            # Just regular number or vector
            M, V = 0, op
        self.M[i,:] = M
        self.V[i] = V
    def __eq__(self, op):
        return Equality(self - op)
    def copy(self):
        return Operator(self.M.copy(),self.V.copy(), self.ref)
    def __pos__(self):
        return self
    def __neg__(self):
        return Operator(-self.M, -self.V, self.ref)
    def __add__(self, op):
        if isinstance(op, Operator):
            assert self.ref is op.ref
            M, V = op.M, op.V
        else:
            #assume it is something that should be just added to the result of op application
            M, V = 0, numpy.asarray(op).flatten()
        return Operator(self.M + M, self.V + V, self.ref)
    def __radd__(self, v):
        return self + v
    def __sub__(self, op):
        return self + (-op)
    def __rsub__(self, op):
        return (-self) + op
    def __mul__(self, v):
        "Multiply by number"
        if numpy.isscalar(v):
            return Operator(self.M*v,self.V*v, self.ref)
        if not isinstance(v, numpy.ndarray):
            raise TypeError('Can multipy Operator only by scalar or NDArray')
        v = v.flatten()
        return Operator(_diag(v).dot(self.M), v*self.V, self.ref)
    def __rmul__(self, v):
        return self*v
    def __truediv__(self, v):
        return self*(1/v)
    def __rtruediv__(self, v):
        raise TypeError('Cannot divide by Operator (or apply any nonlinear operation)')
    def cat(self, op, in_place=False):
        assert op.ref is self.ref
        Mx = op.M if self.M is None else _vstack((self.M, op.M))
        Vx = op.V if self.V is None else numpy.hstack((self.V, op.V))
        if in_place:
            self.M = Mx
            self.V = Vx
            return None
        else:
            return Operator(Mx, Vx, self.ref)
    # In-place operations
    # -------------------
    def __iadd__(self, op):
        tmp = self + op
        self.M = tmp.M
        self.V = tmp.V
        return self
    def __isub__(self, op):
        self += (-op)
        return self
    def __imul__(self, v):
        tmp = self*v
        self.M = tmp.M
        self.V = tmp.V
        return self
    def __itruediv__(self, v):
        self *= (1/v)
        return self
    # NumPy operations
    # ----------------
    # By default, NumPy uses ndarray operators for each element of an uknown-type operand
    # instead of allowing that operand to use its own reverse function on ndarray.
    # This is fixed like this: https://docs.scipy.org/doc/numpy-1.14.0/neps/ufunc-overrides.html
    #__array_ufunc__ = None
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        arg = inputs[0]
        if len(inputs)==2:
            if not (len(kwargs)==0 and self is inputs[1]):
                print(ufunc, ufunc.__class__, len(inputs), kwargs)
                raise TypeError('Nonlinear functions are not supported by Operator')
            if ufunc is numpy.multiply:
                return self.__rmul__(arg)
            elif ufunc is numpy.add:
                return self.__radd__(arg)
            elif ufunc is numpy.subtract:
                return self.__rsub(arg)
            elif ufunc is numpy.true_divide:
                return self.__rtruediv__(arg)
        else:
            print(ufunc, ufunc.__class__, len(inputs), kwargs)
            raise TypeError('Nonlinear functions are not supported by Operator')

def _cat_operators(ref, operators):
    res = Operator(None, None, ref)
    for oper in operators:
        res.cat(oper, in_place=True)
    res.M = _to_solvable(res.M)
    return res

class FieldRef:
    "All the common things for the same-variable operators"
    def __init__(self, name, shape):
        self.name = name
        self.shape = shape
        self._bc = {}

class FieldOperator(Operator):
    "An interface to Operator allowing multi-axis arrays and constraints"
    def __init__(self, ref, init=False):
        Operator.__init__(self, None, None, ref)
        if init:
            n = numpy.prod(ref.shape)
            self.fill( _eye(n), numpy.zeros((n,)), ref.shape)
        # if not init, still need M, V, shape
    def fill(self, M, V, shape):
        self.M = M
        self.V = V
        self.shape = shape
        self._index = numpy.arange(numpy.prod(shape)).reshape(shape)
        return self
    def __getitem__(self, i):
        ind = self._index[i]
        op = Operator.__getitem__(self, ind.flatten())
        return FieldOperator(self.ref).fill(op.M, op.V, ind.shape)
    def __setitem__(self, i, op):
        Operator.__setitem__(self, self._index[i].flatten(), op)
    def allocate(self, shape):
        "Create an empty symbolic array of length n with the same reference"
        n = numpy.prod(shape)
        # Create a "virtual" operator -- virtuality indicated by NaNs
        M = _zeros((n, self.num_vars))
        V = numpy.full((n,), fill_value=numpy.nan)
        return FieldOperator(self.ref).fill(M, V, shape)
    def apply(self, x):
        return Operator.apply(self, x.flatten()).reshape(self.shape)
    # "Upgraded" functions
    def upgrade(self, op):
        "Upgrade a simple operator (of same shape) to FieldOperator"
        return FieldOperator(self.ref).fill(op.M, op.V, self.shape)
    def copy(self):
        return self.upgrade(Operator.copy(self))
    def __neg__(self):
        return self.upgrade(Operator.__neg__(self))
    def __add__(self, op):
        return self.upgrade(Operator.__add__(self, op))
    def __radd__(self, v):
        return self.upgrade(Operator.__radd__(self, v))
    def __sub__(self, op):
        return self.upgrade(Operator.__sub__(self, op))
    def __rsub__(self, op):
        return self.upgrade(Operator.__rsub__(self, op))
    def __mul__(self, v):
        return self.upgrade(Operator.__mul__(self, v))
    def __rmul__(self, v):
        return self.upgrade(Operator.__rmul__(self, v))
    def __truediv__(self, v):
        return self.upgrade(Operator.__truediv__(self, v))
    def reshape(self, shape):
        assert numpy.prod(self.shape)==numpy.prod(shape)
        self.shape = shape
        self._index = numpy.arange(numpy.prod(shape)).reshape(shape)
        return self
    # By default, NumPy uses ndarray operators for each element of an uknown-type operand
    # instead of allowing that operand to use its own reverse function on ndarray.
    # This is fixed like this: https://docs.scipy.org/doc/numpy-1.14.0/neps/ufunc-overrides.html
    #__array_ufunc__ = None

make_indented_printable(Equality)
make_indented_printable(Equation)
make_indented_printable(FieldRef, multiline=False)
make_indented_printable(Operator)

def ndarray_sym(name, shape):
    "A convenient interface to creation of a FieldOperator"
    return FieldOperator(FieldRef(name, shape), init=True)

def _unextend(f):
    "Take the 'meat' of an ExtArray only"
    return f._arr if isinstance(f, ExtArray) else f

def _get_ref(unknown):
    "Argument: a FieldOperator, symbolic ExtArray or an iterable of these, or EACollection"
    if not isinstance(unknown, EACollection):
        if isinstance(unknown, _Iterable):
            unknown = unknown[0] # pick any variable from the collection, ref should be the same
        unknown = _unextend(unknown)
        if not isinstance(unknown, FieldOperator):
            raise TypeError('The argument must be a symbolic, non numeric, array')
    # unknown may also be anything that has a ref
    return unknown.ref

#%% Constraint management
class ConstraintEnforcer:
    "Not sure if we need it at all"
    def __init__(self, f, dep=False):
        f = _unextend(f)
        dep = _unextend(dep)
        self.ref = f.ref
        if isinstance(dep, bool):
            self.dep = numpy.full(self.ref.shape, fill_value=dep, dtype=bool)
        else:
            assert dep.shape==self.ref.shape and dep.dtype=='bool'
            self.dep = dep
            self.freeze()
    def freeze(self):
        "Call it after changing self.dep"
        assert self.dep.shape==self.ref.shape
        bc = _cat_operators(self.ref, self.ref._bc.values())
        Cd = _to_solvable(-bc.M[:, self.dep.flatten()])
        M = _solve(Cd, _to_solvable(bc.M[:, (~self.dep).flatten()]))
        V = _solve(Cd, bc.V)
        self.op = Operator(M, V, None)
        self._Cd = Cd
    def update(self):
        # Only V has changed, can optimize
        bcV = numpy.hstack(tuple(op.V for op in self.ref._bc.values()))
        self.op.V =  _solve(self._Cd, bcV)
        return self
    def enforce(self, f):
        f = _unextend(f)
        f[self.dep] = self.op(f[~self.dep])

def constraint_info(unknown):
    "Quick information about constraints which are already set"
    bcs = _get_ref(unknown)._bc # a dictionary of Operators
    if len(bcs)==0:
        return None
    num_vars = None
    info = {}
    num_eqs = 0
    for name, bc in bcs.items():
        if num_vars is None:
            num_vars = bc.num_vars
        else:
            assert num_vars == bc.num_vars
        info[name] = bc.num_eqs
        num_eqs += bc.num_eqs
    info[None] = num_vars - num_eqs
    return info

def good_constraints(f):
    """Check for conficting or repeating constraints.
    Caveat: there still can be a conflict with the main equation."""
    fref = _get_ref(f)
    bc = _cat_operators(fref, fref._bc.values())
    # Calculate the rank of the constraint matrix
    # Maybe there is a better way without creating a dense matrix
    M = bc.M[:, bc.M.getnnz(0)>0] # reduce the number of columns before converting to dense
    return numpy.linalg.matrix_rank(_to_dense(M))==M.shape[0]

make_indented_printable(ConstraintEnforcer)

#%% Indices for extended arrays
from numbers import Integral as _Integral
from collections.abc import Iterable as _Iterable

half_string = '½' # customizeable global
class _HalfIndex:
    """Half-index like `k+1/2`, for the staggered arrays.
    Really, just a decorated integer or _EndIndex"""
    def __init__(self, whole_part=0):
        assert isinstance(whole_part, _Integral)
        self.int = whole_part # The "old" value of index into staggered array
        # The index on the grid is self.int + (1/2)
    def __float__(self):
        return self.int + 0.5
    def __neg__(self):
        return _HalfIndex(-self.int - 1)
    def __pos__(self):
        return self
    def __radd__(self, i):
        return _HalfIndex(i + self.int) # can be anything that supports __add__
    def __rsub__(self, i):
        return (i + (-self))
    def __eq__(self, o):
        return (type(self)==type(o) and (self.int==o.int))
    def __format__(self, spec):
        return self._out(spec[0]=='+')
    def _out(self, sign):
        "Fancy printout of int+½"
        sign_str = ('+' if sign else '')
        i = self.int + 1
        if i < 1:
            return '-' + ('' if i==0 else repr(-i)) + half_string
        else:
            return sign_str + ('' if i==1 else repr(i-1)) + half_string
    def __repr__(self):
        return self._out(False)
    pass

class _EndIndex:
    def __init__(self, i=0):
        self.i = i
    def __add__(self, i):
        "Returns an index"
        return _EndIndex(self.i + i)
    def __sub__(self,i):
        return self + (-i)
    def __eq__(self, o):
        return (type(self)==type(o) and (self.i==o.i))
    def __format__(self, spec):
        return self.__repr__()
    def __repr__(self):
        return 'end' + ('' if self.i==0 else '{:+d}'.format(self.i))

# "Constants"
half = _HalfIndex()
end = _EndIndex()

def _is_ea_index(i):
    return isinstance(i, _HalfIndex) or isinstance(i, _EndIndex) or isinstance(i, _Integral)

#%% Slicing
def _info_span(nc, span):
    "Output a span recorded as a slice"
    assert isinstance(span.stop, _EndIndex)
    return '{:d}:{:d}{:+d}'.format(span.start, nc, span.stop.i)

def _reslice(ea_index, nc, span, a=None):
    """numpy_index = _reslice(ea_index, nc, span, a=None)
    Convert ExtArray index into a NumPy or Python array index.
    The axis is given only for reference (for IndexError output).
    
    Parameters
    ----------
    ea_index : slice or number or 1D array
        Index into ExtArray.
    nc : int
        Number of cells.
    span: slice
        The range of indeces along a given axis
    a : int, optional (for IndexError output)
        The axis. The default is None.
    """
    is_half = isinstance(span.start, half.__class__)
    def de_half(ih):
        return (ih.int if isinstance(ih, half.__class__) else ih)
    nl = -de_half(span.start)
    nu = de_half(span.stop.i) # NOT the ghost cells if is_half !!!
    nt = nc + nl + nu + 1 # total number of points
    msg = ' out of bounds [{:s}]'.format(_info_span(nc, span))
    # The axis number information is only used here, for debugging output
    if a is not None:
        msg += ' on axis {:d}'.format(a)
    def to_i(ie):
        "Want this to be fast"
        assert _is_ea_index(ie)
        #ih = de_end(nc, ie)
        ih = (nc + ie.i) if isinstance(ie, end.__class__) else ie
        assert isinstance(ih, half.__class__)==is_half
        i = de_half(ih) + nl
        if (i<0 or i>=nt):
            raise IndexError(repr(ie) + msg)
        return i
    if isinstance(ea_index, slice):
        if ea_index.step is not None:
            assert isinstance(ea_index.step, _Integral)
            if ea_index.step < 0:
                raise IndexError('Negative step not supported')
        start = None if ea_index.start is None else to_i(ea_index.start)
        stop = None if ea_index.stop is None else to_i(ea_index.stop)+1
        return slice(start, stop, ea_index.step)
    elif _is_ea_index(ea_index):
        # Scalar index
        return to_i(ea_index)
    elif isinstance(ea_index, _Iterable):
        return numpy.array([to_i(ei) for ei in ea_index])
    else:
        raise IndexError('Unknown index type: ' + repr(ea_index))

def _union_or_intersection_span(operation, span1, span2):
    "Common code for 'intersection' and 'union'"
    is_half = isinstance(span1.start, half.__class__)
    assert isinstance(span2.start, half.__class__)==is_half # compatibility
    def de_half(ih):
        return (ih.int if isinstance(ih, half.__class__) else ih)
    nl1 = de_half(span1.start)
    nl2 = de_half(span2.start)
    nl = -operation(-nl1, -nl2)
    nu1 = de_half(span1.stop.i)
    nu2 = de_half(span2.stop.i)
    nu = operation(nu1, nu2)
    h0 = (half if is_half else 0)
    return slice(nl + h0, end + nu + h0, None)

def _union_or_intersection_spans(operation, spans1, spans2):
    return tuple(_union_or_intersection_span(operation, span1, span2)
                 for span1, span2 in zip(spans1, spans2))

def intersection_spans(spans1, spans2):
    "We override 'min' so be careful here"
    return _union_or_intersection_spans(builtins.min, spans1, spans2)

#%% Extended Arrays
class Box:
    "Rudimentary geometry info and ExtArray factory"
    def __init__(self, num_cells):
        self.num_cells = num_cells
        self.ndim = len(num_cells)
        self._reset()
    def _reset(self):
        "Clean up after use"
        self._operation = None
        self._data = None
    def zeros(self, dtype='double'):
        self._operation = 'zeros'
        self._data = {'dtype': dtype}
        return self
    def sym(self, name):
        self._operation = 'sym'
        self._data = {'name': name}
        return self
    def allocate_as(self, ea):
        self._operation = 'allocate_as'
        self._data = {'ea': ea}
        return self
    def ndgrid(self, *xs):
        self._operation = 'ndgrid'
        self._data = {'xs': xs}
        return self
    def __getitem__(self, spans):
        if not isinstance(spans, tuple): spans = (spans,)
        if self._operation is None:
            result = ExtArray(self, spans)
        elif self._operation == 'ndgrid':
            # Note: cannot use 'self' to construct ExtArrays!
            xs = tuple(ExtArray(self, spans) for k in range(self.ndim))
            arrs = numpy.meshgrid(*self._data['xs'], indexing='ij')
            for x, arr in zip(xs, arrs):
                x._arr = arr
            result = xs
        elif self._operation == 'zeros':
            result = ExtArray(self, spans)
            result._arr = numpy.zeros(result.nt, dtype=self._data['dtype'])
        elif self._operation == 'sym':
            result = ExtArray(self, spans)
            ref = FieldRef(self._data['name'], result.nt)
            # Extra info in ref for ExtArray
            ref.box = self
            ref.spans = spans
            result._arr = FieldOperator(ref, init=True)
        elif self._operation == 'allocate_as':
            ea = self._data['ea']
            result = ExtArray(self, spans)
            if ea.is_sym:
                result._arr = ea._arr.allocate(result.nt)
            else:
                result._arr = numpy.ndarray(result.nt, dtype=ea._arr.dtype)
        self._reset()
        return result

make_indented_printable(Box, multiline=False)

def _shift_ea_index(ei, d):
    assert _is_ea_index(ei)
    if d==0:
        return ei # Don't do anything
    is_half = isinstance(d, half.__class__)
    if isinstance(ei, end.__class__):
        return _EndIndex(_shift_ea_index(ei.i, d))
    elif isinstance(ei, half.__class__):
        if is_half:
            return ei.int + d.int + 1
        else:
            return _HalfIndex(ei.int + d)
    else:
         return ei + d   

def _shift_ea_slice(es, d):
    return es if d==0 else slice(_shift_ea_index(es.start, d), _shift_ea_index(es.stop, d))

class _ExtArrayRestrict:
    "Auxiliary class to call 'restrict' method for ExtArray"
    def __init__(self, ea):
        self.ea = ea
    def __getitem__(self, i):
        return ExtArray(self.ea.box, i, self.ea[i])

class ExtArray:
    def __init__(self, box, spans, array=None):
        assert isinstance(box, Box)
        self.box = box
        self.restrict = _ExtArrayRestrict(self)
        # Analize the spans
        assert len(spans)==box.ndim
        self.spans = spans # has all the information
        self.nt = () # Need for allocation
        self.on = () # Need for something?
        for a, nc, span in zip(range(box.ndim), box.num_cells, spans):
            assert isinstance(span, slice)
            assert span.step is None
            assert isinstance(span.stop, end.__class__)
            is_half = isinstance(span.start, half.__class__)
            assert isinstance(span.stop.i, half.__class__)==is_half
            ne = (-span.start.int + span.stop.i.int) if is_half else (-span.start + span.stop.i)
            self.nt += (ne + nc + 1,)
            self.on += ((not is_half),)
        if array is not None:
            if isinstance(array, numpy.ndarray) or isinstance(array, FieldOperator):
                assert array.shape==self.nt
            self._arr = array
    def _numpy_index(self, index):
        if isinstance(index, ExtArray):
            if not (index.is_num and index._arr.dtype=='bool'):
                raise IndexError('An ExtArray index must be boolean')
            return index[self.spans]
        if index is Ellipsis:
            return Ellipsis
        if not isinstance(index, tuple):
            assert self.box.ndim==1
            index = (index,)
        np_index = tuple(_reslice(i, self.box.num_cells[a], self.spans[a], a)
                         for a, i in enumerate(index))
        return np_index
    def __getitem__(self, i):
        return self._arr[self._numpy_index(i)]
    def __setitem__(self, i, v):
        self._arr[self._numpy_index(i)] = v
    def at(self, delta):
        newspans = tuple(_shift_ea_slice(span, -d) for span, d in zip(self.spans, delta))
        return ExtArray(self.box, newspans, self._arr)
    def shift(self, delta, axis=None):
        "Same as 'at' but only along a single axis"
        ndim = self.box.ndim
        if axis is None:
            if ndim==1:
                axis = 0
            else:
                # Better safe than sorry
                raise ValueError('axis is not given in shift')
        newspans = tuple(_shift_ea_slice(span, -delta) if axis==a
                         else span for a, span in enumerate(self.spans))
        return ExtArray(self.box, newspans, self._arr)
    def as_empty(self):
        return self.box[self.spans]
    def as_zeros(self, dtype=None):
        return self.box.zeros(dtype)[self.spans]
    def as_sym(self, name):
        return self.box.sym(name)[self.spans]
    def copy(self):
        return ExtArray(self.box, self.spans, array=self._arr.copy())
    def __repr__(self):
        spans = '[' + ', '.join(_info_span(self.box.num_cells[a], self.spans[a])
                            for a in range(self.box.ndim)) + ']'
        if not hasattr(self, '_arr'):
            info = ''
        elif self.is_num:
            info = self._arr.dtype.name
        elif self.is_sym:
            info = 'Operator('+self._arr.ref.name+')'
        else:
            info = self._arr.__class__.__name__
        return self.__class__.__name__ + '<' + info + '>' + spans
    @property
    def is_sym(self):
        return isinstance(self._arr, FieldOperator)
    @property
    def is_num(self):
        return isinstance(self._arr, numpy.ndarray)
    def apply(self, ea):
        assert self.is_sym and isinstance(ea, ExtArray)
        res = ExtArray(self.box, self.spans)
        res._arr = self._arr.apply(ea._arr)
        return res
    def __call__(self, ea):
        return self.apply(ea)
    def assign(self, ea):
        "The argument is 'bigger' than the object"
        if isinstance(ea, ExtArray):
            self._arr = ea[self.spans]
        else:
            assert ea.shape == self.nt
            self._arr = ea
        return self
    def update(self, ea):
        "We assume that not all values are set, the argument is 'smaller' than the object"
        assert isinstance(ea, ExtArray)
        spans = intersection_spans(self.spans, ea.spans)
        self[spans] = ea[spans]
        return self
    # By default, NumPy uses ndarray operators for each element of an uknown-type operand
    # instead of allowing that operand to use its own reverse function on ndarray.
    # This is fixed like this: https://docs.scipy.org/doc/numpy-1.14.0/neps/ufunc-overrides.html
    __array_ufunc__ = None

#%% Override NumPy operators and functions: setup

def compatible_ea(ea1, ea2):
    return ea1.box is ea2.box and ea1.on==ea2.on

_info_unary = """

FIDELIOR Note
=============

This is a FIDELIOR-overriden unary function. It may take an ``ExtArray`` as
the first argument, and return an ``ExtArray``."""

_info_binary = """

FIDELIOR Note
=============

This is a FIDELIOR-overriden binary function. It may take ``ExtArray`` s as
the first two arguments, and return an ``ExtArray``."""

_info_default = """

FIDELIOR Note
=============

This is a FIDELIOR-overriden variable-arg function. It may take FIDELIOR objects as
arguments in the same way as NumPy does, and return FIDELIOR objects."""

def extend_unary_func(func, allow_symbolic=False, in_place=False):
    """Make a function taking numpy arrays into a function which can also
    take ExtendedArray. Works for both 1D and 2D arrays.
    In-place functions are assumed to return the first argument or None."""
    def newfunc(ea, *args, **kws):
        if not isinstance(ea, ExtArray):
            return func(ea, *args, **kws) # will return None for in-place
        assert ea.is_num or ea.is_sym
        if ea.is_sym and not allow_symbolic:
            raise TypeError('Cannot apply nonlinear operation '+func.__name__+
                            ' to a symbolic array')
        if not in_place:
            return ExtArray(ea.box, ea.spans, func(ea._arr, *args, **kws))
        else:
            tmp = func(ea._arr, *args, **kws)
            return (None if tmp is None else ea)
    return newfunc

def extend_binary_func(func, allow_symbolic=False, in_place=False):
    """Make a function taking two numpy arrays into a function which can also
    take two ExtendedArray. Works for both 1D and 2D arrays.
    In-place functions are assumed to return the first argument or None"""
    def newfunc(ea1, ea2, *args, **kws):
        # First, consider cases when one of the arguments is NOT an extended_array
        if not (isinstance(ea1, ExtArray) and isinstance(ea2, ExtArray)):
            if isinstance(ea1, ExtArray):
                if not in_place:
                    res = ExtArray(ea1.box, ea1.spans)
                    res._arr = func(ea1._arr, ea2, *args, **kws)
                else:
                    tmp = func(ea1._arr, ea2, *args, **kws)
                    res = (None if tmp is None else ea1)
                return res
            elif isinstance(ea2, ExtArray):
                # Both in_place and not in_place are treated the same
                res = ExtArray(ea2.box, ea2.spans)
                res.arr = func(ea1, ea2.arr, *args, **kws)
                return res
            else: # None of them are extended_array
                return func(ea1, ea2, *args, **kws)
        assert (ea1.is_num or ea1.is_sym) and (ea2.is_num or ea2.is_sym)
        if not compatible_ea(ea1, ea2):
            raise TypeError('in binary operation '+ func.__name__ +' operands must match')
        # Now we know that both are extended arrays
        if not allow_symbolic and (ea1.is_sym or ea2.is_sym):
            raise TypeError('Cannot apply nonlinear operation '+func.__name__+
                            ' to symbolic arrays')
        spans = intersection_spans(ea1.spans, ea2.spans)
        tmp = func(ea1[spans], ea2[spans], *args, **kws)
        if not in_place:
            return ExtArray(ea1.box, spans, tmp)
        else:
            return (None if tmp is None else ea1)
    return newfunc

# See https://numpy.org/devdocs/reference/ufuncs.html
_UFUNC_ATTRIBUTES = ['nin','nout','nargs','ntypes','types','identity','signature',
                    'reduce','accumulate','reduceat','outer','at']

def _update_wrapper(newfunc, func, nin, copy_info):
    if copy_info:
        functools.update_wrapper(newfunc, func)
        if nin==1:
            info = _info_unary
        elif nin==2:
            info = _info_binary
        else:
            info = _info_default
        if newfunc.__doc__ is None:
            newfunc.__doc__ = info
        else:
            newfunc.__doc__ += info
    else:
        newfunc.__name__ = func.__name__
    # Copy ufunc attributes
    if func.__class__ is numpy.ufunc:
        for attr in _UFUNC_ATTRIBUTES:
            setattr(newfunc, attr, getattr(func, attr))
            
def extend_vectorized_function(nin=None, allow_symbolic=False, in_place=False, copy_info=True):
    "Decorator maker"
    def decorator(func):
        if hasattr(func,'nin'):
            the_nin = func.nin
        else: # I am not sure why this is needed
            the_nin = nin
        if the_nin is None:
            raise SyntaxError('For non-ufunc, need number of args (nin)')
        if the_nin == 1:
            extend_func = extend_unary_func
        elif the_nin == 2:
            extend_func = extend_binary_func
        else:
            raise NotImplementedError('Extending functions with nin>2 is not implemented')
        newfunc = extend_func(func, allow_symbolic=allow_symbolic, in_place=in_place)
        _update_wrapper(newfunc, func, the_nin, copy_info)
        return newfunc
    return decorator

def extend_minmax_function(np_minmax):
    def _minmax(f, axis=None, **kws):
        if isinstance(f, ExtArray):
            if len(kws)>0:
                print('FIDELIOR warning: ignoring some keywords')
            return np_minmax(f._arr, axis=axis)
        else:
            return np_minmax(f, axis=axis, **kws)
    _update_wrapper(_minmax, np_minmax, 1, True)
    return _minmax

#%% Override NumPy operators and functions: Monkey-patching galore

_UNARY_OPERATORS = ['neg', 'pos', 'abs', 'invert']

# Note: '__eq__' will need special treatment (see below)
# __divmod__ returns a tuple, so it is skipped for now
_DIRECT_BINARY_OPERATORS = ['add', 'sub', 'mul', 'pow', 'truediv', 'floordiv', 'mod', 
    'and', 'or', 'xor', 'rshift', 'lshift', 'eq', 'ne', 'gt', 'lt', 'ge', 'le']

# The following are dangerous because NumPy has its own implementation for direct op for ndarray
# Alternative would be not to allow operations between ExtArray and ndarray
# This was fixed using this: https://docs.scipy.org/doc/numpy-1.14.0/neps/ufunc-overrides.html
_REVERSE_BINARY_OPERATORS = ['radd', 'rsub', 'rmul', 'rpow', 'rtruediv', 'rfloordiv', 'rmod',
                             'rand', 'ror', 'rxor', 'rrshift', 'rrlshift']

_INPLACE_OPERATORS = ['iadd', 'isub', 'imul', 'itruediv', 'ipow', 'iand', 'ior']

# See https://numpy.org/devdocs/reference/ufuncs.html for complete list of ufunc functions
_NUMPY_FUNCS = ['sign', 'sqrt', 'exp', 'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'log', 'log10',
               'arcsin', 'arccos', 'arctan', 'arctan2', 'arcsinh', 'arccosh', 'arctanh',
               'minimum', 'maximum', 'abs']
_NUMPY_MMFUNCS = ['min', 'max', 'nanmin', 'nanmax', 'mean']

def _make_unary_func(op):
    def _tmp(t1):
        return getattr(t1,op)()
    _tmp.__name__ = op
    return extend_unary_func(_tmp, allow_symbolic=True, in_place=False)

def _make_binary_func(op):
    def _tmp(t1,t2):
        return getattr(t1,op)(t2)
    _tmp.__name__ = op
    return extend_binary_func(_tmp, allow_symbolic=True, in_place=False)

def _make_inplace_func(op):
    def _tmp(t1,t2):
        return getattr(t1,op)(t2)
    _tmp.__name__ = op
    return extend_binary_func(_tmp, allow_symbolic=True, in_place=True)

def _monkey_patch():
    for uop in _UNARY_OPERATORS:
        uopd = '__' + uop + '__'
        setattr(ExtArray, uopd, _make_unary_func(uopd))
    
    for bop in _DIRECT_BINARY_OPERATORS + _REVERSE_BINARY_OPERATORS:
        bopd = '__' + bop + '__'
        setattr(ExtArray, bopd, _make_binary_func(bopd))

    # Re-patch the equality
    _old_ea_equality = getattr(ExtArray, '__eq__')
    def _new_ea_equality(ea1, ea2):
        res = _old_ea_equality(ea1, ea2)
        return res._arr if isinstance(res._arr, Equality) else res
    setattr(ExtArray, '__eq__', _new_ea_equality)
    
    for iop in _INPLACE_OPERATORS:
        iopd = '__' + iop + '__'
        setattr(ExtArray, iopd, _make_inplace_func(iopd))
    
    current_module = sys.modules[__name__]
    for func_name in _NUMPY_FUNCS:
        np_func = getattr(numpy, func_name)
        setattr(current_module, func_name, extend_vectorized_function()(np_func))
    for func_name in _NUMPY_MMFUNCS:
        np_func = getattr(numpy, func_name)
        setattr(current_module, func_name, extend_minmax_function(np_func))

_monkey_patch()


#%% A collection of unknown variables
class EACollection:
    def __init__(self, numeric_collection):
        "Create from several ExtArrays which may have different boxes"
        self.numeric_collection = numeric_collection
        n = []
        for uv in numeric_collection:
            assert isinstance(uv, ExtArray)
            n.append(int(numpy.prod(uv.nt)))
        self.addr = numpy.hstack((0, numpy.cumsum(n)))
    def sym(self, name):
        self.ref = FieldRef(name, (self.addr[-1],)) # Keep it just in case
        storage = FieldOperator(self.ref, init=True)
        symbolic_collection = []
        for k, uv in enumerate(self.numeric_collection):
            u = uv.box[uv.spans]
            u._arr = storage[self.addr[k]:self.addr[k+1]].reshape(u.nt)
            symbolic_collection.append(u)
        return symbolic_collection
    def assign(self, solution):
        for k, uv in enumerate(self.numeric_collection):
            uv._arr = solution[self.addr[k]:self.addr[k+1]].reshape(uv.nt)

make_indented_printable(EACollection)

#%% Operations
def aver(ea, axis=None):
    return (ea.shift(half, axis) + ea.shift(-half, axis))/2

def diff(ea, axis=None):
    return ea.shift(half, axis) - ea.shift(-half, axis)

def upstream(ea, v, axis=None):
    return ea.shift(-half, axis)*(v>=0) + ea.shift(half, axis)*(v<0)

def cumsum(ea, axis=0):
    "Operation opposite to diff, useful for integration."
    assert ea.is_num # don't use on symbolic!
    spans = tuple(_shift_ea_slice(ea.spans[a], half) if a==axis else ea.spans[a]
                     for a in range(ea.box.ndim))
    return ExtArray(ea.box, spans, numpy.cumsum(ea._arr, axis=axis))
