import unittest
import client 
import server

class TestHEncode(unittest.TestCase):

    def test_h_encode(self):
        self.assertEqual(client.encoder("101010"), "0011010110")

        self.assertEqual(client.encoder("110011001100"), "01111000110011000")

        self.assertEqual(client.encoder(""), "")

class TestStringToBinary(unittest.TestCase):

    def test_string_to_binary(self):
        self.assertEqual(client.string_to_binary("hello"), "01101000 01100101 01101100 01101100 01101111")

        self.assertEqual(client.string_to_binary("!@#$%"), "00100001 01000000 00100011 00100100 00100101")

        self.assertEqual(client.string_to_binary(""), "")

class TestConnectBinaryStrings(unittest.TestCase):

    def test_connect_binary_strings(self):
        self.assertEqual(client.connect_binary_strings("01101000 01100101 01101100 01101100 01101111"), "0110100001100101011011000110110001101111")

        self.assertEqual(client.connect_binary_strings("11001100"), "11001100")

        self.assertEqual(client.connect_binary_strings(""), "")

class TestNumOfZero(unittest.TestCase):

    def test_num_of_zero(self):
        self.assertEqual(server.num_of_zero(11000), "011000")

        self.assertEqual(server.num_of_zero(1500), "001500")

        self.assertEqual(server.num_of_zero(5), "000005")

class TestIsPowerOfTwo(unittest.TestCase):

    def test_is_power_of_two(self):
        self.assertTrue(server.is_power_of_two(8))

        self.assertFalse(server.is_power_of_two(10))

        self.assertFalse(server.is_power_of_two(0))

class TestHDecode(unittest.TestCase):

    def test_h_decode(self):
        self.assertEqual(server.decoder("1001001")[0], ("0001"))

        self.assertEqual(server.decoder("111001110010011")[0], ("00110010011"))

        self.assertEqual(server.decoder("100100100")[0], ("00010"))

class TestSplitBinaryString(unittest.TestCase):

    def test_split_binary_string(self):
        self.assertEqual(server.split_binary_string("0110100001100101011011000110110001101100"), "01101000 01100101 01101100 01101100 01101100")

        self.assertEqual(server.split_binary_string("0110100001100101011011000110110001101100"), "01101000 01100101 01101100 01101100 01101100")

        self.assertEqual(server.split_binary_string(""), "")

class TestBinaryToString(unittest.TestCase):

    def test_binary_to_string(self):
        self.assertEqual(server.binary_to_string("01101000 01100101 01101100 01101100 01101111"), "hello")

        self.assertEqual(server.binary_to_string("00100001 01000000 00100011 00100100 00100101"), "!@#$%")

        self.assertEqual(server.binary_to_string(""), "")

if __name__ == '__main__':
    unittest.main(exit=False)