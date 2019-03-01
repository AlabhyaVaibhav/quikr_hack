import numpy as np
# import matplotlib.pyplot as plt
import pyrebase
from django.conf import settings
from datetime import datetime, timedelta
from .constants import month_hourly_adcount_data, month_hourly_revenue_data, daily_hourly_revenue_data


def generate_average_revenue_hourly():
    arr = [
        (0, 16547), (1, 12141), (2, 6870), (3, 4493), (4,
  1348), (5, 8035), (6, 5776), (7, 15863), (8, 35052), (9, 54368), (10,
  94148), (11, 111377), (12, 142872), (13, 127734), (14, 106868), (15,
  109021), (16, 99235), (17, 100590), (18, 69164), (19, 64213), (20,
  46394), (21, 47453), (22, 39875), (23, 35032)]

    for i in range(len(arr)):
        arr[i] = (i, round(arr[i][1] / 6),)

    points = np.array(arr)

    x = points[:, 0]
    y = points[:, 1]

    # calculate polynomial
    z = np.polyfit(x, y, 14)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 24)
    y_new = f(x_new)

    # plt.plot(x, y, 'o', x_new, y_new)
    # plt.xlim([x[0] - 1, x[-1] + 1])
    # plt.show()
    # print(y_new)
    return y, y_new


def mock_revenue_sets():
    y, y_new = generate_average_revenue_hourly()
    # print(y, y_new)
    i = 0
    c = [[],[],[],[]]
    for i in range(4):
        j = 0
        for k in range(len(y)):
            print(y[j], y_new[j])
            b = round((y[j] + y_new[j]) / 2)
            j += 1
            c[i].append(int(b))

    for i in c:
        print(i)

    return c


def add_firebase_nodes():
    try:
        firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
        db = firebase.database()

        current_date = datetime.now() + timedelta(hours=5, minutes=30)
        child_key = "trainingData/{0}/{1}/{2}".format(current_date.month, current_date.day, current_date.hour)
        db.child(child_key).update({
            "averageAdCount": "0",
            "averageRevenue": "0",
            "currentAdCount": "0",
            "currentRevenue": "0"
        })
    except Exception:
        print("firebase error")


def get_daily_hourly_adcount():
    arr = []
    for i in range(len(month_hourly_adcount_data)):
        arr.append(round(month_hourly_adcount_data[i]/26, 2))
    print(arr)

def get_round_daily():
    arr = []
    for i in range(len(daily_hourly_revenue_data)):
        arr.append(round(daily_hourly_revenue_data[i], 2))
    print(arr)
    

def get_daily_hourly_revenue():
    arr = []
    for i in range(len(month_hourly_revenue_data)):
        arr.append(int(round(month_hourly_revenue_data[i]/26)))
    print(arr)
