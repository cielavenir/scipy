# Author:  Travis Oliphant, 2002
#
# Further enhancements and tests added by numerous SciPy developers.
#
from __future__ import division, print_function, absolute_import

import warnings

import numpy as np
from numpy.random import RandomState
from numpy.testing import (TestCase, run_module_suite, assert_array_equal,
    assert_almost_equal, assert_array_less, assert_array_almost_equal,
    assert_raises, assert_, assert_allclose, assert_equal, dec, assert_warns)

from scipy import stats

# Matplotlib is not a scipy dependency but is optionally used in probplot, so
# check if it's available
try:
    import matplotlib.pyplot as plt
    have_matplotlib = True
except:
    have_matplotlib = False


g1 = [1.006, 0.996, 0.998, 1.000, 0.992, 0.993, 1.002, 0.999, 0.994, 1.000]
g2 = [0.998, 1.006, 1.000, 1.002, 0.997, 0.998, 0.996, 1.000, 1.006, 0.988]
g3 = [0.991, 0.987, 0.997, 0.999, 0.995, 0.994, 1.000, 0.999, 0.996, 0.996]
g4 = [1.005, 1.002, 0.994, 1.000, 0.995, 0.994, 0.998, 0.996, 1.002, 0.996]
g5 = [0.998, 0.998, 0.982, 0.990, 1.002, 0.984, 0.996, 0.993, 0.980, 0.996]
g6 = [1.009, 1.013, 1.009, 0.997, 0.988, 1.002, 0.995, 0.998, 0.981, 0.996]
g7 = [0.990, 1.004, 0.996, 1.001, 0.998, 1.000, 1.018, 1.010, 0.996, 1.002]
g8 = [0.998, 1.000, 1.006, 1.000, 1.002, 0.996, 0.998, 0.996, 1.002, 1.006]
g9 = [1.002, 0.998, 0.996, 0.995, 0.996, 1.004, 1.004, 0.998, 0.999, 0.991]
g10 = [0.991, 0.995, 0.984, 0.994, 0.997, 0.997, 0.991, 0.998, 1.004, 0.997]


class TestShapiro(TestCase):
    def test_basic(self):
        x1 = [0.11,7.87,4.61,10.14,7.95,3.14,0.46,
              4.43,0.21,4.75,0.71,1.52,3.24,
              0.93,0.42,4.97,9.53,4.55,0.47,6.66]
        w,pw = stats.shapiro(x1)
        assert_almost_equal(w,0.90047299861907959,6)
        assert_almost_equal(pw,0.042089745402336121,6)
        x2 = [1.36,1.14,2.92,2.55,1.46,1.06,5.27,-1.11,
              3.48,1.10,0.88,-0.51,1.46,0.52,6.20,1.69,
              0.08,3.67,2.81,3.49]
        w,pw = stats.shapiro(x2)
        assert_almost_equal(w,0.9590270,6)
        assert_almost_equal(pw,0.52460,3)

    def test_bad_arg(self):
        # Length of x is less than 3.
        x = [1]
        assert_raises(ValueError, stats.shapiro, x)


class TestAnderson(TestCase):
    def test_normal(self):
        rs = RandomState(1234567890)
        x1 = rs.standard_exponential(size=50)
        x2 = rs.standard_normal(size=50)
        A,crit,sig = stats.anderson(x1)
        assert_array_less(crit[:-1], A)
        A,crit,sig = stats.anderson(x2)
        assert_array_less(A, crit[-2:])

    def test_expon(self):
        rs = RandomState(1234567890)
        x1 = rs.standard_exponential(size=50)
        x2 = rs.standard_normal(size=50)
        A,crit,sig = stats.anderson(x1,'expon')
        assert_array_less(A, crit[-2:])
        olderr = np.seterr(all='ignore')
        try:
            A,crit,sig = stats.anderson(x2,'expon')
        finally:
            np.seterr(**olderr)
        assert_(A > crit[-1])

    def test_bad_arg(self):
        assert_raises(ValueError, stats.anderson, [1], dist='plate_of_shrimp')


