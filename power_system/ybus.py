"""Bus admittance matrix construction."""

import numpy as np

def build_ybus(line_data: np.ndarray, n_buses: int) -> np.ndarray:
    """Build Ybus using the pi-model line charging convention from the original code."""
    ybus = np.zeros((n_buses, n_buses), dtype=complex)

    for row in line_data:
        i = int(row[0]) - 1
        j = int(row[1]) - 1
        r, x, b = row[2:5]

        z = complex(r, x)
        y_series = 1 / z
        y_shunt = 1j * b / 2

        ybus[i, i] += y_series + y_shunt
        ybus[j, j] += y_series + y_shunt
        ybus[i, j] -= y_series
        ybus[j, i] -= y_series

    return ybus
