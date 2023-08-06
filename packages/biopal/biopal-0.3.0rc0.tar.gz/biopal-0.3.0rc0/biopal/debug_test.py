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

_path = r"C:\ARESYS_PROJ\workingDir\biopal_data_V2_update\demo_lope_two\dataSet\GC_02_H_275.00_RGSW_00_RGSBSW_00_AZSW_00_BSL_00"
SLC_obj = BiomassL1cRaster(_path, channel_to_read=2)
plot_db(SLC_obj, title="SLC_obj")
plt.show()

_path = r"C:\bio\outNotebook\AGB\Products\temp\geocoded\GC_02_H_230.00_RGSW_00_RGSBSW_00_AZSW_00\theta.tif"
theta_obj = BiomassL2Raster(_path, intermediate_latlon_flag=True)
plot_rad2deg(theta_obj, title="theta_obj")
plt.show()

_path = r"C:\bio\outNotebook\AGB\Products\temp\geocoded\GC_02_H_230.00_RGSW_00_RGSBSW_00_AZSW_00\theta.tif"
theta_obj = BiomassL2Raster(_path)
plot_rad2deg(theta_obj, title="theta_obj wrong labels")
plt.show()

_path = r"C:\bio\outNotebook\AGB\Products\temp\geocoded\GC_02_H_230.00_RGSW_00_RGSBSW_00_AZSW_00\sigma0_hh.tif"
sigma_obj = BiomassL2Raster(_path, band_to_read=1, intermediate_latlon_flag=True)
plot(sigma_obj, title="sigma_obj")
plt.show()


_path = (
    r"C:\ARESYS_PROJ\workingDir\biopal_data_V2_update\demo_lope_two\auxiliary_data_pf\ReferenceAGB\cal_05_no_errors.tif"
)
cal_agb_obj = BiomassL2Raster(_path, band_to_read=1)
plot(cal_agb_obj)
plt.show()

_path = r"C:\bio\outNotebook\AGB\Products\global_AGB\AF050M\E045N048T3\agb_1_est_db_backtransf_.tif"
agb_obj = BiomassL2Raster(_path)
plot(agb_obj, xlims=[4512, 4523], ylims=[5033, 5043])
plt.show()