class TestAndersonKSamp(TestCase):
    def test_example1a(self):
        # Example data from Scholz & Stephens (1987), originally
        # published in Lehmann (1995, Nonparametrics, Statistical
        # Methods Based on Ranks, p. 309)
        # Pass a mixture of lists and arrays
        t1 = [38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0]
        t2 = np.array([39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8])
        t3 = np.array([34.0, 35.0, 39.0, 40.0, 43.0, 43.0, 44.0, 45.0])
        t4 = np.array([34.0, 34.8, 34.8, 35.4, 37.2, 37.8, 41.2, 42.8])
        Tk, tm, p = assert_warns(UserWarning, stats.anderson_ksamp, (t1, t2,
                                 t3, t4), discrete=True)
        assert_almost_equal(Tk, 4.449, 3)
        assert_array_almost_equal([0.4985, 1.3237, 1.9158, 2.4930, 3.2459],
                                  tm, 4)
        assert_almost_equal(p, 0.0021, 4)

    def test_example1b(self):
        # Example data from Scholz & Stephens (1987), originally
        # published in Lehmann (1995, Nonparametrics, Statistical
        # Methods Based on Ranks, p. 309)
        # Pass arrays
        t1 = np.array([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
        t2 = np.array([39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8])
        t3 = np.array([34.0, 35.0, 39.0, 40.0, 43.0, 43.0, 44.0, 45.0])
        t4 = np.array([34.0, 34.8, 34.8, 35.4, 37.2, 37.8, 41.2, 42.8])
        Tk, tm, p = assert_warns(UserWarning, stats.anderson_ksamp, (t1, t2,
                                 t3, t4), discrete=False)
        assert_almost_equal(Tk, 4.480, 3)
        assert_array_almost_equal([0.4985, 1.3237, 1.9158, 2.4930, 3.2459],
                                  tm, 4)
        assert_almost_equal(p, 0.0020, 4)

    def test_example2a(self):
        # Example data taken from an earlier technical report of
        # Scholz and Stephens
        # Pass lists instead of arrays
        t1 = [194, 15, 41, 29, 33, 181]
        t2 = [413, 14, 58, 37, 100, 65, 9, 169, 447, 184, 36, 201, 118]
        t3 = [34, 31, 18, 18, 67, 57, 62, 7, 22, 34]
        t4 = [90, 10, 60, 186, 61, 49, 14, 24, 56, 20, 79, 84, 44, 59, 29,
              118, 25, 156, 310, 76, 26, 44, 23, 62]
        t5 = [130, 208, 70, 101, 208]
        t6 = [74, 57, 48, 29, 502, 12, 70, 21, 29, 386, 59, 27]
        t7 = [55, 320, 56, 104, 220, 239, 47, 246, 176, 182, 33]
        t8 = [23, 261, 87, 7, 120, 14, 62, 47, 225, 71, 246, 21, 42, 20, 5,
              12, 120, 11, 3, 14, 71, 11, 14, 11, 16, 90, 1, 16, 52, 95]
        t9 = [97, 51, 11, 4, 141, 18, 142, 68, 77, 80, 1, 16, 106, 206, 82,
              54, 31, 216, 46, 111, 39, 63, 18, 191, 18, 163, 24]
        t10 = [50, 44, 102, 72, 22, 39, 3, 15, 197, 188, 79, 88, 46, 5, 5, 36,
               22, 139, 210, 97, 30, 23, 13, 14]
        t11 = [359, 9, 12, 270, 603, 3, 104, 2, 438]
        t12 = [50, 254, 5, 283, 35, 12]
        t13 = [487, 18, 100, 7, 98, 5, 85, 91, 43, 230, 3, 130]
        t14 = [102, 209, 14, 57, 54, 32, 67, 59, 134, 152, 27, 14, 230, 66,
               61, 34]
        Tk, tm, p = assert_warns(UserWarning, stats.anderson_ksamp,
                                 (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
                                  t11, t12, t13, t14), discrete=True)
        assert_almost_equal(Tk, 3.288, 3)
        assert_array_almost_equal([0.5990, 1.3269, 1.8052, 2.2486, 2.8009],
                                  tm, 4)
        assert_almost_equal(p, 0.0041, 4)

    def test_example2b(self):
        # Example data taken from an earlier technical report of
        # Scholz and Stephens
        t1 = [194, 15, 41, 29, 33, 181]
        t2 = [413, 14, 58, 37, 100, 65, 9, 169, 447, 184, 36, 201, 118]
        t3 = [34, 31, 18, 18, 67, 57, 62, 7, 22, 34]
        t4 = [90, 10, 60, 186, 61, 49, 14, 24, 56, 20, 79, 84, 44, 59, 29,
              118, 25, 156, 310, 76, 26, 44, 23, 62]
        t5 = [130, 208, 70, 101, 208]
        t6 = [74, 57, 48, 29, 502, 12, 70, 21, 29, 386, 59, 27]
        t7 = [55, 320, 56, 104, 220, 239, 47, 246, 176, 182, 33]
        t8 = [23, 261, 87, 7, 120, 14, 62, 47, 225, 71, 246, 21, 42, 20, 5,
              12, 120, 11, 3, 14, 71, 11, 14, 11, 16, 90, 1, 16, 52, 95]
        t9 = [97, 51, 11, 4, 141, 18, 142, 68, 77, 80, 1, 16, 106, 206, 82,
              54, 31, 216, 46, 111, 39, 63, 18, 191, 18, 163, 24]
        t10 = [50, 44, 102, 72, 22, 39, 3, 15, 197, 188, 79, 88, 46, 5, 5, 36,
               22, 139, 210, 97, 30, 23, 13, 14]
        t11 = [359, 9, 12, 270, 603, 3, 104, 2, 438]
        t12 = [50, 254, 5, 283, 35, 12]
        t13 = [487, 18, 100, 7, 98, 5, 85, 91, 43, 230, 3, 130]
        t14 = [102, 209, 14, 57, 54, 32, 67, 59, 134, 152, 27, 14, 230, 66,
               61, 34]
        Tk, tm, p = assert_warns(UserWarning, stats.anderson_ksamp,
                                 (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
                                  t11, t12, t13, t14), discrete=False)
        assert_almost_equal(Tk, 3.294, 3)
        assert_array_almost_equal([0.5990, 1.3269, 1.8052, 2.2486, 2.8009],
                                  tm, 4)
        assert_almost_equal(p, 0.0041, 4)

    def test_not_enough_samples(self):
        assert_raises(ValueError, stats.anderson_ksamp, np.ones(5))

    def test_no_distinct_observations(self):
        assert_raises(ValueError, stats.anderson_ksamp,
                      (np.ones(5), np.ones(5)))

    def test_empty_sample(self):
        assert_raises(ValueError, stats.anderson_ksamp, (np.ones(5), []))


class TestAnsari(TestCase):

    def test_small(self):
        x = [1,2,3,3,4]
        y = [3,2,6,1,6,1,4,1]
        W, pval = stats.ansari(x,y)
        assert_almost_equal(W,23.5,11)
        assert_almost_equal(pval,0.13499256881897437,11)

    def test_approx(self):
        ramsay = np.array((111, 107, 100, 99, 102, 106, 109, 108, 104, 99,
                           101, 96, 97, 102, 107, 113, 116, 113, 110, 98))
        parekh = np.array((107, 108, 106, 98, 105, 103, 110, 105, 104,
                           100, 96, 108, 103, 104, 114, 114, 113, 108, 106, 99))

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',
                        message="Ties preclude use of exact statistic.")
            W, pval = stats.ansari(ramsay, parekh)

        assert_almost_equal(W,185.5,11)
        assert_almost_equal(pval,0.18145819972867083,11)

    def test_exact(self):
        W,pval = stats.ansari([1,2,3,4],[15,5,20,8,10,12])
        assert_almost_equal(W,10.0,11)
        assert_almost_equal(pval,0.533333333333333333,7)

    def test_bad_arg(self):
        assert_raises(ValueError, stats.ansari, [], [1])
        assert_raises(ValueError, stats.ansari, [1], [])


class TestBartlett(TestCase):

    def test_data(self):
        args = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10]
        T, pval = stats.bartlett(*args)
        assert_almost_equal(T,20.78587342806484,7)
        assert_almost_equal(pval,0.0136358632781,7)

    def test_bad_arg(self):
        # Too few args raises ValueError.
        assert_raises(ValueError, stats.bartlett, [1])


