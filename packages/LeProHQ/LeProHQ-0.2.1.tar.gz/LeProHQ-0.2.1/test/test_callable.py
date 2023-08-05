from numbers import Number

import numpy as np

import LeProHQ
from LeProHQ.partonic_vars import build_prime

xis = [1.0, 2.0]
etas = [1e-5, 1.0, 10.0]


def test_callable():
    for proj in ["F2"]:
        for cc in ["VV"]:
            for xi in xis:
                for eta in etas:
                    for cf in [
                        LeProHQ.cg0,
                        LeProHQ.cg1,
                        LeProHQ.cgBar1,
                        LeProHQ.cqBarF1,
                        LeProHQ.dq1,
                    ]:
                        x = cf(proj, cc, xi, eta)
                        assert isinstance(x, Number)
                        assert np.isfinite(x)
                    for cf in [LeProHQ.cgBarF1, LeProHQ.cgBarR1]:
                        x = cf(proj, cc, xi, eta, 3)
                        assert isinstance(x, Number)
                        assert np.isfinite(x)


def test_build_prime():
    for xi in xis:
        for eta in etas:
            x = build_prime(xi, eta)
            assert isinstance(x[0], Number)
            assert isinstance(x[1], Number)
            assert isinstance(x[2], Number)
            assert np.isfinite(x[0])
            assert np.isfinite(x[1])
            assert np.isfinite(x[2])
