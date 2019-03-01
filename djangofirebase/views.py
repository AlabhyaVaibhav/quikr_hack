import pyrebase
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from mysite.exceptions import ServiceUnavailable
from .constants import (
    month_hourly_revenue_data, month_hourly_adcount_data,
    daily_hourly_adcount_data, daily_hourly_revenue_data, daily_hourly_revenue_current_data,
    daily_hourly_adcount_data_increase, daily_hourly_revenue_data_increase,
    daily_hourly_adcount_data_decrease, daily_hourly_revenue_data_decrease,
)
from .utils import mock_revenue_sets



# Create your views here.
class FirebaseListApiView(APIView):
    def get_prices(self):
        mock_revenue_sets()

        try:
            firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
            db = firebase.database()

            current_role = "deliverycollection"
            current_city = "bangalore"
        
            results = db.child("jobs").child("2018").child("feb").child("1").child("friday").child(current_role + "_" + current_city).get()
            # print('=========', results.val())

            return results.val()
        except Exception:
            raise ServiceUnavailable

    def get(self, request):
        prices = self.get_prices() or {}
        return JsonResponse(prices, safe=False)


class FirebaseCreateNodeApiView(APIView):
    version = 'v1'
    averageAdCount = daily_hourly_adcount_data
    averageRevenue = daily_hourly_revenue_data
    currentAdCount = daily_hourly_adcount_data
    currentRevenue = daily_hourly_revenue_current_data

    def get(self, request):
        current_date = datetime.now() + timedelta(hours=5, minutes=30)
        hour = int(request.query_params.get('hour', 0))
        response_json = {}

        if hour is not None:
            child_key = "trainingData/{0}/{1}/{2}/{3}".format(self.version, current_date.month, current_date.day, hour)
            response_json = self.get_response_json(hour)

            firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
            db = firebase.database()
            db.child(child_key).update(response_json)
        else:
            pass

        return JsonResponse(response_json)

    def get_response_json(self, hour):
        response_json = {
            "averageAdCount": self.averageAdCount[hour],
            "averageRevenue": self.averageRevenue[hour],
            "currentAdCount": self.currentAdCount[hour],
            "currentRevenue": self.currentRevenue[hour]
        }

        return response_json


class FirebaseCreateNodeV2(FirebaseCreateNodeApiView):
    version = 'v2'
    # averageAdCount = daily_hourly_adcount_data
    # averageRevenue = daily_hourly_revenue_data
    currentAdCount = daily_hourly_adcount_data_increase
    currentRevenue = daily_hourly_revenue_current_data


class FirebaseCreateNodeV3(FirebaseCreateNodeApiView):
    version = 'v3'
    # averageAdCount = daily_hourly_adcount_data
    # averageRevenue = daily_hourly_revenue_data
    currentAdCount = daily_hourly_adcount_data_decrease
    currentRevenue = daily_hourly_revenue_current_data