class TestLevene(TestCase):

    def test_data(self):
        args = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10]
        W, pval = stats.levene(*args)
        assert_almost_equal(W,1.7059176930008939,7)
        assert_almost_equal(pval,0.0990829755522,7)

    def test_trimmed1(self):
        # Test that center='trimmed' gives the same result as center='mean'
        # when proportiontocut=0.
        W1, pval1 = stats.levene(g1, g2, g3, center='mean')
        W2, pval2 = stats.levene(g1, g2, g3, center='trimmed', proportiontocut=0.0)
        assert_almost_equal(W1, W2)
        assert_almost_equal(pval1, pval2)

    def test_trimmed2(self):
        x = [1.2, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 100.0]
        y = [0.0, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 200.0]
        np.random.seed(1234)
        x2 = np.random.permutation(x)

        # Use center='trimmed'
        W0, pval0 = stats.levene(x, y, center='trimmed', proportiontocut=0.125)
        W1, pval1 = stats.levene(x2, y, center='trimmed', proportiontocut=0.125)
        # Trim the data here, and use center='mean'
        W2, pval2 = stats.levene(x[1:-1], y[1:-1], center='mean')
        # Result should be the same.
        assert_almost_equal(W0, W2)
        assert_almost_equal(W1, W2)
        assert_almost_equal(pval1, pval2)

    def test_equal_mean_median(self):
        x = np.linspace(-1,1,21)
        np.random.seed(1234)
        x2 = np.random.permutation(x)
        y = x**3
        W1, pval1 = stats.levene(x, y, center='mean')
        W2, pval2 = stats.levene(x2, y, center='median')
        assert_almost_equal(W1, W2)
        assert_almost_equal(pval1, pval2)

    def test_bad_keyword(self):
        x = np.linspace(-1,1,21)
        assert_raises(TypeError, stats.levene, x, x, portiontocut=0.1)

    def test_bad_center_value(self):
        x = np.linspace(-1,1,21)
        assert_raises(ValueError, stats.levene, x, x, center='trim')

    def test_too_few_args(self):
        assert_raises(ValueError, stats.levene, [1])


