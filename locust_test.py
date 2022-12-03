from locust import HttpUser, task
from requests.auth import HTTPBasicAuth


class WebsiteUser(HttpUser):

    @task
    def prime(self):
        self.client.get(url='/prime/127')

    @task
    def invert(self):
        file = open("lena.jpg", "rb")
        data = file.read()
        self.client.post(url='/picture/invert', files={'file': data})

    @task
    def getTime(self):
        basic = HTTPBasicAuth("jakub", "&AxO96k0%")
        self.client.get(url='/current_time', auth=basic)
