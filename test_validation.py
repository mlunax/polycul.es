from unittest import TestCase
from jsonschema import validate
import json


DATABASE = 'dev.db'


def validatejson(body):
    with open('schema.json') as json_data:
        schema = json.load(json_data)
    return validate(json.loads(body), schema)


class EmptyHash(TestCase):
    def test(self):
        self.assertIsNone(validatejson('{}'))


class SingleNode(TestCase):
    def test(self):
        self.assertIsNone(validatejson('''{"lastId":2,
        "nodes":[
        {"id":1,
        "name":"Alice",
        "x":477.1,
        "y":297.6,
        "r":12,
        "index":0,
        "weight":0,
        "px":477.2,
        "py":297.4}
        ],
        "links":[]}
        '''))


class SingleNodeExtraParamaters(TestCase):
    def test(self):
        with self.assertRaises(Exception):
            validatejson('''
{"lastId":2,
        "nodes":[
        {"id":1,
        "name":"Alice",
        "x":477.1,
        "y":297.6,
        "r":12,
        "index":0,
        "weight":0,
        "px":477.2,
        "py":297.4,
        "watcher":"Eve"}
        ],
        "links":[]}
            ''')


class SingleNodeFullParamaters(TestCase):
    def test(self):
        self.assertIsNone(validatejson(
            '''
{"lastId":2,
  "nodes":[
  {
    "id":1,
    "name":"Alice",
    "x":480.2,
    "y":249.7,
    "r":"4",
    "index":0,
    "weight":0,
    "px":480.1,
    "py":249.9,
    "dashed":true
  }
  ],
  "links":[]
}
            '''
        ))


class TestLink(TestCase):
    def test(self):
        self.assertIsNone(validatejson(
            '''
{
   "links" : [
      {
         "strength" : 10,
         "target" : {
            "py" : 250,
            "index" : 1,
            "name" : "Bob",
            "y" : 250,
            "px" : 480,
            "weight" : 1,
            "x" : 480,
            "r" : 12,
            "id" : 2
         },
         "source" : {
            "index" : 0,
            "name" : "Alice",
            "y" : 250,
            "px" : 480,
            "py" : 250,
            "x" : 480,
            "r" : 12,
            "id" : 1,
            "weight" : 1
         }
      }
   ],
   "lastId" : 2,
  "nodes" : [
      {
         "py" : 250,
         "px" : 480,
         "y" : 250,
         "index" : 0,
         "name" : "Alice",
         "weight" : 1,
         "id" : 1,
         "r" : 12,
         "x" : 480
      },
      {
         "weight" : 1,
         "x" : 480,
         "id" : 2,
         "r" : 12,
         "py" : 250,
         "y" : 250,
         "index" : 1,
         "name" : "Bob",
         "px" : 480
      }
   ]
}
            '''
        ))


class TestLinkFullParamaters(TestCase):
    def test(self):
        self.assertIsNone(validatejson(
            '''
{
   "lastId" : 2,
   "nodes" : [
      {
         "px" : 506.708606373103,
         "y" : 286.523952566997,
         "name" : "Alice",
         "x" : 506.787452218671,
         "r" : 12,
         "index" : 0,
         "weight" : 1,
         "py" : 286.416448430355,
         "id" : 1
      },
      {
         "x" : 453.212547781329,
         "px" : 453.291393626897,
         "y" : 213.476047433002,
         "name" : "Bob",
         "r" : 12,
         "index" : 1,
         "weight" : 1,
         "py" : 213.583551569644,
         "id" : 2
      }
   ],
   "links" : [
      {
         "targetText" : "bob",
         "centerText" : "center",
         "dashed" : true,
         "sourceText" : "alice",
         "target" : {
            "y" : 213.476047433002,
            "px" : 453.291393626897,
            "x" : 453.212547781329,
            "name" : "Bob",
            "r" : 12,
            "index" : 1,
            "py" : 213.583551569644,
            "weight" : 1,
            "id" : 2
         },
         "source" : {
            "py" : 286.416448430355,
            "weight" : 1,
            "id" : 1,
            "name" : "Alice",
            "px" : 506.708606373103,
            "y" : 286.523952566997,
            "x" : 506.787452218671,
            "r" : 12,
            "index" : 0
         },
         "strength" : "5"
      }
   ]
}
            '''
        ))
