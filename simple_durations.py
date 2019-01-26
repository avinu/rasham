from simple_durations_base import *


df_to_use = df_simple


# Investigate effect of representation
fig, ax = plt.subplots(figsize=(20, 10))
title = 'התפלגות משך תיקים פשוטים עם/בלי ייצוג'
freq = draw_reference_dist(durations_simple.values, ax, title)

mask_rep = pd.isna(df_to_use[eng_to_heb('representative')])
df_to_use_no_rep = df_to_use[mask_rep]
durations_no_rep = df_to_use_no_rep['duration']
label = 'ללא ייצוג'
draw_front_dist(durations_no_rep.values, ax, label, freq)

plt.legend()
plt.savefig(out_path + '/' + 'durations_simple_cases_representation.pdf')

# Investigate effect of representation per district
courts = set(df_to_use[eng_to_heb('court')].values)
for court in courts:
    fig, ax = plt.subplots(figsize=(20, 10))
    title = 'התפלגות משך תיקים פשוטים בכל הארץ מול מחוז מסויים'
    freq = draw_reference_dist(durations_simple, ax, title)

    mask_court = df_to_use[eng_to_heb('court')] == court
    df_to_use_by_court = df_to_use[mask_court]
    durations_by_court = df_to_use_by_court['duration']
    label = court
    draw_front_dist(durations_by_court.values, ax, label, freq)

    plt.legend()
    plt.savefig(out_path + '/' + 'durations_simple_cases_in_districts_' + court + '.pdf')
