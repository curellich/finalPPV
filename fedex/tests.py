from django.test import TestCase
from .models import Category


# Create your tests here.

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='Category 1', surcharge_percentage=5)
        Category.objects.create(name='Category 2', surcharge_percentage=10)
        Category.objects.create(name='Category 3', surcharge_percentage=15)

    def test_category(self):
        category1 = Category.objects.get(name='Category 1')
        category2 = Category.objects.get(name='Category 2')
        category3 = Category.objects.get(name='Category 3')
        self.assertEqual(category1.surcharge_percentage, 5)
        self.assertEqual(category2.surcharge_percentage, 10)
        self.assertEqual(category3.surcharge_percentage, 15)

    def test_category_update(self):
        category1 = Category.objects.get(name='Category 1')
        category1.surcharge_percentage = 10
        category1.save()
        self.assertEqual(category1.surcharge_percentage, 10)

    def test_category_delete(self):
        category1 = Category.objects.get(name='Category 1')
        category1.delete()
        self.assertEqual(Category.objects.count(), 1) ## This test fails
