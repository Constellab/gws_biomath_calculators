import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.linear_dna_ug_to_pmol_ends.linear_dna_ug_to_pmol_ends import LinearDNAUgToPmolEnds


class TestLinearDNAUgToPmolEnds(BaseTestCase):
    """µg → pmol of DNA ends  (2 ends per linear molecule)"""

    def test_basic_conversion(self):
        """1 µg of 3 kb linear dsDNA => pmol of ends"""
        outputs = TaskRunner(
            task_type=LinearDNAUgToPmolEnds,
            params={"mass_ug": "1", "length_kb": "3"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))

    def test_double_mass_double_ends(self):
        """2 µg vs 1 µg => twice as many ends"""
        out1 = TaskRunner(
            task_type=LinearDNAUgToPmolEnds,
            params={"mass_ug": "1", "length_kb": "5"},
        ).run()
        out2 = TaskRunner(
            task_type=LinearDNAUgToPmolEnds,
            params={"mass_ug": "2", "length_kb": "5"},
        ).run()
        r1 = json.loads(open(out1["json"].path, encoding="utf-8").read())["result"]
        r2 = json.loads(open(out2["json"].path, encoding="utf-8").read())["result"]
        val1 = float(str(r1).split()[0])
        val2 = float(str(r2).split()[0])
        self.assertAlmostEqual(val2, val1 * 2, places=6)
