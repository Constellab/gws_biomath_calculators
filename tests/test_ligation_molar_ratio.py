import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.ligation_molar_ratio.ligation_molar_ratio import LigationMolarRatio


class TestLigationMolarRatio(BaseTestCase):
    """ng_insert = (I/V) × (kb_insert / kb_vector) × ng_vector"""

    def test_1_to_3_ratio(self):
        """1:3 ratio, 0.5 kb insert, 3 kb vector, 50 ng vector"""
        outputs = TaskRunner(
            task_type=LigationMolarRatio,
            params={
                "insert_kb": "0.5",
                "vector_ng": "50",
                "vector_kb": "3",
                "ratio_insert": "1",
                "ratio_vector": "3",
            },
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        self.assertNotIn("ERROR", str(data["result"]))
        ng_val = float(data["result"].split(" ng ")[0].strip())
        expected = (1 / 3) * (0.5 / 3) * 50
        self.assertAlmostEqual(ng_val, expected, places=4)

    def test_1_to_1_ratio(self):
        """1:1 ratio, 1 kb insert, 4 kb vector, 100 ng vector"""
        outputs = TaskRunner(
            task_type=LigationMolarRatio,
            params={
                "insert_kb": "1",
                "vector_ng": "100",
                "vector_kb": "4",
                "ratio_insert": "1",
                "ratio_vector": "1",
            },
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertNotIn("ERROR", str(data["result"]))
        ng_val = float(data["result"].split(" ng ")[0].strip())
        expected = (1 / 1) * (1 / 4) * 100
        self.assertAlmostEqual(ng_val, expected, places=4)
