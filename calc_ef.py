import numpy as np
import os
import pandas as pd


def get_peak_intensities(df, peaks):

    # Getting the value of the peak (max - min values in the range) so-called baseline subtraction,
    peaks_values_df = pd.DataFrame()
    for name, values in peaks.items():
        peaks_values_df.loc[:, name] = df.loc[:, values[0]:values[1]].max(axis=1) \
                                           - df.loc[:, values[0]:values[1]].min(axis=1)

    peaks_values_df.reset_index(drop=True, inplace=True)

    return peaks_values_df



def calculate_ef(i_sers=100000, i_raman=1000):
    """
    Calculating EF for spectra quality labeling
    :return:  Float
    """
    # First step of calculations

    # Concentration of analyte in solution (in mol/dm^3)
    concentration = 1 * 10 ** (-6)

    # # Volume of solution (ml)
    # TODO is it ml or ul
    volume = 200.0

    # # Calculating the number of molecules
    n_av = 6.023 * 10 ** 23
    v_dm = volume * 10 ** (-3)

    num_molecules = n_av * concentration * v_dm

    # zSecond step of calculations - Calculating the laser spot (S_{Laser}S

    # # Laser wavelength in nm
    laser_wave_length = 785 * 10 ** (-9)

    # # Lens parameter - Numerical aperture
    lens_params = 0.22

    # # Calculating the Laser spot

    s_laser = (1.22 * laser_wave_length) / lens_params

    # Third step of calculations - Calculating the surface area irradiated with the laser S0

    s0_spot_area = np.pi * (s_laser / 2) ** 2

    # # Fourth step of calculations - Determination of the number of molecules per laser irradiated surface Nsers

    # # Active surface dimensions
    x_dimension = 3.5
    y_dimension = 3.5

    # # Surface area development coefficient
    surface_dev = 2

    # # The area of active surface of the SERS substrate
    s_platform = x_dimension * y_dimension * 10 ** (-6) * surface_dev

    # # The coverage of the analyte on the surface between 10^-6 and 6*10^-6 ~=10%
    surface_coverage = 0.1

    # n_sers = (num_molecules * s_laser * surface_coverage) / s_platform  # formula version (s_laser zamiast s0)
    n_sers = (num_molecules * s0_spot_area * surface_coverage) / s_platform  # Szymborski use

    # # # #
    # # #
    # # Fifth step of calculations - Calculation of the volume from which the Raman
    # # signal for your compound in solids is recorded
    #

    penetration_depth = 2
    v_compound = s0_spot_area * penetration_depth

    # # # #
    # # #
    # # Sixth step of calculations - Determining the number of p-MBA molecules
    # # from which the Raman signal (N_Raman) comes
    #

    # # Molecular weight
    compound_density = 1.3
    compound_molecular_weight = 154.19

    n_raman = v_compound * (compound_density * 10 ** 6) *6.02*10**(23)/ compound_molecular_weight

    # # Final, seventh, step of calculations - Calculating the Enhancement Factor

    # # SERS intensity and Raman Intensity
    # raman and sers intensities must be provided as parameters
    enhancement_factor = (i_sers / n_sers) * (n_raman / i_raman)

    return enhancement_factor



