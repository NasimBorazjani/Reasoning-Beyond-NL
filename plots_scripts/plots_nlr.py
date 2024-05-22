

import matplotlib.pyplot as plt
import numpy as np

# Math Word Problems (GSM8k)
problems = [ 'GPT3.5', 'GPT3.5 + Prolog', 'GPT4', 'GPT4 + Prolog']

# Solve rate (%)
solve_rate = [0, 50, 8.3, 100]#[0, 16.7, 8.3, 66.7]#[0, 50, 12.5, 100]#[0, 41.7, 16.7, 100]#[0, 16.7, 0, 66.7]  # replace with actual values

# Bar colors
colors = [ '#ff7f1e', '#ff7f1e', '#5ff04d', '#5ff04d']

darker_colors = [ '#b37f07', '#b33f0f', '#2fb926','#2f7055']

patterns = [ "" , "**" , "" , "**", "",  "**" ]

# Spacing between bars
spacing = [0, 0.75, 1.75, 2.5]

fig, ax = plt.subplots(figsize=(4, 3))

# Create solid bars
bars = ax.bar(spacing, solve_rate, color=colors, width=0.6, bottom=0.8)

# Create hatched bars
for i in range(len(bars)):
    bars[i].set_hatch(patterns[i])
    bars[i].set_edgecolor(darker_colors[i])

# Adding percentage above each bar
for i in range(len(problems)):
    ax.text(spacing[i], solve_rate[i] + 1.1, f'{solve_rate[i]}%', ha = 'center', fontsize=12)

ax.set_ylabel('Solve rate (%)')
ax.set_title('Solve rate (%) vs Constraint Satisfaction')

ax.set_xticks(spacing)  # set x-axis labels
ax.set_xticklabels(problems, ha='right', rotation=25)  # set x-axis labels to problem names
ax.set_ylim(0, 109)  # set y-axis limits

plt.tight_layout()
plt.show()