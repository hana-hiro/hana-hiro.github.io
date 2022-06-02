import numpy as np
import matplotlib.pyplot as plt

APPROX_RANGE_X = (0, 1)
DRAW_RANGE_X = (-1, 2)
DRAW_RANGE_Y = (0, 3)

x = np.linspace(DRAW_RANGE_X[0], DRAW_RANGE_X[1], 1000)
y = 1 / (1+x)

# Degree 3
y_approx = {
    # In sollya: remez(1/(1+x), 3, [APPROX_RANGE_X[0];APPROX_RANGE_X[1]]);
    3: (0.99873734200703370255650542617590628500070645822909 + x *
        (-0.95079348766754853145575955686649968095374245776007 + x *
         (0.6862914918332974716537832986049998194156383639214 + x *
          (-0.23549800416574894019802374173850013846189590616134)))),
    # In sollya: remez(1/(1+x), 4, [APPROX_RANGE_X[0];APPROX_RANGE_X[1]]);
    4: (0.99978336205666073932449132488871571809338894249251 + x *
        (-0.9872990769195582144432969724273695104121489380699 + x *
         (0.87791823506740268929364876843023904083643614405478 + x *
          (-0.55180616654142593405599781593693816998179579921571 + x *
           0.16162028428025998055666337015663720337073070824582)))),
}

for d, ya in y_approx.items():
    plt.figure(figsize=(3.6, 2.7))
    plt.plot(x, y, lw=3, label="1/(1+x)")
    plt.plot(x, ya, lw=3, label="Approximated")
    for xa in APPROX_RANGE_X:
        plt.plot((xa, xa), DRAW_RANGE_Y, c="gray", ls=":", lw=3)
    plt.title(f"Approximated by polynomial of degree {d}")
    plt.legend()
    plt.xlim(DRAW_RANGE_X)
    plt.ylim(DRAW_RANGE_Y)
    plt.savefig(f"sollya-degree{d}.png")
