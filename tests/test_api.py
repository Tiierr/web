import unittest
import json
from flask import url_for
from app import create_app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    # 用户已存在
    def test_register(self):
        data = {"username": "demo","password": "demo"}
        response = self.client.post(url_for('api.register'),
                                   content_type='application/json', data=json.dumps(data))
        self.assertTrue(response.status_code == 400)

    # 用户已在三个以上设备登录
    def test_login(self):
        data = {"username": "demo","password": "demo"}
        response = self.client.post(url_for('api.login'),
                                   content_type='application/json', data=json.dumps(data))
        self.assertTrue(response.status_code == 403)


    # token 错误
    def test_get_info(self):
        token = "meiyou"
        response = self.client.post(url_for('api.info'),
                                   content_type='application/json', data=json.dumps({"token":token}))
        self.assertTrue(response.status_code == 400)

    # token 错误
    def test_update_age(self):
        token = "meiyou"
        age = 15
        response = self.client.post(url_for('api.update_age'),
                                   content_type='application/json', data=json.dumps({"token":token, "age":age}))
        self.assertTrue(response.status_code == 400)

    # token 错误
    def test_logout(self):
        token = "meiyou"
        response = self.client.post(url_for('api.logout'),
                                   content_type='application/json', data=json.dumps({"token":token}))
        self.assertTrue(response.status_code == 400)

if __name__ == '__main__':
    unittest.main()
