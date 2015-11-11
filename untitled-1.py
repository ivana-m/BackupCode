import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.add_patch(
    patches.Rectangle(
        (0.1, 0.1), 0.5, 0.5,
    )
)

ax.add_patch(
    patches.Rectangle(
        (0.1, 0.4), 0.1, 0.3,
    )
)

fig.savefig('rect1.png', dpi=90, bbox_inches='tight')