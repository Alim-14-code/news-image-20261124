// Entry program for make.fun competition news-image-20261124 (Node 22,
// standard library only). The image is the pre-rendered entry.png beside
// this file (drawn by render.py, Pillow, local use only). This program
// copies it into the grader's /output directory as entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readdirSync, rmSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
// Clear only the CONTENTS of the output dir (never the directory itself).
for (const name of readdirSync(outDir)) {
  rmSync(join(outDir, name), { recursive: true, force: true });
}

copyFileSync(src, join(outDir, 'entry.png'));
const size = statSync(join(outDir, 'entry.png')).size;
if (size === 0 || size > 1024 * 1024) {
  throw new Error(`entry.png has an unexpected size: ${size} bytes`);
}
console.log(`wrote ${join(outDir, 'entry.png')} (${size} bytes)`);
