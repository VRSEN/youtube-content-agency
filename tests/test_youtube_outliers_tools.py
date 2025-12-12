import unittest


class TestOutliersToolInputNormalization(unittest.TestCase):
    def test_competitors_accepts_list_of_objects(self):
        """Agent often passes a list of {channel_id, channel_name} objects."""
        from yt_content_strategy_agent.tools.FindOutliersForChannelsTool import (
            FindOutliersForChannelsTool,
        )

        competitors = [
            {"channel_id": "UC123", "channel_name": "Chan A"},
            {"channel_id": "UC456", "channel_name": "Chan B"},
        ]

        # Should validate/instantiate without raising.
        _ = FindOutliersForChannelsTool(competitors=competitors)

    def test_competitors_accepts_dict_id_to_name(self):
        from yt_content_strategy_agent.tools.FindOutliersForChannelsTool import (
            FindOutliersForChannelsTool,
        )

        competitors = {"UC123": "Chan A", "UC456": "Chan B"}
        _ = FindOutliersForChannelsTool(competitors=competitors)

    def test_competitors_accepts_comma_separated_ids(self):
        from yt_content_strategy_agent.tools.FindOutliersForChannelsTool import (
            FindOutliersForChannelsTool,
        )

        competitors = "UC123,UC456"
        _ = FindOutliersForChannelsTool(competitors=competitors)


class TestFindChannelOutliersStats(unittest.TestCase):
    def test_median_even_count_is_average(self):
        """Median should be average of middle two for even N."""
        from yt_content_strategy_agent.tools.FindChannelOutliersTool import (
            _median,
        )

        self.assertEqual(_median([1.0, 3.0, 5.0, 7.0]), 4.0)

    def test_median_odd_count_is_middle(self):
        from yt_content_strategy_agent.tools.FindChannelOutliersTool import (
            _median,
        )

        self.assertEqual(_median([1.0, 3.0, 5.0]), 3.0)


if __name__ == "__main__":
    unittest.main()
