# jenkem_data
data driven skate stuff for jenkemmag

### Articles

- **Greco**: http://www.jenkemmag.com/home/2019/07/31/statistical-analysis-every-jim-greco-clip/


## How To Add New Data

The shittiest part about this is creating the data. But it's really not that bad. Here's how:

We want a dataset with the following schema:


| Column | Description | Data Type |
|---|---|---|
| `clip_index` | The number of the video clip in which the clip occurred. For example, if the third clip of a video part is a line, each clip in the line should have a `clip_index` of `3`.|text|
| `trick_index` | The trick number, i.e. the `ith` trick in the video should have a `trick_index` of `i`. Each `trick_index` should be unique and consecutive, unless the trick is shown multiple times (e.g. double-angle or slow motion). | text |
| `trick` | Name of the trick. Try to use 'fs' and 'bs', and separate tricks in manuals with 'to'. | text |
| `switch` | Boolean indicating whether or not the trick was switch. `1` if yes, else leave blank. | number |
| `line` | Boolean indicating whether or not the trick was done in a line. `1` if yes, else leave blank. | number |
| `slowmo` | Boolean indicating whether or not the trick was filmed in slow motion. `1` if yes, else leave blank. | number |
| `obstacle` | Not-very-detailed description of obstacle. Should be `rail`, `ledge`, `manual`, `gap`, `stair`, `flat`, `hip`. (Use `obstacle_detailed` column to add more description). | text |
| `obstacle_detailed` | A slightly more detailed description of the obstacle. Try to use what's been used before (e.g. for `rail` use `handrail` or `shootout` or `flatbar`, or for `ledge`, use `hubba`, etc.). | text |
| `location` | Location of trick, if it's notable. Otherwise leave blank (don't worry too much about this). | text |
| `video` | Name of video. | text |


That is, for a given video part, add a row to the dataset above for each trick. 


#### Example

For [Koston's part](https://www.youtube.com/watch?v=8Y3_l_phKA4) in the 101 promo, I created [this dataset]().

For all of Greco's parts, I created [this dataset]().



### Adding the New Data

Once you're done, save the data as a `csv` or `xlsx` document.

Then:

**You Know Git**: Fork the repo, add data, and make a pull-request.

**You Don't Know git**: Email me the data/description! jdwlbr at gmail
