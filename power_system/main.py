"""Stage-1 executable: build Ybus and run Newton-Raphson load flow."""

from data.system_data import (
    BUS_DATA,
    LINE_DATA,
    BUS_IDS,
    BUS_INDEX,
    SystemConfig,
)

from power_system.ybus import build_ybus
from power_system.load_flow import solve_load_flow


def main():
    config = SystemConfig()

    ybus = build_ybus(LINE_DATA, BUS_INDEX)

    result = solve_load_flow(
        BUS_DATA,
        ybus,
        tolerance=config.tolerance,
        max_iterations=config.max_iterations,
    )

    print("=" * 72)
    print("IEEE-18 BUS LOAD FLOW — PYTHON")
    print("=" * 72)

    print(f"Converged : {result.converged}")
    print(f"Iterations: {result.iterations}")
    print(f"Mismatch  : {result.max_mismatch:.3e}")
    print()

    print("Bus   | V (pu) | Angle (deg) | P (pu) | Q (pu)")
    print("-" * 52)

    for i, (v, a, p, q) in enumerate(
        zip(
            result.voltage,
            result.angle_rad,
            result.p_injection,
            result.q_injection,
        )
    ):
        bus_id = BUS_IDS[i]

        print(
            f"{bus_id:>4} | "
            f"{v:>6.4f} | "
            f"{a * 180 / 3.141592653589793:>11.4f} | "
            f"{p:>6.4f} | "
            f"{q:>6.4f}"
        )

    print()
    print("Ybus shape:", ybus.shape)
    print("Ybus symmetry error:", abs(ybus - ybus.T).max())


if __name__ == "__main__":
    main()