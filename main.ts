import * as fs from 'node:fs';
import * as path from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR || '.';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || 'out';

fs.mkdirSync(outputDir, { recursive: true });

const srcPost = path.join(botDir, 'POST.json');
const destPost = path.join(outputDir, 'POST.json');

fs.copyFileSync(srcPost, destPost);
