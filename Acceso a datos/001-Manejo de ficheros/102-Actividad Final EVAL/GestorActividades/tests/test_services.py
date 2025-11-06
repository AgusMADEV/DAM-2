import unittest
from services.activity_service import ActivityService
from domain.models import Activity


class TestServices(unittest.TestCase):
    def setUp(self):
        # use a temp file location to avoid interfering with user's data
        self.svc = ActivityService()

    def test_create_and_find(self):
        a = Activity(title='Test Svc', category='work', date='2025-11-05', duration_min=45)
        self.svc.create(a)
        found = self.svc.find(a.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.title, 'Test Svc')


if __name__ == '__main__':
    unittest.main()
