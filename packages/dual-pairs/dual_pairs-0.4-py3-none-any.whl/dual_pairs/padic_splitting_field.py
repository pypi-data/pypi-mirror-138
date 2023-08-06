# -*- coding: utf-8 -*-
"""
A class for `p`-adic splitting fields
"""

from sage.categories.fields import Fields
from sage.rings.padics.factory import Qp
from sage.rings.ring import Field

# TODO

class pAdicSplittingField(Field):
    def __init__(self, f, L, roots, H, aut):
        self._f = f
        self._L = L
        self._roots = roots
        self._H = H
        self._aut = aut
        p = L.prime()
        self.Element = L.Element
        self.prime_pow = L.prime_pow
        Field.__init__(self, base_ring=Qp(p),
                       category=Fields().Infinite())

    # def _coerce_map_from_(self, R):
    #     if R is self._L:
    #         from sage.structure.coerce_maps import DefaultConvertMap
    #         return self._generic_coerce_map(R)
    #     return self._coerce_map_via([self._L], R)
        
    def _roots_univariate_polynomial(self, f, *args, **kwds):
        if f == self._f:
            return self._roots
        elif f.degree() == 1:
            return [self(-f[0]/f[1])]
        else:
            raise NotImplementedError('_roots_univariate_polynomial')


def add_splitting_field_data(L, f, roots, H, aut):
    L._splf_poly = f
    L._splf_roots = roots
    L._splf_H = H
    L._splf_aut = aut
    
    def _roots_univariate_polynomial(g, *args, **kwds):
        if g == f:
            return roots
        elif g.degree() == 1:
            return [L(-g[0]/g[1])]
        else:
            raise NotImplementedError('_roots_univariate_polynomial')

    L._roots_univariate_polynomial = _roots_univariate_polynomial