class TestBinomP(TestCase):

    def test_data(self):
        pval = stats.binom_test(100,250)
        assert_almost_equal(pval,0.0018833009350757682,11)
        pval = stats.binom_test(201,405)
        assert_almost_equal(pval,0.92085205962670713,11)
        pval = stats.binom_test([682,243],p=3.0/4)
        assert_almost_equal(pval,0.38249155957481695,11)

    def test_bad_len_x(self):
        # Length of x must be 1 or 2.
        assert_raises(ValueError, stats.binom_test, [1,2,3])

    def test_bad_n(self):
        # len(x) is 1, but n is invalid.
        # Missing n
        assert_raises(ValueError, stats.binom_test, [100])
        # n less than x[0]
        assert_raises(ValueError, stats.binom_test, [100], n=50)

    def test_bad_p(self):
        assert_raises(ValueError, stats.binom_test, [50, 50], p=2.0)


class TestFindRepeats(TestCase):

    def test_basic(self):
        a = [1,2,3,4,1,2,3,4,1,2,5]
        res,nums = stats.find_repeats(a)
        assert_array_equal(res,[1,2,3,4])
        assert_array_equal(nums,[3,3,2,2])

    def test_empty_result(self):
        # Check that empty arrays are returned when there are no repeats.
        a = [10, 20, 50, 30, 40]
        repeated, counts = stats.find_repeats(a)
        assert_array_equal(repeated, [])
        assert_array_equal(counts, [])


class TestFligner(TestCase):

    def test_data(self):
        # numbers from R: fligner.test in package stats
        x1 = np.arange(5)
        assert_array_almost_equal(stats.fligner(x1,x1**2),
                           (3.2282229927203536, 0.072379187848207877), 11)

    def test_trimmed1(self):
        # Test that center='trimmed' gives the same result as center='mean'
        # when proportiontocut=0.
        Xsq1, pval1 = stats.fligner(g1, g2, g3, center='mean')
        Xsq2, pval2 = stats.fligner(g1, g2, g3, center='trimmed', proportiontocut=0.0)
        assert_almost_equal(Xsq1, Xsq2)
        assert_almost_equal(pval1, pval2)

    def test_trimmed2(self):
        x = [1.2, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 100.0]
        y = [0.0, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 200.0]
        # Use center='trimmed'
        Xsq1, pval1 = stats.fligner(x, y, center='trimmed', proportiontocut=0.125)
        # Trim the data here, and use center='mean'
        Xsq2, pval2 = stats.fligner(x[1:-1], y[1:-1], center='mean')
        # Result should be the same.
        assert_almost_equal(Xsq1, Xsq2)
        assert_almost_equal(pval1, pval2)

    # The following test looks reasonable at first, but fligner() uses the
    # function stats.rankdata(), and in one of the cases in this test,
    # there are ties, while in the other (because of normal rounding
    # errors) there are not.  This difference leads to differences in the
    # third significant digit of W.
    #
    #def test_equal_mean_median(self):
    #    x = np.linspace(-1,1,21)
    #    y = x**3
    #    W1, pval1 = stats.fligner(x, y, center='mean')
    #    W2, pval2 = stats.fligner(x, y, center='median')
    #    assert_almost_equal(W1, W2)
    #    assert_almost_equal(pval1, pval2)

    def test_bad_keyword(self):
        x = np.linspace(-1,1,21)
        assert_raises(TypeError, stats.fligner, x, x, portiontocut=0.1)

    def test_bad_center_value(self):
        x = np.linspace(-1,1,21)
        assert_raises(ValueError, stats.fligner, x, x, center='trim')

    def test_bad_num_args(self):
        # Too few args raises ValueError.
        assert_raises(ValueError, stats.fligner, [1])


