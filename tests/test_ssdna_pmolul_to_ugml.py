import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.ssdna_pmol_par_ul_to_ug_par_ml.ssdna_pmolul_to_ugml import SSDNAPmolulToUgml


class TestSSDNAPmolulToUgml(BaseTestCase):
    """ssDNA pmol/µl → µg/ml  formula: µg/ml = (pmol/µl × N × 330) / 1000"""

    def test_basic_conversion(self):
        """10 pmol/µl of 20-nt oligo => 66 µg/ml"""
        outputs = TaskRunner(
            task_type=SSDNAPmolulToUgml,
            params={"length_nt": "20", "conc_pmolul": "10"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        ugml_val = float(str(data["result"]).split()[0])
        # (10 * 20 * 330) / 1000 = 66
        self.assertAlmostEqual(ugml_val, 66.0, places=3)

    def test_longer_oligo(self):
        """5 pmol/µl of 50-nt oligo => 82.5 µg/ml"""
        outputs = TaskRunner(
            task_type=SSDNAPmolulToUgml,
            params={"length_nt": "50", "conc_pmolul": "5"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        ugml_val = float(str(data["result"]).split()[0])
        expected = (5 * 50 * 330) / 1000
        self.assertAlmostEqual(ugml_val, expected, places=3)
