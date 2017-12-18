import unittest
from survey import AnonymousSurvey

class AnonymousSurveyTest(unittest.TestCase):
    """Tests for the class AnonymousSurvey."""

    def setUp(self):
        """
        Create a survey and a set of responses for use in all test methods.
        """
        question = 'What language did you first learn to speak?'
        self.survey = AnonymousSurvey(question)

    def test_store_single_response(self):
        """Test that a single response is stored properly."""
        self.survey.store_response('English')
        self.assertIn('English', self.survey.responses)

    def test_store_three_responses(self):
        """Test that three individual resopnses are stored properly."""
        responses = ['English', 'Spanish', 'Mandarin']
        for response in responses:
            self.survey.store_response(response)
        for response in responses:
            self.assertIn(response, self.survey.responses)

unittest.main()
