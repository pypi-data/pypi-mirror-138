
#import libraries
from MyHeartCounts import MyHeartCounts
##############################

#Initilize a MyHeartCounts object
#MHC = MyHeartCounts(user_password_file_path = 'synapseAccess.txt',synapseCachePath ='/oak/stanford/groups/euan/projects/mhc/code/ali_code/data/synapseCache')
MHC = MyHeartCounts(user_password_file_path='synapseAccess.txt',synapseCachePath='/Users/ajaved/Three/MHC_DataBase/code/synapseCache')
#Rev up your engine!! -- Setting up of cache and other administrative scripts
MHC.start()
#load a studies
MHC.loadStudy(studyName = 'HealthKitDataCollector',studyTable = 'syn3560085')
MHC.loadStudy(studyName = 'mindset_adequacy',studyTable = ' syn18143711')
MHC.loadStudy(studyName = 'AB_TestResults',studyTable = 'syn7188351')

#unquire users in our analysis. start with smallest, mindset
users= MHC.Studies[1].studyUsers
#get users of all studies
users.intersection(MHC.Studies[2].studyUsers)
    
#we are down to 1044 users now. Let us see how much data they have in healthkit data collector. Lets start with 10 users just to check
#download all data
users = sorted(list(users))
c = 0
for i in range(len(users), 0, -10):
    print(str(10*c) +' of '+ str(len(users))+' downloaded.')
    MHC.Studies[0].retrieve_blobs(blob_names=['data.csv'], healthCodes=users[i-10:i], silent=False)
    c+=1


