[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/mag0k0romi7-gif/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/mag0k0romi7-gif/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The World in One Page — Tuesday, 24 November 2026

A single 1024×1024 image summing up the world's news of Tuesday, 24 November 2026:
50 stories from 9 regions (North America, Latin America, Europe, Middle East,
Africa, South Asia, East Asia, Southeast Asia, Oceania), led by Nvidia bringing
back Jensen Huang as chief executive. Every story was reported on 24 November 2026.

## How it is made

- `render.py` draws `entry.png` with Pillow (DejaVu fonts): a newspaper-style
  grid with one panel per region, numbered headlines, a top-story strip and a
  sources footer. Run it with `python3 render.py`; two runs are byte-identical.
- `main.py` (Python 3.13, standard library only) is the entrypoint: it copies
  `entry.png` to the output directory, following the kit's starter pattern.
- `entry.png` is the rendered image the entry ships.

## Sources

Reuters, AP, AFP, BBC, Al Jazeera, The Straits Times, CNA.

## Competition

Entered in [news-image-20261124](https://make.fun/bounty/news-image-20261124) on
[make.fun](https://make.fun).
