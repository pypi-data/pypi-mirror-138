#!/usr/bin/env python
import requests
from .eureka import Eureka


class ApisClient(object):
    @staticmethod
    def get(service_name, endpoint, headers=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.get(url, headers=headers).json()
        return response

    @staticmethod
    def post(service_name, endpoint, body=None, headers=None, json=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.post(url, data=body, headers=headers, json=json)
        return response

    @staticmethod
    def put(service_name, endpoint, body=None, headers=None, json=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.put(url, data=body, headers=headers, json=json)
        return response

    @staticmethod
    def delete(service_name, endpoint, body=None, headers=None, json=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.delete(url, data=body, headers=headers, json=json)
        return response

