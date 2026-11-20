import * as fs from 'node:fs';
import * as path from 'node:path';

const botDir: string = process.env.MAKEFUN_BOT_DIR || '.';
const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR || 'out';

const src: string = path.join(botDir, 'POST.json');
const dest: string = path.join(outputDir, 'POST.json');

fs.mkdirSync(outputDir, { recursive: true });
fs.copyFileSync(src, dest);