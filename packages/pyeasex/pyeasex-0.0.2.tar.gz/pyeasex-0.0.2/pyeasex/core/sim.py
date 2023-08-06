import requests
import pandas as pd
import json

class EaseXFile():
  def __init__(self, resource_uuid):
    self.resource_uuid = resource_uuid
    self.data = None


class EaseXTimeSeries():
  def __init__(self, resource_uuid, start, stop, tags, fields):
    self.resource_uuid = resource_uuid
    self.start = start
    self.stop = stop
    self.tags = tags
    self.fields = fields
    self.data = None

class Simulation():
  def __init__(self, token, project_uuid):
    self.host = "https://app-backend.ease-x.com"
    self.token = token
    self.project_uuid = project_uuid
    self.geojson_list = []
    self.dataframe_list = []

  def fetch_data(self, ease_x_file):
    endpoint = f'{self.host}/api/s3/maplayer/data'
    headers = {"Authorization": f"Bearer {self.token}"}
    params = {
      "resource_uuid": ease_x_file.resource_uuid,
      "project_uuid": self.project_uuid,
    }
    with requests.get(endpoint, params=params, headers=headers, stream=True) as r:
      r.raise_for_status()
      with open(ease_x_file.resource_uuid, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192): 
          f.write(chunk)
    with open(ease_x_file.resource_uuid, 'r') as f:
      ease_x_file.data = json.loads(f.read())

  def fetch_dataframe(self, ease_x_time_series):
    endpoint = f'{self.host}/api/influx/data'
    headers = {"Authorization": f"Bearer {self.token}"}
    data = {
      "resource_uuid": ease_x_time_series.resource_uuid,
      "project_uuid": self.project_uuid,
      "start": ease_x_time_series.start,
      "stop": ease_x_time_series.stop,
      "tags": ease_x_time_series.tags,
      "fields": ease_x_time_series.fields 
    }
    r = requests.get(endpoint, json=data, headers=headers)
    ease_x_time_series.data = pd.read_json(r.json()["data"], orient ='index')

  def prepare(self):
    for ease_x_file in self.geojson_list:
      self.fetch_data(ease_x_file)
    for ease_x_time_series in self.dataframe_list:
      self.fetch_dataframe(ease_x_time_series)

  def run(self):
    pass