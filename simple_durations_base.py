# -*- coding: utf-8 -*-
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable
from collections import Counter
from utils import *
import draw_utils
import numpy as np
import matplotlib.pyplot as plt
plt.rcdefaults()


# "Globals"
def my_exp(x):
    return 0 if x == 0 else np.power(10, x)


max_weeks = 56
n_weeks = int(max_weeks / 2)
n_days_per_bin = int(7 * max_weeks/n_weeks)


def draw_durations_dist(vals, ax, label, col):
    c = Counter(vals)

    freq = np.zeros(n_weeks)
    for n in c.keys():
        bin_ind = min(int(max(n, 0) / n_days_per_bin), n_weeks - 1)
        freq[bin_ind] += c[n]
    freq = [np.log10(max(f, 1)) for f in freq]

    y_pos = np.arange(n_weeks)
    rects = ax.barh(y_pos, freq, align='center', color=col, ecolor='black', alpha=0.5, label=label[::-1])
    return freq, rects


def draw_reference_dist(vals, ax, title):
    label = 'כל התיקים'
    col = 'green'
    freq, rects = draw_durations_dist(vals, ax, label, col)

    y_pos = np.arange(n_weeks)
    categories = [7 * (i + 1) for i in range(n_weeks)]
    ax.set_yticks(y_pos)
    ax.set_yticklabels([str(int(2 * c / 7)) + 'w' for c in categories])

    xticks = np.arange(int(max(freq)) + 1)
    xtick_labels = [np.power(10, t) for t in xticks]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)

    ax.set_xlabel('מספר תיקים פשוטים לפי משך'[::-1])
    ax.set_ylabel('משך'[::-1])
    ax.set_title(title[::-1])
    make_axes_area_auto_adjustable(ax)
    draw_utils.autolabel(rects, ax)
    return freq


def draw_front_dist(vals, ax, label, freq):
    col = 'red'
    freq_front, rects_front = draw_durations_dist(vals, ax, label, col)
    ratio_front = [int(100 * my_exp(f_front) / my_exp(f)) for (f_front, f) in zip(freq_front, freq)]
    draw_utils.autolabel_arbitrary_value(rects_front, ax, ratio_front)


# Duration availability mask
mask_request_and_closing_dates_available = np.array(pd.notna(df[eng_to_heb('request_date')]) &
                                                    pd.notna(df[eng_to_heb('closing_date')]))
df_with_duration = df[mask_request_and_closing_dates_available].copy()
durations = (df_with_duration[eng_to_heb('closing_date')] - df_with_duration[eng_to_heb('request_date')]).dt.days
df_with_duration['duration'] = durations


# Get common cases masks
mask_request_type_will = np.array(df_with_duration[eng_to_heb('request_type')] == 'לצו קיום צוואה')
mask_request_type_inherit = np.array(df_with_duration[eng_to_heb('request_type')] == 'לצו ירושה')

mask_closing_reason_warrent_granted = np.array(df_with_duration[eng_to_heb('closing_reason')] == 'ניתן צו')
mask_closing_reason_pass_to_court = np.array(df_with_duration[eng_to_heb('closing_reason')] == 'העברה לבימש')

mask_warrent_granted_combo = (mask_request_type_will | mask_request_type_inherit) & mask_closing_reason_warrent_granted

mask_pass_to_court_combo = (mask_request_type_will | mask_request_type_inherit) & mask_closing_reason_pass_to_court

mask_common = mask_warrent_granted_combo | mask_pass_to_court_combo

df_warrent_granted = df_with_duration[mask_warrent_granted_combo]
df_pass_to_court = df_with_duration[mask_pass_to_court_combo]
df_common = df_with_duration[mask_common]
durations_common = df_common['duration']


# Get "simple" mask
attorney_general_responses_lists = [[] if pd.isna(lst) else lst[1:-1].split(',')
                                    for lst in df_warrent_granted[eng_to_heb('attorney_general_responses')]]
mask_attorney_general_response_no_interest = [len(lst) == 2 and lst[0] == 'אין עניין'
                                              for lst in attorney_general_responses_lists]

decisions_lists = [[] if pd.isna(lst) else lst[1:-1].split(',') for lst in df_warrent_granted[eng_to_heb('decisions')]]
mask_decision_to_give_warrent = [len(lst) == 2 and lst[0] == 'מתן צו' for lst in decisions_lists]

mask_attorney_general_response_no_interest = np.array(mask_attorney_general_response_no_interest)
mask_decision_to_give_warrent = np.array(mask_decision_to_give_warrent)

mask_request_status_completed = np.array(df_warrent_granted[eng_to_heb('request_status')] == 'הטיפול בבקשה הסתיים')

mask_simple = mask_attorney_general_response_no_interest & \
              mask_decision_to_give_warrent & \
              mask_request_status_completed

df_simple = df_warrent_granted[mask_simple]
durations_simple = (df_simple[eng_to_heb('closing_date')] - df_simple[eng_to_heb('request_date')]).dt.days


# durations_simple = df_pass_to_court['duration']
# df_simple = df_pass_to_court
# durations_simple = df_warrent_granted['duration']
# df_simple = df_warrent_granted
# durations_simple = df_common['duration']
# df_simple = df_common


# attorney_general_responses_lists = [[] if pd.isna(l) else l[1:-1].split(',')
#                                     for l in df[eng_to_heb('attorney_general_responses')]]
# notes_seq = [[lst for i, lst in enumerate(l) if i % 2 == 0] for l in attorney_general_responses_lists]
# notes_seq_last = ['-' if len(n)==0 else n[0] for n in notes_seq]
# mask_final_response_no_interest = np.array(notes_seq_last) == 'אין עניין'
# mask_final_response_no_interest_with_comments = np.array(notes_seq_last) == 'אין עניין +הערות'
# mask_final_response_response = np.array(notes_seq_last) == 'תגובת בכ היועץ המשפ'
# mask_final_response_na = np.array(notes_seq_last) == ''
# mask_final_response = mask_final_response_no_interest | \
#                       mask_final_response_no_interest_with_comments | \
#                       mask_final_response_response | \
#                       mask_final_response_na

# decisions_lists = [[] if pd.isna(l) else l[1:-1].split(',') for l in df[eng_to_heb('decisions')]]
# notes_seq = [[lst for i, lst in enumerate(l) if i % 2 == 0] for l in decisions_lists]
# notes_seq_last = ['-' if len(n)==0 else n[-1] for n in notes_seq]
# mask_final_decision_warrent_granted = np.array(notes_seq_last) == 'מתן צו'
# mask_final_decision_pass_to_court = np.array(notes_seq_last) == 'העברה לבימש'


# TODO: Print some basic stats like sum(mask_will | mask_inherit)/len(df)
# TODO: Fix SettingWithCopyWarning
# TODO: Add all dates dependencies (open < publish < resposnce < decision < closure), perhaps when available
