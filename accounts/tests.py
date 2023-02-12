from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your tests here.
class SignupPageTest(TestCase):
    def test_url_exists(self):
        response = self.client.post("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.post(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "dammy@dm.com",
                "age": 33,
                "password1": "test123passw",
                "password2": "test123passw",
            },
        )
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, "testuser")
        self.assertEqual(users[0].email, "dammy@dm.com")
        self.assertEqual(users[0].age, 33)
