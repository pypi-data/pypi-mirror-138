#python libraries needed in code
#from Interaction.Interaction import Interaction
from collections import defaultdict
import os
import gzip
import json
import datetime
class User:
    def __init__(self,healthCode):
        ##############################
        # author: Ali Javed
        # October: 3 February 2022
        # email: ajaved@stanford.edu; alijaved@live.com
        #############################
        # Description: Class is used to access Amazon Web Services interaction data.
        
        # Inputs:
        # HealthCode: Health Code is the only required entry for a user. If we do not have a health code, we can not initilize a user.
       
        #To access Amazon S3 a key needs to be set up. For instructions
        # Amazon Key: Figure out how to best set this
        
        #Output
        #An Object of MyHeartCounts
    
        ########################################
        
        self.healthCode = healthCode
        self.awsID = None
        self.interactions = defaultdict(lambda: [])
        self.awsCachePath = None
        
    def set_attributes(self, user_attributes):
            #############################
            # Description: Set other attribuributes using a dictionary.

            # Inputs:
            # user_attributes: Dictionary of user attributes. Acceptable keys are
            #['healthCode','daysInStudy','weight','gender','bloodType','skinType','height','dob']
            #weight is assumed to be in lbs
            #dob is approximately calculated by subtracting age from createdOn date.
            # Output:
            # self.Users: List of user objects that contain all the loaded users.

            ########################################
            if 'healthCode' not in user_attributes:
                print('Can not add user attributes. Health code is missing in the dictionary.')
                return False
            if self.healthCode != user_attributes['healthCode']:
                print('Can not add user attributes. HealthCodes do not match.')
                return False
            if len(user_attributes.keys()) != 10:
                print("Please check if all 10 attriburtes are present in user dictionary ['healthCode','daysInStudy','weight','gender','bloodType','skinType','height','dob'],'createdOn'.")
                
            #set attributes
            self.createdOn = user_attributes['createdOn']
            self.daysInStudy = user_attributes['daysInStudy']
            self.weight = user_attributes['weight']
            self.gender = user_attributes['gender']
            self.bloodType = user_attributes['bloodType']
            self.skinType = user_attributes['skinType']
            self.height = user_attributes['height']
            self.dob = user_attributes['dob']
            self.awsID = user_attributes['awsID']
            
            
            return True

    def get_interaction(self,date,awsCachePath = '/oak/stanford/groups/euan/projects/mhc/code/ali_code/data/mobile-analytics/'):
        #############################
        # Description: Get user interactions from aws data on oak.  Currently only 2018 onwards dates are supported. For 2017 or early 2018 the path is different.

        # Inputs:
        # date: date for which all interactions of a particular user are to be loaded
        #Output:
        # interactions_loaded: Number of interactions loaded for particular day for the user
        ########################################
        #set aws cache path
        self.awsCachePath = awsCachePath
        #extract year month and day form the date to build a path
        year = date.year
        month = date.month
        if len(str(month)) ==1:
            month = '0'+str(month)
        day = date.day
        if len(str(day)) == 1:
            day = '0'+str(day)

        path = awsCachePath+'pinpoint'+str(year)+'/'+str(month)+'/'+str(day)

        # The interactions can be in the folder of the same date, or next date. This maybe because of multiple timezone issue.
        date+=datetime.timedelta(days=1)
        year = date.year
        month = date.month
        if len(str(month)) == 1:
            month = '0' + str(month)
        day = date.day
        if len(str(day)) == 1:
            day = '0' + str(day)
        path2 = awsCachePath + 'pinpoint' + str(year) + '/' + str(month) + '/' + str(day)

        # Get the list of all files in directory tree at given path
        listOfFiles = list()

        if os.path.exists(path):
            for (dirpath, dirnames, filenames) in os.walk(path):
                listOfFiles += [os.path.join(dirpath, file) for file in filenames if file.endswith('.gz')]
        if os.path.exists(path2):
            for (dirpath, dirnames, filenames) in os.walk(path2):
                listOfFiles += [os.path.join(dirpath, file) for file in filenames if file.endswith('.gz')]

        #load data from paths
        json_list = []
        if len(listOfFiles)>0:
            for file in listOfFiles:
                for line in gzip.open(file, 'r'):
                    line = line.decode("utf-8")
                    json_list.append(json.loads(line))


        #for each interaction loaded, check if user has an interaction for that day.
        interactions_loaded = 0

        for row in json_list:
            #if current user
            if 'client' in row:
                if 'client_id' in row['client']:
                    if row['client']['client_id'] == self.awsID:
                        interactionDate = datetime.datetime.fromtimestamp(row['event_timestamp'] / 1e3).date()
                        if interactionDate== date:
                            row['event_timestamp'] = datetime.datetime.fromtimestamp(row['event_timestamp'] / 1e3)
                            self.interactions[interactionDate].append(row)
                            interactions_loaded+=1



        return interactions_loaded







