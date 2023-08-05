import pytest

import LeProHQ


def test_thr_xi():
    LeProHQ.cg1("F2", "VV", 10.0, 1e-10)
    with pytest.raises(LeProHQ.utils.LeProHQError):
        LeProHQ.cg1("F2", "VV", 1e5, 1e-10)


def test_bulk_xi():
    LeProHQ.cg1("F2", "VV", 99.0, 1)
    with pytest.raises(LeProHQ.utils.LeProHQError):
        LeProHQ.cg1("F2", "VV", 1e5, 1)
