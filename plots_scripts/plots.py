import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# Math Word Problems (GSM8k)
problems = ['davinci-003', 'davinci-003 + Prolog', 'GPT3.5', 'GPT3.5 + Prolog', 'GPT4', 'GPT4 + Prolog']

# Solve rate (%)
solve_rate = [61.3, 74.0, 57.1, 80.4, 92.0, 95.2]  # replace with actual values

# Bar colors
colors = ['#1f77c4', '#1f77c4', '#ff7f1e', '#ff7f1e', '#5ff04d', '#5ff04d']

darker_colors = ['#1f5a73', '#0f3e8a', '#b37f07', '#b33f0f', '#2fb926','#2f7055']

patterns = [ "" , "**" , "" , "**", "",  "**" ]

# Spacing between bars
spacing = [0, 1, 2.5, 3.5, 5, 6]

fig, ax = plt.subplots(figsize=(5, 3.5))

# Create solid bars
bars = ax.bar(spacing, solve_rate, color=colors, width=0.8)

# Create hatched bars
for i in range(len(bars)):
    bars[i].set_hatch(patterns[i])
    bars[i].set_edgecolor(darker_colors[i])

# Adding percentage above each bar
for i in range(len(problems)):
    ax.text(spacing[i], solve_rate[i] + 0.5, f'{solve_rate[i]}%', ha = 'center', fontsize=11)

ax.set_ylabel('Solve rate (%)')
ax.set_title('Solve rate (%) vs GSM8k dataset')

ax.set_xticks(spacing)  # set x-axis labels
ax.set_xticklabels(problems, ha='right', rotation=25)  # set x-axis labels to problem names
ax.set_ylim(0, 106)  # set y-axis limits

plt.tight_layout()
plt.show()

# Create proxy artists
proxy_artists = []
for i in range(len(problems)):
    proxy_artists.append(mpatches.Patch(facecolor=colors[i], edgecolor=darker_colors[i], hatch=patterns[i]))

# Create a legend in the new figure
legend = ax_legend.legend(proxy_artists, problems, title="Models", loc='center', ncol=6, prop={'size': 12})

# Hide the subplot in the new figure
ax_legend.axis('off')

plt.show()
