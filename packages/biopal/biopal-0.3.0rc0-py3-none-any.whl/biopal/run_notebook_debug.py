from pathlib import Path
import sys
import os
from matplotlib import pyplot as plt
import numpy as np

biopal_path = Path("C:\ARESYS_PROJ\BioPAL")

sys.path.append(str(biopal_path))
os.chdir(biopal_path)

from biopal.io.data_io import BiomassL1cRaster, BiomassL2Raster
from biopal.utility.plot import *

input_path = r"C:\bio\demo_input_file_run_AGB.xml"

from biopal.dataset_query.dataset_query import dataset_query

dataset_query_obj = dataset_query()
input_path_from_query = dataset_query_obj.run(input_path)

from biopal.io.xml_io import parse_input_file

input_params_obj = parse_input_file(input_path_from_query)
stack_based_processing_obj = input_params_obj.stack_based_processing
found_stack_ids = stack_based_processing_obj.stack_composition.keys()
print("SLC SAR images (slant range geometry) stacks and acquisitions found from the query")
for stack_id, acquisition_ids in stack_based_processing_obj.stack_composition.items():
    print("\n    Stack:")
    print("    ", stack_id)
    print("        Acquisitions:")
    for acq_id in acquisition_ids:
        print("        ", acq_id)
dataSet_path = input_params_obj.dataset_query.L1C_repository
print("\n The above stacks with the acquisitions can be found at following path:\n {}".format(dataSet_path))
# Print the path of the DTM projected in radar coordinates
reference_height_path = Path.home().joinpath(
    dataSet_path, stack_based_processing_obj.reference_height_file_names[stack_id]
)
print(
    "\n Full path of the reference height file valid for the above stack {}: \n {}".format(
        stack_id, reference_height_path
    )
)


#################### Plotting one of the SLC
slc_pf_path = Path.home().joinpath(dataSet_path, acq_id)

# initialize the SLC data object (its an L1C Raster)
SLC_obj = BiomassL1cRaster(slc_pf_path, channel_to_read=2)

# BioPAL offers different ways to plot a data with internal methods "plot_db", "plot_abs", "plot_angle", "plot":

# 1) Automatic plot
plot_db(SLC_obj)
plt.show()

# 2) Automatic plot with custom inputs:
plot_abs(
    SLC_obj, title="custom title 1 (ABS example)", clims=[0, 0.4], xlims=[8, 10], ylims=[6, 8],
)
plt.show()

# 3) Passing a pyplot axis to the automatic plot, than customize the axis as desired:
fig, ax = plt.subplots()
plot_angle(SLC_obj, ax=ax)
ax.set_xlabel("my xlabel")
ax.set_ylabel("my ylabel")
ax.set_title("custom title 2 (Angle example)")
ax.set_xlim([8, 10])
ax.set_ylim([6, 8])
fig.show()

# 4) Manual plot, from SLC_obj attributes:
plt.figure()
plt.imshow(
    10 * np.log10(np.abs(SLC_obj.data) ** 2),
    extent=[SLC_obj.x_axis[0], SLC_obj.x_axis[-1], SLC_obj.y_axis[-1], SLC_obj.y_axis[0],],
    cmap="gray",
)
plt.xlabel(SLC_obj.x_axis_description)
plt.ylabel(SLC_obj.y_axis_description)
plt.title("custom title 3 manual example")
plt.show()

# From here, into this Notebook automatic plot functions are used.


channel_to_read = 0  # Counter is zero based, there is only one channel
reference_height_obj = BiomassL1cRaster(reference_height_path, channel_to_read)
plot_db(reference_height_obj)
plt.show()

from biopal.agb.main_AGB import StackBasedProcessingAGB

configuration_file_path = str(Path.home().joinpath(biopal_path, "biopal", "conf", "Configuration_File.xml"))

# Initialize Stack Based Processing AGB APP
stack_based_processing_obj = StackBasedProcessingAGB(configuration_file_path)

# Run Stack Based Processing AGB APP
print("AGB stack-based processing APP started...")
(input_file_from_stack_based, configuration_file_updated,) = stack_based_processing_obj.run(input_path_from_query)

