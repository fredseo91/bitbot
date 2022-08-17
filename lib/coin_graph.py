import numpy as np
import matplotlib.pyplot as plt


def data_viewer(dataframe, type, day_length):

    size_x = len(dataframe.index)
    dataframe = dataframe[size_x - day_length : size_x]
    # print(dataframe)
    x = dataframe.index
    y = dataframe[type]

    plt.plot(x,y)



def raw_data_viewer(dataframe, day_length, name='default'):
    size_x = len(dataframe.index)
    dataframe = dataframe[size_x - day_length : size_x]

    x = dataframe.index
    y = dataframe

    plt.plot(x,y, label=name)
    plt.legend()

def show():
    plt.show()

#moving average
#https://wikidocs.net/4373
