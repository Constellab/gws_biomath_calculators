import importlib
import json
import os

from gws_core import BaseTestCase, File, TaskRunner

# DilutionCalculator lives in "dilution_ calculator" (space in folder name)
_mod = importlib.import_module("gws_biomath_calculators.biomath_calcul.dilution_ calculator.dilution")
DilutionCalculator = _mod.DilutionCalculator


class TestDilutionCalculator(BaseTestCase):

    def test_basic_dilution(self):
        """100 mM stock → 10 mM final in 1 mL => 0.1 mL stock needed"""
        outputs = TaskRunner(
            task_type=DilutionCalculator,
            params={
                "stock_conc": "100",
                "stock_unit": "mM",
                "final_conc": "10",
                "final_unit": "mM",
                "final_vol": "1",
                "final_vol_unit": "mL",
                "stock_vol_unit_out": "mL",
            },
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))

    def test_unit_conversion(self):
        """1 M stock → 1 mM final in 10 mL"""
        outputs = TaskRunner(
            task_type=DilutionCalculator,
            params={
                "stock_conc": "1",
                "stock_unit": "M",
                "final_conc": "1",
                "final_unit": "mM",
                "final_vol": "10",
                "final_vol_unit": "mL",
                "stock_vol_unit_out": "µL",
            },
        ).run()
        result_file: File = outputs["json"]
        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))
