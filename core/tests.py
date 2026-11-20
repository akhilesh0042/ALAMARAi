import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from wardrobe.models import ClothingItem
from ai.detector import detect_season, analyze_image


class WebsiteTestSuite(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user with a small wardrobe collection
        cls.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com"
        )
        cls.top = ClothingItem.objects.create(
            user=cls.user,
            name="Classic White Shirt",
            category="Top",
            brand="Ralph Lauren",
            color="White",
            season="All Season",
            occasion="Office",
            style="Formal",
            image="test_top.jpg"
        )
        cls.bottom = ClothingItem.objects.create(
            user=cls.user,
            name="Navy Trousers",
            category="Bottom",
            brand="Zara",
            color="Navy Blue",
            season="All Season",
            occasion="Office",
            style="Formal",
            image="test_bottom.jpg"
        )
        cls.shoes = ClothingItem.objects.create(
            user=cls.user,
            name="Leather Oxfords",
            category="Shoes",
            brand="Clarks",
            color="Brown",
            season="All Season",
            occasion="Office",
            style="Formal",
            image="test_shoes.jpg"
        )

    def setUp(self):
        self.client = Client()

    # 1. LANDING PAGE
    def test_landing_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ALAMARA")

    # 2. AUTHENTICATION
    def test_login_page_renders(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")

    def test_signup_page_renders(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        login_success = self.client.login(username="testuser", password="password123")
        self.assertTrue(login_success)

    # 3. DASHBOARD
    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_authenticated_dashboard(self):
        self.client.force_login(self.user)
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
        self.assertIn("total_items", response.context)
        self.assertEqual(response.context["total_items"], 3)

    # 4. WARDROBE
    def test_wardrobe_view_and_filtering(self):
        self.client.force_login(self.user)
        response = self.client.get("/wardrobe/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic White Shirt")

        # Filter by category
        res_filter = self.client.get("/wardrobe/?category=Top")
        self.assertEqual(res_filter.status_code, 200)
        self.assertContains(res_filter, "Classic White Shirt")

    # 5. ADD OUTFIT / AI UPLOAD
    def test_add_outfit_view(self):
        self.client.force_login(self.user)
        response = self.client.get("/wardrobe/ai-upload/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload clothing photograph")

        # Test alias endpoint /wardrobe/upload/
        response_alias = self.client.get("/wardrobe/upload/")
        self.assertEqual(response_alias.status_code, 200)

    # 6. STYLIST RECOMMENDATIONS
    def test_stylist_view(self):
        self.client.force_login(self.user)
        response = self.client.get("/stylist/")
        self.assertEqual(response.status_code, 200)

    # 7. USER PROFILE
    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    # 8. AI DETECTOR LOGIC
    def test_season_detector(self):
        winter_data = {"description": "Thick wool knit sweater", "fabric": "wool"}
        self.assertEqual(detect_season(winter_data), "Winter")

        summer_data = {"description": "Lightweight cotton tank top", "fabric": "cotton"}
        self.assertEqual(detect_season(summer_data), "Summer")

        rainy_data = {"description": "Waterproof nylon raincoat", "fabric": "nylon"}
        self.assertEqual(detect_season(rainy_data), "Rainy")

    def test_ai_detector_graceful_fallback(self):
        # Call with nonexistent or dummy path to verify safe fallback
        result = analyze_image("dummy_nonexistent_image.jpg")
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIn("category", result)
        self.assertIn("season", result)
        self.assertEqual(result["category"], "Top")
