import cvxpy as cp
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.datasets import load_svmlight_file

# 設定
regularization = 1.0

# データを読み込む
x, y = load_svmlight_file('housing_scale')
n, d = x.shape # n: 事例数, d: 特徴数

# まずは、既存のLasso実装で学習計算を行う。
# 今回はfit_interceptをFalseにしたが、これはTrueにした場合の定式化を
# CVXPYで書こうとすると、CVXPYが凸であると判定できるように書くのが
# 面倒になるため。
print('---------- Solving with sklearn.linear_model.Lasso ----------')
lasso = Lasso(alpha=regularization, fit_intercept=False, max_iter=1000000, tol=1.0e-6)
lasso.fit(x, y)

# 続いて、CVXPYで定式化を書いて学習計算を行う。
print('---------- Solving with CVXPY (naive) ----------')
beta = cp.Variable(d)
obj_function = (cp.norm(y - x @ beta, 2) ** 2) / (2 * n) + regularization * cp.norm(beta, 1)
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()
print('Used solver:', problem.solver_stats.solver_name)
# 今回はLassoで用いる二乗誤差を計算するのに、 cp.norm(y - x @ beta, 2) ** 2 という
# 式を用いている。
# この場合、CVXPYは「L2ノルムを計算し、その後それを二乗したもの」が凸であると判定できる
# （凸関数に、外から「単調増加な凸関数」を付けてもなお凸であるため）のだが、
# 最適なソルバーを選ぶことができず、警告が出る。

# そこでCVXPYの定式化を少し変えてみる。
# CVXPYで二乗和を求める関数として「sum_squares」というものがあらかじめ定義されて
# いるので、これを使う。
print('---------- Solving with CVXPY (sum_squares) ----------')
beta_ss = cp.Variable(d)
obj_function_ss = cp.sum_squares(y - x @ beta_ss) / (2 * n) + regularization * cp.norm(beta_ss, 1)
problem_ss = cp.Problem(cp.Minimize(obj_function_ss))
problem_ss.solve()
print('Used solver:', problem_ss.solver_stats.solver_name)

# 結果を表示
# CVXPYのどちらの結果も、おおむね既存のLasso実装の結果に近い値が出るが、
# sum_squaresを使ったときのほうが精度が高い。
print('---------- Results ----------')
print('Optimal variable value (Lasso Package / CVXPY-naive / CVXPY-sum_squares):')
print(np.vstack((lasso.coef_, beta.value, beta_ss.value)).T)
print('Difference (Lasso Package - CVXPY-naive / Lasso Package - CVXPY-sum_squares):')
print(np.vstack((lasso.coef_ - beta.value, lasso.coef_ - beta_ss.value)).T)
