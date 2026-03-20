"""
Car insurance cost comparison.

Two strategies for someone starting with a bad car:
  - Scenario 1: Drive bad car ($500/yr) for 10 years, then switch to new car ($1000/yr).
  - Scenario 2: Buy new car ($1000/yr) directly from the start.

Discount decreases by 5% per year until reaching 50% (i.e. the base rate).
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)

P_bad = 500    # annual insurance for bad car (full price)
P_new = 1000   # annual insurance for new car (full price)
T_switch = 10  # year at which scenario 1 switches to new car
T_total = 20   # total years simulated


def cumulative_cost(prices):
    """Return cumulative sum of a list of annual costs."""
    return np.cumsum(prices)


def discount(year, base_price):
    """Price after bonus-malus discount: -5% per year, minimum 50%."""
    rate = max(0.5, 1.0 - year * 0.05)
    return base_price * rate


# --- Scenario 1: bad car then new car ---
costs_1 = []
for y in range(T_switch):
    costs_1.append(discount(y, P_bad))
for y in range(T_total - T_switch):
    # after switch: discount resets for the new car, bad car kept at 50%
    costs_1.append(discount(y, P_new) + P_bad * 0.5)

# --- Scenario 2: new car directly ---
costs_2 = []
for y in range(T_switch):
    costs_2.append(discount(y, P_new))
for y in range(T_total - T_switch):
    costs_2.append(P_new * 0.5)


years = np.arange(T_total)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].set_title("Annual insurance cost")
axes[0].plot(years, costs_1, label="Scenario 1 (bad → new)", color="steelblue")
axes[0].plot(years, costs_2, label="Scenario 2 (new directly)", color="tomato")
axes[0].axvline(T_switch, color="gray", linestyle="--", linewidth=1, label="Switch year")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Cost (€)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].set_title("Cumulative insurance cost")
axes[1].plot(years, cumulative_cost(costs_1), label="Scenario 1 (bad → new)", color="steelblue")
axes[1].plot(years, cumulative_cost(costs_2), label="Scenario 2 (new directly)", color="tomato")
axes[1].axvline(T_switch, color="gray", linestyle="--", linewidth=1, label="Switch year")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Cumulative cost (€)")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("output/car_insurance.png", dpi=120)
plt.show()
print("Saved output/car_insurance.png")
