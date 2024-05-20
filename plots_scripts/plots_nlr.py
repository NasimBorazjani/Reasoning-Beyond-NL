"""import matplotlib.pyplot as plt
import numpy as np

# Math Word Problems (GSM8k)
problems = [ 'GPT3.5', 'GPT3.5 + Prolog', 'GPT4', 'GPT4 + Prolog']

# Solve rate (%)
solve_rate = [0, 16.7, 0, 66.7]  # replace with actual values

# Bar colors
colors = [ '#ff7f1e', '#ff7f1e', '#5ff04d', '#5ff04d']

darker_colors = [ '#b37f07', '#b33f0f', '#2fb926','#2f7055']

patterns = [ "" , ".." , "" , "..", "",  ".." ]


# Spacing between bars
spacing = [0, 1, 3, 4]

fig, ax = plt.subplots(figsize=(6, 4))

# Create solid bars
bars = ax.bar(spacing, solve_rate, color=colors, width=0.8, bottom=0.8)

# Create hatched bars
for i in range(len(bars)):
    bars[i].set_hatch(patterns[i])
    bars[i].set_edgecolor(darker_colors[i])

# Adding percentage above each bar
for i in range(len(problems)):
    ax.text(spacing[i], solve_rate[i] + 1, f'{solve_rate[i]}%', ha = 'center', fontsize=11.5)

ax.set_xlabel('Algorithmic Instructions')
ax.set_ylabel('Solve rate (%)')
ax.set_title('Solve rate (%) vs Algorithmic Instructions')

ax.set_xticks([])  # remove x-axis labels
ax.set_ylim(0, 107)  # set y-axis limits

plt.tight_layout()
plt.show()

# Create a separate figure for the legend
fig_legend = plt.figure(figsize=(12, 2))
ax_legend = fig_legend.add_subplot(111)

# Create a legend in the new figure
legend = ax_legend.legend(bars, problems, title="Models", loc='center', ncol=3, prop={'size': 12})

# Hide the subplot in the new figure
ax_legend.axis('off')

plt.show()"""

"""import matplotlib.pyplot as plt
import numpy as np

# Math Word Problems (GSM8k)
problems = [ 'GPT3.5', 'GPT3.5 + Prolog', 'GPT4', 'GPT4 + Prolog']

# Solve rate (%)
solve_rate = [0, 16.7, 0, 66.7]  # replace with actual values

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
    ax.text(spacing[i], solve_rate[i] + 1, f'{solve_rate[i]}%', ha = 'center', fontsize=12)

#ax.set_xlabel('MWPs with VE')
ax.set_ylabel('Solve rate (%)')
ax.set_title('Solve rate (%) vs Algorithmic Instructions')

ax.set_xticks([])  # remove x-axis labels
ax.set_ylim(0, 108)  # set y-axis limits

plt.tight_layout()
plt.show()

# Create a separate figure for the legend
fig_legend = plt.figure(figsize=(8, 1))
ax_legend = fig_legend.add_subplot(111)

# Create a legend in the new figure
legend = ax_legend.legend(bars, problems, title="Models", loc='center', ncol=4, prop={'size': 10})

# Hide the subplot in the new figure
ax_legend.axis('off')

plt.show()"""

import matplotlib.pyplot as plt
import numpy as np

# Math Word Problems (GSM8k)
problems = [ 'GPT3.5', 'GPT3.5 + Prolog', 'GPT4', 'GPT4 + Prolog']

# Solve rate (%)
solve_rate = [0, 41.7, 0, 100]#[0, 16.7, 0, 66.7]  # replace with actual values

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