#python libraries needed in code
import csv
import synapseclient
import string


class Study:
    def __init__(self, studyName,studyTable,synapseCachePath= '',synapseUserName = '', synapsePassword=''):
        ##############################
        # author: Ali Javed
        # October: 3 February 2022
        # email: ajaved@stanford.edu; alijaved@live.com
        #############################
        # Description:Class initilizer for a study. Model assumes that study will be in a single table.
        
        # Inputs
        #StudyName: Study name for readability
        #TableName: Table name in synapse.
        #Below inputs should be inhereted from MyHeartCounts object
        #synapseCachePath: It is copied from MHC class
        #synapseUserName: Copied from MHC class
        #synapsePassword: Copied from MHC class
        #Output
        #Study Object
    
        ########################################
        
        #check if synapse connection is active (I am not sure if there is a timeout). If not activate it again.
        self.studyName = studyName
        self.studyTable = studyTable


        #study data. These are essentially rows in table. Parsed if you have a parser.
        self.observations = []

        #Users enrolled in study.
        self.studyUsers = set()


        #This is not the best, we should only connect to Synapse in MHC class. One place.
        self.synapseCachePath = synapseCachePath
        self.synapseConection = None
        self.synapseUserName = synapseUserName
        self.synapsePassword = synapsePassword

    def connectToSynapse(self, multi_threaded=True, silent=True):
        #############################
        # Description: Function connects to synapse, incase of longer analysis there may be a time out

        # Inputs:
        # multi_threaded: Synapse connection parameter
        # Output:
        # None
        #############################################################################
        # Synapse Connection
        # Read https://python-docs.synapse.org/build/html/index.html for details
        if self.synapseCachePath == '':
            synapseConnection = synapseclient.Synapse(silent=silent)
        else:
            synapseConnection = synapseclient.Synapse(cache_root_dir=self.synapseCachePath, silent=silent)
        synapseConnection.multi_threaded = multi_threaded

        # return the status of connection
        synapseConnection.login(self.synapseUserName, self.synapsePassword)
        return synapseConnection
        #############################################################################


    def retrieve_blobs(self,blob_names,healthCodes = [], silent = True):
        #############################
        # Description: Retrieve parse and clean blobs for a study.

        # Inputs:
        # observation: Row of dataframe in study table
        # Output:
        # observation: Parsed/cleaned row of dataframe provided as input

        ########################################

        # connect to synapse
        self.synapseConnection = self.connectToSynapse(silent=silent)
        #only if we have healthCodes to short list
        if len(healthCodes) > 0:
            # replace square brackets with parenthesis for SQL formatting
            healthCodes = "(%s)" % str(healthCodes).strip('[]')
            #get all data from the study table for healthCodes needed. Can further narrow down with dates here if data is unmanagable.
            query = "SELECT * FROM " + self.studyTable +" WHERE healthCode in "+str(healthCodes) + " ORDER BY createdOn DESC"
        else:
            query = "SELECT * FROM " + self.studyTable + " ORDER BY createdOn DESC"




        response = self.synapseConnection.tableQuery(query)
        #response_df = response.asDataFrame()

        #download all the blobs needed files study.
        files = self.synapseConnection.downloadTableColumns(response, blob_names)

        # logout of synapse
        status = self.synapseConnection.logout()
        if status != None:
            print('Logout not sucessfull')
        # Data loading and class initilization complete.



        #create a mapping of file handle id and path to replace handle id with path for easy parsing
        fileHandleId_to_Path = {}
        #add data.csv files or their path to observations
        for file_handle_id, path in files.items():
            #file handle id is the kay and its path is the value
            fileHandleId_to_Path[int(file_handle_id)] = path

        #change all blobnames to int
        for i in range(0, len(self.observations)):
            for blob_name in blob_names:
                try:
                    self.observations[i][blob_name] = int(self.observations[i][blob_name])
                except:
                    continue


        #For all observations loaded update with file paths of blobs we have
        for i in range(0,len(self.observations)):
            #for all the downloaded columns
            for blob_name in blob_names:
                #check if the blob was downloaded:
                if self.observations[i][blob_name] in fileHandleId_to_Path:
                    # replace file handle id with file path from cache
                    self.observations[i][blob_name] = fileHandleId_to_Path[self.observations[i][blob_name]]


        #decide which parser is to be used for this study
        parser_function_name = f"retrieve_{self.studyName}"


        #some libraries used in below line
        #The hasattr() method returns true if an object has the given named attribute and false if it does not.
        #In general, a callable is something that can be called. This built-in method in Python checks and returns True if the object passed appears to be callable, but may not be, otherwise False.
        #The getattr() method returns the value of the named attribute of an object. If not found, it returns the default value provided to the function.

        #check if we have a function for parsing, if so parse the observations in that study which have a file path
        if hasattr(self, parser_function_name):
            func = getattr(self, parser_function_name)
            if callable(func):
                status = func(blob_names)
                return status

        #if there is no parser.
        else:
            return False
            



    def add_observation(self,observation):
        self.observations.append(observation)

        return True

    def refresh_studyUsers(self):
        #############################
        # Description: Function refreshes the list of study users. Usefull to know which users are in the study

        # Inputs:
        # None. Function uses self
        # Output:
        # None. Function updates self

        ########################################

        self.studyUsers = set()
        for observation in self.observations:
            #each observation must have a healthCode
            self.studyUsers.add(observation['healthCode'])


        return True


    def retrieve_all_observations(self,blob_names,silent = True):
        #############################
        # Description: Retrieve all blobs


        # Inputs:
        # None. Function uses self.observations
        # Output:
        # None. Function updates self.observations

        ########################################
        #which healthCodes:
        #loop through all observations in self.observations and update them to parsed version if parser is available for current studyName.
        for i in range(0,len(self.observations)):
            healthCodes.add(observations[i]['healthCode'])

        #retrieve all the blobs
        status = self.retrieve_blobs(list(healthCodes),blob_names,silent)

        return status

    def isfloat(self,x):
        #############################
        # Description:Check if string is float

        # Inputs:
        # x: any str
        # Output:
        # True if it is a float.

        ########################################
        # which healthCodes:
        try:
            float(x)
            return True
        except:
            return False
    ########################################################
    ############## Write study/Table parsers here the function name format is parse_<tablename/study name>




    def retrieve_HealthKitDataCollector(self, blob_names):
        #############################
        # Description: Parser for health kit data collector for available blobs

        # Inputs:
        # observation: Row of dataframe in study table
        # Output:
        # observation: Parsed/cleaned row of dataframe provided as input

        #######################################

        for i in range(0,len(self.observations)):
            for blob_name in blob_names:
                # blob is a list of different measurements in the data.csv
                blob_list = []
                #if file path is not present for blob, this blob was not downloaded and not needed
                if self.isfloat(str(self.observations[i][blob_name])):
                    continue
                else:
                    try:
                        #open the blob
                        fopen = open(self.observations[i][blob_name], encoding='utf-8-sig')
                        csvr = csv.DictReader(fopen)

                        try:
                            for row in csvr:
                                #create a list of rows
                                blob_list.append(row)
                        except:
                            continue
                    except:
                        print('Error: File name parsing issue '+str(self.studyName) +' observation recordId: '+str(self.observations[i]['recordId'])+' blob name: '+str(blob_name))
                        continue

                    #add read csv here
                self.observations[i][str(blob_name)+str('_data')] = blob_list

        #parsing complete
        return True










        
        
        
        
 
