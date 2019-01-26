# -*- coding: utf-8 -*-
import pandas as pd
from dateutil import parser
import os


cache = {}


def cached_date_parser(s):
    if pd.isna(s):
        return pd.NaT

    if s in cache:
        return cache[s]

    dt = parser.parse(s, dayfirst=True).date()  # dt = pd.to_datetime(s, format='%Y%m%d', coerce=True)
    cache[s] = dt
    return dt

# Columns
# TODO: Change to  {name:i for i,name in enumerate(df.columns)} and vice-versa


columns_direct_heb = \
    {0: 'בית משפט',
     1: 'תאריך הגשת בקשה',
     2: 'מספר בקשה',
     3: 'מספר תיק',
     4: 'סוג בקשה',
     5: 'ת.ז. מנוח',
     6: 'עיתון מפרסם',
     7: 'תאריך פרסום',
     8: 'סטטוס בקשה',
     9: 'תאריך סגירה',
     10: 'סיבת סגירה',
     11: 'מבקש',
     12: 'מייצג',
     13: 'טלפון מייצג',
     14: 'כתובת מייצג',
     15: 'קישור',
     16: 'תגובות בא-כח היועץ המשפטי',
     17: 'החלטות',
     18: 'na_count',
     19: 'spaces_count',
     20: 'punctuation_count',
     21: 'id_valid'}

# After
final_dtypes = [
    'str',       # 0: 'בית משפט'
    'datetime',  # 1: 'תאריך הגשת בקשה'
    'int',       # 2: 'מספר בקשה'
    'int',       # 2: 'מספר בקשה'
    'int',       # 3: 'מספר תיק'
    'str',       # 4: 'סוג בקשה'
    'int',       # 5: 'ת.ז. מנוח'
    'str',       # 6: 'עיתון מפרסם'
    'datetime',  # 7: 'תאריך פרסום'
    'str',       # 8: 'סטטוס בקשה'
    'datetime',  # 9: 'תאריך סגירה'
    'str',       # 10: 'סיבת סגירה'
    'str',       # 11: 'מבקש'
    'str',       # 12: 'מייצג'
    'str',       # 13: 'טלפון מייצג'
    'str',       # 14: 'כתובת מייצג'
    'int',       # 15: 'קישור'
    'str',       # 16: 'תגובות בא-כח היועץ המשפטי'
    'str',       # 17: 'החלטות'
    'int',       # 18: 'na_count'
    'int',       # 19: 'spaces_count'
    'int',       # 20, 'punctuation_count'
    'bool'       # 21: 'id_valid'
]

columns_reverse_eng = \
    {'court':                       0,   # בית משפט
     'request_date':                1,   # תאריך הגשת בקשה
     'request_number':              2,   # מספר בקשה
     'file_number':                 3,   # מספר תיק
     'request_type':                4,   # סוג בקשה
     'deceased_id':                 5,   # ת.ז. מנוח
     'publishing_paper':            6,   # עיתון מפרסם
     'publishing_date':             7,   # תאריך פרסום
     'request_status':              8,   # סטטוס בקשה
     'closing_date':                9,   # תאריך סגירה
     'closing_reason':              10,  # סיבת סגירה
     'petitioner':                  11,  # מבקש
     'representative':              12,  # מייצג
     'representative phone':        13,  # טלפון מייצג
     'representative_address':      14,  # כתובת מייצג
     'link':                        15,  # קישור
     'attorney_general_responses':  16,  # תגובות בא-כח היועץ המשפטי
     'decisions':                   17,  # החלטות
     'na_count':                    18,
     'excessive_spaces_count':      19,
     'punctuation_count':           20,
     'id_valid':                    21}


columns_direct_eng = {columns_reverse_eng[k]: k for k in columns_reverse_eng.keys()}
columns_reverse_heb = {columns_direct_heb[k]: k for k in columns_direct_heb.keys()}


def eng_to_heb(x):
    return columns_direct_heb[columns_reverse_eng[x]]


def heb_to_eng(x):
    return columns_direct_eng[columns_reverse_heb[x]]


col_names_orig_eng = \
    {'court',
     'request_date',
     'request_number',
     'file_number',
     'request_type',
     'deceased_id',
     'publishing_paper',
     'publishing_date',
     'request_status',
     'closing_date',
     'closing_reason',
     'petitioner',
     'representative',
     'representative phone',
     'representative_address',
     'link',
     'attorney_general_responses',
     'decisions'}

col_names_orig_eng_ordered = \
    ['court',
     'request_date',
     'request_number',
     'file_number',
     'request_type',
     'deceased_id',
     'publishing_paper',
     'publishing_date',
     'request_status',
     'closing_date',
     'closing_reason',
     'petitioner',
     'representative',
     'representative phone',
     'representative_address',
     'link',
     'attorney_general_responses',
     'decisions']

dates_cols = ['request_date', 'publishing_date', 'closing_date']
simple_cols = ['court', 'request_type', 'publishing_paper', 'request_status', 'closing_reason']
list_cols = ['decisions', 'attorney_general_responses']
list_cols_final = [-1, 0]
diverse = ['petitioner', 'representative']
synthetics = ['na_count', 'excessive_spaces_count', 'punctuation_count', 'id_valid', 'duration']

# Note: The deceased name is available online but not in the file (not sure if it was on the spec).
# Note: A UID for the DB should NOT be 'file_number' + 'request_number' (may be duplicates accross districts)
# Note: The field 'link' may be used as a UID

