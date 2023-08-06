#import useful libraries
import getpass
import requests
import json
import getpass, os
import ast
import uuid
from .upload import Model
from .linkModelDataSet import LinkModelDataSet

class User():

    '''
    Parameters: username, password

    ***
    Please provide a valid username and password
    Call getToken method on Login to get new token for provided
    username and password
    '''

    def __init__(self):

        self.__username = input("Enter Username ")
        self.__password = getpass.getpass("Enter Password ")
        self.__token = self.login()
        self.__weights = False

    def login(self):
        '''Function to get Token for username provided'''
        try:
            url = "https://xray-backend-develop.azurewebsites.net/api-token-auth/"
            r = requests.post(url, data = {"username": self.__username, "password": self.__password})
            if r.status_code == 200:
                print(f"Logged in as {self.__username}")
            token = json.loads(r.text)['token']
            return token
        except Exception as e:
            print("Login credentials are not correct. Please try again.")
            print("\n")
            return ""

    def logout(self):
        '''Call this to logout from current sesion'''
        try:
            url = "https://xray-backend-develop.azurewebsites.net/logout/"
            r = requests.post(url)
            if r.status_code == 200:
                self.__token = None
                print("You have been logged out.")
                print("\n")
        except Exception as e:
            print("Failed to logout")
            print("\n")
            return None
            
    def uploadModel(self,modelname:str,weights=False):

        '''
        Make sure model file and weights are in current directory
        Parameters: modelname

        modelname: model file name eg: vggnet, if file name is vggnet.py
        weights: upload pre trained weights if set True. Default: False

        *******
        return: model unique Id
        '''
        try:
            if self.__token == "":
                print("You are not Logged in. Please go to Login step.")
            self.__weights = weights
            model = Model(modelname,self.__token,weights)
            self.__modelId = model.getNewModelId()
            if self.__modelId != "":
                text = colored(f'/"{modelname}/" Upload successful.', "green")
                print(text, "\n")
            else:
                text = colored(f'Server: Model {modelname} upload failed!', 'red')
                print(text, "\n")
        except:
            text = colored('You are not Logged in. Please go to Login step.', 'red')
            print(text, "\n")

    def linkModelDataset(self,datasetId:str):

        """
        Role: Link and checks model & datasetId compatibility
              create training plan object
              
        parameters: modelId, datasetId
        return: training plan object
        """
        try:
            trainingObject = LinkModelDataSet(self.__modelId,datasetId,self.__token,self.__weights)
            if trainingObject:
                return trainingObject
            # else:
            #     text = colored('You are not Logged in. Please go to Login step.', 'red')
            #     print(text, "\n")
        except:
            text = colored('You are not Logged in. Please go to Login step.', 'red')
            print(text, "\n")

