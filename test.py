import numpy as np
import matplotlib.pyplot as plt
import requests


def generate_average_revenue_hourly():
    arr = [11537,7342,4673,3296,799,5593,2647,12838,24512,34047,51511,67077,84281,83239,68334,60459,63325,61832,45641,34226,29002,23878,22646,20790]
    arr1 = []
    for i in range(len(arr)):
        arr1.append((i, arr[i],))

    points = np.array(arr1)
    x = points[:, 0]
    y = points[:, 1]

    # calculate polynomial
    z = np.polyfit(x, y, 14)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 24)
    y_new = f(x_new)

    plt.plot(x, y, 'o', x_new, y_new)
    plt.xlim([x[0] - 1, x[-1] + 1])
    plt.show()

    return y, y_new

# generate_average_revenue_hourly()


def mock_v1_data():
    for i in range(24):
        requests.get('http://localhost:8000/firebase/v1/node?hour={0}'.format(i))

# mock_v1_data()

def mock_v2_data():
    for i in range(24):
        requests.get('http://localhost:8000/firebase/v2/node?hour={0}'.format(i))

mock_v2_data()

def mock_v3_data():
    for i in range(24):
        requests.get('http://localhost:8000/firebase/v3/node?hour={0}'.format(i))

mock_v3_data()
