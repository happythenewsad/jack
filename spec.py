import unittest
import re
import jack

class Tester(unittest.TestCase):

  # def __init__(self):
  #   pass

  def check_for_foo_or_bar(self, text):
     my_re = re.compile(r'\b(foo.+bar|bar.+foo)\b')
     if my_re.search(text) == None:
        return False
     return True

  def test_check_for_foo_or_bar(self):
    result = self.check_for_foo_or_bar("foo bar")
    self.assertEqual(True, result)
    result = self.check_for_foo_or_bar("fo bar")
    self.assertEqual(False, result)
    result = self.check_for_foo_or_bar("1 bar 1 foo")
    self.assertEqual(True, result)
    result = self.check_for_foo_or_bar("foo bart")
    self.assertEqual(False, result)



if __name__ == '__main__':
    unittest.main()


# @staticmethod












