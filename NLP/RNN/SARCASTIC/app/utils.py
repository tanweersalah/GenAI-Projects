
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def convert_range(value):
    if value < 0 or value > 1:
        raise ValueError("Input value must be in the range [0, 1].")
    
    return value * 2 - 1

def create_bidirectional_bar(value):
    value = convert_range(value)
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Set the range and ticks
    ax.set_xlim(-1, 1)
    ax.set_xticks(np.arange(-1, 1.1, 0.25))
    
    # Remove y-axis
    ax.yaxis.set_visible(False)
    
    # Add vertical line at 0
    ax.axvline(x=0, color='#333333', linestyle='-', linewidth=1)
    
    # Create custom colormap
    colors = ['#FF0000', '#808080', '#00FF00']  # Red, Grey, Green
    n_bins = 100  # Number of color segments
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
    
    # Create the gradient bar
    if value >= 0:
        gradient = np.linspace(0, value, int(n_bins * value))
        for i in range(len(gradient)-1):
            ax.barh(0, gradient[i+1]-gradient[i], left=gradient[i], height=0.6, 
                    align='center', color=cmap(0.5 + (i+0.5)/(len(gradient)*2)), alpha=0.8)
    else:
        gradient = np.linspace(value, 0, int(n_bins * abs(value)))
        for i in range(len(gradient)-1):
            ax.barh(0, gradient[i+1]-gradient[i], left=gradient[i], height=0.6, 
                    align='center', color=cmap(0.5 - (len(gradient)-i-0.5)/(len(gradient)*2)), alpha=0.8)
    
    # Add value label
    ax.text(value, 0, f'{value:.2f}', 
            verticalalignment='center',
            horizontalalignment='left' if value >= 0 else 'right',
            fontweight='bold', fontsize=12, color='#333333')
    
    # Customize the chart appearance
    ax.set_facecolor('#f0f2f6')
    fig.patch.set_facecolor('#f0f2f6')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#333333')
    ax.tick_params(axis='x', colors='#333333')
    
    plt.title('Sentiment Bar Chart', fontsize=16, fontweight='bold', color='#333333')
    plt.tight_layout()
    return fig