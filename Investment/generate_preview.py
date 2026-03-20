"""
Generate a static preview image of the investment tradeoff curves.
Reproduces the core computation from bokeh_script.py and bokeh_script_cont.py
using only numpy + matplotlib (no Bokeh required).

Output: assets/preview.png
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("assets", exist_ok=True)

# --- Default parameters ---
year_max  = 20
r_fee     = 0.03
r_div     = 0.05
C_invest0 = 100
C_house   = 200
S_earn    = 10
S_save    = 10

alphas = np.linspace(0, 1, 101)


def tradeoff_discrete(alpha):
    C_used  = C_invest0 * alpha
    C_loan  = C_house - C_used
    C_inv   = C_invest0 - C_used
    t1      = C_loan / S_earn
    fees    = C_loan * r_fee * (t1 + 1) / 2
    s0      = S_save - fees / t1
    s1      = S_save + S_earn
    C1      = C_inv + s0 * t1
    C2      = C1 + (year_max - t1) * s1
    D0      = (C_inv + C1) / 2 * t1 * r_div
    D1      = (C1 + C2) / 2 * (year_max - t1) * r_div
    return C2 + D0 + D1


def tradeoff_continuous(alpha):
    C_used  = C_invest0 * alpha
    C_loan  = C_house - C_used
    C_inv   = C_invest0 - C_used
    t1      = C_loan / S_earn
    fees    = C_loan * r_fee * (t1 + 1) / 2
    s0      = S_save - fees / t1
    s1      = S_save + S_earn
    k       = 50
    r1      = np.exp(np.log(1 + r_div) / k)
    c       = C_inv
    for _ in range(int(k * t1)):
        c = c * r1 + s0 / k
    for _ in range(int(k * t1), k * year_max):
        c = c * r1 + s1 / k
    return c


y_disc = np.array([tradeoff_discrete(a) for a in alphas])
y_cont = np.array([tradeoff_continuous(a) for a in alphas])

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(alphas * 100, y_disc, linewidth=2.5, label="Discrete compounding", color="steelblue")
ax.plot(alphas * 100, y_cont, linewidth=2.5, label="Continuous compounding", color="tomato", linestyle="--")
ax.set_xlabel("Capital used for house down payment (%)", fontsize=12)
ax.set_ylabel("Total wealth after {} years (k€)".format(year_max), fontsize=12)
ax.set_title("Investment tradeoff: house vs. portfolio", fontsize=13)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/preview.png", dpi=130)
print("Saved assets/preview.png")
