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

## Working through a library

- **Views:** Loupe (E), Grid (G), Compare (C) and Survey (N), in the bar above the filmstrip. Compare puts two selected photos side by side, or one photo before and after. It keeps the left photo and lets you arrow through candidates on the right. Survey shows every selected photo at once. Side by side, edits only go to the outlined photo.
- **Choosing selects:** 1–5 stars (0 clears), P pick, X reject, U unflag, Auto-advance optional. Filter by flag, rating, edited, variants or look-alikes; sort by name, rating, cohesion or look-alikes together. Export can take just the picks or what's showing.
- **Right-click** any frame, grid cell or the photo itself for everything: rate, flag, reference, compare, variant, paste, even out, match, reset, export, delete. Delete (or the Delete key) takes photos out of the library, lands on the one before, and undoes with Ctrl/Cmd + Z.
- **Pregrade** is a per-photo layer under the look (levels, saturation, white balance, exposure). It's never copied by paste, sync or presets. *Even out* brings each photo's exposure, cast and range to the median of the photos showing, keeping the set's mood. *Neutral* goes for grey whites and middle-grey exposure. *Match reference* solves pregrade exposure, temperature, tint and saturation so the graded photo sits with the graded reference.
- **Cohesion:** every photo is scored 0–100 against the reference (R), or the library average if none is set. The score covers lightness, contrast, neutral cast, colourfulness and palette. The Pregrade panel says what's off ("0.4 stops darker, cooler").
- **Variants:** Ctrl/Cmd + ' makes a second version of the same file with its own edits, shown beside the original in Compare and exported as `-v2`.
- **Look-alikes:** photos that look like the same shot (re-generations, near-identical frames, crops or re-exports) get a ≈ set badge, and "Look-alikes together" sorts them next to each other. Right-click › Survey its look-alikes to pick the best.

## How it works

Everything runs in WebGL 2. Per pixel: sRGB decode → white balance and exposure → vignette → halation and bloom (blurred highlight energy, tinted) → highlight shoulder → levels, shadows/highlights, contrast → film LUT (3D texture) → saturation and vibrance → fade → grain (sized to the image, so preview and export match) → dither.

Library, settings, presets and imported LUTs are stored in the browser (IndexedDB and localStorage) on whichever device you use. Nothing is uploaded.
