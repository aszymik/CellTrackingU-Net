import sys
import os
import rasterio
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import torch
import pandas as pd
# from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from PIL import Image
import torch.nn as nn
from helper_utils import *
from U_Net_helper_functions import *

class TIF_dataset(Dataset):

    def __init__(self, path_list_data, path_list_label, transform=None):
        """

        All of our data is in the same format. I sugest using the silver truths as they are in the format ideal for training.
        I dont understand how the golden truths are suposed to work, we need to look into that. (especialy in the file PhC-C2DH-U373)

        Arguments:
            path_list_data: list of paths to tif files that will be datapoints
            path_list_label: list of paths to tif files that will be labels
            transform (callable, optional): Optional transform to be applied
                on a sample.

        Returns : a pair of tensors of shape (1, W, H), coresponding to data and label
        """
        self.path_list_data = path_list_data
        self.path_list_label = path_list_label
        self.transform = transform

    def __len__(self):
        return len(self.path_list_data)

    def __getitem__(self, idx):
        image = Image.open(self.path_list_data[idx])
        image_np = np.array(image)
        label = Image.open(self.path_list_label[idx])
        label_np = np.array(label)
        label_np = np.where(label_np != 0, 1, label_np)

        image_tensor = torch.from_numpy(image_np).unsqueeze(0)
        label_tensor = torch.from_numpy(label_np).unsqueeze(0)

        image_tensor = image_tensor.float() / np.mean(image_np) #normalizing the image tensor
        label_tensor = label_tensor.float()


        if self.transform:
            image_tensor = self.transform(image_tensor)
            label_tensor = self.transform(label_tensor)

        return image_tensor, label_tensor