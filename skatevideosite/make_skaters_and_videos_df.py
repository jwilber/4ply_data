# -*- coding: utf-8 -*-
# author: Jared Wilber
"""make_skaters_and_videos_df.py
This script scrapes all skate videos on skatevideosite.com and creates a data-frame with the following schema:
    -
    -
    -
    -
Example:
    $ python make_skaters_and_videos_df.py
"""

import re
import requests
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

BASE_URL = "http://www.skatevideosite.com/index.php?page=skatevideos&sort=rating&p={}"
SITE_BASE_URL = 'http://www.skatevideosite.com{video}'
DICT_KEYS    = ['company', 'filmmaker', 'year', 'country']


def load_soup(base_url):
    # load a given url with beautifulsoup
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_video_urls(soup):
    # get urls to all skate videos on page
    skate_videos = soup.find_all('table', {"id": "skatevideos"})
    trs = skate_videos[0].find_all('td')
    tr_links = [tr.find_all('a') for tr in trs]
    videos_info = []
    for tr in tr_links:
        try:
            videos_info.append(tr[0].find_all('a', href=True))
        except: 
            continue
    video_urls = []
    for vid in videos_info:
        try:
            video_urls.append(vid[0]['href'])
        except:
            continue
    return video_urls


def get_skaters(soup):
    # get names of all skaters listed on page
    skater_links = soup.find_all('div', {"id": "skaterlist"})[0].find_all('a')
    return [a.text for a in skater_links]


def get_video_info(soup):
    # get basic info for current page's skate video
    video_dict = {k:[] for k in DICT_KEYS}
    for a in soup.find_all('table', class_="videoinfo")[0].find_all('a'):
        if "colspan" in a.attrs:
            continue
        else:
            href = a['href']
            if 'companies' in href:
                video_dict['company'] = a.text
            elif 'filmmakers' in href:
                video_dict['filmmaker'] = a.text
            elif 'year' in href:
                video_dict['year'] = a.text
            elif 'countries' in href:
                video_dict['country'] = a.text
    video_df = pd.DataFrame(list(video_dict.items())).set_index(0).T
    return video_df


def get_title(soup):
    # get title of current page's skate video
    return soup.find_all('div', class_='twelve columns')[0].find('h1').text


def make_video_df(soup):
    # create dataframe for current page's skate video
    lst_col = 'skater'
    skaters = get_skaters(soup)
    df = get_video_info(soup)
    video_title = get_title(soup)
    df['title'] = video_title
    df[lst_col] = [skaters]
    video_df = pd.DataFrame({
          col:np.repeat(df[col].values, df[lst_col].str.len())
          for col in df.columns.drop(lst_col)}
        ).assign(**{lst_col:np.concatenate(df[lst_col].values)})[df.columns]
    return video_df


def make_videos_info(video_urls):
    # create list of dataframes for all skate-videos on current page
    videos_info = []
    for vid in video_urls:
        full_vid_url = SITE_BASE_URL.format(video=vid)
        video_soup = load_soup(full_vid_url)
        try:
            video_df = make_video_df(video_soup)
            videos_info.append(video_df)
        except:
            continue
    return videos_info


def scrape_page(url):
    # scrape current page
    soup = load_soup(url)
    video_urls = get_video_urls(soup)
    videos_info = make_videos_info(video_urls)
    all_videos_df = pd.concat(videos_info)
    return all_videos_df


def scrape_all_videos(page_start, page_end):
    # scrape pages `page_start` to `page_end` for info
    all_video_dfs = []
    for i in range(page_start, page_end):
        print('Scraping page :', i)
        print()
        current_page = BASE_URL.format(i)
        page_scraped_df = scrape_page(current_page)
        all_video_dfs.append(page_scraped_df)
    all_video_dfs = pd.concat(all_video_dfs)
    return all_video_dfs


def resolve_name(name):
    if name == []:
        return ''
    return name


if __name__ == '__main__':

    all_videos_df = scrape_all_videos(1, 19)

    all_videos_df['company'] = all_videos_df.company.apply(lambda x: resolve_name(x))
    all_videos_df['year'] = all_videos_df.year.apply(lambda x: resolve_name(x))
    all_videos_df['title'] = all_videos_df.title.apply(lambda x: resolve_name(x))
    all_videos_df['filmmaker'] = all_videos_df.filmmaker.apply(lambda x: resolve_name(x))
    all_videos_df['country'] = all_videos_df.country.apply(lambda x: resolve_name(x))

    # sort videos descending
    all_videos_df.sort_values(by = ['company', 'year', 'title'], ascending=False, inplace=True)

    all_video_dfs.to_csv('skaters_and_videos.csv', index=False)
