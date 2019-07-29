import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({'x': range(1,11), 'y1': range(11,21), 'y2': range(21,31), 'y3': range(1,11)})

plt.plot('x', 'y1', data=df, marker='o', linewidth=2)
plt.plot('x', 'y2', data=df, marker='o', linewidth=4)
plt.plot('x', 'y3', data=df, marker='o', linewidth=6)
plt.legend()