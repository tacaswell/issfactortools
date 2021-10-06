from pymcr.mcr import McrAR
import numpy as np


class DataSet:

    def __init__(self, x, t, data,
                 x_name='energy', t_name='curve index', data_name='mu norm',
                 x_units='eV', t_units='', data_units='',
                 name='dataset'):

        self._validate_input(x, t, data)
        self._x = x
        self._t = t
        self._data = data

        self.set_x_limits(x.min(), x.max())

        self.t_mask = np.ones(t.size, dtype=bool)

        self.x_name = x_name
        self.t_name = t_name
        self.data_name = data_name

        self.x_units = x_units
        self.t_units = t_units
        self.data_units = data_units

        self.name = name

    def _validate_input(self, x, t, data):
        nx, nt = data.shape
        sizes_match = (nx == x.size) and (nt == t.size)
        if not sizes_match:
            raise Exception('x, t, and data sizes/shapes do not match')

    def set_x_limits(self, xmin, xmax):
        self.xmin = xmin
        self.xmax = xmax
        self.x_mask = (self._x >= self.xmin) & (self._x <= self.xmax)

    def set_t_mask(self, t_mask):
        if t_mask.size == self._t.size:
            self.t_mask = t_mask
        else:
            raise Exception('Error: t_mask must be the same size as t')

    @property
    def data(self):
        # return self._data[self.x_mask, self.t_mask]
        return self._data[np.ix_(self.x_mask, self.t_mask)]

    @property
    def x(self):
        return self.x[self.x_mask]

    @property
    def t(self):
        return self.t[self.t_mask]



class ReferenceSet:
    def __init__(self):
        self.reference_dict = {}

    def append_reference(self, x, data, label:str, fixed:bool):
        self.validate_reference(x, data, label)
        _d = {'x' : x, 'data': data, 'fixed' : fixed}
        self.reference_dict = {label : _d}

    def validate_reference(self, x, data, label):
        shape_match = (len(data.shape) == 1)
        if not shape_match:
            raise Exception(f'{label} Reference data shape mismatch: data.shape should be ({data.size}, );  currently is {data.shape}')

        size_match = (data.size == x.size)
        if not size_match:
            raise Exception(f'{label} Reference data size mismatch: data.size should be == x.size; currently: data.size={data.ize} and x.size={x.size}')

        label_match = (label in self.labels)
        if not label_match:
            raise KeyError(f'Provided labels must be unique. {label} already exists')

    @property
    def labels(self):
        return list(self.reference_dict.keys())


class ConstraintSet:
    def __init__(self):
        self.c_constraints = []
        self.st_constraints = []

    def append_c_constraint(self, c_constraint):
        self.c_constraints.append(c_constraint)

    def append_st_constraint(self, st_constraint):
        self.st_constraints.append(st_constraint)




class MCRProject:

    def __init__(self, data=None,
                 data_ref = None,
                 c_fix=None, st_fix=None,
                 c_constraints=None, st_constraints=None,
                 c_regr=None, st_regr=None, max_iter:int=1000):
        self.data = data
        self.data_ref = data_ref
        self.c_fix = None
        self.st_fix = None
        self.c_constraints = c_constraints
        self.st_constraints = st_constraints
        self.c_regr = c_regr
        self.st_regr = st_regr
        self.max_iter = max_iter

        if ((data is not None) and
            (data_ref is not None) and
            (c_fix is not None) and
            (st_fix is not None) and
            (c_constraints is not None) and
            (st_constraints is not None) and
            (c_regr is not None) and
            (st_regr is not None)
            (max_iter is not None)):

            self.mcr = McrAR(st_regr=self.s_optmizer, c_regr=self.c_optimizer,
                             c_constraints=self.c_constraints,
                             st_constraints=self.st_constraints,
                             max_iter=self.max_iter)

    def fit(self):
        self.mcr.fit(self.data.T, ST=self.data_ref.T,
                     c_fix=self.c_fix,
                     st_fix=self.st_fix)

        self.data_ref_fit = self.mcr.ST_opt_.T
        self.c_fit = self.mcr.C_opt_.T
        self.data_fit = (self.data_ref_fit @ self.c_fit)












