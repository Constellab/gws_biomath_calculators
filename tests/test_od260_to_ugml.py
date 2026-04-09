import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.od260_to_ugml.od260_to_ugml import OD260ToUgml


class TestOD260ToUgml(BaseTestCase):
    """OD260 × conversion factor => µg/ml"""

    def test_dna(self):
        """OD260=1.0, DNA => 50 µg/ml"""
        outputs = TaskRunner(
            task_type=OD260ToUgml,
            params={"od260": "1.0", "sample_type": "DNA"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        ugml_val = float(str(data["result"]).split()[0])
        self.assertAlmostEqual(ugml_val, 50.0, places=2)

    def test_rna(self):
        """OD260=1.0, RNA => 40 µg/ml"""
        outputs = TaskRunner(
            task_type=OD260ToUgml,
            params={"od260": "1.0", "sample_type": "RNA"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        ugml_val = float(str(data["result"]).split()[0])
        self.assertAlmostEqual(ugml_val, 40.0, places=2)

    def test_ssdna(self):
        """OD260=1.0, Single-stranded-DNA => 35 µg/ml"""
        outputs = TaskRunner(
            task_type=OD260ToUgml,
            params={"od260": "1.0", "sample_type": "Single-stranded-DNA"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        ugml_val = float(str(data["result"]).split()[0])
        self.assertAlmostEqual(ugml_val, 35.0, places=2)

    def test_oligo(self):
        """OD260=1.0, Single-stranded-Oligo => 20 µg/ml"""
        outputs = TaskRunner(
            task_type=OD260ToUgml,
            params={"od260": "1.0", "sample_type": "Single-stranded-Oligo"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        ugml_val = float(str(data["result"]).split()[0])
        self.assertAlmostEqual(ugml_val, 20.0, places=2)