class TestMood(TestCase):
    def test_mood(self):
        # numbers from R: mood.test in package stats
        x1 = np.arange(5)
        assert_array_almost_equal(stats.mood(x1, x1**2),
                                  (-1.3830857299399906, 0.16663858066771478), 11)

    def test_mood_order_of_args(self):
        # z should change sign when the order of arguments changes, pvalue
        # should not change
        np.random.seed(1234)
        x1 = np.random.randn(10, 1)
        x2 = np.random.randn(15, 1)
        z1, p1 = stats.mood(x1, x2)
        z2, p2 = stats.mood(x2, x1)
        assert_array_almost_equal([z1, p1], [-z2, p2])

    def test_mood_with_axis_none(self):
        #Test with axis = None, compare with results from R
        x1 = [-0.626453810742332, 0.183643324222082, -0.835628612410047,
               1.59528080213779, 0.329507771815361, -0.820468384118015,
               0.487429052428485, 0.738324705129217, 0.575781351653492,
              -0.305388387156356, 1.51178116845085, 0.389843236411431,
              -0.621240580541804, -2.2146998871775, 1.12493091814311,
              -0.0449336090152309, -0.0161902630989461, 0.943836210685299,
               0.821221195098089, 0.593901321217509]

        x2 = [-0.896914546624981, 0.184849184646742, 1.58784533120882,
              -1.13037567424629, -0.0802517565509893, 0.132420284381094,
               0.707954729271733, -0.23969802417184, 1.98447393665293,
              -0.138787012119665, 0.417650750792556, 0.981752777463662,
              -0.392695355503813, -1.03966897694891, 1.78222896030858,
              -2.31106908460517, 0.878604580921265, 0.035806718015226,
               1.01282869212708, 0.432265154539617, 2.09081920524915,
              -1.19992581964387, 1.58963820029007, 1.95465164222325,
               0.00493777682814261, -2.45170638784613, 0.477237302613617,
              -0.596558168631403, 0.792203270299649, 0.289636710177348]

        x1 = np.array(x1)
        x2 = np.array(x2)
        x1.shape = (10, 2)
        x2.shape = (15, 2)
        assert_array_almost_equal(stats.mood(x1, x2, axis=None),
                                  [-1.31716607555, 0.18778296257])

    def test_mood_2d(self):
        # Test if the results of mood test in 2-D case are consistent with the
        # R result for the same inputs.  Numbers from R mood.test().
        ny = 5
        np.random.seed(1234)
        x1 = np.random.randn(10, ny)
        x2 = np.random.randn(15, ny)
        z_vectest, pval_vectest = stats.mood(x1, x2)

        for j in range(ny):
            assert_array_almost_equal([z_vectest[j], pval_vectest[j]],
                                      stats.mood(x1[:, j], x2[:, j]))

        # inverse order of dimensions
        x1 = x1.transpose()
        x2 = x2.transpose()
        z_vectest, pval_vectest = stats.mood(x1, x2, axis=1)

        for i in range(ny):
            # check axis handling is self consistent
            assert_array_almost_equal([z_vectest[i], pval_vectest[i]],
                                      stats.mood(x1[i, :], x2[i, :]))

    def test_mood_3d(self):
        shape = (10, 5, 6)
        np.random.seed(1234)
        x1 = np.random.randn(*shape)
        x2 = np.random.randn(*shape)

        for axis in range(3):
            z_vectest, pval_vectest = stats.mood(x1, x2, axis=axis)
            # Tests that result for 3-D arrays is equal to that for the
            # same calculation on a set of 1-D arrays taken from the
            # 3-D array
            axes_idx = ([1, 2], [0, 2], [0, 1])  # the two axes != axis
            for i in range(shape[axes_idx[axis][0]]):
                for j in range(shape[axes_idx[axis][1]]):
                    if axis == 0:
                        slice1 = x1[:, i, j]
                        slice2 = x2[:, i, j]
                    elif axis == 1:
                        slice1 = x1[i, :, j]
                        slice2 = x2[i, :, j]
                    else:
                        slice1 = x1[i, j, :]
                        slice2 = x2[i, j, :]

                    assert_array_almost_equal([z_vectest[i, j],
                                               pval_vectest[i, j]],
                                              stats.mood(slice1, slice2))

    def test_mood_bad_arg(self):
        # Raise ValueError when the sum of the lengths of the args is less than 3
        assert_raises(ValueError, stats.mood, [1], [])


class TestProbplot(TestCase):

    def test_basic(self):
        np.random.seed(12345)
        x = stats.norm.rvs(size=20)
        osm, osr = stats.probplot(x, fit=False)
        osm_expected = [-1.8241636, -1.38768012, -1.11829229, -0.91222575,
                        -0.73908135, -0.5857176, -0.44506467, -0.31273668,
                        -0.18568928, -0.06158146, 0.06158146, 0.18568928,
                        0.31273668, 0.44506467, 0.5857176, 0.73908135,
                        0.91222575, 1.11829229, 1.38768012, 1.8241636]
        assert_allclose(osr, np.sort(x))
        assert_allclose(osm, osm_expected)

        res, res_fit = stats.probplot(x, fit=True)
        res_fit_expected = [1.05361841, 0.31297795, 0.98741609]
        assert_allclose(res_fit, res_fit_expected)

    def test_sparams_keyword(self):
        np.random.seed(123456)
        x = stats.norm.rvs(size=100)
        # Check that None, () and 0 (loc=0, for normal distribution) all work
        # and give the same results
        osm1, osr1 = stats.probplot(x, sparams=None, fit=False)
        osm2, osr2 = stats.probplot(x, sparams=0, fit=False)
        osm3, osr3 = stats.probplot(x, sparams=(), fit=False)
        assert_allclose(osm1, osm2)
        assert_allclose(osm1, osm3)
        assert_allclose(osr1, osr2)
        assert_allclose(osr1, osr3)
        # Check giving (loc, scale) params for normal distribution
        osm, osr = stats.probplot(x, sparams=(), fit=False)

    def test_dist_keyword(self):
        np.random.seed(12345)
        x = stats.norm.rvs(size=20)
        osm1, osr1 = stats.probplot(x, fit=False, dist='t', sparams=(3,))
        osm2, osr2 = stats.probplot(x, fit=False, dist=stats.t, sparams=(3,))
        assert_allclose(osm1, osm2)
        assert_allclose(osr1, osr2)

        assert_raises(ValueError, stats.probplot, x, dist='wrong-dist-name')
        assert_raises(AttributeError, stats.probplot, x, dist=[])

        class custom_dist(object):
            """Some class that looks just enough like a distribution."""
            def ppf(self, q):
                return stats.norm.ppf(q, loc=2)

        osm1, osr1 = stats.probplot(x, sparams=(2,), fit=False)
        osm2, osr2 = stats.probplot(x, dist=custom_dist(), fit=False)
        assert_allclose(osm1, osm2)
        assert_allclose(osr1, osr2)

    @dec.skipif(not have_matplotlib)
    def test_plot_kwarg(self):
        np.random.seed(7654321)
        fig = plt.figure()
        fig.add_subplot(111)
        x = stats.t.rvs(3, size=100)
        res1, fitres1 = stats.probplot(x, plot=plt)
        plt.close()
        res2, fitres2 = stats.probplot(x, plot=None)
        res3 = stats.probplot(x, fit=False, plot=plt)
        plt.close()
        res4 = stats.probplot(x, fit=False, plot=None)
        # Check that results are consistent between combinations of `fit` and
        # `plot` keywords.
        assert_(len(res1) == len(res2) == len(res3) == len(res4) == 2)
        assert_allclose(res1, res2)
        assert_allclose(res1, res3)
        assert_allclose(res1, res4)
        assert_allclose(fitres1, fitres2)

        # Check that a Matplotlib Axes object is accepted
        fig = plt.figure()
        ax = fig.add_subplot(111)
        stats.probplot(x, fit=False, plot=ax)
        plt.close()

    def test_probplot_bad_args(self):
        # Raise ValueError when given an invalid distribution.
        assert_raises(ValueError, stats.probplot, [1], dist="plate_of_shrimp")


