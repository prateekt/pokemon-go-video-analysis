import os
from typing import Optional

import numpy as np
import pandas as pd
from algo_ops.ops.op import Op
from ocr_ops.framework.op.result.ocr_result import OCRPipelineResult

from battle_logger.battle_logger_result import BattleLoggerResult


class BattleLoggerOp(Op):
    def __init__(self):
        """
        Operation that parses the battle log and determines which Pokémon are in the battle.
        """
        super().__init__(func=self.parse_battle_log)
        self.input: Optional[OCRPipelineResult] = None
        self.output: Optional[BattleLoggerResult] = None
        self.opponent_pkmn_screen_coord = np.array([696, 164], dtype=float)
        self.my_pkmn_screen_coord = np.array([105, 164], dtype=float)
        self.max_text_dist: float = 50

    def parse_battle_log(self, ocr_result: OCRPipelineResult) -> BattleLoggerResult:
        """
        Parses the battle log and determines which Pokémon are in the battles.

        param ocr_result: OCRPipelineResult object containing the OCR result.

        return:
            BattleLoggerResult object containing the Pokémon in the battle.
        """

        # obtain the OCR result as a dataframe of detected text boxes
        df = ocr_result.to_df()
        df["frame"] = [
            int(os.path.basename(f).split(".")[0][3:]) for f in df.input_path
        ]

        # load Pokémon moves backend file
        pokemon_df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                              "pkmn_data", "pokemon_moves.csv"))
        all_pokemon_names = pokemon_df["Pokémon"].str.lower().values

        # run Pokémon filter on text in text boxes
        found_pokemon = df.text.str.lower().str.contains("|".join(all_pokemon_names))
        found_pokemon[found_pokemon.isnull()] = False
        df["found_pokemon"] = df.text.str.lower().str.extract(
            "(" + "|".join(all_pokemon_names) + ")", expand=False
        )

        # isolate text boxes that fall within my or the opponent's Pokémon screen locations
        text_boxes = df.bounding_box.values.astype(str)
        starting_vertices = [
            text[str(text).find("(") + 2: str(text).find(",")]
            for text in text_boxes
        ]
        starting_vertices = np.array(
            [[float(v.split()[0]), float(v.split()[1])] for v in starting_vertices],
            dtype=float,
        )
        d1 = np.sum(np.abs(starting_vertices - self.my_pkmn_screen_coord), 1)
        my_pkmn_text_boxes = df[(d1 < self.max_text_dist) & found_pokemon]
        d2 = np.sum(np.abs(starting_vertices - self.opponent_pkmn_screen_coord), 1)
        opponent_pkmn_text_boxes = df[(d2 < self.max_text_dist) & found_pokemon]

        # isolate unique pokemon in battle
        my_pokemon_list = my_pkmn_text_boxes.found_pokemon.unique()
        opponents_pokemon_list = opponent_pkmn_text_boxes.found_pokemon.unique()

        # determine mapping to frame number
        pokemon_in_frames = {
            (my_pokemon, "my"): my_pkmn_text_boxes.frame[
                my_pkmn_text_boxes.found_pokemon == my_pokemon
            ]
            .unique()
            .tolist()
            for my_pokemon in my_pokemon_list
        }
        opponent_pokemon_in_frames = {
            (opponents_pokemon, "opponent"): opponent_pkmn_text_boxes.frame[
                opponent_pkmn_text_boxes.found_pokemon == opponents_pokemon
            ]
            .unique()
            .tolist()
            for opponents_pokemon in opponents_pokemon_list
        }
        pokemon_in_frames.update(opponent_pokemon_in_frames)

        # return BattleLoggerResult object
        return BattleLoggerResult(pokemon_in_frames=pokemon_in_frames)

    def vis(self) -> None:
        """
        Visualizes the result of the BattleLoggerOp operation.
        """
        if self.output is None:
            raise ValueError("Output is None. Run the operation first.")
        self.output.vis()

    def vis_input(self) -> None:
        """
        Visualizes the input to the BattleLoggerOp operation.
        """
        if self.input is None:
            raise ValueError("Input is None. Run the operation first.")
        print(self.input.to_df())

    def save_input(self, out_path: str, basename: Optional[str] = None) -> None:
        """
        Saves the input to the BattleLoggerOp operation.
        """
        if self.input is None:
            raise ValueError("Input is None. Run the operation first.")
        self.input.to_df().to_csv(
            os.path.join(out_path, basename + ".csv"), index=False
        )

    def save_output(self, out_path, basename: Optional[str] = None) -> None:
        """
        Saves the output of the BattleLoggerOp operation.
        """
        if self.output is None:
            raise ValueError("Output is None. Run the operation first.")
        self.output.to_df().to_csv(
            os.path.join(out_path, basename + ".csv"), index=False
        )
        self.output.plot(
            outfile=os.path.join(out_path, basename + ".png"), suppress_output=True
        )
