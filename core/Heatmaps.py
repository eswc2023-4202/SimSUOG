#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame
import textwrap

measure='SUOG'
df = pd.read_csv('csv/sim_HPO_heatmap_2.csv', sep = ',', index_col = 0)

fig = plt.figure(num=None, figsize=(12, 12), dpi=80, facecolor='w', edgecolor='k')
cmap = sns.cubehelix_palette(light=1, as_cmap=True)
sns.set(font_scale=1.6)

res = sns.heatmap(df, annot=True, fmt='.2f', cmap=cmap, cbar_kws={"shrink": .87},
                  linewidths=0.1, linecolor='gray')

res.invert_yaxis()


# Split string xticks into multiple lines
max_width = 20
max_width2 = 30

res.set_xticklabels(textwrap.fill(x.get_text(), max_width2) for x in res.get_xticklabels())

res.set_xticklabels(res.get_xmajorticklabels(), fontsize = 18, rotation=30, ha="right", rotation_mode="anchor")

res.set_yticklabels(textwrap.fill(x.get_text(), max_width) for x in res.get_yticklabels())
res.set_yticklabels(res.get_ymajorticklabels(), fontsize = 18)


plt.title('Sim_SUOG')

#plt.show()

plt.savefig("Heatmap_SUOG_HPO.png")