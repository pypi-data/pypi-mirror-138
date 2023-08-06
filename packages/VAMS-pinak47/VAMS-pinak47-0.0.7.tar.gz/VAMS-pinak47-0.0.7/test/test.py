

import unittest
from src import fitness_calc as fitness
import utility as util

# unittest will test all the methods whose name starts with 'test'

class SampleTest(unittest.TestCase):

    def test_bmi(self):
        ft_cal = fitness.fitness_calculation()
        uti = util.utility_main()
        df_test = uti.read_json("test_data.json")
        df_cal = ft_cal.BMI_calc("details.json")
        self.assertEqual(True, df_test.equals(df_cal))
       

# running the test
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
 