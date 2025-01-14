---
layout: default
title: CVXPYによる凸関数の最小化
---
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script"></script>

-   [Back to top page](../../)
-   [Back to other notes](../)

# CVXPYによる凸関数の最小化

## 概要

[CVXPY](https://www.cvxpy.org/)とは、Pythonにおける「凸関数を書くと、その式を最小化する変数を求めてくれる」ライブラリである。

ただし、以下の点には注意が必要である。

- どのような凸関数でも最小化できるわけではなく、CVXPYのライブラリが取り扱える関数の組み合わせで書く必要があり、かつCVXPYのライブラリが「凸関数と認識できるように」書く必要がある。（詳細は後述）
- 特定の問題に特化したソルバーに比べると、遅いことが多く、かつ計算精度も出ない場合が多い。

このため筆者は主に、「自前で特定の問題に特化したソルバーを書いたときに、計算がうまくいったかを確認する」ために用いている。

## インストール

-   pipやcondaでインストールするのが容易である。
    -   condaの場合、デフォルトのチャンネルには含まれておらず、`conda-forge`チャンネルなどを指定する必要がある。`conda install -c conda-forge cvxpy` となる。
-   その他、詳しくは[公式サイトの案内](https://www.cvxpy.org/install/)を参照されたい。

## 最初の例

コード: [cvxpy_samples_basic.py](cvxpy_samples_basic.py)

まずは単純な例として、1変数の二次関数 $$ x^2 + 2x $$ の最小化を行う。

```py
import cvxpy as cp

x = cp.Variable(1) # 1: 変数の次元数
obj_function = x ** 2 + 2 * x
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()

print('Used solver:', problem.solver_stats.solver_name)
print('Optimal function value:', problem.value)
print('Optimal variable value:', x.value)
```

これを実行すると、

```
Used solver: OSQP
Optimal function value: -1.0
Optimal variable value: [-1.]
```

と表示される。すなわち、 $$ x=-1 $$ のときに最小値 $$ -1 $$ を取ることを示している。

最適化したい変数はベクトルや行列でもよい。2次元ベクトル $$ \mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix} $$ についての二次式 $$ \mathbf{x}^\top A \mathbf{x} + \mathbf{b}^\top \mathbf{x} $$ ($$ A = \begin{bmatrix}1 & 2 \\ 2 & 5\end{bmatrix} $$, $$ \mathbf{b} = \begin{bmatrix}-1 \\ 1\end{bmatrix} $$) を最小化してみよう。CVXPYの変数は、NumPyの変数などとも演算が可能なので、定数ベクトルや定数行列を使いたいときはこれで用意するとよい。

```py
import cvxpy as cp
import numpy as np

x = cp.Variable(2) # 2: 変数の次元数
a = np.array([[1, 2], [2, 5]])
b = np.array([-1, 1])

obj_function = cp.quad_form(x, a) + x @ b
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()

print('Used solver:', problem.solver_stats.solver_name)
print('Optimal function value:', problem.value)
print('Optimal variable value:', x.value)
```

これを実行すると、

```
Used solver: OSQP
Optimal function value: -2.500000000000001
Optimal variable value: [ 3.5 -1.5]
```

となり、$$ \mathbf{x} = \begin{bmatrix}3.5 \\ -1.5\end{bmatrix} $$ のとき最小値 $$ -2.5 $$ を取るとわかる。

## 注意点

ここで代わって、凸でない関数 $$ -x^2 + 2x $$ を最小化しようとすると

```py
import cvxpy as cp

x = cp.Variable(1) # 1: 変数の次元数
obj_function = -x ** 2 + 2 * x
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()
```

実行したとき

```
cvxpy.error.DCPError: Problem does not follow DCP rules. Specifically:
The objective is not DCP, even though each sub-expression is.
You are trying to minimize a function that is concave.
```

というエラーが表示される。これはDCP (Disciplined Convex Programming) rules、すなわち「このライブラリが凸であると判定できなかったため」解けなかったという意味である。

ところで、最初の凸である二次関数 $$ x^2 + 2x $$ の最小化であっても、`x ** 2` を `x * x` と書き換えたもの

```py
import cvxpy as cp

x = cp.Variable(1) # 1: 変数の次元数
obj_function = x * x + 2 * x
problem = cp.Problem(cp.Minimize(obj_function))
problem.solve()
```

を実行すると

```
cvxpy.error.DCPError: Problem does not follow DCP rules. Specifically:
The objective is not DCP. Its following subexpressions are not:
var1 @ var1
```

と、こちらでもDCP rulesに反していて計算できないというエラーになる。人が見て凸とわかるというだけではだめで、あくまでプログラム側が凸であると判定できるように書かないとならないのである。

Disciplined Convex Programming（日本語でいうと「規律凸計画法」という感じだろうか）というのは、与えられた式に一定のルールを適用することで、凸関数であるか判定したり、どのようなソルバーが使えるかを判定したりし最適化計算を行うものである。  
例えば「 $$ f $$ が線形関数、 $$ g $$ が凸関数ならば、 $$ g(f(\cdot)) $$ は凸関数」や「 $$ f $$ が凸関数、 $$ g $$ が凸関数かつ単調増加ならば、 $$ g(f(\cdot)) $$ は凸関数」といった条件が一般に成り立つので、それらを繰り返し適用し、式が凸関数であるか判定するのである。

## 定義済みの関数を利用する

上記の事情から、CVXPYでは「凹凸がわかっている関数」や「単調性がわかっている関数」が多数定義されており、該当する関数が存在する場合は極力それを使うようにしたい。

一覧は [Atomic Functions](https://www.cvxpy.org/tutorial/functions/index.html) にあるため参照のこと。

特に私がよく使う関数には以下のものがある。（`import cvxpy as cp`としているとする）

-   以下のものは、 $$ x $$ がベクトルであることを想定
    -   `cp.norm(x, p)`: $$ x $$ のノルム（$$ p $$ は正実数などオプションあり）。 $$ p $$ が1以上の実数なら、 $$ \lVert x\rVert_p = \sqrt[p]{\sum_{k=1}^m \lvert x_k\rvert^p} $$ と定義され、 $$ x $$ について凸
    -   `cp.sum(x)`: $$ x $$ の要素の和。 $$ x $$ について線形（凸かつ凹）
    -   `cp.sum_squares(x)`: $$ x $$ の要素の二乗和。 $$ x $$ について凸
    -   `cp.quad_form(x, P)`: 二次形式 $$ x^\top P x $$ 。 $$ P $$ が定数行列で半正定値なら、 $$ x $$ について凸
        -   `cp.quad_form(x, P, assume_PSD=True)`とすると、 $$ P $$ が半正定値であるかのチェックを行わず、強制的にそうみなす
-   以下のものは、 $$ x $$ がベクトル・行列なら要素ごとに適用
    -   `cp.entr(x)`: エントロピーの式 $$ - x \log x $$ （$$ x > 0 $$）。 $$ x $$ について凹
    -   `cp.logistic(x)`: ロジスティック回帰の損失関数の式 $$ \log(1 + e^x) $$ 。 $$ x $$ について凸
    -   `cp.pos(x)`: $$ \max\{x, 0\} $$ （負数は0に置き換え、正数はそのまま）。 $$ x $$ について凸

## 制約条件を入れる - 単純な例

コード: [cvxpy_samples_basic.py](cvxpy_samples_basic.py)

制約付きの最小化・最大化も（凸性の条件を満たしていれば）可能である。

先程の例では1変数の二次関数 $$ x^2 + 2x $$ の最小化を、制約を設けずに行ったが、
これに制約 $$ 1\leq x\leq 2 $$ を入れて解いてみる。
制約条件は、等式や不等式を書いたものをリストに並べ、それを `cp.Problem` の
作成時に指定すればよい。

```py
import cvxpy as cp

x = cp.Variable(1) # 1: 変数の次元数
obj_function = x ** 2 + 2 * x
constraints = [x >= 1, x <= 2]
problem = cp.Problem(cp.Minimize(obj_function), constraints)
problem.solve()
```

結果はこのようになり、 $$ x=1 $$ で最小値 $$ 3 $$ を取ると計算された。

```
Used solver: OSQP
Optimal function value: 3.0
Optimal variable value: [1.]
```

## 制約条件を入れる - 多変数の例

制約条件を入れるのは、ベクトル変数や行列変数でも同様に可能である。例として、以下の最小化問題を考える。

-   最小化したい関数：凸関数 $$ x_1^2 + x_2^2 $$
-   制約：凸領域 $$ (x_1 - 3)^2 + (x_2 - 4)^2 \leq 4 $$

図にすると以下のような状況となる。赤の背景色が凸関数の値、大きい青の丸が制約条件の領域、小さい緑の丸がその最小化を達成する点である。

![凸関数 x_1^2 + x_2^2 を、制約条件 (x_1 - 3)^2 + (x_2 - 4)^2 <= 4 のもとで最小化する。赤の背景色が凸関数の値、大きい青の丸が制約条件の領域、小さい緑の丸がその最小化を達成する点。](image_2dim_minimization.svg)

これはCVXPYでは以下の通り書ける。

```py
import cvxpy as cp

x = cp.Variable(2) # 2: 変数の次元数
c = np.array([3, 4])
obj_function = cp.sum_squares(x)
constraints = [cp.sum_squares(x - c) <= 4]
problem = cp.Problem(cp.Minimize(obj_function), constraints)
problem.solve()
```

結果は以下の通りで、`(x_1, x_2) = (1.8, 2.4)`のときに最小値9を取る。

```
Used solver: ECOS
Optimal function value: 8.999999904868837
Optimal variable value: [1.79999999 2.39999999]
```

## より複雑な問題を書いてみる

コード: [cvxpy_samples_lasso.py](cvxpy_samples_lasso.py)  
データ: [housing_scale](housing_scale)（[LIBSVM Data](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/regression.html#housing)より。動かす際はこちらもダウンロードが必要）

※このコードを動かす際は、[scikit-learn](https://scikit-learn.org/)のインストールも必要となる（pipやcondaでもインストールできる）

----

scikit-learnで定義されている[Lasso](https://scikit-learn.org/1.5/modules/generated/sklearn.linear_model.Lasso.html)の式に従って、CVXPYで最適化問題を書き、解いた結果がscikit-learnのものとほぼ一致することを確認するデモを用意している。

Lassoは線形回帰の一種で、訓練データの目的変数（予測したい変数） $$ y\in\mathbb{R}^n $$ 、訓練データの説明変数（予測に利用できる変数） $$ X\in\mathbb{R}^{n\times d} $$ 、ハイパーパラメータ $$ \alpha > 0 $$ が与えられたとき、予測係数 $$ w\in\mathbb{R}^d $$ を以下の式によって学習するものである。

 $$ \min_w \left(\frac{1}{2n} \lVert y - X w\rVert _2^2 + \alpha \lVert w\rVert _1\right) $$ 

ただし、 $$ t\in\mathbb{R}^m $$ と自然数 $$ p $$ に対して、 $$ \lVert t\rVert_p $$ は $$ p $$ -ノルム $$ \lVert t\rVert _p = \sqrt[p]{\sum_{k=1}^m \lvert t_k\rvert^p} $$ である。

この最小化したい式は以下のように書ける。ただし`@`は行列の積である。

`cp.sum_squares(y - x @ w) / (2 * n) + alpha * cp.norm(w, 1)`

コード全体については上記のリンクから参照されたい。
