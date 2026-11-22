import * as fs from 'node:fs';
import * as path from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR || '.';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || 'out';
const srcPost = path.join(botDir, 'POST.json');
const destPost = path.join(outputDir, 'POST.json');

let postText: string;
try {
  postText = fs.readFileSync(srcPost, 'utf8');
} catch (error) {
  const detail = error instanceof Error ? error.message : String(error);
  console.error(`Error: cannot read ${srcPost}: ${detail}`);
  process.exit(1);
}

let post: unknown;
try {
  post = JSON.parse(postText);
} catch (error) {
  const detail = error instanceof Error ? error.message : String(error);
  console.error(`Error: ${srcPost} is not valid JSON: ${detail}`);
  process.exit(1);
}

if (
  typeof post !== 'object' ||
  post === null ||
  !('url' in post) ||
  typeof post.url !== 'string' ||
  post.url.trim().length === 0
) {
  console.error(`Error: ${srcPost} must contain a non-empty string field named "url".`);
  process.exit(1);
}

try {
  fs.mkdirSync(outputDir, { recursive: true });
  fs.copyFileSync(srcPost, destPost);
} catch (error) {
  const detail = error instanceof Error ? error.message : String(error);
  console.error(`Error: cannot copy ${srcPost} to ${destPost}: ${detail}`);
  process.exit(1);
}

console.log(`post: ${post.url}`);
