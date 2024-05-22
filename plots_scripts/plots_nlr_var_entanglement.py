

import matplotlib.pyplot as plt
import numpy as np

# Math Word Problems (GSM8k)
problems = ['GPT4', 'GPT4 + Prolog', 'GPT4', 'GPT4 + Prolog', 'GPT4', 'GPT4 + Prolog', 'GPT4', 'GPT4 + Prolog']
ve = ["1 Entangled\nVariable", "2 Entangled\nVariables", "3 Entangled\nVariables", "4 Entangled\nVariables"]
# Solve rate (%)
solve_rate = [100, 100, 60, 100, 60, 100, 0, 100]#[60, 100, 20, 80, 20, 100, 0, 80]

# Bar colors
colors = ['#5ff04d', '#5ff04d', '#5ff04d', '#5ff04d', '#5ff04d', '#5ff04d', '#5ff04d', '#5ff04d']

darker_colors = [ '#2fb926','#2f7055',  '#2fb926','#2f7055',  '#2fb926','#2f7055',  '#2fb926','#2f7055']

patterns = [ "" , "**" , "" , "**", "",  "**", "",  "**" ]

# Spacing between bars
spacing = [0, 0.75, 2, 2.75, 4, 4.75, 6, 6.75]
x = [0, 2, 4, 6]
fig, ax = plt.subplots(figsize=(6, 3.5))

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
ax.set_title('Math Word Problems with Varying Variable Entanglement')

ax.set_xticks(spacing)  # set x-axis labels
ax.set_xticklabels(problems, ha='right', rotation=25,  fontsize=9)  # set x-axis labels to problem names
# Add text annotations for the category labels
for i, category in enumerate(ve):
    ax.text(x[i] + 0.25 , -40, category, ha='center', va='top', fontsize=10)
ax.set_ylim(0, 110)  # set y-axis limits

plt.tight_layout()
plt.show()