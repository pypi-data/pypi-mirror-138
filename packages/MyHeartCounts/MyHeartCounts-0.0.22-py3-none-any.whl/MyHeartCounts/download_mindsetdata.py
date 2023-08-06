# import libraries
from MyHeartCounts import MyHeartCounts

##############################
print('Start')
# Initilize a MyHeartCounts object
# MHC = MyHeartCounts(user_password_file_path = 'synapseAccess.txt',synapseCachePath ='/oak/stanford/groups/euan/projects/mhc/code/ali_code/data/synapseCache')
MHC = MyHeartCounts(user_password_file_path='../synapseAccess.txt',
                    synapseCachePath='/Users/ajaved/Three/MHC_DataBase/code/synapseCache')
# Rev up your engine!! -- Setting up of cache and other administrative scripts
MHC.start()

# load a studies
MHC.loadStudy(studyName='HealthKitDataCollector', studyTable='syn3560085', limit = 100)
#MHC.loadStudy(studyName='mindset_adequacy', studyTable=' syn18143711')
#MHC.loadStudy(studyName='AB_TestResults', studyTable='syn7188351')

# unquire users in our analysis. start with smallest, mindset
users = MHC.Studies[0].studyUsers
# get users of all studies
# we are down to 1044 users now. Let us see how much data they have in healthkit data collector. Lets start with 10 users just to check
# download all data
users = sorted(list(users))
for i in range(len(users), 0, -1):
    MHC.Studies[0].retrieve_blobs(blob_names=['data.csv'], healthCodes=users[i-2:i], silent=False)
    print(str(1044 - i) + ' of '+str(len(users))+ ' users downloaded.')
