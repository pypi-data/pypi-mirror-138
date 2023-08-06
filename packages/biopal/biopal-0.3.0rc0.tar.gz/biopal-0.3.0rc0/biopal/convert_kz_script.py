import os
from biopal.io.data_io import (
    read_data,
    read_ecef_grid,
    read_auxiliary_multi_channels,
    read_auxiliary_single_channel,
    tandemx_fnf_read,
    tiff_formatter,
    readBiomassHeader,
)
from arepytools.io.productfolder import ProductFolder
from matplotlib import pyplot as plt

kz_pf_name_in = r"C:\bio\BenchmarkBPS\datasets\demo_tomoSAR_3acq_10m\auxiliary_data_pf\Geometry\KZ\GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00"
slope_pf_name_in = r"C:\bio\BenchmarkBPS\datasets\demo_tomoSAR_3acq_10m\auxiliary_data_pf\Geometry\Slope\GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00"

kz_pf_name_out = r"C:\bio\BenchmarkBPS\datasets\demo_tomoSAR_3acq_10m_inv_kz\auxiliary_data_pf\Geometry\KZ\GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00"
slope_pf_name_out = r"C:\bio\BenchmarkBPS\datasets\demo_tomoSAR_3acq_10m_inv_slope\auxiliary_data_pf\Geometry\Slope\GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00"

acquisitions_pf_names = [
    "GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_0001",
    "GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_0002",
    "GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_0003",
]
num_lines = 3008
num_samples = 378
pf_name_kz = os.path.basename(kz_pf_name_in)
folder_name_kz = os.path.dirname(kz_pf_name_in)
kz = read_auxiliary_multi_channels(folder_name_kz, pf_name_kz)

pf_name_slope = os.path.basename(slope_pf_name_in)
folder_name_slope = os.path.dirname(slope_pf_name_in)
slope = read_auxiliary_single_channel(folder_name_slope, pf_name_slope)
if 0:

    pf = ProductFolder(kz_pf_name_out, "w")

    pf.append_channel(num_lines, num_samples, "FLOAT32", header_offset=0)
    pf.write_data(0, -1 * kz["GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_BSL_00"].transpose())
    pf.append_channel(num_lines, num_samples, "FLOAT32", header_offset=0)
    pf.write_data(1, -1 * kz["GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_BSL_01"].transpose())
    pf.append_channel(num_lines, num_samples, "FLOAT32", header_offset=0)
    pf.write_data(2, -1 * kz["GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_BSL_02"].transpose())

    pf_s = ProductFolder(slope_pf_name_out, "w")

    pf_s.append_channel(num_lines, num_samples, "FLOAT32", header_offset=0)
    pf_s.write_data(0, -1 * slope.transpose())


print("fatto")

pf_name_slope = os.path.basename(slope_pf_name_in)
folder_name_slope = os.path.dirname(slope_pf_name_in)
slope_inv = read_auxiliary_single_channel(folder_name_slope, pf_name_slope)


plt.figure()
plt.imshow(slope - slope_inv)
plt.show()
pf_name_kz = os.path.basename(kz_pf_name_in)
folder_name_kz = os.path.dirname(kz_pf_name_in)
kz_inv = read_auxiliary_multi_channels(folder_name_kz, pf_name_kz)
plt.figure()
plt.imshow(
    kz["GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_BSL_01"] - kz_inv["GC_03_H_320.00_RGSW_00_RGSBSW_00_AZSW_00_BSL_01"]
)
plt.show()
