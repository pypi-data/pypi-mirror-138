import h5py


def gef_is_cell_bin(gef_file):
    h5f = h5py.File(gef_file)
    if 'cellBin' in h5f:
        h5f.close()
        return True
    else:
        h5f.close()
        return False
