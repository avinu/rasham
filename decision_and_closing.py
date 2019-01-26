from simple_durations_base import *


def int_to_list(i):
    res = [int(v) for v in list(str(i))]
    if i < 10:
        res = [0] + res
    return res


def date_to_list(d):
    res = int_to_list(d.day) + int_to_list(d.month) + int_to_list(d.year)
    return np.array(res)


def simple_textual_dist(date1, date2):
    l0 = sum(date_to_list(date1) != date_to_list(date2))
    # l1 = sum(np.abs(date_to_list(date1) - date_to_list(date2)))
    return l0


def get_bin(k, n_bins):
    k_abs = np.abs(k)
    if k_abs < 3:
        bin_ind = k_abs
    else:
        bin_ind = min(int(np.log2(k_abs) + 1), n_bins - 1)
    if k < 0:
        bin_ind = -1*bin_ind
    return bin_ind


# 0, 1, 2, 6, 10, 14, 18...
def get_bin_linear(k, n_bins):
    k_abs = np.abs(k)
    if k_abs < 3:
        bin_ind = k_abs
    else:
        bin_ind = int((k_abs - 3)/4)
        bin_ind += 3
        bin_ind = min(bin_ind, n_bins - 1)
    if k < 0:
        bin_ind = -1*bin_ind
    return bin_ind


mask = pd.notna(df_simple[eng_to_heb('decisions')])
df_simple = df_simple[mask]

final_decision_date = np.array([cached_date_parser(d[1:-1].split(',')[-1]) for d in df_simple[eng_to_heb('decisions')]])
closing_date = np.array(df_simple[eng_to_heb('closing_date')].values)

diff = closing_date - final_decision_date
dist = np.array([simple_textual_dist(cd, fdd) for (cd, fdd) in zip(closing_date, final_decision_date)])

# Standardize (by bins) the two arrays and draw the two dimensional map.
n_bins = 9
diff_dist_bins_pairs = [(get_bin(dff.days, n_bins), dst) for (dff, dst) in zip(diff, dist)]
# diff_dist_bins_pairs = [(get_bin_linear(dff.days, n_bins), dst) for (dff, dst) in zip(diff, dist)]
c = Counter(diff_dist_bins_pairs)

dim_v = 2*n_bins-1
dim_h = max([pair[1] for pair in c])+1
rows_norms = np.array([sum([c[pair] for pair in c if pair[0] == i]) for i in np.arange(dim_v) - n_bins + 1])
rows_norms[rows_norms == 0] = 1 # we devide by the norms, and we would devide by 0 only when all values are 0 too
c_array = np.zeros((dim_v, dim_h))
for pair in c:
    c_array[pair[0]+8, pair[1]] = c[pair]/rows_norms[pair[0]+8]
c_quotient = np.log10(c_array[:n_bins - 1, 1:5]/(c_array[n_bins:, 1:5][::-1]))  # To avoid deviding by 0

fig, ax = plt.subplots(1, 2, figsize=(20, 10))

# ax[0]: Heatmap
im = ax[0].imshow(c_array)
ax[0].set_xlabel('מרחק טקסטואלי'[::-1])
ax[0].set_ylabel('הפרש בימים בין תאריך ההכרעה ותאריך הסגירה'[::-1])
# ax[0].set_title('מפת חום של שכיחות הפרשי ההכרעה והסגירה ושל מרחקם הטקסטואלי'[::-1])

# We want to show all ticks... and label them with the respective list entries
ax[0].set_xticks(np.arange(dim_h))
ax[0].set_yticks(np.arange(dim_v))
ax[0].set_xticklabels(np.arange(dim_h))
bins_signs = [-1 for _ in range(n_bins-1)] + [1 for _ in range(n_bins)]
bins_vals = [bins_signs[i]*(np.power(2, np.abs(i - n_bins + 1)) - 1) for i in np.arange(dim_v)]
ax[0].set_yticklabels(bins_vals)
# ax.set_yticklabels(rows_norms, left=False) TODO

# ax[1]: Probabilities ratio
lines = ax[1].plot(c_quotient)
ax[1].legend(lines, ('הפרש טסטואלי = 1'[::-1],
                     'הפרש טסטואלי = 2'[::-1],
                     'הפרש טסטואלי = 3'[::-1],
                     'הפרש טסטואלי = 4'[::-1]))
ax[1].set_xlabel('הפרש בימים בין תאריך ההכרעה ותאריך הסגירה'[::-1])
ax[1].set_ylabel('לוג של מנת הסיכוי שההפרש הוא שלילי והסיכוי שההפרש הוא חיובי'[::-1])
ax[1].set_xticks(np.arange(n_bins-1))
ax[1].set_xticklabels(bins_vals[-n_bins+1:])
# ax[1].set_title('הסיכוי שהפרש תאריכים הוא שלילי )סיכוי ששלילי/סיכוי שחיובי('[::-1])

plt.suptitle('ניתוח תאריכי ההחלטות הסופיות והסגירה - הפרשי ימים ומרחק טקסטואלי'[::-1])

fig_name = 'decision_and_closing_dates'
plt.savefig(out_path + '/' + fig_name + '.pdf')
plt.close()


# # Investigate effect of representation
# import datetime
# df_simple_fixed = df_simple.copy()
# mask_diff = diff < datetime.timedelta(0)
# mask_dist = dist==1
# mask = mask_diff & mask_dist
# df_simple_fixed.loc[mask, eng_to_heb('closing_date')] = final_decision_date[mask]
# durations_simple_fixed = (df_simple_fixed[eng_to_heb('closing_date')] - df_simple_fixed[eng_to_heb('request_date')]).dt.days
# df_simple_fixed['duration_fixed'] = durations_simple_fixed
#
# fig, ax = plt.subplots(figsize=(20, 10))
# title = 'התפלגות משך תיקים פשוטים עם/בלי שליליים'
# freq = draw_reference_dist(durations_simple.values, ax, title)
#
# l = 'מתוקנים'
# draw_front_dist(durations_simple_fixed.values, ax, l, freq)
#
# plt.legend()
# plt.savefig(out_path + '/' + 'durations_simple_cases_fixed.pdf')

# Motivation:
# - observe uniform distribution on dists for "normal" diffs (medium positive diffs)
# - observe a larger weight on small dists for "abnormal" diffs (neg/large diffs)
# Then we would have a justification for doing the "small" corrections when the diff is abnormal (if indeed it's a correction)

# Motivation 2: Observe the quotient of the neg over pos (or vice versa) probability per duration per textual diff.
# - In other words, given that the text-diff is 1, for every duration how likely is that duration to be positive/negative?
# - If the data is clean then the answer should be ~1 and that is what I expect to see for all durations for text-diff > 1.
# - for text-diff = 1, I expect negative to be exceedingly more likely as the duration goes up (in absolute value)

# Note: When trying to get better resolution (linear) of the durations I'm running into many zeros which break the comparison


# Examples:
# 72600 - closing-date day/month swap (07/04 instead of 04/07)
# 435060 - closing-date-year is off by one (2014 instead of 2015)
# 72607 - closing-date-year is off by one
# 75275 - typo?

# TODO: Fix lables (get bin isn't pure log, it has an offset)
# TODO: Add the values to the bins?
# TODO: Split by something? Add all-dates-hint (or just duration)? Note that when duration is neg so is the closing/decision diff.
# TODO: Change tags to something alongs the lines of 'at least X days'?
