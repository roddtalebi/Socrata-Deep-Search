#Build a script that can search through our Socrata Data Catalogue

#STRATEGY
# Filter for only original (derived_view=false) then for maps (type=map). print a list of those.
# Then search again for original (^) tables (type=table). of that list extract the u_id and
# then open each link to search for location data

#Sources
# http://docs.python-requests.org/en/latest/user/authentication/#basic-authentication
# https://stackoverflow.com/questions/26741193/socrata-soda-and-python
# https://stackoverflow.com/questions/27823583/is-there-a-socrata-api-for-reading-a-datasets-metadata
# https://stackoverflow.com/questions/29783413/is-there-a-socrata-api-for-reading-a-sites-catalog
# https://stackoverflow.com/questions/24745820/socrata-get-data-types-of-dataset-columns


##### NOTE ######
# Since the 'dataset of datasets' is not open to the public, can use this instead
# https://data.lacity.org/data.json
# every open data portal should have a similar one


import requests
from requests.auth import HTTPBasicAuth
username = 'rodd.talebi.intern@lacity.org'
password = '' #put password here
headers = {
	'X-App-Token': '', #put app key here [not secret one]
	'Content-Type': 'application/json'
	}
domain = 'https://data.lacity.org/'
UID = 'n2n7-ucjp'
url = domain+'resource/'+UID+'.json'

##################
# define function to look up website/json file and pull the data

def json_pull(url1, query):
	r = requests.get(url1, params=query, headers=headers, auth=HTTPBasicAuth(username,password))
	content = r.json()
	return content

##################
# define function to look up and extract metadata from each dataset

def meta_search(uid): # 'u_id' as string
	url0 = domain+'api/views/'+uid+'.json'
	query = ''
	info = json_pull(url0, query)
	return info

##################
# define function to see if the dataset has a column with dataTypeName = location

def location_check(columns):
	ncol = len(columns)
	check = False
	for i in range(0,ncol):
		if str(columns[i]['dataTypeName']) == 'location':
			check = True
			break
	return check

##################

import csv

#SET UP by creating and opening a csv file
with open("SocrataSearch.csv", 'w') as c:
	fieldnames = ['dataset name', 'type', 'dataset id', 'link', 'owner', 'owner id']
	writer = csv.DictWriter(c, fieldnames=fieldnames, restval=' ', extrasaction='ignore')
	writer.writeheader()
	
	####
	#FIRST look at original maps
	query1 = {'derived_view':'false', 'type':'map'}
	data = json_pull(url, query1)
	for dataset in data:
		meta = meta_search(str(dataset['u_id']))
		writer.writerow({
			'dataset name': str(meta['name']),
			'type': str(meta['displayType']),
			'dataset id': str(meta['id']),
			'link': domain+'resource/'+str(meta['id']),
			'owner': str(meta['owner']['displayName']),
			'owner id': str(meta['owner']['id'])
		})
		
	####
	#SECOND look at original tables with 'location' data 
	query2 = {'derived_view':'false', 'type':'table'}
	data = json_pull(url, query2)
	for dataset in data:
		meta = meta_search(str(dataset['u_id']))
		loc_check = location_check(meta['columns'])
		if loc_check == True:
			writer.writerow({
				'dataset name': str(meta['name']),
				'type': str(meta['displayType']),
				'dataset id': str(meta['id']),
				'link': domain+'resource/'+str(meta['id']),
				'owner': str(meta['owner']['displayName']),
				'owner id': str(meta['owner']['id'])
			})
		