# Film pack

These looks come from the **RawTherapee Film Simulation Collection** (version 2015-09-20) by Pat David, Pavlov Dmitry and Michael Ezra, <https://rawpedia.rawtherapee.com/Film_Simulation>, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

**Changes made:** each HaldCLUT (level 12 or 16) was resampled to a 33×33×33 cube with trilinear interpolation, file names were tidied (for example "Kodak Portra 400 1 -" is listed as "Portra 400 −" under Kodak), the identity and "Negative" utility images were left out, and each brand folder was packed into one PNG: 33 rows per look, row = blue, column = red + 33 × green. `index.json` lists the groups and look names in file order. Made with `tools/pack_hald.py`.

This adapted pack is shared under the same licence, CC BY-SA 4.0.

The trademarked names are there only to say which film stock each look approximates. Neither the original authors nor this project are affiliated with or endorsed by the companies that own the trademarks.
