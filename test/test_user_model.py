import unittest
from APP.modle import User
class UserModleTestCase(unittest.TestCase):
	def test_password_setter(self):
		u = User('allen', password = 'cat')
		self.assertTrue(u.password_hash is not  None)
	def test_no_password_getter(self):
		u = User('allen', password= 'cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verif(self):
		u = User('allen', password = 'cat')
		self.assertTrue(u.ver_password('cat'))
		self.assertFalse(u.ver_password('dog'))

	def test_password_salts_are_random(self):
		u1 = User('allen', password = 'cat')
		u2 = User('allen', password = 'cat')
		self.assertTrue(u1.password_hash != u2.password_hash)
