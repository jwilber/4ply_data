import pandas as pd

df2 = pd.read_csv("https://raw.githubusercontent.com/jwilber/koston_article/master/data/koston.csv", sep="\t", encoding = "ISO-8859-1")

# total num tricks
aggregated = df2.groupby('video').max()['trick_index']
aggregated.name = 'total_num_tricks'
df3 = df2.join(aggregated, on='video')

# total num clips
aggregated = df2.groupby('video').max()['clip_index']
aggregated.name = 'total_num_clips'
df3 = df3.join(aggregated, on='video')


# total slowmo tricks
aggregated = df2.groupby('video').sum()['slowmo']
aggregated.name = 'total_slowmo_tricks'
df3 = df3.join(aggregated, on='video')


# total switch tricks
aggregated = df2.groupby('video').sum()['switch']
aggregated.name = 'total_switch_tricks'
df3 = df3.join(aggregated, on='video')

# total distinct
aggregated = df2.groupby('video').nunique()['trick']
aggregated.name = 'total_distinct_tricks'
df3 = df3.join(aggregated, on='video')

# total num fs tricks
aggregated = df2[['trick', 'video', 'trick_index', 'obstacle']].drop_duplicates().groupby(['video'])['trick'].apply(lambda x: x[x.str.contains('fs ')].count())
aggregated.name = 'total_fs_tricks'
df3 = df3.join(aggregated, on='video')

# total num bs tricks
aggregated = df2[['trick', 'video', 'trick_index', 'obstacle']].drop_duplicates().groupby(['video'])['trick'].apply(lambda x: x[x.str.contains('bs ')].count())
aggregated.name = 'total_bs_tricks'
df3 = df3.join(aggregated, on='video')

vids = df3.groupby('video')

# percent stair
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='stair']) + len(x[x=='gap']) ) / len(x))
obstacles.name = 'perc_stair'
df3 = df3.join(obstacles, on="video")


# percent ledge
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='ledge'])) / len(x))
obstacles.name = 'perc_ledge'
df3 = df3.join(obstacles, on="video")

# percent manual
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='manual'])) / len(x))
obstacles.name = 'perc_manual'
df3 = df3.join(obstacles, on="video")

# percent transition
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='transition'])) / len(x))
obstacles.name = 'perc_transition'
df3 = df3.join(obstacles, on="video")

# percent flat
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='flat'])) / len(x))
obstacles.name = 'perc_flat'
df3 = df3.join(obstacles, on="video")

# percent picnic table
obstacles = vids['obstacle_detailed'].agg(lambda x: (len(x[x=='picnic table'])) / len(x))
obstacles.name = 'perc_picnic'
df3 = df3.join(obstacles, on="video")

# percent handrail
obstacles = vids['obstacle_detailed'].agg(lambda x: (len(x[x=='handrail'])) / len(x))
obstacles.name = 'perc_handrail'
df3 = df3.join(obstacles, on="video")

# percent curb
obstacles = vids['obstacle_detailed'].agg(lambda x: (len(x[x=='curb'])) / len(x))
obstacles.name = 'perc_curb'
df3 = df3.join(obstacles, on="video")

cols_to_keep = ['video', 'total_num_tricks', 'total_num_clips', 'total_slowmo_tricks', 'total_switch_tricks',
       'total_distinct_tricks', 'total_fs_tricks', 'total_bs_tricks',
       'perc_stair', 'perc_ledge', 'perc_manual', 'perc_transition',
       'perc_picnic', 'perc_handrail', 'perc_curb', 'perc_flat']


df4 = df3[cols_to_keep].drop_duplicates().reset_index().drop(columns='index')

df4['perc_distinct'] = df4.apply(lambda x: x['total_distinct_tricks'] / x['total_num_tricks'], axis=1)

df4['perc_slowmo'] = df4.apply(lambda x: x['total_slowmo_tricks'] / x['total_num_tricks'], axis=1)

df4['perc_switch'] = df4.apply(lambda x: x['total_switch_tricks'] / x['total_num_tricks'], axis=1)

df4['perc_fs'] = df4.apply(lambda x: x['total_fs_tricks'] / x['total_num_tricks'], axis=1)

