#
#  Copyright (c) 2022 - The .... Project.
#  @Author: ...
#


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

measure='suog'
df = pd.read_csv('csv/sim_ic_distribution.csv')
print(df)

# Draw the density plot
sns.distplot(df, hist=False, kde=True,
                 kde_kws={'linewidth': 3})

# Plot formatting
plt.title('Distribution of similarity using Sim_IC')
plt.xlabel('Similarity')
plt.ylabel('Density')
plt.savefig("Density_IC.png")