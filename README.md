# Socrata-Deep-Search
Do deep level search of a data catalogue hosted by Socrata. Allows me to search the meta data from every dataset--including the meta data for the column properties. Written with Python. 

First I open a catologue of datasets--Socrata wrote for the City of Los Angeles a private dataset listing all datasets: 'The Dataset of Datsets'. I chose to extract a list from that dataset but later I discovered that a similar public list is available--that is linked as a comment in the intro to the script.

From the list of datasets I can pose a querey to slim down the list to relavent datasets: derived_view=False so that it is an original upload, type=map or type=table because I was lookign for datasets that can be pushed to ESRI's platform ie they have location datatypes.
NOTE: the 'requests' package has a great SQL dictionary implemented so that you can easily put in search queries without knowing the proper SQL syntax. Just put in the information as a dictionary-type and set that equal to 'params' when calling the requests function. (I'm slowly learning how great 'requests' is for api's. If there is something better then let me know!)

Once I had my list, I opened the .json file for every dataset and searched specifically within that dataset. If I found something I liked, I stored it into a csv file.