df4['perc_bs'] = df4.apply(lambda x: x['total_bs_tricks'] / x['total_num_tricks'], axis=1)

df5 = df4.drop(columns=['total_num_tricks', 'total_num_clips', 'total_slowmo_tricks', 'total_switch_tricks', 'total_distinct_tricks', 
                       'total_fs_tricks', 'total_bs_tricks'])


df5['video'] = df5.video.str.replace(' - ', '_', regex=False).str.replace(' ', '_', regex=False).str.replace('é', 'e', regex=False).str.replace('-', '_', regex=False).str.replace('.', '', regex=False)

for col in ['perc_stair', 'perc_ledge', 'perc_manual', 'perc_transition',
       'perc_picnic', 'perc_handrail', 'perc_curb', 'perc_distinct',
       'perc_slowmo', 'perc_switch', 'perc_fs', 'perc_bs', 'perc_flat']:
    df5[col] = round(df5[col] * 100)
    


# Multiline

df2 = pd.read_csv("https://raw.githubusercontent.com/jwilber/koston_article/master/data/koston.csv", sep="\t", encoding = "ISO-8859-1")


year_dict = {
    '101 - WWII Report': '1992',
    'Union - Right to Skate': '1992',
    'H-Street - Next Generation': '1992',
    'Girl - Goldfish': '1994',
    '101 - Falling Down': '1993',
    'Girl - Pretty Sweet':'2012',
    'Etnies - High 5': '1995',
    'Transworld - Uno': '1996',
    'Girl - Mouse': '1996',
    'Chocolate - The Chocolate Tour': '1999',
    'Lakai - Fully Flared': '2007',
    'Nike - The SB Chronicles Vol. 3':'2015',
    'Girl - Yeah Right': '2003',
    'éS - Menikmati': '2000',
    'Chomp On This': '2002'
}


df2['year'] = df2.apply(lambda x: year_dict[x['video']], axis=1)


# total num tricks
aggregated = df2.groupby('year').max()['trick_index']
aggregated.name = 'total_num_tricks'
df3 = df2.join(aggregated, on='year')

# total num clips
aggregated = df2.groupby('year').max()['clip_index']
aggregated.name = 'total_num_clips'
df3 = df3.join(aggregated, on='year')


# total slowmo tricks
aggregated = df2.groupby('year').sum()['slowmo']
aggregated.name = 'total_slowmo_tricks'
df3 = df3.join(aggregated, on='year')


# total switch tricks
aggregated = df2.groupby('year').sum()['switch']
aggregated.name = 'total_switch_tricks'
df3 = df3.join(aggregated, on='year')

# total distinct
aggregated = df2.groupby('year').nunique()['trick']
aggregated.name = 'total_distinct_tricks'
df3 = df3.join(aggregated, on='year')


vids = df3.groupby('year')



# percent stair
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='stair']) + len(x[x=='gap']) ))
obstacles.name = 'stairs'
df3 = df3.join(obstacles, on="year")


# percent ledge
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='ledge'])))
obstacles.name = 'ledge'
df3 = df3.join(obstacles, on="year")


# percent transition
obstacles = vids['obstacle'].agg(lambda x: (len(x[x=='transition'])))
obstacles.name = 'transition'
df3 = df3.join(obstacles, on="year")

# percent handrail
obstacles = vids['obstacle_detailed'].agg(lambda x: (len(x[x=='handrail'])))
obstacles.name = 'handrail'
df3 = df3.join(obstacles, on="year")

cols_to_keep = ['year', 'total_num_tricks', 'total_num_clips', 'total_slowmo_tricks', 'total_switch_tricks',
       'total_distinct_tricks',
       'stairs', 'ledge', 'transition',
       'handrail']


df4 = df3[cols_to_keep].drop_duplicates().reset_index().drop(columns='index')

df5 = df4.drop(columns=['total_num_tricks', 'total_num_clips', 'total_slowmo_tricks', 'total_switch_tricks', 'total_distinct_tricks'])

perc_df = pd.melt(df5, id_vars =['year'], value_vars =['stairs', 'ledge', 'handrail', 'transition'])
perc_df.sort_values('year', inplace=True)
perc_df.columns = ['year', 'obstacle', 'count']