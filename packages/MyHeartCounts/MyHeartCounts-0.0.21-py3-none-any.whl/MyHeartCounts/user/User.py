#python libraries needed in code
#from Interaction.Interaction import Interaction


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
            if len(user_attributes.keys()) != 9:
                print("Please check if all 9 attriburtes are present in user dictionary ['healthCode','daysInStudy','weight','gender','bloodType','skinType','height','dob'],'createdOn'.")
                
            #set attributes
            self.createdOn = user_attributes['createdOn']
            self.daysInStudy = user_attributes['daysInStudy']
            self.weight = user_attributes['weight']
            self.gender = user_attributes['gender']
            self.bloodType = user_attributes['bloodType']
            self.skinType = user_attributes['skinType']
            self.height = user_attributes['height']
            self.dob = user_attributes['dob']
            
            
            return True
            
