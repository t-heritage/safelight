# Safelight Film Lab

A browser app for grading photos like film: film stocks, halation, bloom, grain and vignette, batch edits across a whole library (Lightroom style), presets, and a colour check against the Wonder brand colours. Photos never leave the browser.

**Use it:** https://t-heritage.github.io/safelight/
Also published as a private Claude artifact: https://claude.ai/artifact/WXzZ8tMazBMkxgpNPueukj

## What's here

| Path | What it is |
|---|---|
| `src/safelight.html` | The app. Edit this one. It's the page body the Claude artifact publishes. |
| `index.html` | The GitHub Pages site, generated from `src/` by `tools/build_page.py`. Don't edit by hand. |
| `film-pack/` | 293 film looks from the RawTherapee Film Simulation Collection, resampled to 33³ and packed one PNG per brand. See `film-pack/README.md` for credits and licence. |
| `tools/pack_hald.py` | Rebuilds `film-pack/` from the original HaldCLUT folder. |

## Updating

1. Edit `src/safelight.html`.
2. `python3 tools/build_page.py`
3. Commit and push to `main`. GitHub Pages redeploys in a minute or two.
4. To update the Claude artifact too, republish `src/safelight.html` with `film-pack/*.png` alongside it.

If the film pack changes: copy the new `index.json` contents into the `PACK` constant in `src/safelight.html`.

```
python3 tools/pack_hald.py ~/Downloads/HaldCLUT film-pack
```

## How it works

Everything runs in WebGL 2. Per pixel: sRGB decode → white balance and exposure → vignette → halation and bloom (blurred highlight energy, tinted) → highlight shoulder → levels, shadows/highlights, contrast → film LUT (3D texture) → saturation and vibrance → fade → grain (sized to the image, so preview and export match) → dither.

Library, settings, presets and imported LUTs are stored in the browser (IndexedDB and localStorage) on whichever device you use. Nothing is uploaded.
