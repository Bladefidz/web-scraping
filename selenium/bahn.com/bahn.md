Looking for someone to program a python script to scrape information on train connections from German train website:
https://www.bahn.com/en/view/index.shtml

The script should take a list of train stations from a CSV file and look up all connections between all possible combinations of stations and store the returned information about the connections in a data file.


stationslist = pd.read_csv(StringIO(Stations.csv))

for each origin_station in stationlist
for each destination_station in stationlist

On www.bahn.com website: look up connections between origin_station and destination_station
on December 1st, 2017 that depart between 6 and 9 am.

Store all train connections in that time window in a dataset (Pandas).

For example Munich to Berlin may result in 5 possible train connections, with different departure times,
trip durations, types of trains ("Products"), number of required train changes. Each of these results should be 
stored in a separate row in the dataset.

Finally export the data as CSV file 


The script should only use open source python libraries if at all possible and should be written in a way that is easy to maintain.

I'm including the CSV file with station names. For testing purposes you can run this with a subsample of stations. I'm also including a file with an example of what the output file should look like. 
