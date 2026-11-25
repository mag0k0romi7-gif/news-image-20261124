# news-image-20261124 — rev4

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/mag0k0romi7-gif/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/mag0k0romi7-gif/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Sum up Tuesday 24 November 2026's world news in one image: 46 stories from
9 regions (North America, Latin America, Europe, Middle East, Africa, South
Asia, East Asia, Southeast Asia, Oceania), each checked against the day's
reporting, drawn as a single 1024×1024 newspaper front page with a top-stories
strip and one card per region.

## How it works

- `draw.py` draws `entry.png` from the story table in `stories.md`
  (46 date-checked stories) using Pillow. It asserts every bullet fits in
  two lines and every card fits its box. Run it twice and the bytes are
  identical.
- `main.py` is the entrypoint: it copies `entry.png` to the output directory
  (`$MAKEFUN_OUTPUT_DIR`, default `/output`), standard library only.
- `stories.md` lists every story with its source.

## Run

```sh
python3 draw.py            # writes entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```
