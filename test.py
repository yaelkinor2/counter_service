import unittest
import xmlrunner
from app import app

class TestCounterService(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    
    # First GET without POST -> counter = 0
    def test_0(self):
        rv = self.app.get('/counter-service')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'0')
        
    # First POST + GET -> counter = 1
    def test_1(self):
        rv = self.app.post('/counter-service')
        self.assertEqual(rv.status, '200 OK')
        
        rv = self.app.get('/counter-service')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'1')
    
    # Second POST + GET -> counter = 2    
    def test_2(self):
        rv = self.app.post('/counter-service')
        self.assertEqual(rv.status, '200 OK')
        
        rv = self.app.get('/counter-service')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'2')
        
if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)