def test_wilcoxon_bad_arg():
    # Raise ValueError when two args of different lengths are given or
    # zero_method is unknown.
    assert_raises(ValueError, stats.wilcoxon, [1], [1,2])
    assert_raises(ValueError, stats.wilcoxon, [1,2], [1,2], "dummy")


def test_mvsdist_bad_arg():
    # Raise ValueError if fewer than two data points are given.
    data = [1]
    assert_raises(ValueError, stats.mvsdist, data)


def test_kstat_bad_arg():
    # Raise ValueError if n > 4 or n > 1.
    data = [1]
    n = 10
    assert_raises(ValueError, stats.kstat, data, n=n)


def test_kstatvar_bad_arg():
    # Raise ValueError is n is not 1 or 2.
    data = [1]
    n = 10
    assert_raises(ValueError, stats.kstatvar, data, n=n)


def test_ppcc_max_bad_arg():
    # Raise ValueError when given an invalid distribution.
    data = [1]
    assert_raises(ValueError, stats.ppcc_max, data, dist="plate_of_shrimp")


class TestBoxcox_llf(TestCase):

    def test_basic(self):
        np.random.seed(54321)
        x = stats.norm.rvs(size=10000, loc=10)
        lmbda = 1
        llf = stats.boxcox_llf(lmbda, x)
        llf_expected = -x.size / 2. * np.log(np.sum(x.std()**2))
        assert_allclose(llf, llf_expected)

    def test_array_like(self):
        np.random.seed(54321)
        x = stats.norm.rvs(size=100, loc=10)
        lmbda = 1
        llf = stats.boxcox_llf(lmbda, x)
        llf2 = stats.boxcox_llf(lmbda, list(x))
        assert_allclose(llf, llf2, rtol=1e-12)

    def test_2d_input(self):
        # Note: boxcox_llf() was already working with 2-D input (sort of), so
        # keep it like that.  boxcox() doesn't work with 2-D input though, due
        # to brent() returning a scalar.
        np.random.seed(54321)
        x = stats.norm.rvs(size=100, loc=10)
        lmbda = 1
        llf = stats.boxcox_llf(lmbda, x)
        llf2 = stats.boxcox_llf(lmbda, np.vstack([x, x]).T)
        assert_allclose([llf, llf], llf2, rtol=1e-12)

    def test_empty(self):
        assert_(np.isnan(stats.boxcox_llf(1, [])))


