import sys
sys.path.append("..")
from utils import *

def test_one_plus_one_is_two():
    "Check that one and one are indeed two."
    assert 1 + 1 == 2

def test_merge_duplicate_energy():
    '''
    Test function utils.merge_duplicate_energy.
    '''
    grid = np.array([1., 2., 3., 3., 4., 5., 6., 6., 6., 7., 8.])
    data = np.array([11, 12, 12.5, 13.5, 14, 15, 16, 17, 18, 19, 20])
    reduced_grid, reduced_data = merge_duplicate_energy(grid, data)
    np.testing.assert_array_equal(reduced_grid,
                                  np.array([1., 2., 3., 4., 5., 6., 7., 8.]))
    np.testing.assert_array_equal(reduced_data,
                                  np.array([11., 12., 13., 14., 15., 17., 19., 20.]))

if __name__ == "__main__":
    test_merge_duplicate_energy()
