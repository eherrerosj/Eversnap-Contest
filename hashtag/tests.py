### Author: Enrique Herreros (eherrerosj@gmail.com)
### Django assignment for EverSnap. July 2014

from django.test import TestCase

# Hopefully we will get a 200 HTTP code when testing albums webpage
class Albums(TestCase):
    def test_index(self):
        resp = self.client.get('/albums/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('pictures' in resp.context) # the whole Album should be in the context

# Hopefully we will get a 200 HTTP code when testing REST API webpage
class Restapi(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
		
# Hopefully we will get a 200 HTTP code when testing mostpopular webpage
class Mostpopular(TestCase):
    def test_index(self):
        resp = self.client.get('/mostpopular/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('top7' in resp.context) # top7 set of Pictures should be in the context
