import os

from battle_logger.pipeline import BattleLoggerPipeline

if __name__ == "__main__":
    # paths
    input_path = ""
    out_root = ""

    # generate output paths
    image_out_path = os.path.join(out_root, "images")
    autosave_output_img_path = os.path.join(out_root, "ocr_images")

    # run pipeline
    pogo_pipeline = BattleLoggerPipeline()
    pogo_pipeline.set_output_paths(
        image_out_path=input_path, autosave_output_img_path=autosave_output_img_path
    )
    output = pogo_pipeline.exec(input_path)

    # save output to disk
    pogo_pipeline.save_output(out_path=out_root, basename="output")
