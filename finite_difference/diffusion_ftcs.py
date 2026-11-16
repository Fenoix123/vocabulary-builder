"""FTCS solution of u_t = omega*u_yy on y >= 0.

Run in Codespaces:
    pip install numpy matplotlib
    python finite_difference/diffusion_ftcs.py
"""
from pathlib import Path
from math import erfc
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

omega = 0.5
h = 0.1
dt = 0.005
L = 6.0                 # approximation of infinity
T = 2.0
r = omega * dt / h**2
assert 0 < r <= 0.5, "FTCS stability requires r <= 1/2"

y = np.arange(0, L + h / 2, h)
u = np.zeros(len(y))
u[0] = 1.0
snapshots = {0.0: u.copy()}
times = {0.1, 0.5, 1.0, 2.0}

for n in range(1, round(T / dt) + 1):
    next_u = u.copy()
    next_u[1:-1] = r * u[:-2] + (1 - 2*r) * u[1:-1] + r * u[2:]
    next_u[0] = 1.0
    next_u[-1] = 0.0
    u = next_u
    t = round(n * dt, 10)
    if t in times:
        snapshots[t] = u.copy()

fig, ax = plt.subplots(figsize=(9, 5.5))
for t, values in snapshots.items():
    ax.plot(y, values, label=f"t = {t:g}")
ax.set(xlabel="Position y", ylabel="u(y,t)",
       title="Diffusion equation: FTCS (omega=0.5, h=0.1, dt=0.005)",
       xlim=(0, 5), ylim=(-0.02, 1.05))
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
output = Path(__file__).with_name("diffusion_plot.png")
fig.savefig(output, dpi=180)
print(f"Stability factor r = {r}")
print(f"Numerical u(0.5,0.5) = {snapshots[0.5][5]:.6f}")
print(f"Numerical u(1,1) = {snapshots[1.0][10]:.6f}")
print(f"Exact u(1,1) = {erfc(1/(2*np.sqrt(omega))):.6f}")
print(f"Plot saved to {output}")
