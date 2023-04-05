# Pokémon Go Video Analysis

Tools for analyzing Pokémon Go Player vs. Player (PvP) Videos.

```commandline
from battle_logger.pipeline import BattleLoggerPipeline

pogo_pipeline = BattleLoggerPipeline()
output = pogo_pipeline.exec('path/to/video')
pogo_pipeline.save_output(out_path="test_output", basename="battle_logger_output")
```

Extract battles from videos and analyze what Pokémon appear in which battles:

![](https://github.com/prateekt/pokemon-go-video-analysis/raw/main/readme_figs/battle_1.png)

Log your battles and analyze your Pokémon's performance:

![](https://github.com/prateekt/pokemon-go-video-analysis/raw/main/readme_figs/example_table.png)

<b>Installation:</b>

```
make conda_dev
conda activate pogo_video_analysis_env
pip install pokemon-go-video-analysis
```