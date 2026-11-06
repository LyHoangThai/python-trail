# Single-file GitHub installer

Customers need only **Install-Python-Trail.cmd**. Double-clicking it downloads the published sample and opens setup with its setup/start action already running. Docker installation approvals, Docker first-launch prompts and required restarts still require the user. No Git, host Python, manual extraction, or PowerShell commands are needed.

## What it does

1. Reads the current `main` commit from GitHub's public API.
2. Reads `distribution/channel.json` and the release ZIP at that same commit. A concurrent update cannot mix the manifest with another release.
3. Verifies the ZIP SHA-256 and every packaged file hash, validates extraction paths, and installs to `%LOCALAPPDATA%\PythonTrail\python-trail-sample-VERSION`.
4. Runs the existing setup UI with `-AutoStart`. It installs missing prerequisites, builds/starts Docker services, and opens http://localhost:8766/learn.
5. Creates a desktop shortcut for later local starts. This shortcut uses the installed files without another GitHub download.

On managed updates, the installer copies the prior database credentials and known editable assignment files to the new version. Old version folders remain. Browser progress lives in the same persistent Docker volume. Do not delete volumes to update. Another copy of the sample using the same Docker project should not run simultaneously. Existing manually extracted sample installations are separate from this managed folder and are not migrated automatically.

This is an open-source distribution workflow, not source-code protection. It requires the repository and release ZIPs to be publicly readable. It does not request/store a GitHub token. The hash validates the release selected by the repository owner; it is not an independent publisher signature. Never include credentials or personal student data in release archives.

## Publish an update

- Update the product/app and bump `VERSION` in `tools/build_sample.py`, along with product version labels.
- Build the clean sample with `python tools/build_sample.py`.
- Set the matching `version` in `tools/build_bootstrap.py`, then run `python tools/build_bootstrap.py`. This writes the channel hash and regenerates the standalone CMD payload from `bootstrap.ps1`.
- Commit/push the app, ZIP, checksum, channel, and installer together. Never overwrite a published ZIP with different contents under the same version.
- The installer source is `bootstrap.ps1`; customers do not need to download it separately. Do not hand-edit only the CMD payload.

Developer validation can use `bootstrap.ps1 -PrepareOnly -InstallRoot PATH` to download and verify without installing Docker, starting the app, or creating shortcuts. Use a disposable folder separate from your live installation. Setup logs and generated `.env` files remain local; share the clean launcher or release archive.
