# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                             calibration_catalog.py
#            Applies the final zero-point to the photometry catalogs
# ******************************************************************************

"""
Generates photometric calibrated catalogs from the final zero-points and the
photometry output tables

The S-PLUS field is given as the first command line argument. Configurations
are set in the config file, given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------
copy_splus_psf_inst_catalog()
apply_final_zero_points_to_psf()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

Assumes that at least calibration_finalzp.py has already been run for this field

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 calibration_catalog.py *field_name* *config_file*

----------------
"""

################################################################################
# Import external packages

import os
import sys

steps_path = os.path.split(__file__)[0]
pipeline_path = os.path.split(steps_path)[0]
spluscalib_path = os.path.split(pipeline_path)[0]

sys.path.append(spluscalib_path)

################################################################################
# Import spluscalib packages

from spluscalib import utils as ut

################################################################################
# Read parameters

field     = sys.argv[1]
conf_file = sys.argv[2]

conf = ut.pipeline_conf(conf_file)

################################################################################
# Get directories

field_path       = os.path.join(conf['run_path'], field)
crossmatch_path  = os.path.join(field_path, 'Crossmatch')

suffix = ut.calibration_suffix(conf)
calibration_path  = os.path.join(field_path, f'Calibration_{suffix}')

catalogs_path = os.path.join(calibration_path, 'catalogs')
catalogs_path_psf    = os.path.join(catalogs_path, 'psf')
catalogs_path_single = os.path.join(catalogs_path, 'single')
catalogs_path_dual   = os.path.join(catalogs_path, 'dual')

photometry_path = os.path.join(field_path, 'Photometry')

psf_path              = os.path.join(photometry_path, 'psf')
psf_catalog_path      = os.path.join(psf_path, 'catalogs')
psf_xycorrection_path = os.path.join(psf_path, 'xy_correction')
psf_master_path       = os.path.join(psf_path, 'master')

single_path         = os.path.join(photometry_path, 'single')
single_catalog_path = os.path.join(single_path, 'aper_correction')
single_master_path  = os.path.join(single_path, 'master')

dual_path         = os.path.join(photometry_path, 'dual')
dual_catalog_path = os.path.join(dual_path, 'aper_correction')
dual_master_path  = os.path.join(dual_path, 'master')
dual_detection_path = os.path.join(dual_path, 'detection')

log_path = os.path.join(calibration_path, 'logs')

################################################################################
# Initiate log file


ut.makedir(catalogs_path)
ut.makedir(log_path)

# Check for photometry folders

has_photometry_single = os.path.exists(single_catalog_path)
has_photometry_dual   = os.path.exists(dual_catalog_path)
has_photometry_psf    = os.path.exists(psf_catalog_path)

if has_photometry_single:
    ut.makedir(catalogs_path_single)

if has_photometry_dual:
    ut.makedir(catalogs_path_dual)

if has_photometry_psf:
    ut.makedir(catalogs_path_psf)

log_file_name = os.path.join(log_path, 'catalog.log')
log_file_name = ut.gen_logfile_name(log_file_name)
log_file = os.path.join(calibration_path, log_file_name)

with open(log_file, "w") as log:
    log.write("")

################################################################################
# Begin script

# ***************************************************
#    Make single mode filter catalogs
# ***************************************************


def generate_singlemode_filter_catalogues():

    """
    Generates single mode calibrated filter catalogues
    """

    print("")
    ut.printlog(('********** '
                 'Generating single mode calibrated filter catalogues '
                 '**********'),
                 log_file)
    print("")

    for filt in conf['filters']:

        catalog_name = f'sex_{field}_{filt}_single_apercorr.fits'
        catalog_file = os.path.join(single_catalog_path, catalog_name)

        master_name = f'{field}_master_photometry_only_single.fits'
        master_file = os.path.join(single_master_path, master_name)

        zp_name = f'{field}_final.zp'
        zp_file = os.path.join(calibration_path, zp_name)

        save_name = f'{field}_{filt}_single.fits'
        save_file = os.path.join(catalogs_path_single, save_name)

        if not os.path.exists(save_file):

            ut.sexcatalog_apply_calibration(catalog_file = catalog_file,
                                            master_file  = master_file,
                                            zp_file      = zp_file,
                                            save_file    = save_file,
                                            filter_name  = filt,
                                            field        = field,
                                            sex_mag_zp   = conf['inst_zp'],
                                            mode         = 'single',
                                      calibration_flag=conf['calibration_flag'],
                              extinction_maps_path=conf['extinction_maps_path'],
                            extinction_correction=conf['extinction_correction'])

            ut.printlog(f"Created file {save_file}", log_file)

        else:
            ut.printlog(f"Catalog {save_name} already exists", log_file)


if has_photometry_single:
    generate_singlemode_filter_catalogues()


# ***************************************************
#    Make dual mode filter catalogs
# ***************************************************

def generate_dualmode_filter_catalogues():

    """
    Generates dual mode calibrated filter catalogues
    """

    print("")
    ut.printlog(('********** '
                 'Generating dual mode calibrated filter catalogues '
                 '**********'),
                 log_file)
    print("")

    for filt in conf['filters']:

        catalog_name = f'sex_{field}_{filt}_dual_apercorr.fits'
        catalog_file = os.path.join(dual_catalog_path, catalog_name)

        master_name = f'{field}_master_photometry_only_dual.fits'
        master_file = os.path.join(dual_master_path, master_name)

        zp_name = f'{field}_final.zp'
        zp_file = os.path.join(calibration_path, zp_name)

        save_name = f'{field}_{filt}_dual.fits'
        save_file = os.path.join(catalogs_path_dual, save_name)

        if not os.path.exists(save_file):

            ut.sexcatalog_apply_calibration(catalog_file = catalog_file,
                                            master_file  = master_file,
                                            zp_file      = zp_file,
                                            save_file    = save_file,
                                            filter_name  = filt,
                                            field        = field,
                                            sex_mag_zp   = conf['inst_zp'],
                                            mode         = 'dual',
                                      calibration_flag=conf['calibration_flag'])

            ut.printlog(f"Created file {save_file}", log_file)

        else:
            ut.printlog(f"Catalog {save_name} already exists", log_file)


