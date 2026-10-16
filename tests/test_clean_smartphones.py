
import unittest
import pandas as pd

from src.cleaning.clean_smartphones import clean_smartphones


class TestCleanSmartphones(unittest.TestCase):

    def setUp(self):
        # Small sample dataset for testing
        self.df = pd.DataFrame({
            "num_cores": [8, None, 6],
            "processor_speed": [2.3, 2.5, None],
            "battery_capacity": [5000, None, 4500],
            "primary_camera_front": [16, 8, None],
            "processor_brand": ["Snapdragon", None, "MediaTek"],
            "os": ["Android", "Android", None],
            "avg_rating": [8.0, None, 7.5],
            "fast_charging": [33.0, None, 18.0],
        })

    def test_original_data_is_not_modified(self):
        original = self.df.copy(deep=True)

        clean_smartphones(self.df)

        pd.testing.assert_frame_equal(self.df, original)

    def test_numeric_missing_values_are_filled(self):
        cleaned, _ = clean_smartphones(self.df)

        numeric_columns = [
            "num_cores",
            "processor_speed",
            "battery_capacity",
            "primary_camera_front",
        ]

        for column in numeric_columns:
            self.assertEqual(cleaned[column].isna().sum(), 0)

    def test_missing_categories_become_unknown(self):
        cleaned, _ = clean_smartphones(self.df)

        self.assertEqual(cleaned["processor_brand"].iloc[1], "Unknown")
        self.assertEqual(cleaned["os"].iloc[2], "Unknown")

    def test_uncertain_missing_values_are_preserved(self):
        cleaned, _ = clean_smartphones(self.df)

        self.assertEqual(cleaned["avg_rating"].isna().sum(), 1)
        self.assertEqual(cleaned["fast_charging"].isna().sum(), 1)

    def test_dataset_shape_is_preserved(self):
        cleaned, _ = clean_smartphones(self.df)

        self.assertEqual(cleaned.shape, self.df.shape)


if __name__ == "__main__":
    unittest.main()
