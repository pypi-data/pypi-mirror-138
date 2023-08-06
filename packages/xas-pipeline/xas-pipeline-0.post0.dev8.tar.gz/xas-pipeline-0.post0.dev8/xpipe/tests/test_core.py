import sys
import numpy as np
sys.path.append('/home/zliang/Documents/xas-data-pipeline/')
from xpipe.core import *
from xpipe.utils import *

def test_standardize_grid():
    '''
    Test `standardize` function in core module.
    '''
    energy_grid = np.array([1,2,2,3,4,4,4,5,6], dtype=np.float32)
    spectrum = np.array([1,2,4,4,5,6,7,8,9],dtype=np.float32)
    x = {
        '1': {
            'filename': 'test_name1',
            'energy': energy_grid,
            'trans': spectrum,
            'fluo': spectrum,
            'ref': spectrum
        },
        '2': {
            'filename': 'test_name2',
            'energy': energy_grid,
            'trans': spectrum,
            'fluo': spectrum,
            'ref': spectrum
        }
    }
    x_out = standardize_grid(x, step=0.5, start=1, end=6)
    np.testing.assert_allclose(x_out['energy'],
                                  np.array([1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5], dtype=np.float32))
    np.testing.assert_allclose(x_out['fluos'],
                               np.array([[1., 2.3, 3., 3.45, 4., 4.9, 6., 7.075, 8., 8.675],
                                         [1., 2.3, 3., 3.45, 4., 4.9, 6., 7.075, 8., 8.675]]))
    np.testing.assert_allclose(x_out['fluos'], x_out['trans'])
    np.testing.assert_allclose(x_out['fluos'], x_out['refs'])
    np.testing.assert_array_equal(x_out['filenames'], ['test_name1', 'test_name2'])



if __name__ == "__main__":
    import pickle
    xd = pickle.load(open('test_data/raw_dict.pkl','rb'))
    xd = remove_background(xd, bg_range=(7650,7675), scan_types=['ref'])
    xd.show()