if has_photometry_dual:
    generate_dualmode_filter_catalogues()


# ***************************************************
#    Make dual mode filter catalogs
# ***************************************************

def generate_detection_catalogue():

    """
    Generates dual mode calibrated filter catalogues
    """

    print("")
    ut.printlog(('********** '
                 'Generating dual mode detection catalogue '
                 '**********'),
                 log_file)
    print("")


    detection_name = f'sex_{field}_detection_catalog.fits'
    detection_file = os.path.join(dual_detection_path, detection_name)

    master_name = f'{field}_master_photometry_only_dual.fits'
    master_file = os.path.join(dual_master_path, master_name)

    save_name = f'{field}_detection_dual.fits'
    save_file = os.path.join(catalogs_path_dual, save_name)

    if not os.path.exists(save_file):

        ut.sexcatalog_detection(detection_file   = detection_file,
                                master_file      = master_file,
                                save_file        = save_file,
                                calibration_flag = conf['calibration_flag'],
                                field            = field,
                              extinction_maps_path=conf['extinction_maps_path'],
                          extinction_correction = conf['extinction_correction'])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if has_photometry_dual:
    generate_detection_catalogue()


# ***************************************************
#    Make PSF filter catalogs
# ***************************************************


def generate_psf_filter_catalogues():

    """
    Generates PSF calibrated filter catalogues
    """

    print("")
    ut.printlog(('********** '
                 'Generating PSF calibrated filter catalogues '
                 '**********'),
                 log_file)
    print("")

    for filt in conf['filters']:

        if conf['sex_XY_correction']:
            catalog_name = f'{field}_{filt}_psf_xycorr.cat'
            catalog_file = os.path.join(psf_xycorrection_path, catalog_name)
        else:
            catalog_name = f'{field}_{filt}_psf.cat'
            catalog_file = os.path.join(psf_catalog_path, catalog_name)

        master_name = f'{field}_master_photometry_only_psf.fits'
        master_file = os.path.join(psf_master_path, master_name)

        zp_name = f'{field}_final.zp'
        zp_file = os.path.join(calibration_path, zp_name)

        save_name = f'{field}_{filt}_psf.fits'
        save_file = os.path.join(catalogs_path_psf, save_name)

        if not os.path.exists(save_file):

            ut.psfcatalog_apply_calibration(catalog_file = catalog_file,
                                            master_file  = master_file,
                                            zp_file      = zp_file,
                                            save_file    = save_file,
                                            filter_name  = filt,
                                            field        = field,
                                            inst_mag_zp  = conf['inst_zp'],
                                      calibration_flag=conf['calibration_flag'],
                              extinction_maps_path=conf['extinction_maps_path'],
                            extinction_correction=conf['extinction_correction'])

            ut.printlog(f"Created file {save_file}", log_file)

        else:
            ut.printlog(f"Catalog {save_name} already exists", log_file)


if has_photometry_psf:
    generate_psf_filter_catalogues()


# ***************************************************
#    Copy splus PSF instrumental catalog
# ***************************************************


def copy_splus_psf_inst_catalog():

    """
    Copy S-PLUS PSF instrumental magnitudes to catalogs path
    """

    print("")
    ut.printlog(('********** '
                 'Copying S-PLUS PSF instrumental magnitudes catalog '
                 '**********'),
                 log_file)
    print("")

    catalog_name = f"{field}_master_photometry_only_psf.fits"
    catalog_file = os.path.join(psf_master_path, catalog_name)

    save_name = f'{field}_psf_inst.cat'
    save_file = os.path.join(catalogs_path, save_name)

    if not os.path.exists(save_file) or True:

        cmd = f"java -jar {conf['path_to_stilts']} tcopy "
        cmd += f"in={catalog_file} ifmt=fits "
        cmd += f"out={save_file} ofmt=ascii"
        ut.printlog(cmd, log_file)
        os.system(cmd)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


#if 'photometry_psf' in conf['run_steps']:
    #copy_splus_psf_inst_catalog()


# ***************************************************
#    Apply final zero points to PSF inst catalog
# ***************************************************


def apply_final_zero_points_to_psf():

    """
    Applies final zero-points to psf mag_inst catalog
    """

    print("")
    ut.printlog(('********** '
                 'Applying final zero-points to PSF mag_inst catalog '
                 '**********'),
                 log_file)
    print("")

    catalog_name = f'{field}_psf_inst.cat'
    catalog_file = os.path.join(catalogs_path, catalog_name)

    zp_name = f"{field}_final.zp"
    zp_file = os.path.join(calibration_path, zp_name)

    save_name = f"{field}_psf_calibrated.cat"
    save_file = os.path.join(catalogs_path, save_name)

    if not os.path.exists(save_file) or True:
        ut.zp_apply(catalog   = catalog_file,
                    save_file = save_file,
                    zp_file   = zp_file,
                    fmt = 'ascii',
                    zp_inst = -conf['inst_zp'])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


#if 'photometry_psf' in conf['run_steps']:
#    apply_final_zero_points_to_psf()
