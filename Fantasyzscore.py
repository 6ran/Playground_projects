import pandas as pd

def cats(x):
    b = x.drop_duplicates(subset = 'Player')
    return b

def segment_drop(y):
   z = y.drop(['Rk','Pos','Age','Tm',
            'PF','FG','FGA','3PA',
            '3P%', '2P','2PA','2P%',
            'eFG%','FT','FTA','ORB',
            'DRB', 'GS' ], axis = 1)
   return z

def mins_played(z):
    x = z.sort_values(['MP'], ascending=False)
    z = x[x['MP'] > 12]
    return z

def z_score_calc(z_score):
    for col in z_score:
        if col == 'Player':
            pass
        else:
            col_zscore = col + '_zscore'
            z_score[col_zscore] = (z_score[col] - z_score[col].mean()) / z_score[col].std(ddof=0)


df2020 = pd.read_excel('nba2020.xlsx')
df2021 = pd.read_excel('sportsref_download.xlsx')


df2020 = cats(df2020)
df2021 = cats(df2021)


df2020 = segment_drop(df2020)
df2021 = segment_drop(df2021)

print(df2021.loc[df2021['Player'] == 'James Harden'])

df2020 = mins_played(df2020)
df2021 = mins_played(df2021)

df2020['check'] = ''

df2020 = df2020.assign(check = df2020.Player.isin(df2021.Player))
df2020 = df2020[df2020['check'] == True]


z_score_calc(df2020)
z_score_calc(df2021)

df2020['net_zscore_2020'] = 0
df2021['net_zscore_2021'] = 0

zscore2020 = df2020.filter(regex="_zscore")
P1Sum = zscore2020.sum(axis=1)

df2020['net_zscore_2020'] = P1Sum

zscore2021 = df2021.filter(regex='_zscore')
P2sum = zscore2021.sum(axis=1)

df2021['net_zscore_2021'] = P2sum

dfresult2021 = pd.merge(df2021, df2020, on='Player',
                      suffixes= ('_2021','_2020'))


dfresult2021 = dfresult2021[sorted(dfresult2021)]

first_column = dfresult2021.pop('Player')

for second_column in dfresult2021:
    if 'zscore' in second_column:
        pass
    else:
        del dfresult2021[second_column]

dfresult2021 = dfresult2021.drop(['check_zscore'], axis = 1)

dfresult2021.insert(0, 'Player', first_column)

xz = dfresult2021['net_zscore_2021'] - dfresult2021['net_zscore_2020']

dfresult2021.insert(1,'Rating',xz)

dfresult2021 = dfresult2021.sort_values('Rating', ascending = False)

dfresult2021 = dfresult2021.round(2)

dfresult2021['Player'] = dfresult2021['Player'].str.wrap(1000)

dfresult2021 = dfresult2021.style.background_gradient(cmap='RdYlGn')

my_data = 'Fantasy_Sleepers.xlsx'
dfresult2021.to_excel(my_data, sheet_name = "Fantasy z-score rating",index= False)







