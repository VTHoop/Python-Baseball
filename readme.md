# Daily Baseball Game Statistical Analysis
Modeling of winning percentages as compared to those provided by Vegas

### Overview
This program will analyze the individual player statistics for a specific game and assign a betting line (based off of determined winning percentage) for that particular game.  

Both statistics-to-date and projected statistics are used to mesh into one final number.  The model is designed to utilize the work done by the folks at FanGraphs so that even if players are hot or cold to begin the season, then we can expect them to regress back to the mean which at this point is considered the projections provided.

Bovada is used for the analysis of sports betting lines.  However, to gain true efficiency, one would shop all sports books to gain the best price of bet.

5/19 - Splits have been added (Home, vs. Left/Right, etc.)

6/6 - MySportsFeed has promised an API to provide real time lineups and projected starting pitchers.  Currently, the lineups are hard coded.  This will be updated as soon as that is provided.

6/6 - Currently the analysis is done game by game.  An enhancement will be made to automatically model any games in which starting lineups have been posted for the day.

6/6 - A log of daily vegas lines and the lines created from this model will be posted to provide analysis of the model.

### Files:
Refer to "table_of_contents.txt" for a description of each of the files.

### Data Sources:
CSV files gathered from mysportsfeed.com  
XML files gathered from bovada.com  
CSV files gathered from fangraphs.com  
Website scraping of espn.com
Website scraping of rotowire.com

### Data Challenges:
The following are the keys used to merge the data sets and the inconsistencies between them:

MySportsFeed to FanGraphs - playerids are assigned by the source they come from.  Statistics were merged by using a combination of player's name and team.  If spelling differences occur in the name (nicknames for example), then the merge will not occur.  Inconsistencies will be addressed as they are identified.  In the result that a projected stat is not found, then the real statistics to date are used for projected stats as well.

MySportsFeed to ESPN - Statistics were merged by using a combination of player's name and team.  If spelling differences occur in the name (nicknames for example), then the merge will not occur.  In the result that a projected stat is not found, then the real statistics to date are used for projected stats as well.

MySportsFeed to Bovada - the keys used in the merging of these data sets is the team cities and team names.  No inconsistencies have been found to this point.

### Future Enhancements:


As the log grows, additional analysis of the model will be done to continually enhance it.
