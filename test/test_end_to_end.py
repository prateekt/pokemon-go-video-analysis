import os
import unittest

from battle_logger.battle_logger_result import BattleLoggerResult
from battle_logger.op import BattleLoggerOp
from battle_logger.pipeline import BattleLoggerPipeline


class TestEndToEnd(unittest.TestCase):

    def test_dep(self) -> None:
        """
        Test that the dependencies are installed.
        """

        # check availability of pkmn_data
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pkmn_data", "pokemon_moves.csv")
        self.assertTrue(os.path.exists(file))

    def test_end_to_end(self) -> None:
        """
        Test end-to-end functionality of the BattleLoggerPipeline on a test video.
        """

        # test up paths
        data_path = os.path.join(os.path.dirname(__file__), "test_data")
        test_video_path = os.path.join(data_path, "test_video.mp4")
        out_root = "test_output"
        image_out_path = os.path.join(out_root, "images")
        autosave_output_img_path = os.path.join(out_root, "ocr_images")

        # create BattleLoggerPipeline
        pogo_pipeline = BattleLoggerPipeline()
        pogo_pipeline.set_output_paths(
            image_out_path=image_out_path,
            autosave_output_img_path=autosave_output_img_path,
        )
        output = pogo_pipeline.exec(test_video_path)
        self.assertTrue(isinstance(output, BattleLoggerResult))

        # check results
        self.assertEqual(len(output.pokemon_in_frames), 4)
        self.assertEqual(
            list(output.pokemon_in_frames.keys()),
            [
                ("medicham", "my"),
                ("plusle", "opponent"),
                ("electrode", "opponent"),
                ("jolteon", "opponent"),
            ],
        )

        # save to file and check
        battle_logger_op = pogo_pipeline.find_ops_by_class(op_class=BattleLoggerOp)[0]
        battle_logger_op.save_input(out_path=out_root, basename="ocr_output")
