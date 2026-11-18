# The World in One Day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/tiars837/news-image-18-nov/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/tiars837/news-image-18-nov/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

An editorial poster that sums up the world's news of **Wednesday 18 November 2026** in one image.

## What happened that day

- **Middle East — Conflict:** U.S. jets hit a Revolutionary Guard missile site on Iran's Qeshm Island; Tehran answered with drone attacks in Bahrain and Kuwait.
- **Europe — War:** Ukraine hits the Kerch Bridge again; part of the road span to Crimea collapses into the strait.
- **Asia — Diplomacy:** APEC opens in Shenzhen; Quad leaders meet in Manila. Trump, Xi and Putin meet tomorrow in Shenzhen, at the first trilateral summit.
- **Africa — Health:** Ebola in DR Congo more than doubles — 11,000+ cases and 5,400 deaths, the UN says.
- **Americas — Health:** The U.S. loses its measles-free status after 26 years.
- **Also today:** Cyclone Xavier slams the Cook Islands; a Russian military plane crash kills 19 in Siberia; Peltola wins the Alaska Senate seat as Democrats reach 56.

## How it was made

The poster is drawn entirely by code — `render.py` renders the 1024×1024 PNG with Pillow primitives and DejaVu fonts. No downloaded photos, no AI image generator, no copied artwork: every illustration (jet and explosion over the Gulf, the broken bridge, the three flags, the virus, the thermometer) is drawn from scratch in this repository.

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to the output directory (`/output/entry.png`, or `$MAKEFUN_OUTPUT_DIR`). It runs with no network, and both runs write the same bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
