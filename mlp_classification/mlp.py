import torch.nn as nn
import torch.nn.functional as F


class MLP_NN(nn.Module):
    def __init__(self):
        super().__init__()
        
        hiddenLayer1Nodes = 256
        hiddenLayer2Nodes = 128
        hiddenLayer3Nodes = 64

        # first dense layer, assumes flattened input, and knows the input size
        self.layer1 = nn.Linear(4, hiddenLayer1Nodes)
        # batch normalization to help w vanishing gradients
        self.bn1 = nn.BatchNorm1d(hiddenLayer1Nodes)
        # first layer activation function: tanh 
        self.layer1Act = nn.Tanh()

        # # second layer 
        self.layer2 = nn.Linear(hiddenLayer1Nodes, hiddenLayer2Nodes)
        # batch normalization
        self.bn2 = nn.BatchNorm1d(hiddenLayer2Nodes)
        # second layer activation function: ReLU
        self.layer2Act = nn.ReLU()

        # thrid layer 
        self.layer3 = nn.Linear(hiddenLayer2Nodes, hiddenLayer3Nodes)
        # batch normalization
        self.bn3 = nn.BatchNorm1d(hiddenLayer3Nodes)
        # third layer activation function: ReLU
        self.layer3Act = nn.ReLU()
        

        # ouput layer, sigmoid activaiton for binary classification
        self.output = nn.Linear(hiddenLayer3Nodes, 1)
        self.outputAct = nn.Sigmoid()


    def forward(self, x):       
        x = x.flatten(1) 
        # layer 1
        x = self.layer1(x)
        x = self.bn1(x)
        x = self.layer1Act(x)
        # print(x)

        #layer2
        x = self.layer2(x)
        # x = self.bn2(x)
        x = self.layer2Act(x)
        # print(x)

        # layer3
        x = self.layer3(x)
        # x = self.bn3(x)
        x = self.layer3Act(x)


        #output 
        x = self.output(x)
        x = self.outputAct(x)
        
        # yay mlp classification hopefully
        return x
        