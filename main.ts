import * as fs from "node:fs";
import * as path from "node:path";

const botDir: string = process.env.MAKEFUN_BOT_DIR || "/bot";
const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR || "/output";

try {
  fs.mkdirSync(outputDir, { recursive: true });
  const src: string = path.join(botDir, "POST.json");
  const dest: string = path.join(outputDir, "POST.json");
  fs.copyFileSync(src, dest);
} catch (err: unknown) {
  console.error(`Error copying POST.json: ${err}`);
  process.exit(1);
}
