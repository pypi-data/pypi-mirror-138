
#import libraries
from MyHeartCounts import MyHeartCounts
import datetime
##############################

#Initilize a MyHeartCounts object
#MHC = MyHeartCounts(user_password_file_path = 'synapseAccess.txt',synapseCachePath ='/oak/stanford/groups/euan/projects/mhc/code/ali_code/data/synapseCache')
MHC = MyHeartCounts(user_password_file_path='../../synapseAccess.txt',synapseCachePath='/Users/ajaved/Three/MHC_DataBase/code/synapseCache')
#Rev up your engine!! -- Setting up of cache and other administrative scripts
MHC.start()
#load a studies
MHC.loadStudy(studyName = 'HealthKitDataCollector',studyTable = 'syn3560085',limit = 1000)
MHC.loadStudy(studyName = 'mindset_adequacy',studyTable = ' syn18143711')
MHC.loadStudy(studyName = 'AB_TestResults',studyTable = 'syn7188351')

#unquire users in our analysis. start with smallest, mindset
users= MHC.Studies[1].studyUsers
#get users of all studies
users.intersection(MHC.Studies[2].studyUsers)
    
#we are down to 1044 users now. Let us see how much data they have in healthkit data collector. Lets start with 10 users just to check
#download all data
users = sorted(list(users))
#initial users are sort of testing users.
for u in users[500:510]:
    dt = datetime.datetime(2018, 4, 30, 18, 0).date()
    MHC.Studies[0].retrieve_blobs(blob_names=['data.csv'], healthCodes=[u], silent=False)
    for i in range(0, 270):
        ints = MHC.Users[0].get_interaction(dt,awsCachePath='/Users/ajaved/Three/ali_code/AWS/mobile-analytics/mobile-analytics/')
        dt += datetime.timedelta(days=1)


print('complete')