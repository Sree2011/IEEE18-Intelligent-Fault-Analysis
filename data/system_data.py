"""IEEE-18-bus data adapted directly from the uploaded MATLAB/Octave project."""

from dataclasses import dataclass
import numpy as np

# Actual layout in the original busdata.m:
# bus_id, type, V_mag, V_angle_deg, Pd_MW, Qd_Mvar, Pg_MW, Qg_Mvar
BUS_DATA = np.array([
    [1,  1, 1.06, 0,  0, 0,  0,  0],
    [2,  2, 1.00, 0, 40, 0, 20, 10],
    [3,  3, 1.00, 0,  0, 0, 45, 15],
    [4,  3, 1.00, 0,  0, 0, 40, 20],
    [5,  3, 1.00, 0,  0, 0, 60, 25],
    [6,  2, 1.00, 0, 30, 0, 25, 15],
    [7,  3, 1.00, 0,  0, 0, 35, 10],
    [8,  3, 1.00, 0,  0, 0, 20, 10],
    [9,  3, 1.00, 0,  0, 0, 15, 5],
    [10, 3, 1.00, 0,  0, 0, 10, 5],
    [11, 3, 1.00, 0,  0, 0, 25, 10],
    [12, 3, 1.00, 0,  0, 0, 30, 15],
    [13, 2, 1.00, 0, 35, 0, 20, 10],
    [14, 3, 1.00, 0,  0, 0, 15, 5],
    [15, 3, 1.00, 0,  0, 0, 20, 10],
    [16, 3, 1.00, 0,  0, 0, 25, 10],
    [17, 3, 1.00, 0,  0, 0, 30, 15],
    [18, 3, 1.00, 0,  0, 0, 20, 10],
], dtype=float)

# Actual layout in original linedata.m:
# from_bus, to_bus, R_pu, X_pu, B_pu
LINE_DATA = np.array([
    [1, 2,  .02, .06, .03],
    [2, 3,  .05, .19, .02],
    [3, 4,  .06, .17, .02],
    [4, 5,  .04, .13, .01],
    [5, 6,  .03, .10, .01],
    [6, 7,  .04, .12, .01],
    [7, 8,  .05, .20, .02],
    [8, 9,  .06, .18, .02],
    [9, 10, .04, .13, .01],
    [10,11, .03, .09, .01],
    [11,12, .04, .12, .01],
    [12,13, .05, .15, .02],
    [13,14, .06, .17, .02],
    [14,15, .04, .13, .01],
    [15,16, .03, .10, .01],
    [16,17, .04, .12, .01],
    [17,18, .05, .20, .02],
], dtype=float)

# Original gendata.m:
# bus_id, generator_type, Pg_MW, Qg_Mvar, V_setpoint_pu, Qmin_Mvar, Qmax_Mvar
GEN_DATA = np.array([
    [1,  1,  0,  0, 1.06,  0,  0],
    [2,  2, 40,  0, 1.00, -20, 50],
    [5,  2, 30,  0, 1.00, -15, 40],
    [9,  2, 20,  0, 1.00, -10, 30],
    [13, 2, 25,  0, 1.00, -15, 35],
], dtype=float)

@dataclass(frozen=True)
class SystemConfig:
    base_mva: float = 100.0
    tolerance: float = 1e-8
    max_iterations: int = 50
