import copy
import matplotlib.pyplot as plt
import sys; sys.path.append('/home/zliang/Documents/xas-data-pipeline/xpipe/')
from utils import *
import logging
import h5py


class XASDataSet:
    
    def __init__(self, raw_data={}, standard_data={}, element=None):
        self.raw = raw_data # the raw dict read from hd5 file
        self.dict = standard_data # the core data structure that the pipeline works on
        self.element = element
        pass
    

    def __len__(self):
        assert len(self.dict) !=0, "Error: Data not standardized!"
        return len(self.dict['key_list'])

    @property
    def raw_energy_range(self):
        '''
        Return the min possible and max possible energy for measurement.
        '''
        grid_ends = []
        for d in self.raw.values():
            grid_ends.extend([d['energy'].min(), d['energy'].max()])
        return [np.min(grid_ends), np.max(grid_ends)]
    
    @property
    def energy(self):
        if self.dict == {}:
            raise ValueError("Energy grid not standardized yet!")
        return self.dict['energy']


    @classmethod
    def from_file(cls, file_path, element=None):
        '''
        Create dataset from suported file (raw data).
        '''
        if file_path.endswith('.h5'):
            raw_data = read_hd5(file_path)
        else:
            raise OSError("Only '.hd5' file is supported so far")
        
        return cls(raw_data=raw_data, element=element)

    @classmethod
    def from_dict(cls, raw_data={}, standard_data={}, element=None):
        '''
        Create dataset from the standard data. 
        This method is different from creating the class directly in that this method usually
        takes a subset of "keys" that are available in the raw data. So raw data is cropped 
        to match what are actually available in standard data.
        '''

        if len(raw_data.keys()) > 0:
            _raw_data = {key:raw_data[key] for key in standard_data['key_list']}
        
        return cls(raw_data = _raw_data, standard_data=standard_data, element=element)

    @property
    def dataframe(self):
        '''
        View the data as dataframe
        '''
        assert len(self.dict) !=0, "Error: Data not standardized!"
        num_rows = len(self.dict['key_list'])
        energy_columns = [f'ENE_{e:.2f}' for e in self.dict['energy']]
        df_property = pd.DataFrame(
            {
                'key': self.dict['key_list'],
                'file_name': self.dict['filename'],
                'label': -1 * np.ones(num_rows),
                'type': [None] * num_rows
            }
        )
        df_spec_list = []
        for scan_type in self.dict.keys():
            if scan_type in ['trans', 'fluo', 'ref']:
                df_spec = pd.concat([df_property,
                                    pd.DataFrame(data=self.dict[scan_type], columns=energy_columns)], axis=1)
                df_spec['type'] = scan_type
                df_spec_list.append(df_spec)
        df_spec_all = pd.concat(df_spec_list, axis=0)
    
        return df_spec_all.sort_values('key')


    def by_key(self, keys):
        '''
        query data by 'key'
        '''
        assert len(self.dict) !=0, "Error: Data not standardized!"

        indices = []
        for key in keys:
            try:
                idx = self.dict['key_list'].index(key)
            except ValueError as e:
                print(e)
            else:
                indices.append(idx)

        dict_subset = {
            'energy': self.dict['energy'],
            'key_list': [self.dict['key_list'][i] for i in indices] ,
            'filename': [self.dict['filename'][i] for i in indices],
            'trans': self.dict['trans'][indices],
            'fluo': self.dict['fluo'][indices],
            'ref': self.dict['ref'][indices]
        }

        return XASDataSet.from_dict(standard_data=dict_subset, raw_data=self.raw)


    def list_scan(self, scan_type):
        '''
        'query data by scan type'
        '''
        assert len(self.dict) !=0, "Error: Data not standardized!"
        assert scan_type in ['fluo', 'trans', 'ref'], "Scan type must be one of: 'fluo', 'trans', 'ref'"

        return self.dict[scan_type]


    def by_filename(self, filename):
        '''
        query by filename
        '''
        assert len(self.dict) !=0, "Error: Data not standardized!"
        indices = []
        for f in filename:
            try:
                idx = self.dict['filename'].index(f)
            except ValueError as e:
                print(e)
            else:
                indices.append(idx)
    
        dict_subset = {
            'energy': self.dict['energy'],
            'key_list': [self.dict['key_list'][i] for i in indices],
            'filename': [self.dict['filename'][i] for i in indices],
            'trans': self.dict['trans'][indices],
            'fluo': self.dict['fluo'][indices],
            'ref': self.dict['ref'][indices]
        }

        return XASDataSet.from_dict(standard_data=dict_subset, raw_data=self.raw)


    def describe(self):
        '''
        Yield a general description of the data.
        '''
        print("A description of the dataset will be added later")
    
    
    def show(self, max_sample=None, keys=None, scan_types='all', plot_range=None, warning_on=True):
        '''
        Plot out spectra
        '''
        
        if scan_types == 'all':
            scan_types = ['trans', 'fluo', 'ref']

        if keys is not None:
            x = self.by_key(keys)
        elif max_sample is not None:
            if max_sample > len(self): max_sample = len(self)
            random_keys = np.random.choice(self.dict['key_list'],size=max_sample)
            x = self.by_key(random_keys)
        else:
            x = self
        
        if plot_range is not None:
            range_select = x.energy > (plot_range[0] & x.energy < plot_range[1])
        else:
            range_select = np.ones_like(x.energy, dtype=bool)
        
        fig_list = []
        for scan_type in scan_types:
            # select content accorting to scan type and energy range
            specs = x.list_scan(scan_type)[:,range_select]
            # Drop rows that contain NaN and Inf in the plot, and warn
            select_drop = np.isnan(specs).any(axis=1) | np.isinf(specs).any(axis=1)
            if warning_on and (select_drop.sum() > 0):
                keys_drop = [x.dict['key_list'][i] for i in np.where(select_drop)[0]]
                logging.warning(f"Thses scans in '{scan_type}' contains NaN or Inf: {str(keys_drop)}")
            # creae plot
            title = f"Element: {x.element} Scan type: {scan_type}"
            fig = plot_spectra(x.energy[range_select], specs[~select_drop],
                               title=title)
            fig_list.append(fig)
            plt.show()

        return fig_list



