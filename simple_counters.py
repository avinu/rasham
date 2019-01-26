# -*- coding: utf-8 -*-
from utils import *
import pandas as pd
from collections import Counter
import draw_utils


# # Mask df [temporary, think of a better way to do this without poluting simple counters]
# c = Counter(df[eng_to_heb('petitioner')])
# edna_lavie = c.most_common(2)[-1][0]
# # edna_lavie = c.most_common(70)[-1][0]
# # edna_lavie = c.most_common(500)[-2][0]
# mask = df[eng_to_heb('petitioner')] == edna_lavie
# df = df[mask]
# print(df)
# # Lawyers who also act as petitioners (can happen), people with common names (everyone there are cohen and levi), and
# # Edna Lavie's files are almost all typos fixes.

# Other masks
# df = df_common
# mask = np.array(df[eng_to_heb('request_status')] == 'הבקשה ממתינה להקלדה במזכירות')
# mask = np.array(df[eng_to_heb('request_type')] == 'הוכחת מוות')
# df = df[mask]


df_to_use = df


# Fetches the information of each "column": Counter, number of NAs, number of (all) elements, column name, title and
# figure name.
# Note that also the decisions' notes are considered a column (even though they are not a column in the table).
def get_col_counter():
    n = len(df_to_use)
    for col_name in df_to_use.columns:
        col = df_to_use[col_name]
        not_na = col[pd.notna(col)]
        n_na = sum(pd.isna(col))
        c = Counter(not_na)

        if col_name in synthetics:
            title = col_name
            fig_name = col_name
        else:
            title = col_name[::-1]
            fig_name = heb_to_eng(col_name)

        yield c, n_na, n, col_name, title, fig_name

    for ind_final, col_name in zip(list_cols_final, [eng_to_heb(name) for name in list_cols]):
        col = df_to_use[col_name]
        not_na = col[pd.notna(col)]
        not_na_lists = [lst[1:-1].split(',') for lst in not_na]

        lengths = [len(lst) / 2 for lst in not_na_lists]
        notes = [val for lst in not_na_lists for i, val in enumerate(lst) if i % 2 == 0]
        dates = [val for lst in not_na_lists for i, val in enumerate(lst) if i % 2 == 1]

        notes_lists = [tuple([lst for i, lst in enumerate(l) if i % 2 == 0]) for l in not_na_lists]
        notes_final = [n[ind_final] for n in notes_lists]

        lists_data = [lengths, notes, dates, notes_final, notes_lists]
        lists_data_names = ['מספר רישומים', 'הערות', 'תאריכים', 'הערות סופיות', 'רצפי הערות']
        lists_data_names_eng = ['n', 'notes', 'dates', 'final_notes', 'notes_sequences']

        print("%s בפירוט (%d)" % (col_name, len(dates)))
        for col, data_name, data_name_eng in zip(lists_data, lists_data_names, lists_data_names_eng):
            n_details = len(col)
            not_na = [val for val in col if val != '']
            n_na = len([val for val in col if val == ''])
            c = Counter(not_na)

            title = (col_name + ' - ' + data_name)[::-1]
            fig_name = heb_to_eng(col_name) + '_' + data_name_eng

            yield c, n_na, n_details, col_name + '-' + data_name, title, fig_name


cols = get_col_counter()
for c, n_na, n, col_name, title, fig_name in cols:
    n_vals = len(c)
    top3 = c.most_common(3)
    top20 = c.most_common(20)
    top20_total = sum([p[1] for p in top20])
    top20_per = 100 * top20_total / n
    na_per = 100 * n_na / n

    print("%s, %d, %2.2f%%, %2.2f%%" % (col_name, n_vals, top20_per, na_per))
    for pair in top3:
        print("%s: %2.2f%% (%d)" % (pair[0], 100 * pair[1] / n, pair[1]))

    if n_vals < 50:
        # When the number of categories is small we draw a logarithmic histogram:
        # - The X-axis (counters) are powers of 10
        draw_utils.draw_count(c, title, fig_name, out_path)
    else:
        # When there are diverse values we draw a "doubple logarithmic" histogram:
        # - The Y-axis (bins) are powers of 2
        # - The X-axis (counters) are powers of 10
        c_c = Counter(list(pd.DataFrame.from_dict(c, orient='index')[0]))
        draw_utils.draw_double_count(c_c, title, fig_name, out_path)

        top20_completed_dict = {str(v[0])[::-1]: v[1] for v in top20}
        if all([isinstance(v[0], tuple) for v in top20]):
            top20_completed_dict = {tuple([note[::-1] for note in v[0]]): v[1] for v in top20}
        elif all([isinstance(v[0], str) for v in top20]):
            top20_completed_dict = {v[0]: v[1] for v in top20}
        title = ("(%2.2f%%)" % top20_per) + (title[::-1] + ', 02 הכי נפוצים ')[::-1]
        fig_name = fig_name + '_top'
        draw_utils.draw_count(top20_completed_dict, title, fig_name, out_path)
