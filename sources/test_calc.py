import unittest
import calc


class TestCalc(unittest.TestCase):
    """
    Test the add function from the calc library
    """

    def test_mult_integers(self):
        """
        Test that the addition of two integers returns the correct total
        """
        result = calc.mult2(1, 2)
        self.assertEqual(result, 2)

    def test_mult_floats(self):
        """
        Test that the addition of two floats returns the correct result
        """
        result = calc.mult2('10.5', 2)
        self.assertEqual(result, 21)


if __name__ == '__main__':
    unittest.main()
