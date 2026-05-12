# Stitched, alpha 2 version

Stitched is an extraction of the framework part of the data
processing software of the CMS experiment,
[CMSSW](https://github.com/cms-sw/cmssw). It contains minimal amount
of changes to make the framework usable outside of CMS.

In this alpha 2 version, the hashes of existing commits are expected to
stay unchanged over time. The repository itself will likely be cleaned
up in the future when the project moves to the next alpha or beta
version.

## Branch structure

The plain extraction from CMSSW is kept in `cmssw_master` branch that
tracks the `master` branch of CMSSW with periodical extractions. The
extraction moments are tagged as `CMSSW_<YYYY>_<MM>_<DD>_<hash>` where
the `YYYY`, `MM`, and `DD` are the date of the extraction, and `hash`
is the short hash of the HEAD of the CMSSW `master` branch at the time
of extraction.

The Stitched specific changes are in `main_<YYYY>_<MM>_<DD>` branches,
where the date denotes the tag of CMSSW extraction.

## Contributing

Contributions to the framework code itself should be made to CMSSW itself.

Contributions to the Stitched modifications on top the CMSSW framework
should be done as PRs to this repository. Those PRs should be merged
with the _Rebase and merge_ strategy.
