import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.molarity_calculator.molarity import MolarityCalculator


class TestMolarityCalculator(BaseTestCase):
    """mass = M × V × MW"""

    def test_basic_molarity(self):
        """MW=180.16 g/mol, 1 mM, 100 mL => 0.018016 g"""
        outputs = TaskRunner(
            task_type=MolarityCalculator,
            params={
                "mw": "180.16",
                "molarity": "1",
                "mol_unit": "mM",
                "final_vol": "100",
                "vol_unit": "mL",
                "mass_unit_out": "g",
            },
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))

    def test_mass_in_mg(self):
        """MW=180.16 g/mol, 10 mM, 1 mL, output in mg"""
        outputs = TaskRunner(
            task_type=MolarityCalculator,
            params={
                "mw": "180.16",
                "molarity": "10",
                "mol_unit": "mM",
                "final_vol": "1",
                "vol_unit": "mL",
                "mass_unit_out": "mg",
            },
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))