class TestBoxcox(TestCase):

    def test_fixed_lmbda(self):
        np.random.seed(12345)
        x = stats.loggamma.rvs(5, size=50) + 5
        xt = stats.boxcox(x, lmbda=1)
        assert_allclose(xt, x - 1)
        xt = stats.boxcox(x, lmbda=-1)
        assert_allclose(xt, 1 - 1/x)

        xt = stats.boxcox(x, lmbda=0)
        assert_allclose(xt, np.log(x))

        # Also test that array_like input works
        xt = stats.boxcox(list(x), lmbda=0)
        assert_allclose(xt, np.log(x))

    def test_lmbda_None(self):
        np.random.seed(1234567)
        # Start from normal rv's, do inverse transform to check that
        # optimization function gets close to the right answer.
        np.random.seed(1245)
        lmbda = 2.5
        x = stats.norm.rvs(loc=10, size=50000)
        x_inv = (x * lmbda + 1)**(-lmbda)
        xt, maxlog = stats.boxcox(x_inv)

        assert_almost_equal(maxlog, -1 / lmbda, decimal=2)

    def test_alpha(self):
        np.random.seed(1234)
        x = stats.loggamma.rvs(5, size=50) + 5

        # Some regular values for alpha, on a small sample size
        _, _, interval = stats.boxcox(x, alpha=0.75)
        assert_allclose(interval, [4.004485780226041, 5.138756355035744])
        _, _, interval = stats.boxcox(x, alpha=0.05)
        assert_allclose(interval, [1.2138178554857557, 8.209033272375663])

        # Try some extreme values, see we don't hit the N=500 limit
        x = stats.loggamma.rvs(7, size=500) + 15
        _, _, interval = stats.boxcox(x, alpha=0.001)
        assert_allclose(interval, [0.3988867, 11.40553131])
        _, _, interval = stats.boxcox(x, alpha=0.999)
        assert_allclose(interval, [5.83316246, 5.83735292])

    def test_boxcox_bad_arg(self):
        # Raise ValueError if any data value is negative.
        x = np.array([-1])
        assert_raises(ValueError, stats.boxcox, x)

    def test_empty(self):
        assert_(stats.boxcox([]).shape == (0,))


class TestBoxcoxNormmax(TestCase):
    def setUp(self):
        np.random.seed(12345)
        self.x = stats.loggamma.rvs(5, size=50) + 5

    def test_pearsonr(self):
        maxlog = stats.boxcox_normmax(self.x)
        assert_allclose(maxlog, 1.804465, rtol=1e-6)

    def test_mle(self):
        maxlog = stats.boxcox_normmax(self.x, method='mle')
        assert_allclose(maxlog, 1.758101, rtol=1e-6)

        # Check that boxcox() uses 'mle'
        _, maxlog_boxcox = stats.boxcox(self.x)
        assert_allclose(maxlog_boxcox, maxlog)

    def test_all(self):
        maxlog_all = stats.boxcox_normmax(self.x, method='all')
        assert_allclose(maxlog_all, [1.804465, 1.758101], rtol=1e-6)


class TestBoxcoxNormplot(TestCase):
    def setUp(self):
        np.random.seed(7654321)
        self.x = stats.loggamma.rvs(5, size=500) + 5

    def test_basic(self):
        N = 5
        lmbdas, ppcc = stats.boxcox_normplot(self.x, -10, 10, N=N)
        ppcc_expected = [0.57783375, 0.83610988, 0.97524311, 0.99756057,
                         0.95843297]
        assert_allclose(lmbdas, np.linspace(-10, 10, num=N))
        assert_allclose(ppcc, ppcc_expected)

    @dec.skipif(not have_matplotlib)
    def test_plot_kwarg(self):
        # Check with the matplotlib.pyplot module
        fig = plt.figure()
        fig.add_subplot(111)
        stats.boxcox_normplot(self.x, -20, 20, plot=plt)
        plt.close()

        # Check that a Matplotlib Axes object is accepted
        fig.add_subplot(111)
        ax = fig.add_subplot(111)
        stats.boxcox_normplot(self.x, -20, 20, plot=ax)
        plt.close()

    def test_invalid_inputs(self):
        # `lb` has to be larger than `la`
        assert_raises(ValueError, stats.boxcox_normplot, self.x, 1, 0)
        # `x` can not contain negative values
        assert_raises(ValueError, stats.boxcox_normplot, [-1, 1] , 0, 1)

    def test_empty(self):
        assert_(stats.boxcox_normplot([], 0, 1).size == 0)


