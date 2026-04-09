import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.molar_conversions.molar_conversions import MolarConversions


class TestMolarConversions(BaseTestCase):
    """Protein kDa / pmol / µg conversions"""

    def test_calculate_ug(self):
        """50 kDa, 10 pmol => 0.5 µg"""
        outputs = TaskRunner(
            task_type=MolarConversions,
            params={
                "calculate_for": "μg of Protein",
                "size_kda": "50",
                "pmol": "10",
                "mass_ug": "",
            },
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))

    def test_calculate_pmol(self):
        """50 kDa, 0.5 µg => 10 pmol"""
        outputs = TaskRunner(
            task_type=MolarConversions,
            params={
                "calculate_for": "pmol of Protein",
                "size_kda": "50",
                "pmol": "",
                "mass_ug": "0.5",
            },
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))

    def test_calculate_kda(self):
        """0.5 µg, 10 pmol => 50 kDa"""
        outputs = TaskRunner(
            task_type=MolarConversions,
            params={
                "calculate_for": "Protein Size (kDa)",
                "size_kda": "",
                "pmol": "10",
                "mass_ug": "0.5",
            },
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))