##################################################################
def read_hd5(file_path):
    '''
    A simple method to create data pipeline directly from an hd5 data file.

    '''
    x = h5py.File(file_path, 'r')
    x_dict = {
        key: {
            'filename': x[key]['filename'][()],
            'energy': x[key]['energy'][()],
            'trans': x[key]['trans'][()],
            'fluo': x[key]['fluo'][()],
            'ref': x[key]['ref'][()]
        }
        for key in list(x.keys())
    }

    return x_dict


def get_energy_range(x):
    '''
    Plot out the histograms for starting energy and ending energies.
    '''
    pass


def remove_background(dataset, bg_range=None, method='linear', scan_types='all'):
    '''
    Subtract backrgound for spectra.
    '''
    y = copy.deepcopy(dataset)

    if scan_types == 'all':
        scan_types = ['trans','fluo', 'ref']
    
    for scan_type in scan_types:
        y.dict[scan_type] = subtract_background(y.dict[scan_type], y.dict['energy'], fit_range=bg_range, method=method)

    return y


def standardize_grid(dataset, step=0.2, start=4000, end=8000, verbose=False):
    '''
    Convert raw data dict to standard data. 
    
    Input data must have no duplicate energy points.

    Parameters
    ----------
    x: dict
        Input dict of data contains the following key/value pairs:
            key_1:{
                'filename': filename of spectrum key_1,
                'energy': energy grid key_1 spectrum was taken on
                'trans': transmission scan for key_1,
                'fluo': fluorescence scan for key_1,
                'ref': reference scan for key_1
            },
            key_2: {...},
            key_3: {...},
            ...
    step : scalar
        The minimum energy difference of the standard grid
    start : scalar
        The start energy of standard grid
    end: : scalar
        The ending energy of the standard grid, note that the actual ending
        energy is one `step` less than the nominal value of `end`.

    Returns
    -------
    dict_standard : dict
        A new dict contains the following key/value pairs:
            `key_list`: A list of length N for keys of all measurements.
            `filename`: A list of length N for filename of all measurements
            `energy`: standard energy grid, 1-D array of length M.
            `fluos`: fluorescence measurements,  2-D array of shape (N, M) 
            `trans`: transmission measurments, 2-D array of shape (N, M)
            `refs`: reference measurements, 2-D array of shape (N, M)
    '''

    y = copy.deepcopy(dataset)
    e_min, e_max = y.raw_energy_range
    if (end < e_min) | (start > e_max):
        raise ValueError(f"energy grid out of range: [{e_min}, {e_max}]")
    
    key_list = list(y.raw.keys())
    grid_standard = np.arange(start, end, step=step, dtype=np.float32)

    for k, d in y.raw.items():
        if len(d['energy']) <= 3: # discarded if smaller than 3 data points
            key_list.remove(k)
            if verbose:
                logging.warning(f"Key {k:s} discarded. Too few data points.")
            continue
        for scan_type in ['trans', 'fluo', 'ref']:
            is_nan = np.isnan(d[scan_type])
            if (~is_nan).sum() <= 3: # 
                y.raw[k][scan_type] = np.array([np.NaN] * len(grid_standard))
                continue
            # merge duplicate measurements
            grid_reduced, spec_reduced = merge_duplicate_energy(d['energy'][~is_nan], 
                                                                d[scan_type][~is_nan])
        
            try: 
            # map spectra onto standard energy grid
                spec_standard = featurize(spec_reduced, grid_reduced, to_grid=grid_standard,
                                        kind='cubic', fill_value='both_ends')
            except ValueError:
                print(k)
                raise
            y.raw[k][scan_type] = spec_standard

    standard_dict = {
        'key_list': key_list,
        'energy': grid_standard,
        'filename': [y.raw[k]['filename'] for k in key_list],
        'trans': np.stack([y.raw[k]['trans'] for k in key_list]),
        'fluo': np.stack([y.raw[k]['fluo'] for k in key_list]),
        'ref' : np.stack([y.raw[k]['ref'] for k in key_list])
    }

    return XASDataSet.from_dict(standard_data=standard_dict, raw_data=dataset.raw, element=dataset.element)
    

