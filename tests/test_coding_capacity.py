import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.coding_capacity_of_dna.coding_capacity import CodingCapacity


class TestCodingCapacity(BaseTestCase):

    def test_from_dna_bp(self):
        """300 bp => 100 aa => 11 kDa"""
        outputs = TaskRunner(
            task_type=CodingCapacity,
            params={"dna_bp": "300", "aa": "", "protein_kda": ""},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        self.assertAlmostEqual(data["results"]["Protein Length (amino acids)"], 100.0, places=4)
        self.assertAlmostEqual(data["results"]["Protein Size (kDa)"], 11.0, places=4)

    def test_from_aa(self):
        """100 aa => 300 bp => 11 kDa"""
        outputs = TaskRunner(
            task_type=CodingCapacity,
            params={"dna_bp": "", "aa": "100", "protein_kda": ""},
        ).run()
        result_file: File = outputs["json"]
        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        self.assertAlmostEqual(data["results"]["DNA Length (bp)"], 300.0, places=4)
        self.assertAlmostEqual(data["results"]["Protein Size (kDa)"], 11.0, places=4)

    def test_from_kda(self):
        """11 kDa => 100 aa => 300 bp"""
        outputs = TaskRunner(
            task_type=CodingCapacity,
            params={"dna_bp": "", "aa": "", "protein_kda": "11"},
        ).run()
        result_file: File = outputs["json"]
        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        self.assertAlmostEqual(data["results"]["DNA Length (bp)"], 300.0, places=4)
        self.assertAlmostEqual(data["results"]["Protein Length (amino acids)"], 100.0, places=4)