link_to_field_with_semi_col = {
    '1032': 'representative',
    '103598': 'representative',
    '108165': 'representative',
    '108181': 'representative',
    '108555': 'representative',
    '110014': 'petitioner',
    '114969': 'representative',
    '115540': 'representative',
    '115545': 'representative',
    '118132': 'representative',
    '118366': 'representative',
    '122212': 'representative',
    '125283': 'representative',
    '128777': 'petitioner',
    '129386': 'representative',
    '130295': 'representative',
    '130804': 'representative',
    '132501': 'representative',
    '132824': 'representative',
    '146313': 'representative',
    '146687': 'representative',
    '153014': 'representative',
    '156555': 'representative',
    '160868': 'representative',
    '161285': 'representative',
    '162118': 'representative',
    '168136': 'representative',
    '173513': 'representative',
    '178732': 'representative',
    '187318': 'representative',
    '192030': 'representative',
    '197069': 'representative',
    '197315': 'representative_address',
    '197837': 'representative',
    '202493': 'representative_address',
    '202612': 'representative_address',
    '207386': 'representative',
    '209662': 'representative',
    '215416': 'representative',
    '216410': 'representative_address',
    '221877': 'representative',
    '224392': 'representative_address',
    '240746': 'representative_address',
    '24419': 'representative_address',
    '250083': 'representative',
    '256099': 'representative_address',
    '267537': 'representative',
    '271218': 'representative_address',
    '278452': 'petitioner',
    '278455': 'petitioner',
    '292525': 'representative',
    '293599': 'representative',
    '293965': 'petitioner',
    '299414': 'representative_address',
    '301582': 'representative_address',
    '302108': 'representative_address',
    '308279': 'representative_address',
    '308722': 'representative_address',
    '318214': 'representative_address',
    '326549': 'petitioner',
    '328424': 'representative_address',
    '328874': 'representative',
    '33385': 'petitioner',
    '33661': 'representative',
    '33678': 'representative',
    '338495': 'representative',
    '339561': 'representative_address',
    '347042': 'representative_address',
    '347706': 'representative_address',
    '347737': 'representative_address',
    '349727': 'representative_address',
    '353033': 'petitioner',
    '358948': 'representative',
    '360097': 'representative',
    '36471': 'representative',
    '369146': 'representative_address',
    '369194': 'representative_address',
    '371497': 'representative',
    '371777': 'representative',
    '375410': 'representative',
    '375490': 'representative',
    '383015': 'representative',
    '384151': 'representative',
    '390478': 'representative_address',
    '392918': 'representative',
    '392924': 'representative',
    '392929': 'representative',
    '393737': 'representative',
    '393743': 'representative',
    '394365': 'petitioner',
    '404151': 'representative',
    '404518': 'representative',
    '408761': 'representative_address',
    '426633': 'representative_address',
    '437302': 'representative',
    '439155': 'representative',
    '443018': 'representative_address',
    '445081': 'representative',
    '445096': 'representative_address',
    '447470': 'representative',
    '453801': 'representative_address',
    '454044': 'representative',
    '463392': 'petitioner',
    '464323': 'representative_address',
    '473260': 'representative',
    '473855': 'representative_address',
    '487333': 'representative_address',
    '500468': 'representative',
    '515865': 'representative',
    '519683': 'representative_address',
    '539082': 'representative_address',
    '71971': 'representative',
    '79869': 'representative_address',
    '86706': 'petitioner',
    '971': 'petitioner',
    '98414': 'representative_address'
}

bad_ids = [
    # Made up names (i.e. בדיקה, נסיון) and numeric names
    '43227115',
    '111111142',
    '54705900',
    '26'
]

bad_request_numbers_and_file_numbers = [
    # 1
    ('0', '14495'),
    ('0', '14496'),
    ('0', '14497'),
    ('0', '14501'),
    ('0', '14502'),
    ('0', '14503'),
    ('0', '14546'),
    ('0', '14547'),
    ('0', '14548'),
    ('0', '14685'),
    ('0', '15271'),
    ('0', '15272'),
    ('1', '28336'),
    ('1', '28337'),
    ('1', '10848')
]

# (id (or 0 if missing), file_number) - verify uniqueness.
bad_file_numbers_and_ids = [
    ('81122', '18'),
]

bad_links = [
    # Non numeric request number
    '444095'
    '374956'
    '374963'
    '374969'
    '374970'
    # בדיקה
    '123209',
    '138318',
    '142056',
    '155762',
    '166245',
    '166246',
    '173818',
    '176499',
    '176611',
    '176612',
    '179961',
    '179962',
    '179963',
    '179967',
    '180085',
    '180849',
    '278635',
    '287299',
    '397792',
    '397799',
    '469457',
    # נסיון
    '504343',
    # 1
    '101269',
    '122349',
    '126643',
    '126644',
    '126645',
    '126781',
    '126795',
    '126796',
    '156237',
    '158531',
    '158534',
    '160762',
    '164775',
    '169693',
    '179796',
    '179797',
    '179798',
    # 2
    '179794',
    # 4
    '161153',
    # 9
    '147216'
]


delim = ';'
latest_input_file_name = 'Data1.csv.clean.2018_10_19__17_00_35.csv'
out_path, file_extension = os.path.splitext(latest_input_file_name)
if not os.path.isdir(out_path):
    os.mkdir(out_path)

df = pd.read_csv(latest_input_file_name, delimiter=delim, index_col=15,
                 parse_dates=[columns_reverse_eng[k] for k in dates_cols], date_parser=cached_date_parser)
