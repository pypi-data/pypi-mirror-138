# import useful libraries
import pickle
from importlib.machinery import SourceFileLoader
import pickle
import tensorflow as tf


class ModelWeights():
    '''
    Parameters: username, password

    ***
    Please provide a valid username and password
    Call getToken method on Login to get new token for provided
    username and password
    '''

    def __init__(self):

        self.__model_name = input("Enter Username ")

    def generateweights(self):

        '''
        Make sure model file and weights are in current directory
        Parameters: modelname

        modelname: model file name eg: vggnet, if file name is vggnet.py
        weights: upload pre trained weights if set True. Default: False

        *******
        return: model unique Id
        '''

        tf.keras.backend.clear_session()
        model = SourceFileLoader(model_name, f'{model_name}.py').load_module()
        model = model.MyModel()
        # print model input and output
        print("Model input shape: ", int(model.input_shape[2]))
        print("Model output shape: ", model.output_shape[-1])
        # Dump weights
        w = model.get_weights()
        output = open(f"{model_name}_weights.pkl", "wb")
        pickle.dump(w, output)
        output.close()
        print(f"Dumped new weights for {model_name} model")

    def checkWeights(self, modelId: str, datasetId: str):

        """
        Role: Link and checks model & datasetId compatibility
              create training plan object

        parameters: modelId, datasetId
        return: training plan object
        """
        # Load weights to check if it works
        w = open(f'{model_name}_weights.pkl', 'rb')
        we = pickle.load(w)
        try:

            model.set_weights(we)
            model.summary()
        except ValueError:
            print("Corrupt or Incompatible weights")