# Some of the computed output paths:
import os

input_params_obj = parse_input_file(input_file_from_stack_based)
output_folder = input_params_obj.output_specification.output_folder

npy_name = str(list(Path(Path.home().joinpath(output_folder, "Products", "breakpoints")).rglob("*.npy"))[0])
ground_canc_sr_path = Path.home().joinpath(output_folder, npy_name,)
print("\n Path of ground cancelled data in slant range geometry: \n {}".format(ground_canc_sr_path))

geocoded_dir = str(list(Path(Path.home().joinpath(output_folder, "Products", "temp", "geocoded")).rglob("GC_*"))[0])
sigma_tif_name = str(list(Path(geocoded_dir).rglob("sigma0_vh.tif"))[0])
ground_canc_gr_path = Path.home().joinpath(geocoded_dir, sigma_tif_name,)
print("\n  Path of ground cancelled VH data, geocoded: \n {}".format(ground_canc_gr_path))

theta_tif_name = str(list(Path(geocoded_dir).rglob("theta.tif"))[0])
theta_inc_path = Path.home().joinpath(geocoded_dir, theta_tif_name,)
print("\n  Path of incidence angle map, geocoded: \n {}".format(theta_inc_path))

# initialize the geocoded tif data object
# (BiomassL2Raster can be used both for intermediate gecoded and for output EQUI7 products)
ground_canc_obj = BiomassL2Raster(str(ground_canc_gr_path), band_to_read=1)
plot_db(ground_canc_obj)
plt.show()


theta_inc_obj = BiomassL2Raster(str(theta_inc_path), band_to_read=1)
theta_inc_figure = plot(theta_inc_obj)
plt.show()

from biopal.agb.main_AGB import CoreProcessingAGB

# Initialize Core Processing AGB APP
agb_processing_obj = CoreProcessingAGB(configuration_file_updated)

# Run Main APP #2: AGB Core Processing
print("AGB core-processing APP started (this will take some time, wait for ending message)...")
agb_processing_obj.run(input_file_from_stack_based)


input_params_obj = parse_input_file(input_file_from_stack_based)
output_folder = input_params_obj.output_specification.output_folder
tile_equi7_folder = list(Path.home().joinpath(Path(output_folder), "Products", "global_AGB").rglob("*"))[0]
tile_equi7_subfolder = list(Path(tile_equi7_folder).rglob("*"))[0]
final_estimation_path = list(Path(tile_equi7_subfolder).rglob("*.tif"))[0]
print("\n Path of the final AGB estimation product, in EQUI7 map geometry: \n {}".format(final_estimation_path))

reference_agb_folder = input_params_obj.stack_based_processing.reference_agb_folder
calibration_path = Path.home().joinpath(reference_agb_folder, "cal_05_no_errors.tif")
print("\n Path of the input calibration data used: \n {}".format(calibration_path))


lidar_agb_path = r"C:\ARESYS_PROJ\workingDir\biopal_data_V2_update\lope_lidar\equi7_50m\lidar_agb\EQUI7_AF050M\E045N048T3\lidar_AGB_AF050M_E045N048T3.tif"
if not Path(lidar_agb_path).exists():
    raise ValueError("Path of Lidar AGB - Reference map for validation should be set manually")

lidar_agb_obj = BiomassL2Raster(lidar_agb_path, band_to_read=1)
lidar_agb_figure = lidar_agb_obj.plot()
plt.show()

theta_inc_obj = BiomassL2Raster(lidar_agb_path, band_to_read=1)
plot(theta_inc_obj)
plt.show()


calibration_path = str(Path.home().joinpath(reference_agb_folder, "cal_05_no_errors.tif"))
band_to_read = 1
calibration_agb_obj = BiomassL2Raster(calibration_path, band_to_read)
calibration_agb_obj.plot(title="il mio titolo")
plt.show()

calibration_agb_obj = BiomassL2Raster(calibration_path, band_to_read)
plot(calibration_agb_obj)
plt.show()
