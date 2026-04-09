import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.ssdna_ug_par_ml_to_pmol_par_ul.ssdna_ugml_to_pmolul import SSDNAUgmlToPmolul


class TestSSDNAUgmlToPmolul(BaseTestCase):
    """ssDNA µg/ml → pmol/µl  formula: pmol/µl = (µg/ml × 1000) / (N × 330)"""

    def test_basic_conversion(self):
        """66 µg/ml of 20-nt oligo => 10 pmol/µl"""
        outputs = TaskRunner(
            task_type=SSDNAUgmlToPmolul,
            params={"length_nt": "20", "conc_ugml": "66"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        pmolul_val = float(str(data["result"]).split()[0])
        expected = (66 * 1000) / (20 * 330)
        self.assertAlmostEqual(pmolul_val, expected, places=3)

    def test_round_trip(self):
        """66 µg/ml → pmol/µl → back to µg/ml should give ~66"""
        from gws_biomath_calculators.biomath_calcul.ssdna_pmol_par_ul_to_ug_par_ml.ssdna_pmolul_to_ugml import SSDNAPmolulToUgml

        out1 = TaskRunner(
            task_type=SSDNAUgmlToPmolul,
            params={"length_nt": "30", "conc_ugml": "99"},
        ).run()
        pmol_str = json.loads(open(out1["json"].path, encoding="utf-8").read())["result"]
        pmol_val = float(str(pmol_str).split()[0])

        out2 = TaskRunner(
            task_type=SSDNAPmolulToUgml,
            params={"length_nt": "30", "conc_pmolul": str(pmol_val)},
        ).run()
        ug_val = float(str(json.loads(open(out2["json"].path, encoding="utf-8").read())["result"]).split()[0])
        self.assertAlmostEqual(ug_val, 99.0, places=3)
