// News-image entry for make.fun bounty news-image-20261118.
//
// The poster (entry.png) is drawn by render.py in this repository and
// shipped as a file. This program only copies it to the output directory,
// so the two grader runs always write the same bytes.
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Never remove outDir itself: in the grader sandbox /output is a mounted
// volume, and removing a mount point fails with EBUSY. Only its contents
// are cleared, one child at a time.
mkdirSync(outDir, { recursive: true });
for (const child of readdirSync(outDir)) {
  rmSync(join(outDir, child), { recursive: true, force: true });
}

const src = join(repoDir, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png not found in repository");
}
copyFileSync(src, join(outDir, "entry.png"));

// The grader runs the program twice and requires identical bytes both
// times, so confirm the copy is whole before exiting.
const copied = statSync(join(outDir, "entry.png")).size;
const original = statSync(src).size;
if (copied !== original) {
  throw new Error(`entry.png copy incomplete: ${copied} of ${original} bytes`);
}
if (copied > 1048576) {
  throw new Error(`entry.png exceeds 1 MiB: ${copied} bytes`);
}
