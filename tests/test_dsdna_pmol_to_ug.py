import importlib
import json
import os

from gws_core import BaseTestCase, File, TaskRunner

# DSDNAPmolToUg lives in "dsdna_pmol_to_µg" (U+00B5 micro sign in folder name)
_mod = importlib.import_module(
    "gws_biomath_calculators.biomath_calcul.dsdna_pmol_to_\u00b5g.dsdna_pmol_to_ug"
)
DSDNAPmolToUg = _mod.DSDNAPmolToUg


class TestDSDNAPmolToUg(BaseTestCase):
    """dsDNA pmol → µg  formula: µg = (pmol × bp × 660) / 1e6"""

    def test_basic_conversion(self):
        """0.505 pmol of 3000 bp => ~0.9999 µg"""
        outputs = TaskRunner(
            task_type=DSDNAPmolToUg,
            params={"length_bp": "3000", "pmol": "0.505"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertNotIn("ERROR", str(data.get("result", "")))
        ug_val = float(str(data["result"]).replace(" µg", "").strip())
        expected = (0.505 * 3000 * 660) / 1e6
        self.assertAlmostEqual(ug_val, expected, places=6)

    def test_round_trip(self):
        """1 µg of 5000 bp → pmol → back to µg should be ~1 µg"""
        from gws_biomath_calculators.biomath_calcul.dsdna_ug_to_pmol.dsdna_ug_to_pmol import DSDNAUgToPmol

        out1 = TaskRunner(
            task_type=DSDNAUgToPmol,
            params={"length_bp": "5000", "mass_ug": "1"},
        ).run()
        pmol_str = json.loads(open(out1["json"].path, encoding="utf-8").read())["result"]
        pmol_val = float(pmol_str.replace(" pmol", "").strip())

        out2 = TaskRunner(
            task_type=DSDNAPmolToUg,
            params={"length_bp": "5000", "pmol": str(pmol_val)},
        ).run()
        ug_str = json.loads(open(out2["json"].path, encoding="utf-8").read())["result"]
        ug_val = float(ug_str.replace(" µg", "").strip())
        self.assertAlmostEqual(ug_val, 1.0, places=5)
