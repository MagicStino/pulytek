# Public OpenPlugin submission

PulyTek follows the same public process as another community author:

1. Publish this separate public repository, root `openplugin.json`, a compatible release package and source/licenses.
2. Search existing [catalog proposals](https://github.com/MagicStino/force-openplugin/issues?q=is%3Aissue+PulyTek).
3. Post a [community plugin submission](https://github.com/MagicStino/force-openplugin/issues/new?template=plugin-submission.yml),
   naming https://github.com/MagicStino/pulytek, the root manifest, release and exact validation scope.
4. A maintainer reviews metadata/package scripts and uses the acceptance workflow to propose a source registry PR.
   Merging that PR adds the source listing; enabling package downloads is an additional explicit review.
5. Refresh the native catalog after acceptance. The source scanner's latest stable release search may skip this
   prerelease; the portable ZIP can be installed manually for hardware pilot testing.

The root manifest is `openplugin.community/1`; it has no fabricated package until a real release exists. CI writes
actual SHA256, size, ARMv7/portable target, device declarations and the GitHub-owned release URL after publication.
The package contains `mpc-plugin.json` schema 1, standard install/uninstall scripts, a portable folder, native metadata,
checksums, skin assets and complete corresponding source. Device declarations are targets, not reports of hardware testing.

This project does not add itself directly to `reviewed_manifest_repositories` or bypass the public review.
