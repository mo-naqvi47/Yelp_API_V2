import requests
import json #this module will let us convert the json into a string
import pandas as pd 
from pandas.io.json import json_normalize #7.24.2020 - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html
writeHeader = True

#enter key
api_key=""

#header dictionary 
headers = {'Authorization': 'Bearer %s' % api_key}

#Saving the URL as a variable
url='https://api.yelp.com/v3/businesses/search'


with open('T:\Share\Audit\Mo\Python\geocode.csv') as csvCoordinates:
    coordinates = csvCoordinates.read().split('\n')
    #print (coordinates)
    for n in range(1, len(coordinates)):
        line = coordinates[n].split(',')
        if not line: continue
        lat = line[0]
        lon = line[1]
        params = {'latitude': lat, 'longitude': lon,'limit':1}
        #standard syntax for the requests library. Could also write 'r = requests.get('https://..)
        # Making a get request to the API
        response = requests.get(url, params=params, headers=headers)
        
        #print(response.text)
        #json_text = response.text
        #print(json_text)
        
        #Extracting JSON data from the response. 
        #Responses now will be a string in a JSON format. Need to convert it. Calling JSON method and convert string to dictionary that we can iterate through
        #Storing result to variable
        #Isolates the JSON data from the response object (parses the data from the metadata)
        business_data = response.json() #now data is a dictionary
        #print(business_data)
        #notice that data is in a dictionary with info inside of the businesses key as a list! 
        
        #Passing JSON data from the response into a pandas dataframe. The necessary data is under the dictionary key "businesses"
        #load data into a pd dataframe not read_json
        #biz_data = pd.DataFrame(business_data["businesses"])
        #print(biz_data.head(2))
        
        
        #Printing dataframe types to see what information were getting 
        #print(biz_data.dtypes)
        
        
        #printing columns containing nested data
        #print(biz_data[["categories", "coordinates", "location"]].head())
        
        #pandas.io.json - a submodule for reading and writing JSON using functions
        #json_normalize flattens nested json
        #json_normalize will take a dictionary/lsit of dictionaries (like pd.Dataframe() does, so dataframe will work for json normalize)
        #default flattened column name pattern: attribute.nestedattribute
        #Choose a different separator with the sep argument(the (.) seperator interferes with pandas .notation for column selection. so use _ with sep)
        #now the nested attributes will have thier own columns
        #normalize = json_normalize(business_data['businesses'], sep="_")
        #print(list(normalize))
        #however, if you look at categories, it still isnt parsed exactly
        #you can write your own custom function, or decide it's irrelevant for the analysis
        #print(normalize.categories.head())
        
        #KeyError: "Try running with errors='ignore' as key 'title' is not always present"
        
        #Another option is to use json_normalize's record path, meta, and metaprefix arguments 
        #record_path takes a string or list of string attributes to the nested data, like listing folders in a file path
        #meta takes a list of other attributes to load to the dataframe
        #so nested data can be flattened by passing record paths as sublists 
        #to make clear what came from where and avoid duplicate column names, use meta_prefix (string to prefix to meta column names)
        #pass the business data to json normalize, specify the seperator, set record path to categories, get the meta name, alias, rating, coordinates. to flatten coordinates, you provide sublists as seen below for both latitude and longitude. biz and categories will have a meta_prefix to differentiate them
        #view the data with print(df.head(4))
        #title doesn't work always, so excluding it
        #errors{‘raise’, ‘ignore’}, default ‘raise’
        #Configures error handling.
        #‘ignore’ : will ignore KeyError if keys listed in meta are not always present.
        #‘raise’ : will raise KeyError if keys listed in meta are not always present.
        df = json_normalize(business_data['businesses'],
                           errors='ignore',  
                           sep='_',
                           #record_path=['location'],
                           meta=['id',
                                 'alias',
                                 'name',
                                 'is_closed',
                                 'url',
                                 'review_count',
                                 'rating',
                                 ['coordinates', 'latitude'],
                                 ['coordinates', 'longitude'],
                                 'transactions',
                                 'price',
                                 ['location', 'address1'],
                                 ['location', 'address2'],
                                 ['location', 'address3'],
                                 ['location', 'city'],
                                 ['location', 'zip_code'],
                                 ['location', 'country'],
                                 ['location', 'state'],
                                 ['location', 'display_address'],
                                 'phone',
                                 'display_phone',
                                 'distance'],
                            meta_prefix='business_')

        #print(df.head())


        #======================7.28
        #how can i add location and transactions to the index and make it work?
        #how can i append alias/categories if it's a duplicate
        #offset
        #write all to CSV 
        

        
        
        #view summary statistics using describe(). data must be loaded into pandas
        #business_data.describe()
        
        #now lets take a look at the keys that have been sent back to us 
        #print(business_data.keys())
        
        #For each "biz" in business_data's "businesses", give me the biz name
        #for biz in business_data['businesses']:
            #print(biz['id'])
    
        #packages_json = r.json()
        # proceed only if the status code is 200
        #print('The status code is {}'.format(r.status_code))
        # checking output from call

        if writeHeader is True:    
            df.to_csv('T:\Share\Audit\Mo\Python\geocodepandasio.csv', encoding='utf-8', index=False, mode='a', header=True)
            writeHeader = False
        else:
            df.to_csv('T:\Share\Audit\Mo\Python\geocodepandasio.csv', encoding='utf-8', index=False, mode='a', header=False)
        
        
        #df.to_csv('T:\Share\Audit\Mo\Python\geocodepandasio.csv', encoding='utf-8', index=False, mode='a', header=False)
        
        Resources: 
            Pandas Cheat sheet 
            https://stackoverflow.com/questions/55906053/pandas-dataframe-only-writing-last-row-to-csv
                https://medium.com/@robblatt/use-python-and-pandas-to-append-to-a-csv-503bf22670ce
                https://stackoverflow.com/questions/28387002/keep-header-while-appending-to-pandas-dataframe-w-python
                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
                        https://github.com/pandas-dev/pandas/issues/27220
                            https://www.kaggle.com/jboysen/quick-tutorial-flatten-nested-json-in-pandas
                                https://stackoverflow.com/questions/53198931/using-pandas-and-json-normalize-to-flatten-nested-json-api-response
                                    https://stackoverflow.com/questions/47242845/pandas-io-json-json-normalize-with-very-nested-json
                                        https://pandas.pydata.org/pandas-docs/version/0.21.1/generated/pandas.io.json.json_normalize.html
                                            