class TestCircFuncs(TestCase):
    def test_circfuncs(self):
        x = np.array([355,5,2,359,10,350])
        M = stats.circmean(x, high=360)
        Mval = 0.167690146
        assert_allclose(M, Mval, rtol=1e-7)

        V = stats.circvar(x, high=360)
        Vval = 42.51955609
        assert_allclose(V, Vval, rtol=1e-7)

        S = stats.circstd(x, high=360)
        Sval = 6.520702116
        assert_allclose(S, Sval, rtol=1e-7)

    def test_circfuncs_small(self):
        x = np.array([20,21,22,18,19,20.5,19.2])
        M1 = x.mean()
        M2 = stats.circmean(x, high=360)
        assert_allclose(M2, M1, rtol=1e-5)

        V1 = x.var()
        V2 = stats.circvar(x, high=360)
        assert_allclose(V2, V1, rtol=1e-4)

        S1 = x.std()
        S2 = stats.circstd(x, high=360)
        assert_allclose(S2, S1, rtol=1e-4)

    def test_circmean_axis(self):
        x = np.array([[355,5,2,359,10,350],
                      [351,7,4,352,9,349],
                      [357,9,8,358,4,356]])
        M1 = stats.circmean(x, high=360)
        M2 = stats.circmean(x.ravel(), high=360)
        assert_allclose(M1, M2, rtol=1e-14)

        M1 = stats.circmean(x, high=360, axis=1)
        M2 = [stats.circmean(x[i], high=360) for i in range(x.shape[0])]
        assert_allclose(M1, M2, rtol=1e-14)

        M1 = stats.circmean(x, high=360, axis=0)
        M2 = [stats.circmean(x[:,i], high=360) for i in range(x.shape[1])]
        assert_allclose(M1, M2, rtol=1e-14)

    def test_circvar_axis(self):
        x = np.array([[355,5,2,359,10,350],
                      [351,7,4,352,9,349],
                  [357,9,8,358,4,356]])

        V1 = stats.circvar(x, high=360)
        V2 = stats.circvar(x.ravel(), high=360)
        assert_allclose(V1, V2, rtol=1e-11)

        V1 = stats.circvar(x, high=360, axis=1)
        V2 = [stats.circvar(x[i], high=360) for i in range(x.shape[0])]
        assert_allclose(V1, V2, rtol=1e-11)

        V1 = stats.circvar(x, high=360, axis=0)
        V2 = [stats.circvar(x[:,i], high=360) for i in range(x.shape[1])]
        assert_allclose(V1, V2, rtol=1e-11)

    def test_circstd_axis(self):
        x = np.array([[355,5,2,359,10,350],
                      [351,7,4,352,9,349],
                      [357,9,8,358,4,356]])

        S1 = stats.circstd(x, high=360)
        S2 = stats.circstd(x.ravel(), high=360)
        assert_allclose(S1, S2, rtol=1e-11)

        S1 = stats.circstd(x, high=360, axis=1)
        S2 = [stats.circstd(x[i], high=360) for i in range(x.shape[0])]
        assert_allclose(S1, S2, rtol=1e-11)

        S1 = stats.circstd(x, high=360, axis=0)
        S2 = [stats.circstd(x[:,i], high=360) for i in range(x.shape[1])]
        assert_allclose(S1, S2, rtol=1e-11)

    def test_circfuncs_array_like(self):
        x = [355,5,2,359,10,350]
        assert_allclose(stats.circmean(x, high=360), 0.167690146, rtol=1e-7)
        assert_allclose(stats.circvar(x, high=360), 42.51955609, rtol=1e-7)
        assert_allclose(stats.circstd(x, high=360), 6.520702116, rtol=1e-7)

    def test_empty(self):
        assert_(np.isnan(stats.circmean([])))
        assert_(np.isnan(stats.circstd([])))
        assert_(np.isnan(stats.circvar([])))


def test_accuracy_wilcoxon():
    freq = [1, 4, 16, 15, 8, 4, 5, 1, 2]
    nums = range(-4, 5)
    x = np.concatenate([[u] * v for u, v in zip(nums, freq)])
    y = np.zeros(x.size)

    T, p = stats.wilcoxon(x, y, "pratt")
    assert_allclose(T, 423)
    assert_allclose(p, 0.00197547303533107)

    T, p = stats.wilcoxon(x, y, "zsplit")
    assert_allclose(T, 441)
    assert_allclose(p, 0.0032145343172473055)

    T, p = stats.wilcoxon(x, y, "wilcox")
    assert_allclose(T, 327)
    assert_allclose(p, 0.00641346115861)

    # Test the 'correction' option, using values computed in R with:
    # > wilcox.test(x, y, paired=TRUE, exact=FALSE, correct={FALSE,TRUE})
    x = np.array([120, 114, 181, 188, 180, 146, 121, 191, 132, 113, 127, 112])
    y = np.array([133, 143, 119, 189, 112, 199, 198, 113, 115, 121, 142, 187])
    T, p = stats.wilcoxon(x, y, correction=False)
    assert_equal(T, 34)
    assert_allclose(p, 0.6948866, rtol=1e-6)
    T, p = stats.wilcoxon(x, y, correction=True)
    assert_equal(T, 34)
    assert_allclose(p, 0.7240817, rtol=1e-6)


def test_wilcoxon_tie():
    # Regression test for gh-2391.
    # Corresponding R code is:
    #   > result = wilcox.test(rep(0.1, 10), exact=FALSE, correct=FALSE)
    #   > result$p.value
    #   [1] 0.001565402
    #   > result = wilcox.test(rep(0.1, 10), exact=FALSE, correct=TRUE)
    #   > result$p.value
    #   [1] 0.001904195
    stat, p = stats.wilcoxon([0.1] * 10)
    expected_p = 0.001565402
    assert_equal(stat, 0)
    assert_allclose(p, expected_p, rtol=1e-6)

    stat, p = stats.wilcoxon([0.1] * 10, correction=True)
    expected_p = 0.001904195
    assert_equal(stat, 0)
    assert_allclose(p, expected_p, rtol=1e-6)


if __name__ == "__main__":
    run_module_suite()
