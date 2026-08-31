import numpy as np
from data.system_data import BUS_DATA, LINE_DATA
from power_system.ybus import build_ybus

def test_ybus_shape_and_symmetry():
    y = build_ybus(LINE_DATA, len(BUS_DATA))
    assert y.shape == (18, 18)
    assert np.allclose(y, y.T)
    assert np.count_nonzero(np.abs(y)) > 18
