from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from accounts.models import User
from blog.models import Post


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(email="ab@ab.com", password="1020")
    return user


@pytest.fixture
def post_obj(common_user):
    post = Post.objects.create(user=common_user, title="test", state="blog")
    return post


@pytest.mark.django_db
class TestpostApi:

    def test_get_post_response_200_status(self, api_client, common_user):
        api_client.force_login(user=common_user)
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "state": "blog",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "state": "blog",
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_post_without_login_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "state": "blog",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("blog:api-v1:post-list")
        data = {
            "state": "blog",
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_get_post_detail_response_200_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        user = common_user
        api_client.force_authenticate(user=user)
        data = {
            "title": "test",
            "state": "blog",
        }
        api_client.post(url, data)

        url_detail = reverse("blog:api-v1:post-detail", kwargs={"pk": 1})
        response = api_client.get(url_detail)
        assert response.status_code == 200

    def test_get_post_detail_response_404_status(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url_detail = reverse("blog:api-v1:post-detail", kwargs={"pk": 1})
        response = api_client.get(url_detail)
        assert response.status_code == 404

    def test_edit_post_detail_response_200_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        user = common_user
        api_client.force_authenticate(user=user)
        data = {
            "title": "test",
            "state": "blog",
        }
        api_client.post(url, data)

        new_data = {
            "title": "edited",
            "state": "done",
        }
        url_detail = reverse("blog:api-v1:post-detail", kwargs={"pk": 1})
        response = api_client.put(url_detail, data=new_data)

        assert response.status_code == 200
        assert response.data["title"] == "edited"
        assert response.data["state"] == "done"

    def test_delete_post(self, api_client, common_user, post_obj):
        api_client.force_authenticate(common_user)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post_obj.pk})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Post.objects.filter(pk=post_obj.pk).exists() is False

    def test_delete_post_not_found(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": 9999})
        response = api_client.delete(url)
        assert response.status_code == 404

    def test_delete_post_with_anonymous_user(self, api_client, common_user):
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": 9999})
        response = api_client.delete(url)
        assert response.status_code == 401
