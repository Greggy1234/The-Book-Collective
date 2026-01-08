from django.test import TestCase
from .forms import FeaturesForm


# Create your tests here
class TestFeaturesForm(TestCase):
    def test_form_is_valid(self):
        """ Test for all fields """
        form = FeaturesForm({
            'name': 'Greg',
            'message': 'I want to add friends'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_form_is_not_valid_name(self):
        """ Test for no name """
        form = FeaturesForm({
            'name': '',
            'message': 'I want to add friends'
        })
        self.assertFalse(form.is_valid(), msg="No name field given in test")

    def test_form_is_not_valid_message(self):
        """ Test for no message """
        form = FeaturesForm({
            'name': 'Greg',
            'message': ''
        })
        self.assertFalse(form.is_valid(), msg="No message field given in test")
