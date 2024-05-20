"""import matplotlib.pyplot as plt
import numpy as np

def create_bar_plot(x, y, z):
    # Create the x-axis labels
    x_labels = list(range(1, x+1)) + list(range(1, y+1)) + list(range(1, z+1))

    # Create the y-axis values
    y_values = np.random.rand(len(x_labels)) * 100  # Random accuracy values

    # Create the colors for each group
    colors = ['b'] * x + ['g'] * y + ['r'] * z

    # Create the bar plot with separation
    plt.figure(figsize=(15, 5))
    bar_width = 0.8
    for i in range(len(x_labels)):
        plt.bar(i+1, y_values[i], color=colors[i], width=bar_width)

    # Remove space between bars and bounds of the plot
    plt.xlim(0.5, len(x_labels) + 0.5)

    # Create the legend
    legend_labels = ['Math word problems with variable entanglement', 'Constraint satisfaction', 'Algorithmic instructions']
    plt.figure(figsize=(15, 1))
    for i in range(3):
        plt.bar(0, 0, color=colors[0 if i==0 else x if i==1 else x+y], label=legend_labels[i])
    plt.legend(ncol=3)
    plt.axis('off')

    # Set the x and y labels for the bar plot
    plt.figure(1)
    plt.xlabel('Problems')
    plt.ylabel('Accuracy of model in 25 tries (%)')
    plt.xticks(np.arange(1, len(x_labels)+1), x_labels)

    # Show the plots
    plt.show()


# Test the function
create_bar_plot(15, 13, 12)"""


import matplotlib.pyplot as plt
import numpy as np

def create_bar_plot(x=16, y=12, z=12):
    # Create the x-axis labels
    x_labels = ['MWP_'+str(i) for i in range(1, x+1)] + ['CS_'+str(i) for i in range(1, y+1)] + ['AI_'+str(i) for i in range(1, z+1)]

    # Create the y-axis values
    mwp_accuracy_25 = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 96, 100, 100, 100, 100]
    mwp_multiple_try = [1, 1, 1, 1, 12.32, 1, 1.32, 1.64, 1, 1, 1, 1, 1, 1, 1, 1.24]
    constraint_accuracy_25 = [100, 100, 100, 100, 100, 96, 100, 48, 100, 100, 100, 100]
    constraint_multiple_try = [1.24, 1, 1.04, 1.44, 1, 1.24, 1, 13, 1, 14.76, 1, 4.12]
    algo_accuracy_25 = [52, 36, 96, 100, 100, 4, 0, 64, 48, 52, 4, 12]
    algo_multiple_try = [1.44, 3.32, 1.52, 1, 1.2, 5.92, 2.32, 2.28, 1.84, 2.2, 20.4, 20.8]
    y_values = mwp_accuracy_25 + constraint_accuracy_25 + algo_accuracy_25
    #y_values = mwp_multiple_try + constraint_multiple_try + algo_multiple_try

    # Create the colors for each group
    colors = ['b'] * x + ['g'] * y + ['r'] * z

    # Create the bar plot with separation
    plt.figure(figsize=(14, 4.3))
    bar_width = 0.8
    for i in range(len(x_labels)):
        plt.bar(i+1, y_values[i], color=colors[i], width=bar_width)
        plt.text(i+1, y_values[i], round(y_values[i], 2), ha = 'center', va = 'bottom', fontsize=8)  # Add y-value on top of each bar

    # Remove space between bars and bounds of the plot
    plt.xlim(0.5, len(x_labels) + 0.5)
    plt.ylim(0, 105)  # Set the bounds for the y-axis

    # Set the x and y labels for the bar plot
    plt.figure(1)
    plt.ylabel('Accuracy (%) in 25 Inferences')#'Count of Inference Made by MTA per Problem')#'Accuracy (%) in 25 Inferences')
    plt.xticks(np.arange(1, len(x_labels)+1), x_labels, rotation=45, fontsize=8, ha='right', va='top')  # Change rotation and fontsize here

    # Show the plots
    plt.show()


# Test the function
create_bar_plot()