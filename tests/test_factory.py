"""
工厂数据测试
"""

from myblog import create_app


def test_config():
    assert not create_app().testing
    assert create_app("test").testing


def test_check_health(client):
    response = client.get("/check_health")
    assert response.data == b"Status: OK"
