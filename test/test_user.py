# !/usr/bin/env python
# coding: utf-8
import unittest
from db.user import User

class TestUser(unittest.TestCase):
  def test_user_find(self):
    res = User.find(1)
    self.assertIsNotNone(res)

if __name__ == "__main__":
  unittest.main()
