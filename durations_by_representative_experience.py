from simple_durations_base import *

df_to_use = df_simple

# Calculate representatives experience masks
representatives = df_to_use[eng_to_heb('representative')]
mask = pd.notna(representatives)
df_to_use = df_to_use[mask].copy()

representatives = df_to_use[eng_to_heb('representative')]
c = Counter(representatives)
representatives_counts = [c[rep] for rep in representatives]
df_to_use['representatives_counts'] = representatives_counts

n_bins = int(np.floor(np.log2(max(c.values()))))
categories = ['1'] + \
             [str(int(np.power(2, i + 1))) + '-' + str(int(np.power(2, i + 2)) - 1) for i in range(n_bins - 2)] + \
             [str(int(np.power(2, n_bins - 1))) + '+']
# For example categories may be ['1', '2-3', '4-7', '8-15', '16-31', '32-63', '64-127', '128+']

for i in range(n_bins):
    fig, ax = plt.subplots(figsize=(20, 10))
    title = 'התפלגות משך תיקים פשוטים לפי נסיון מייצג: ' + categories[i][::-1]
    freq = draw_reference_dist(durations_simple, ax, title)

    mask = (df_to_use['representatives_counts'] >= np.power(2, i)) & \
           (df_to_use['representatives_counts'] < np.power(2, i+1))
    df_to_use_by_exp = df_to_use[mask]
    durations_by_court = df_to_use_by_exp['duration']
    label = categories[i][::-1]
    draw_front_dist(durations_by_court.values, ax, label, freq)

    plt.legend()
    plt.savefig(out_path + '/' + 'durations_simple_cases_by_representative_experience_' + categories[i] + '.pdf')
