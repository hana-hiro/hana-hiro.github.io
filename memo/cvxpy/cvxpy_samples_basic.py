import cvxpy as cp
import numpy as np

# ---------- スカラー変数の最適化

x = cp.Variable(1) # 1: 変数の次元数
obj_function = x ** 2 + 2 * x
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()

print('Used solver:', problem.solver_stats.solver_name)
print('Optimal function value:', problem.value)
print('Optimal variable value:', x.value)

# ---------- ベクトル変数の最適化

x = cp.Variable(2) # 2: 変数の次元数
a = np.array([[1, 2], [2, 5]])
b = np.array([-1, 1])

obj_function = cp.quad_form(x, a) + x @ b
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()

print('Used solver:', problem.solver_stats.solver_name)
print('Optimal function value:', problem.value)
print('Optimal variable value:', x.value)

# ---------- 制約付き最適化

x = cp.Variable(1) # 1: 変数の次元数
obj_function = x ** 2 + 2 * x
constraints = [x >= 1, x <= 2]
problem = cp.Problem(cp.Minimize(obj_function), constraints)
problem.solve()

print('Used solver:', problem.solver_stats.solver_name)
print('Optimal function value:', problem.value)
print('Optimal variable value:', x.value)
