import unittest
# import app
import kmeans

class MyAppUnitTestCase(unittest.TestCase):

    def test_distance(self):
        point1 = (20, 30, 40)
        point2 = (20, 30, 40)
        point3 = (250, 240, 230)

        print "Running test 1.a"
        assert kmeans.distance(point1,point2) == 0
        print "Runnign test 1.b"
        assert kmeans.distance(point1,point3) == 133100


    def test_add(self):
        point1 = (0, 0, 0)
        point2 = (20, 30, 40)
        point3 = (250, 240, 230)

        print  "Running test 2.a"
        assert kmeans.add(point1,point2) == (20, 30, 40)
        print "Running test 2.b"
        assert kmeans.add(point2,point3) == (270, 270, 270)

    # def test_mult(self):
    #     point_sums1 = (20, 30, 40)
    #     point_sums2 = (250, 240, 230)
    #     point_sums3 = (0,0,0)

    #     point_count = 



    #     print  "Running test 3.a"
    #     assert kmeans.mult(,) == 
    #     print "Running test 3.b"
    #     assert kmeans.mult(,) == 
    #     print "Running test 3.c"
    #     assert kmeans.mult(,) == 


if __name__ == "__main__":
    unittest.main()