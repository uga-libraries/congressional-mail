import unittest
from css_archiving_format import topics_sort_normalize


class MyTestCase(unittest.TestCase):

    def test_asterix(self):
        """Test for when the topic includes an asterix"""
        result = topics_sort_normalize('*topic')
        expected = '_topic'
        self.assertEqual(expected, result, "Problem with test for asterix")

    def test_backslash(self):
        """Test for when the topic includes a backslash"""
        result = topics_sort_normalize('to\\pic')
        expected = 'to_pic'
        self.assertEqual(expected, result, "Problem with test for backslash")

    def test_bracket_closed(self):
        """Test for when the topic includes a closed angle bracket"""
        result = topics_sort_normalize('topic>')
        expected = 'topic_'
        self.assertEqual(expected, result, "Problem with test for bracket_closed")

    def test_bracket_open(self):
        """Test for when the topic includes an open angle bracket"""
        result = topics_sort_normalize('to<pi<c')
        expected = 'to_pi_c'
        self.assertEqual(expected, result, "Problem with test for bracket_open")

    def test_colon(self):
        """Test for when the topic includes a colon"""
        result = topics_sort_normalize(':topic')
        expected = '_topic'
        self.assertEqual(expected, result, "Problem with test for colon")

    def test_double_quote(self):
        """Test for when the topic includes a double quote"""
        result = topics_sort_normalize('top"ic')
        expected = 'top_ic'
        self.assertEqual(expected, result, "Problem with test for double_quote")

    def test_end_period(self):
        """Test for when the topic ends with a period"""
        result = topics_sort_normalize('topic...')
        expected = 'topic'
        self.assertEqual(expected, result, "Problem with test for end_period")

    def test_end_space(self):
        """Test for when the topic ends with a space"""
        result = topics_sort_normalize('topic ')
        expected = 'topic'
        self.assertEqual(expected, result, "Problem with test for end_period")

    def test_forward_slash(self):
        """Test for when the topic includes a forward slash"""
        result = topics_sort_normalize('topic/')
        expected = 'topic_'
        self.assertEqual(expected, result, "Problem with test for forward_slash")

    def test_pipe(self):
        """Test for when the topic includes a pipe"""
        result = topics_sort_normalize('||to|pic|')
        expected = '__to_pic_'
        self.assertEqual(expected, result, "Problem with test for pipe")

    def test_question(self):
        """Test for when the topic includes a question mark"""
        result = topics_sort_normalize('?topic')
        expected = '_topic'
        self.assertEqual(expected, result, "Problem with test for question")


if __name__ == '__main__':
    unittest.main()
