from simple_durations_base import *


# Investigate effect of representation
fig, ax = plt.subplots(figsize=(20, 10))
title = 'התפלגות משך תיקים שסיבת סגירתם העברה לבימש/מתן צו'
freq = draw_reference_dist(durations_common.values, ax, title)

durations_main = df_pass_to_court['duration']
label = 'העברה לבימש'
draw_front_dist(durations_main.values, ax, label, freq)

plt.legend()
plt.savefig(out_path + '/' + 'durations_common_cases_warrnet_vs_court.pdf')

# Investigate effect of representation per district
courts = set(df_common[eng_to_heb('court')].values)
for court in courts:
    mask_court = df_common[eng_to_heb('court')] == court
    df_common_by_court = df_common[mask_court]
    durations_common_by_court = df_common_by_court['duration']

    fig, ax = plt.subplots(figsize=(20, 10))
    title = 'התפלגות משך תיקים שסיבת סגירתם העברה לבימש/מתן צו בכל הארץ מול מחוז מסויים'
    freq = draw_reference_dist(durations_common_by_court, ax, title)

    mask_closing_reason_pass_to_court = np.array(df_common_by_court[eng_to_heb('closing_reason')] == 'העברה לבימש')
    df_common_by_court_pass_to_court = df_common_by_court[mask_closing_reason_pass_to_court]
    durations_common_by_court_main = df_common_by_court_pass_to_court['duration']
    label = court
    draw_front_dist(durations_common_by_court_main.values, ax, label, freq)

    plt.legend()
    plt.savefig(out_path + '/' + 'durations_common_cases_warrnet_vs_court_' + court + '.pdf')
