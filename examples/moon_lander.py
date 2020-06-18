"""
Created: 5th May 2020
Author : Devakumar Thammisetty
"""
from context import mpopt
from mpopt import mp

ocp = mp.OCP(n_states=2, n_controls=1)


def dynamics0(x, u, t):
    return [x[1], u[0] - 1.5]


ocp.dynamics[0] = dynamics0


def running_cost0(x, u, t):

    return u[0]


ocp.running_costs[0] = running_cost0


def terminal_constraints0(xf, tf, x0, t0):

    return [xf[0], xf[1]]


ocp.terminal_constraints[0] = terminal_constraints0

ocp.tf0[0] = 4.0
ocp.x00[0] = [10.0, -2.0]
ocp.lbx[0] = [-20.0, -20.0]
ocp.ubx[0] = [20.0, 20.0]
ocp.lbu[0] = 0
ocp.ubu[0] = 3
ocp.lbtf[0], ocp.ubtf[0] = 3, 5

ocp.validate()

mpo = mp.mpopt(ocp, 5, 4)
sol = mpo.solve()
post = mpo.process_results(sol, plot=True)
mp.plt.title(
    f"non-adaptive solution segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
)

mpo = mp.mpopt_h_adaptive(ocp, 10, 4)
sol = mpo.solve(
    max_iter=3, mpopt_options={"method": "residual", "sub_method": "merge_split"}
)
post = mpo.process_results(sol, plot=True)
mp.plt.title(
    f"Adaptive solution: merge_split : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
)

mpo = mp.mpopt_h_adaptive(ocp, 10, 4)
sol = mpo.solve(
    max_iter=2, mpopt_options={"method": "residual", "sub_method": "equal_area"}
)
post = mpo.process_results(sol, plot=True)
mp.plt.title(
    f"Adaptive solution: equal_residual : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
)

mpo = mp.mpopt_h_adaptive(ocp, 5, 4)
sol = mpo.solve(
    max_iter=10, mpopt_options={"method": "control_slope", "sub_method": ""}
)
post = mpo.process_results(sol, plot=True)
mp.plt.title(
    f"Adaptive solution: Control slope : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
)

mpo = mp.mpopt_adaptive(ocp, 3, 2)
mpo.lbh[0] = 1e-6
mpo.mid_residuals = True
sol = mpo.solve()
post = mpo.process_results(sol, plot=True)
mp.plt.title(
    f"Adaptive solution: Direct opt. : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
)

mp.plt.show()