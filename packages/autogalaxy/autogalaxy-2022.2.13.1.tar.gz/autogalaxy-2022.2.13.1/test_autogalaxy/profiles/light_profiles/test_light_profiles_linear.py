import numpy as np
import pytest

import autoarray as aa
import autogalaxy as ag


def test__inversion_via_linear_sersic():

    grid = ag.Grid2D.uniform(shape_native=(11, 11), pixel_scales=0.2)

    psf = ag.Kernel2D.manual_native(
        array=[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]], pixel_scales=0.2
    )

    sersic = ag.lp.EllSersic(centre=(0.1, 0.1), intensity=0.1)

    galaxy = ag.Galaxy(redshift=0.5, light=sersic)

    simulator = ag.SimulatorImaging(
        exposure_time=300.0, psf=psf, add_poisson_noise=False
    )

    imaging = simulator.via_galaxies_from(galaxies=[galaxy], grid=grid)

    mask = ag.Mask2D.circular(
        shape_native=grid.shape_native, pixel_scales=grid.pixel_scales, radius=0.5
    )

    masked_imaging = imaging.apply_mask(mask=mask)

    blurred_image_2d = sersic.blurred_image_2d_via_convolver_from(
        grid=masked_imaging.grid,
        convolver=masked_imaging.convolver,
        blurring_grid=masked_imaging.blurring_grid,
    )

    sersic_linear = ag.lp_linear.EllSersic(centre=(0.1, 0.1))

    lp_linear = ag.lp_linear.LightProfileLinear(
        light_profile=sersic_linear,
        grid=masked_imaging.grid,
        blurring_grid=masked_imaging.blurring_grid,
        convolver=masked_imaging.convolver,
    )

    inversion = ag.Inversion(
        dataset=masked_imaging,
        linear_obj_list=[lp_linear],
        settings=ag.SettingsInversion(use_w_tilde=False, check_solution=False),
    )

    assert isinstance(inversion.linear_obj_list[0], ag.lp_linear.LightProfileLinear)
    assert isinstance(inversion.leq, aa.LEqImagingMapping)
    assert inversion.reconstruction[0] == pytest.approx(0.1, 1.0e-4)
    assert inversion.mapped_reconstructed_image == pytest.approx(
        blurred_image_2d, 1.0e-4
    )

    inversion = ag.Inversion(
        dataset=masked_imaging,
        linear_obj_list=[lp_linear],
        settings=ag.SettingsInversion(use_w_tilde=True, check_solution=False),
    )

    assert isinstance(inversion.linear_obj_list[0], ag.lp_linear.LightProfileLinear)
    assert isinstance(inversion.leq, aa.LEqImagingWTilde)
    assert inversion.reconstruction[0] == pytest.approx(0.1, 1.0e-4)
    assert inversion.mapped_reconstructed_image == pytest.approx(
        blurred_image_2d, 1.0e-4
    )
