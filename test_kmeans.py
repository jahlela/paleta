import unittest
import kmeans

class MyAppUnitTestCase(unittest.TestCase):

    def test_distance(self):
        point1 = (20, 30, 40)
        point2 = (20, 30, 40)
        point3 = (250, 240, 230)

        print "Running test 1.a"
        assert kmeans.distance(point1,point2) == 0
        print "Running test 1.b"
        assert kmeans.distance(point1,point3) == 133100


    def test_add(self):
        point1 = (0, 0, 0)
        point2 = (20, 30, 40)
        point3 = (250, 240, 230)

        print  "Running test 2.a"
        assert kmeans.add(point1,point2) == (20, 30, 40)
        print "Running test 2.b"
        assert kmeans.add(point2,point3) == (270, 270, 270)

    def test_mult(self):
        point_sums1 = (153, 422, 1107)
        point_sums2 = (136817, 77356, 71454)
        point_sums3 = (0,0,0)

        point_count1 = 0.0990099009901
        point_count2 = 0.00162575191026
        point_count3 = 10.0


        print  "Running test 3.a"
        assert kmeans.mult(point_sums1, point_count1) == (15.1485148514853, 41.7821782178222, 109.6039603960407)
        print "Running test 3.b"
        assert kmeans.mult(point_sums2, point_count2) == (222.43049910604242, 125.76166477007256, 116.16647699571803)
        print "Running test 3.c"
        assert kmeans.mult(point_sums3, point_count3) == (0.0, 0.0, 0.0)


    def test_get_kmeans(self):
        file_path = "static/img/demo/caterpillar.png"
        iterations = 10
        assert kmeans.get_kmeans(file_path, iterations) == [(219, 196, 137), (171, 66, 20), (76, 43, 27), (199, 108, 46), (184, 147, 100)]



if __name__ == "__main__":
    unittest.main()