"""Newton-Raphson AC load-flow solver."""

from dataclasses import dataclass
import numpy as np

@dataclass
class LoadFlowResult:
    voltage: np.ndarray
    angle_rad: np.ndarray
    p_injection: np.ndarray
    q_injection: np.ndarray
    converged: bool
    iterations: int
    max_mismatch: float

def _calc_power(v, theta, ybus):
    """Calculate bus P/Q injections from V∠theta."""
    Vc = v * np.exp(1j * theta)
    S = Vc * np.conj(ybus @ Vc)
    return S.real, S.imag

def _specified_power(bus_data):
    # bus_data columns: id,type,V,angle,Pd,Qd,Pg,Qg
    return bus_data[:, 6] - bus_data[:, 4], bus_data[:, 7] - bus_data[:, 5]

def solve_load_flow(bus_data, ybus, tolerance=1e-8, max_iterations=50):
    """
    Solve using the bus types encoded in bus_data:
      1 = slack
      2 = PV
      3 = PQ

    The actual busdata.m row layout is used explicitly.
    """
    n = len(bus_data)
    bus_type = bus_data[:, 1].astype(int)

    slack = np.where(bus_type == 1)[0]
    pv = np.where(bus_type == 2)[0]
    pq = np.where(bus_type == 3)[0]

    if len(slack) != 1:
        raise ValueError(f"Expected exactly one slack bus, found {len(slack)}.")

    p_spec, q_spec = _specified_power(bus_data)

    v = bus_data[:, 2].copy()
    theta = np.deg2rad(bus_data[:, 3].copy())

    # PV buses keep their specified voltage magnitude.
    pv_v = v[pv].copy()

    angle_buses = np.r_[pv, pq]
    pq_buses = pq

    converged = False
    max_mismatch = np.inf

    for iteration in range(1, max_iterations + 1):
        p, q = _calc_power(v, theta, ybus)

        dp = p_spec - p
        dq = q_spec - q

        mismatch = np.r_[dp[angle_buses], dq[pq_buses]]
        max_mismatch = float(np.max(np.abs(mismatch))) if mismatch.size else 0.0

        if max_mismatch < tolerance:
            converged = True
            break

        J = _build_jacobian(v, theta, ybus, p, q, angle_buses, pq_buses)

        try:
            dx = np.linalg.solve(J, mismatch)
        except np.linalg.LinAlgError as exc:
            raise RuntimeError("Newton-Raphson Jacobian is singular.") from exc

        n_ang = len(angle_buses)
        theta[angle_buses] += dx[:n_ang]
        v[pq_buses] += dx[n_ang:]

        # Re-impose PV/slack magnitudes.
        v[pv] = pv_v
        v[slack[0]] = bus_data[slack[0], 2]
        theta[slack[0]] = np.deg2rad(bus_data[slack[0], 3])

        if np.any(v <= 0):
            raise RuntimeError("Newton-Raphson produced a non-positive bus voltage.")

    p, q = _calc_power(v, theta, ybus)

    return LoadFlowResult(
        voltage=v,
        angle_rad=theta,
        p_injection=p,
        q_injection=q,
        converged=converged,
        iterations=iteration,
        max_mismatch=max_mismatch,
    )

def _build_jacobian(v, theta, ybus, p, q, angle_buses, pq_buses):
    """Analytical Newton-Raphson Jacobian for polar coordinates."""
    G = ybus.real
    B = ybus.imag

    n_a = len(angle_buses)
    n_q = len(pq_buses)
    J = np.zeros((n_a + n_q, n_a + n_q), dtype=float)

    # H = dP/dtheta
    for a, i in enumerate(angle_buses):
        for b, k in enumerate(angle_buses):
            if i == k:
                J[a, b] = -q[i] - B[i, i] * v[i] ** 2
            else:
                d = theta[i] - theta[k]
                J[a, b] = v[i] * v[k] * (
                    G[i, k] * np.sin(d) - B[i, k] * np.cos(d)
                )

    # N = dP/dV
    for a, i in enumerate(angle_buses):
        for b, k in enumerate(pq_buses):
            if i == k:
                J[a, n_a + b] = p[i] / v[i] + G[i, i] * v[i]
            else:
                d = theta[i] - theta[k]
                J[a, n_a + b] = v[i] * (
                    G[i, k] * np.cos(d) + B[i, k] * np.sin(d)
                )

    # M = dQ/dtheta
    for a, i in enumerate(pq_buses):
        for b, k in enumerate(angle_buses):
            if i == k:
                J[n_a + a, b] = p[i] - G[i, i] * v[i] ** 2
            else:
                d = theta[i] - theta[k]
                J[n_a + a, b] = -v[i] * v[k] * (
                    G[i, k] * np.cos(d) + B[i, k] * np.sin(d)
                )

    # L = dQ/dV
    for a, i in enumerate(pq_buses):
        for b, k in enumerate(pq_buses):
            if i == k:
                J[n_a + a, n_a + b] = q[i] / v[i] - B[i, i] * v[i]
            else:
                d = theta[i] - theta[k]
                J[n_a + a, n_a + b] = v[i] * (
                    G[i, k] * np.sin(d) - B[i, k] * np.cos(d)
                )

    return J
