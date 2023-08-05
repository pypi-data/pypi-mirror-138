import os
import tarfile
import unittest
import urllib.request
from pathlib import Path
import pytest

from dagmc_bounding_box import DagmcBoundingBox


class TestPythonApi(unittest.TestCase):
    """Tests functionality of the package"""

    def setUp(self):

        if not Path("tests/v0.0.2.tar.gz").is_file():
            url = "https://github.com/fusion-energy/neutronics_workflow/archive/refs/tags/v0.0.2.tar.gz"
            urllib.request.urlretrieve(url, "tests/v0.0.2.tar.gz")

            tar = tarfile.open("tests/v0.0.2.tar.gz", "r:gz")
            tar.extractall("tests")
            tar.close()

        self.h5m_filename_smaller = "tests/neutronics_workflow-0.0.2/example_01_single_volume_cell_tally/stage_2_output/dagmc.h5m"
        self.h5m_filename_bigger = "tests/neutronics_workflow-0.0.2/example_02_multi_volume_cell_tally/stage_2_output/dagmc.h5m"

    def test_corners_returns_correct_type(self):

        for dagmc_filename in [self.h5m_filename_smaller, self.h5m_filename_bigger]:
            my_bb = DagmcBoundingBox(dagmc_filename).corners()
            assert isinstance(my_bb, tuple)
            assert isinstance(my_bb[0], tuple)
            assert isinstance(my_bb[1], tuple)
            assert isinstance(my_bb[0][0], float)
            assert isinstance(my_bb[0][1], float)
            assert isinstance(my_bb[0][2], float)
            assert isinstance(my_bb[1][0], float)
            assert isinstance(my_bb[1][1], float)
            assert isinstance(my_bb[1][2], float)
            assert len(my_bb) == 2
            assert len(my_bb[0]) == 3
            assert len(my_bb[1]) == 3

    def test_corners_relative_magnitude(self):

        for dagmc_filename in [self.h5m_filename_smaller, self.h5m_filename_bigger]:
            my_bb = DagmcBoundingBox(dagmc_filename).corners()

            assert my_bb[0][0] < my_bb[1][0]
            assert my_bb[0][1] < my_bb[1][1]
            assert my_bb[0][2] < my_bb[1][2]

    def test_bounding_box_size(self):

        my_bb = DagmcBoundingBox(self.h5m_filename_bigger).corners()

        print(my_bb)
        assert len(my_bb) == 2
        assert len(my_bb[0]) == 3
        assert len(my_bb[1]) == 3
        assert my_bb[0][0] == pytest.approx(-10005, abs=0.1)
        assert my_bb[0][1] == pytest.approx(-10005, abs=0.1)
        assert my_bb[0][2] == pytest.approx(-10005, abs=0.1)
        assert my_bb[1][0] == pytest.approx(10005, abs=0.1)
        assert my_bb[1][1] == pytest.approx(10005, abs=0.1)
        assert my_bb[1][2] == pytest.approx(10005, abs=0.1)

    def test_bounding_box_size_with_expand(self):

        my_bb = DagmcBoundingBox(self.h5m_filename_bigger).corners(
            expand=(100, 200, 300)
        )

        print(my_bb)
        assert len(my_bb) == 2
        assert len(my_bb[0]) == 3
        assert len(my_bb[1]) == 3
        assert my_bb[0][0] == pytest.approx(-10005 - 100, abs=0.1)
        assert my_bb[0][1] == pytest.approx(-10005 - 200, abs=0.1)
        assert my_bb[0][2] == pytest.approx(-10005 - 300, abs=0.1)
        assert my_bb[1][0] == pytest.approx(10005 + 100, abs=0.1)
        assert my_bb[1][1] == pytest.approx(10005 + 200, abs=0.1)
        assert my_bb[1][2] == pytest.approx(10005 + 300, abs=0.1)

    def test_bounding_box_size_2_with_expand(self):

        my_bb = DagmcBoundingBox(self.h5m_filename_smaller).corners(
            expand=(100, 200, 300)
        )

        assert len(my_bb) == 2
        assert len(my_bb[0]) == 3
        assert len(my_bb[1]) == 3
        assert my_bb[0][0] == pytest.approx(-10005 - 100, abs=0.1)
        assert my_bb[0][1] == pytest.approx(-10005 - 200, abs=0.1)
        assert my_bb[0][2] == pytest.approx(-10005 - 300, abs=0.1)
        assert my_bb[1][0] == pytest.approx(10005 + 100, abs=0.1)
        assert my_bb[1][1] == pytest.approx(10005 + 200, abs=0.1)
        assert my_bb[1][2] == pytest.approx(10005 + 300, abs=0.1)
