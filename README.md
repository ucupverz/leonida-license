# Leonida License — image meme entry

A parody driver-license card meme rendered with Python + Pillow (render.py), using the make.fun ghost mascot (assets/mark-1024.png) as the licensee photo. The joke is a 13-year wait (2013 to 2026) for the video game, told as a license that never expires.

## How to Run

- Regenerate meme image (1024x1024):
  python render.py

- Copy post metadata to the output directory:
  node main.ts

Outside the grader, run:
  mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

(If Node.js requires type stripping: node --experimental-strip-types main.ts)

## Files

- assets/mark-1024.png: make.fun ghost mascot graphic used as licensee photo
- meme.png: Generated 1024x1024 meme image
- render.py: Python script using Pillow to render the meme
- main.ts: Script that copies POST.json to the output directory
- POST.json: Metadata payload containing caption and account details
- README.md: Documentation
- LICENSE: Standard MIT License

## Notes

- The meme is posted on X from the public account @pucuys
- POST.json post_url is filled in after posting
- make.fun play code: makefun-basket-inkwell-saffron
