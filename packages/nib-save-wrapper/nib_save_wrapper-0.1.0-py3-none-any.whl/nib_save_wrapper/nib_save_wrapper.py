import numpy as np
import nibabel as nib

def nib_save(img, fname):
    """Converts an image to a nifti image file on disk. Forces int64 to
    int32"""

    arr = np.asanyarray(img.dataobj)
    if arr.dtype == np.int64:
        arr = np.int32(arr)
        hdr = img.header
        hdr["datatype"] = np.int16([8])
        img = nib.Nifti1Image(arr, img.affine, header=hdr)
    nib.save(img, fname)
