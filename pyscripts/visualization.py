import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.collections import LineCollection
from .genomeutil import get_intervaltree

class ColorUniversalDesign():
    # Okabe & Ito's color palette
    # Color Universal Design (CUD) - How to make figures and presentations that are friendly to Colorblind people -
    # https://jfly.uni-koeln.de/color/
    OkabeIto_cmap = colors.ListedColormap('#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000'.split())
    OkabeIto_cpal = sns.color_palette('#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000'.split())
    
class SyntenyViewer():
    def __init__(self, rec):
        self.__rec = rec
        self.__intervals = get_intervaltree(self.__rec)
    
    def show(self, start, end, y_func=None, label_func=None, label_kwargs=None, collection_kwargs=None, feature_filter=None, ax=None):
        # Handle default args
        y_func = y_func or (lambda _: 0)
        label_kwargs = label_kwargs or {}
        collection_kwargs = collection_kwargs or {}    
        feature_filter = feature_filter or (lambda _: True)
        
        ax = ax or plt.gca()
        
        # Draw features as segments
        ax.add_collection(LineCollection([
            [(start, y_func(feature)), (end, y_func(feature))]
            for start, end, feature in self.__intervals[start:end]
            if feature_filter(feature)
        ], **collection_kwargs))
        
        # Add text information
        if label_func is not None:
            for s, e, data in self.__intervals[start:end]:
                if feature_filter(data):
                    ax.text(
                        s if data.strand>0 else e, y_func(data), label_func(data), 
                        ha='left' if data.strand>0 else 'right', va='center', **label_kwargs
                    )
        
        ax.autoscale()
        ax.set_xlim(start, end)
        ax.set_xlabel('genomic position (bp)')
        return ax