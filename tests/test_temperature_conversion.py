import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.temperature_conversion.temperature_conversion import TemperatureConversion


class TestTemperatureConversion(BaseTestCase):

    def test_celsius_to_all(self):
        """25°C => 77°F => 298.16°K"""
        outputs = TaskRunner(
            task_type=TemperatureConversion,
            params={"value": "25", "unit": "C"},
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        self.assertAlmostEqual(data["result"]["°C"], 25.0, places=2)
        self.assertAlmostEqual(data["result"]["°F"], 77.0, places=2)
        self.assertAlmostEqual(data["result"]["°K"], 298.16, places=2)

    def test_fahrenheit_to_celsius(self):
        """32°F => 0°C"""
        outputs = TaskRunner(
            task_type=TemperatureConversion,
            params={"value": "32", "unit": "F"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        self.assertAlmostEqual(data["result"]["°C"], 0.0, places=2)

    def test_kelvin_to_celsius(self):
        """273.16°K => 0°C"""
        outputs = TaskRunner(
            task_type=TemperatureConversion,
            params={"value": "273.16", "unit": "K"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertNotIn("error", data)
        self.assertAlmostEqual(data["result"]["°C"], 0.0, places=2)

    def test_body_temperature(self):
        """37°C => 98.6°F"""
        outputs = TaskRunner(
            task_type=TemperatureConversion,
            params={"value": "37", "unit": "C"},
        ).run()
        data = json.loads(open(outputs["json"].path, encoding="utf-8").read())
        self.assertAlmostEqual(data["result"]["°F"], 98.6, places=1)
