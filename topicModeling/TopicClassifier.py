import numpy as np
import torch
import torch.nn as nn

class TopicClassifier(nn.Module):
    def __init__(self, numMessages, vocab):
        super(TopicClassifier, self).__init__()

        inSize = len(vocab)
        hiddenSize1 = 64
        hiddenSize2 = 128
        self.dense1 = nn.Linear(inSize, hiddenSize1)
        self.dense2 = nn.Linear(hiddenSize1, hiddenSize2)
        self.dense3 = nn.Linear(hiddenSize2, 1)

    def forward(self, x):
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        x = torch.sigmoid(x)
        return x