import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.dsdna_ug_to_pmol.dsdna_ug_to_pmol import DSDNAUgToPmol


class TestDSDNAUgToPmol(BaseTestCase):
    """dsDNA µg → pmol  formula: pmol = (µg × 1e6) / (bp × 660)"""

    def test_basic_conversion(self):
        """1 µg of 3000 bp => ~0.5051 pmol"""
        outputs = TaskRunner(
            task_type=DSDNAUgToPmol,
            params={"length_bp": "3000", "mass_ug": "1"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        pmol_val = float(data["result"].replace(" pmol", "").strip())
        self.assertAlmostEqual(pmol_val, 1e6 / (3000 * 660), places=6)

    def test_large_fragment(self):
        """1 µg of 10000 bp => ~0.1515 pmol"""
        outputs = TaskRunner(
            task_type=DSDNAUgToPmol,
            params={"length_bp": "10000", "mass_ug": "1"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        pmol_val = float(data["result"].replace(" pmol", "").strip())
        self.assertAlmostEqual(pmol_val, 1e6 / (10000 * 660), places=6)
