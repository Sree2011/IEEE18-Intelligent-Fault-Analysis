from data.system_data import BUS_DATA, LINE_DATA
from power_system.ybus import build_ybus
from power_system.load_flow import solve_load_flow

def test_load_flow_converges():
    y = build_ybus(LINE_DATA, len(BUS_DATA))
    result = solve_load_flow(BUS_DATA, y)
    assert result.converged
    assert result.max_mismatch < 1e-8
    assert len(result.voltage) == 18
    assert (result.voltage > 0).all()
