import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

price_a = np.full(12, 325.)
price_b = np.array([300, 300, 290, 275, 275, 280,
                    260, 250, 230, 200, 210, 190.])
price_c = np.array([100, 110, 98, 115, 200, 220,
                    210, 500, 500, 490, 487, 550.])

a = cp.Variable(12)
b = cp.Variable(12)
c = cp.Variable(12)
constraints = [
    a + b + c == 10000,
    a >= 2000, b >= 2000, c >= 2000,
    c[7:] <= 5000, b <= 4500, a[:7] <= 4000]
profit = price_a*a + price_b*b + price_c*c
objective = cp.Maximize(profit)
problem = cp.Problem(objective, constraints)
problem.solve(verbose=True)

a = np.around(a.value, decimals = 0)
b = np.around(b.value, decimals = 0)
c = np.around(c.value, decimals = 0)
profit_a = a * price_a
profit_b = b * price_b
profit_c = c * price_c
cumul_a = []
cumul_b = []
cumul_c = []
sum = 0

for each in profit_a:
    sum += each
    cumul_a.append(sum)
for each in profit_b:
    sum += each
    cumul_b.append(sum)
for each in profit_c:
    sum += each
    cumul_c.append(sum)

plt.figure(1)
plt.subplot(231)
plt.plot(price_a, linewidth = 2.5, label="price_a")
plt.plot(price_b, linewidth = 2.5, label="price_b")
plt.plot(price_c, linewidth = 2.5, label="price_c")
plt.title("Price of mobiles a, b, c")
plt.grid()
plt.legend()
plt.xlabel("Month")
plt.ylabel("Price of each unit")

plt.subplot(232)
plt.plot(a, linewidth = 2.5, label="type a")
plt.plot(b, linewidth = 2.5, label="type b")
plt.plot(c, linewidth = 2.5, label="type c")
plt.title("Units of mobiles a, b, c per month")
plt.grid()
plt.legend()
plt.xlabel("Month")
plt.ylabel("No. of units")

plt.subplot(233)
plt.plot(a*price_a, linewidth = 2.5, label="type a")
plt.plot(b*price_b, linewidth = 2.5, label="type b")
plt.plot(c*price_c, linewidth = 2.5, label="type c")
plt.title("Total profit per month for a, b, c")
plt.grid()
plt.legend()
plt.xlabel("Month")
plt.ylabel("Total Profit")

plt.subplot(234)
plt.plot(cumul_a, linewidth = 2.5, label="type a")
plt.plot(cumul_b, linewidth = 2.5, label="type b")
plt.plot(cumul_c, linewidth = 2.5, label="type c")
plt.title("Cumulative profit for a, b, c")
plt.grid()
plt.legend()
plt.xlabel("Month")
plt.ylabel("Total Cumulative Profit")

plt.subplot(235)
plt.plot(profit_a + profit_b + profit_c, linewidth = 2.5, label="type a")
plt.title("Total profit (a+b+c)")
plt.grid()
plt.xlabel("Month")
plt.ylabel("Total Profit")

plt.subplot(236)
plt.plot(cumul_a+cumul_b+cumul_c, linewidth = 2.5, label="type a")
plt.title("Total cumulative profit")
plt.grid()
plt.xlabel("Month")
plt.ylabel("Total Cumulative Profit")
plt.show()

print("Total profit for next year: " + str(np.sum(profit_a) + np.sum(profit_b) + np.sum(profit_c)))