# -*- coding: utf-8 -*-
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable
import numpy as np
import matplotlib.pyplot as plt
plt.rcdefaults()


def autolabel(rects, ax):  # label with rect size
    for rect in rects:
        ax.text(rect.get_width(),
                1.0*rect.get_y() + rect.get_height()/2.0,
                '%d' % int(np.power(10, rect.get_width())),
                ha='left', va='center', fontsize=7)


def autolabel_arbitrary_value(rects, ax, vals):  # label with provided values
    for (rect, val) in zip(rects, vals):
        ax.text((val + 1) * 0.01,
                1.0 * rect.get_y() + rect.get_height() / 2.0,
                '%d' % val + "%",
                ha='left', va='center', fontsize=7)


def draw_count(c, title, fig_name, out_path):
    categories = c.keys()
    freq = [max(np.log10(max(c[cat], 0.1)), 0) for cat in categories]

    if all([isinstance(cat, str) for cat in categories]) or all([isinstance(cat, tuple) for cat in categories]):
        categories_rev = [cat[::-1] for cat in categories]
        categories_rev = [x for _, x in sorted(zip(freq, categories_rev))]
        freq = sorted(freq)
    else:  # Integers, sort by value
        categories_rev = [cat for cat in categories]
        freq = [x for _, x in sorted(zip(categories_rev, freq))]
        categories_rev = sorted(categories_rev)

    xticks = np.arange(int(max(freq))+1)
    xtick_labels = [np.power(10, t) for t in xticks]

    fig, ax = plt.subplots(figsize=(20, 10))
    y_pos = np.arange(len(categories))
    rects = ax.barh(y_pos, freq, align='center', color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories_rev)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlabel('מספר מופעים'[::-1])
    ax.set_title(title)
    make_axes_area_auto_adjustable(ax)
    autolabel(rects, ax)
    plt.savefig(out_path + '/' + fig_name + '.pdf')
    plt.close()


def draw_double_count(c_c, title, fig_name, out_path):
    n_bins = int(np.floor(np.log2(max(c_c.keys()))))
    categories = ['1'] + \
                 [str(int(np.power(2, i + 1))) + '-' + str(int(np.power(2, i + 2)) - 1) for i in range(n_bins - 2)] + \
                 [str(int(np.power(2, n_bins - 1))) + '+']
    # For example categories may be ['1', '2-3', '4-7', '8-15', '16-31', '32-63', '64-127', '128+']
    y_pos = np.arange(len(categories))

    freq = np.zeros(n_bins)
    for n in c_c.keys():
        b = min(n_bins - 1, int(np.log2(n)))
        freq[b] += c_c[n]
    freq = [max(np.log10(max(f, 0.1)), 0) for f in freq]
    xticks = np.arange(int(max(freq)) + 1)
    xtick_labels = [np.power(10, t) for t in xticks]

    fig, ax = plt.subplots(figsize=(20, 10))
    rects = ax.barh(y_pos, freq, align='center', color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlabel('מספר מופעים'[::-1])
    ax.set_title(title)
    make_axes_area_auto_adjustable(ax)
    autolabel(rects, ax)
    plt.savefig(out_path + '/' + fig_name + '.pdf')
    plt.close()


# TODO: Create a load units (to be used both in simple counters and in simple durations base)
