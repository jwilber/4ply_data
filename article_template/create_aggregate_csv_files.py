	# -*- coding: utf-8 -*-
# author: Jared Wilber
"""create_aggregate_csv_files.py

This script creates all the required csv files with which to populate the javascript charts..

Example:
    The function may be called from the cli with or without arguments:

        # call without arguments
        $ python create_aggregate_csv_files.py

        # call with arguments
        $ python create_aggregate_csv_files.py --csv_path koston_data.csv --data_dir ./data
"""

import argparse
import os

import pandas as pd


# dict for years. Only use for Koston.
# todo: remove in favor of year column
YEAR_DICT = {
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


def rename_obstacle(x):
    "Rename obstacles to have correct values."
    if x == 'rail':
        return 'Rail'
    elif x == 'ledge':
        return "Ledge"
    elif x == "gaps":
        return "Stairs/Gaps"
    elif x == "flat":
        return "Flatground"
    elif x == "transition":
        return "Transition"



def main(csv_path, data_dir):

	# Set paths for data
	TOP_TRICKS_PATH = os.path.join(data_dir, "top_tricks.csv")
	TRICKS_BY_OBSTACLE_PATH = os.path.join(data_dir, "tricks_by_obstacle.csv")
	TIME_SERIES_PATH = os.path.join(data_dir, "timeseries.csv")
	SQUARE_PIE_PATH = os.path.join(data_dir, "square_pie.csv")

	# create dir if it doesn't exist
	if not os.path.exists(data_dir):
	    os.makedirs(data_dir)

	df = pd.read_csv(csv_path, sep="\t")

	# create place-holder df
	df2 = df


	# ================================
	# Create data for top tricks chart
	# ================================

	trick_df = pd.DataFrame(df2.trick.value_counts())
	trick_df['val'] = trick_df.index
	trick_df.columns = ['count', 'trick']
	trick_df = trick_df[trick_df['count'] > 4]
	trick_df.to_csv(TOP_TRICKS_PATH, index=False)


	# ==================================
	# Create data for tricks by obstacle
	# ==================================

	df['gaps'] = df.apply(lambda x: x['obstacle'] == 'gap' or x['obstacle'] == 'stair' or x['obstacle'] == 'stairs', axis=1)

	df.obstacle[df.gaps == True] = 'gaps'

	obstacles_keep = ['ledge', 'rail', 'flat', 'gaps', 'transition']
	df.obstacle.value_counts()
	df_o = df[df.obstacle.isin(obstacles_keep)]

	cnt_df = pd.DataFrame(df_o.groupby(['obstacle', 'trick']).trick.value_counts())# .groupby('obstacle').head(5)

	cnt_df.columns = ['trickcount']

	cnt_df = pd.DataFrame(cnt_df.sort_values(['obstacle', 'trickcount'], ascending=False).groupby('obstacle').head(n=8))
	cnt_df = cnt_df[cnt_df.trickcount > 1]

	cnt_df.index = cnt_df.index.set_names(['obstacle', 'trick', 'trick1'])
	cnt_df.reset_index(inplace=True)
	cnts_df = cnt_df[['obstacle', 'trick', 'trickcount']]
	    
	cnts_df.obstacle = cnts_df.obstacle.apply(rename_obstacle)
	cnts_df.columns = ['obstacle', 'trick', 'count']

	cnts_df.to_csv(TRICKS_BY_OBSTACLE_PATH, index=False)


	# ============================
	# Create data for time-series
	# ============================

	df2['year'] = df2.apply(lambda x: YEAR_DICT[x['video']], axis=1)
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

	perc_df.to_csv(TIME_SERIES_PATH, index=False)


	# ================================
	# Create data for square-pie chart
	# ================================

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
	    
	df5.to_csv(SQUARE_PIE_PATH, index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Create intermediate csv files."
    )
    parser.add_argument('--csv_path',
                        help="Name of csv file to create data from.")

    parser.add_argument('--data_dir', default="./data/",
                        help="Name of data dir to save data to.")

    args = vars(parser.parse_args())
    print(args)
    main(**args)