def standardize_intensity(dataset, mean_range=(4000,8000), scan_types='all'):
    '''
    Subtract mean and divide by standardard deviation.
    '''
    y = copy.deepcopy(dataset)

    if scan_types == "all":
        scan_types = ['fluo', 'trans', 'ref']

    for scan_type in scan_types:
        spec_standard = normalize(y.dict[scan_type], grid=y.dict['energy'],
                                  mean_range=mean_range)

        num_nan_rows = np.isnan(spec_standard).any(axis=1).astype('bool').sum()
        num_inf_rows = np.isinf(spec_standard).any(axis=1).astype('bool').sum()
        if num_nan_rows >0:
            logging.warning(f"Type {scan_type}: {num_nan_rows} contains NaN!")
        if num_inf_rows >0:
            logging.warning(f"Type {scan_type}: {num_inf_rows} contains Inf!")

        y.dict[scan_type] = spec_standard

    return y


import matplotlib.pyplot as plt
def plot_spectra(grid, specs, figsize=(8,6), lw=1, ls='-', alpha=0.8, title=None):
    
    fig, ax = plt.subplots(figsize=figsize)
    for spec in specs:
        ax.plot(grid, spec, alpha=alpha, lw=lw, ls=ls)
    ax.set_title(title)
    return fig
