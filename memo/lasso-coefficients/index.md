---
layout: default
title: Different lasso coefficients for same data (同一のデータに対してlassoの解が複数生じうる問題)
---
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script"></script>

-   [Back to top page](../../)
-   [Back to other notes](../)

# Different lasso coefficients for same data (同一のデータに対してlassoの解が複数生じうる問題)

※大部分は英語でしか書いていません

## Problem (問題)

In lasso, or more generally L1-regularized empirical risk minimization, it is known that multiple set of model parameters can be optimal (presented as the result of analysis) for a fixed dataset.

Lasso、あるいは一般にL1正則化付き経験損失最小化においては、単一のデータセットに対し、最適になる（解析結果として提示される）モデルパラメータが複数存在しうることが知られている。

## What to read (読むもの)

-   R. J. Tibshirani, "The Lasso Problem and Uniqueness". [http://www.stat.cmu.edu/~ryantibs/papers/lassounique.pdf](http://www.stat.cmu.edu/~ryantibs/papers/lassounique.pdf)
    -   Consideration by the researcher who proposed lasso. The condition when the lasso solution becomes unique for a fixed dataset is discussed.<br>Lassoを提案した方による考察。単一の解が得られる条件を検討している。
-   Y. Pantazis, V. Lagani, P. Charonyktakis, I. Tsamardinos, "Multiple Equivalent Solutions for the Lasso". [https://arxiv.org/abs/1710.04995](https://arxiv.org/abs/1710.04995)
    -   Consideration of conditions for not only exactly optimal multiple solutions, but also approximately optimal solutions.<br>Only discussing lasso (L1-regularized linear regression), not for general L1-regularized empirical risk minimizations.<br>厳密に最適である解がそもそも複数存在する場合のみならず、最適に近い解が複数存在する場合についても考察している。<br>Lassoのみの検討で、一般のL1正則化付き経験損失最小化についての検討ではない。

## Problem settings (問題設定)

Consider a linear predictor $$(w, b)$$ ($$w\in\mathbb{R}^d$$: linear coefficients, $$b\in\mathbb{R}$$: intercept), that is, $$y \approx x^\top w + b$$ for a sample $$x\in\mathbb{R}^d$$ and its outcome $$y\in\mathbb{R}$$.

For an $$n$$-sample dataset consisting of input variables $$X\in\mathbb{R}^{n\times d}$$ and outcome variables $$Y\in\mathbb{R}^n$$, lasso estimates $$(w, b)$$ by

$$\mathrm{arg}\min_{w,b} \frac{1}{2} \|Y - (Xw + \mathbf{1})\|_2^2 + \lambda\|w\|_1,$$

or, equivalently,

$$\mathrm{arg}\min_{w,b} \frac{1}{2} \sum_{i=1}^n [Y_i - (X_{i:}w + b)]^2 + \lambda\|w\|_1,$$

where $$\mathbf{1}$$ (bold) is an $$n$$-dimensional vector of all ones, and $$X_{i:}$$ is the $$i$$th row of $$X$$ (i.e., $$i$$th sample of $$X$$).

We also consider replacing the "squared loss" with another loss. We write the formulation above as

$$\mathrm{arg}\min_{w,b} f_Y(w, b)$$
for
$$f_Y(w, b) := \sum_{i=1}^n \mathrm{loss}_{Y_i}(X_{i:}w + b) + \lambda\|w\|_1,$$

where $$\mathrm{loss}_y(t)$$ is any function that represents the fitness between $$y$$ and $$t$$. This framework is called the (linear) *L1-regularized empirical risk minimization*. A famous example is $$\mathrm{loss}_y(t) = \log(1 + \exp(-yt))$$ ($$y = -1, +1$$), which is for the *logistic regression*. We assume that $$\mathrm{loss}_y(t)$$ is convex w.r.t. $$t$$, at that time $$f_Y(w, b)$$ is also convex w.r.t. $$w$$.

## Example (例)

A typical case when multiple optimal solutions are found is the matrix rank of $$X$$ is less than $$d$$.

Here we especially suppose that $$X$$ has two equivalent columns (i.e., two of features in $$X$$ are the same); $$X_{:j} = X_{:k}$$ ($$1 \leq j, k \leq d$$).

複数の解が見つかる典型的な例としては、Xの行列の階数がd以下である場合である。

特にここでは、Xが二つの同一な行を持つ（つまり、Xの特徴のうち二つは同じである）場合を考える。

Suppose that $$(w^*, b^*)$$ is a lasso solution, and define $$w^* = [w^*_1, w^*_2, \ldots, w^*_d]$$.
Then, 
$$(w^{*(j,k,h)}, b^*)$$
($$w*(j,k,h) := [w^*_1, w^*_2, ..., h w^*_j + (1-h) w^*_k, ..., (1-h) w^*_j + h w^*_k, ..., w^*_d]$$)
is also a lasso solution as long as all of the below holds:

-   $$0 \leq h \leq 1,$$
    <sup>(*1)</sup>  
-   the signs of $$w_j$$ and $$h w^*_j + (1-h) w^*_k$$ are the same, and
-   the signs of $$w_j$$ and $$(1-h) w^*_j + h w^*_k$$ are the same.

(*1): For lasso for squared loss ($$\mathrm{loss}_y(t) = [y - (x^\top w + b)]^2$$), $$h$$ may be any real number.

### Sketch of the proof

Because $$X_{:j} = X_{:k}$$, it is obvious that $$w^{**} := [w^*_1, w^*_2, ..., w^*_k, ..., w^*_j, ..., w^*_d]$$ ($$w^*_j$$ and $$w^*_k$$ are swapped) is also an optimal lasso solution.

Then let us exploit the property of convex functions.

-   Since $$f_Y(w, b)$$ is convex w.r.t. $$w$$, $$f_Y(h w^* + (1-h)w^{**}, b^*) \leq h f_Y(w^*, b^*) + (1-h) f_Y(w^{**}, b^*)$$ must hold.
-   Since we assume $$f_Y(w^*, b^*)$$ and $$f_Y(w^{**}, b^*)$$ are both optimal (at minimum), $$f_Y(w, b^*)\geq f_Y(w^*, b^*) = f_Y(w^{**}, b^*)$$ must hold for any $$w$$.
    Moreover, $$h f_Y(w^*, b^*) + (1-h) f_Y(w^{**}, b^*) = h f_Y(w^*, b^*) + (1-h) f_Y(w^*, b^*) = f_Y(w^*, b^*)$$.
-   Combining them, the first inequality can be replaced with the equality, that is, $$f_Y(h w^* + (1-h)w^{**}, b^*) = h f_Y(w^*, b^*) + (1-h) f_Y(w^{**}, b^*)$$.

## Viewpoints from Fenchel duality (フェンシェル双対からの観点)

In case we take the dual problem by Fenchel's duality theorem, the optimum becomes unique even for the example above ($$X$$ has two equivalent columns). In fact, the dual problem is a minimization of convex quadratic function in a convex set.

### Fenchel's duality theorem

For a convex function $$f: \mathbb{R}^d\to\mathbb{R}$$, its *convex conjugate* $$f^*: \mathbb{R}^d\to\mathbb{R}\cup\{+\infty\}$$ is defined as follows:

$$f^*(t) := \sup_{s\in\mathbb{R}^d} \{ t^\top s - f(s) \}.$$

Then, given two convex functions $$L: \mathbb{R}^n\to\mathbb{R}$$,  $$R: \mathbb{R}^d\to\mathbb{R}$$ and a matrix $$X\in\mathbb{R}^{n\times d}$$, consider the following functions $$P:\mathbb{R}^d\to\mathbb{R}$$ and $$D:\mathbb{R}^n\to\mathbb{R}$$:

$$P(t) := L(Xt) + R(t),$$  
$$D(u) := -L^*(-u) - R^*(X^\top u).$$

Here, Fenchel's duality theorem states that the following relationship holds under certain regularity conditions (See, for example, "Convex analysis" R. T. Rockafellar, Princeton university press, 1970):

$$\min_{t\in\mathbb{R}^d} P(t) = \max_{u\in\mathbb{R}^n} D(u).$$

Moreover, defining the optima as $$t^* := \mathrm{arg}\min_{t\in\mathbb{R}^d} P(t)$$ and $$u^* := \mathrm{arg}\max_{u\in\mathbb{R}^n} D(u)$$, the followings hold:

$$X^\top u^* \in \partial R(t^*),$$  
$$-u^* \in \partial L(X t^*),$$  

where $$\partial$$ denotes the subderivative.

### Fenchel's duality theorem for Lasso

Let us apply the theorem to the problem stated before:

$$f_Y(w, b) := \sum_{i=1}^n \mathrm{loss}_{Y_i}(X_{i:}w + b) + \lambda\|w\|_1.$$

First, let $$t := [w^\top \mid b]^\top \in \mathbb{R}^{d+1}$$ and $$\bar{X} := [X \mid \mathbf{1}] \in \mathbb{R}^{n\times(d+1)}$$. Then, we have only to define $$L\in\mathbb{R}^n$$ and $$R\in\mathbb{R}^{d+1}$$ as follows:

$$L(u) := \sum_{i=1}^n \mathrm{loss}_{Y_i}(u_i),$$  
$$R(t) := \lambda\sum_{j=1}^d |t_j|.$$

Their convex conjugates are calculated as follows:

$$L^*(u) = \sup_{u^\prime\in\mathbb{R}^n} \Bigl[ u^\top u^\prime - \sum_{i=1}^n \mathrm{loss}_{Y_i}(u^\prime_i) \Bigr] = \sup_{u^\prime\in\mathbb{R}^n} \Bigl[ \sum_{i=1}^n u_i u^\prime_i - \mathrm{loss}_{Y_i}(u^\prime_i) \Bigr]$$  
$$\therefore L^*(u) = \sum_{i=1}^n \mathrm{loss}^*_{Y_i}(u_i)$$  
$$R^*(t) = \sup_{t^\prime\in\mathbb{R}^{d+1}} \Bigl[ t^\top t^\prime - \lambda\sum_{j=1}^d |t^\prime_j| \Bigr] = \sup_{t^\prime\in\mathbb{R}^{d+1}} \Bigl[ t_{d+1} t^\prime_{d+1} + \sum_{j=1}^d (t_j t^\prime_j - \lambda|t^\prime_j|) \Bigr]$$  
$$\therefore R^*(t) = \begin{cases} 0 & (t_{d+1} = 0 ~\text{and}~\forall j\in\{1, 2, \ldots, d\}: |t_j|\leq\lambda) \\ +\infty & (\text{otherwise}) \end{cases}$$

Thus we have

$$f_Y(w, b) := P(t) = L(\bar{X}t) + R(t),$$  
$$D(u) := -L^*(-u) - R^*(\bar{X}^\top u).$$

Note that, since $$u$$ that makes $$R^*(\bar{X}^\top u)$$ infinite must be removed from the optimization. So, in the viewpoint of the optimization, $$D(u)$$ can be rewritten as follows:

$$D(u) = -L^*(-u)~\text{subject to}~\mathbf{1}^\top u = 0~\text{and}~\forall j\in\{1, 2, \ldots, d\}: |\bar{X}_{:j}^\top u|\leq\lambda.$$

The optimality conditions are written as follows:

$$\forall j\in\{1, 2, \ldots, d\}:~~~~\bar{X}_{:j}^\top u^* \begin{cases} = -\lambda & (t^*_j < 0), \\ = \lambda & (t^*_j > 0), \\ \in [-\lambda, \lambda] & (t^*_j = 0)\end{cases}$$  
$$\forall i\in\{1, 2, \ldots, n\}:~~~~-u^*_i \in \partial \mathrm{loss}_{Y_i}(\bar{X}_{i:}t^*),$$  

### If the loss function is differentiable and strictly convex (損失関数が微分可能かつ真に凸である場合)

Suppose that $$\mathrm{loss}_{Y_i}$$ is strictly convex.
Then, $$D(u) = -L^*(-u)$$ is also strictly convex and therefore its minimum must be unique.
So, even if $$t^*$$ (the minimizer for $$P(t)$$) is not unique, $$u^*$$ (the maximizer for $$D(u)$$) must be unique.

Moreover, if $$\mathrm{loss}_{Y_i}$$ is differentiable, $$\partial\mathrm{loss}_{Y_i}$$ must be increasing and single-valued. (Since we consider the subderivative $$\partial$$, it may be multi-valued if not differentiable.) As a result, the inverse function of $$\partial \mathrm{loss}_{Y_i}$$ can be defined and therefore we have

$$\bar{X}_{i:}t^* = [\partial \mathrm{loss}_{Y_i}]^{-1}(-u^*_i).$$

Since we found that $$u^*$$ must be unique, $$\bar{X}_{i:}t^*$$ must be unique for all $$i$$.

Conversely, for multiple $$t^*$$'s such that $$\bar{X}_{i:}t^*$$ is fixed for all $$i$$,
$$D(u^*)$$
(and also $$P(t^*)$$) must be unique.

In summary, if $$\mathrm{loss}_{Y_i}$$ is differentiable and strictly convex, then multiple $$t^*$$'s can be the minimizers for $$P(t)$$ such that
$$\bar{X}_{i:}t^*$$
is identical for all $$i$$.

## [To Be Added] If the loss function is not necessarily differentiable or strictly convex (損失関数が微分可能かつ真に凸とは限らない場合)

(To be added)
