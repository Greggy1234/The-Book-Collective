from django.test import TestCase
from .forms import RatingForm, ReviewForm


# Create your tests here
class TestReviewForm(TestCase):
    def test_form_is_valid(self):
        """ Test for all fields """
        form = ReviewForm({
            'review': 'It was good'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_form_is_not_valid_review(self):
        """ Test for no review """
        form = ReviewForm({
            'review': ''
        })
        self.assertFalse(form.is_valid(), msg="No review field given in test")


class TestRatingForm(TestCase):
    def test_form_is_valid(self):
        """ Test for all fields """
        form = RatingForm({
            'rating': '2.25'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_form_is_not_valid_rating(self):
        """ Test for no rating """
        form = RatingForm({
            'rating': '2.23'
        })
        self.assertFalse(form.is_valid(), msg="No review field given in test")
