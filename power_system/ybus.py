"""Bus admittance matrix construction."""

import numpy as np


def build_ybus(line_data, bus_index):
    """Build the bus admittance matrix using the pi-model.

    Accepts either:
      - a dict mapping bus IDs to matrix indices, or
      - an integer number of buses for compatibility with older callers/tests.
    """
    if isinstance(bus_index, dict):
        bus_map = bus_index
    elif isinstance(bus_index, (int, np.integer)):
        unique_buses = sorted(
            {int(row[0]) for row in line_data} | {int(row[1]) for row in line_data}
        )
        if len(unique_buses) != int(bus_index):
            raise ValueError(
                f"Expected {int(bus_index)} buses, but found {len(unique_buses)} unique IDs."
            )
        bus_map = {bus_id: idx for idx, bus_id in enumerate(unique_buses)}
    else:
        raise TypeError("bus_index must be a dict or an integer bus count.")

    n_buses = len(bus_map)
    ybus = np.zeros((n_buses, n_buses), dtype=complex)

    for row in line_data:
        from_bus = int(row[0])
        to_bus = int(row[1])
        r, x, b = row[2:5]

        i = bus_map[from_bus]
        j = bus_map[to_bus]

        z = complex(r, x)
        y_series = 1 / z
        y_shunt = 1j * b / 2

        ybus[i, i] += y_series + y_shunt
        ybus[j, j] += y_series + y_shunt
        ybus[i, j] -= y_series
        ybus[j, i] -= y_series

    return ybus