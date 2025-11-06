import unittest
from domain.models import Activity


class TestModels(unittest.TestCase):
    def test_activity_to_from_dict(self):
        a = Activity(title='Test', category='study', date='2025-11-05', duration_min=30, notes='ok')
        d = a.to_dict()
        b = Activity.from_dict(d)
        self.assertEqual(b.title, 'Test')
        self.assertEqual(b.category, 'study')


if __name__ == '__main__':
    unittest.main()
