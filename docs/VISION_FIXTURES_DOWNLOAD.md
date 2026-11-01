# Vision fixtures download (Release assets)

The `vision_images*` trees under `evo/office/fixtures/` are large (~3.4 GiB) and are **not** stored in the `main` Git history. Restore them from the GitHub Release when you need vision self-checks, heldout evals, or flywheel work on a new machine.

## Release

- Tag: [`vision-fixtures-c2290-v363`](https://github.com/jlk1997/SuperEnvolutionModel/releases/tag/vision-fixtures-c2290-v363)
- Matches repo tip content for commit `5a263887` (C2290 / V363 era fixtures)
- Assets:
  - `vision_images_part1.tar`
  - `vision_images_part2.tar`

## Clone code (no images)

```bash
git clone https://github.com/jlk1997/SuperEnvolutionModel.git
cd SuperEnvolutionModel
```

## Download assets

From the [Release page](https://github.com/jlk1997/SuperEnvolutionModel/releases/tag/vision-fixtures-c2290-v363), download both `.tar` files (browser, `gh release download`, or `curl -L`).

Example with GitHub CLI:

```bash
gh release download vision-fixtures-c2290-v363 \
  --repo jlk1997/SuperEnvolutionModel \
  --pattern 'vision_images_part*.tar' \
  --dir /tmp/envolution-vision
```

## Extract into fixtures

Paths inside each archive are relative to `evo/office/fixtures/` (for example `vision_images/...`, `vision_images_v10/...`).

```bash
mkdir -p evo/office/fixtures
tar -xf /tmp/envolution-vision/vision_images_part1.tar -C evo/office/fixtures
tar -xf /tmp/envolution-vision/vision_images_part2.tar -C evo/office/fixtures
```

Windows (PowerShell), from the repo root:

```powershell
New-Item -ItemType Directory -Force -Path evo\office\fixtures | Out-Null
tar -xf $env:TEMP\vision_images_part1.tar -C evo\office\fixtures
tar -xf $env:TEMP\vision_images_part2.tar -C evo\office\fixtures
```

## Notes

- Do **not** `git add` / commit the extracted images; keep them local or re-download from the Release.
- A normal `git push` of the full image blobs was unstable on GitHub (~3 GiB pack HTTP 500); Release assets are the supported distribution path.
- After extract, vision scripts that read `evo/office/fixtures/vision_images*` should find the same layout as on the original development machine.
