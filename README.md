# Maturam
## Introduction
This is my attempt at a roguelike game in python.
The aim of the exercise is to stretch my python skills.
Hone my development skills and have some fun.

## Version History

Date| Version | Author | Reason
--|---|---|--
20220618| 00.00.00 |Denis Jackman | Initial Version
20220621| 00.00.01 |Denis Jackman | Added tables and updated notes
20220823| 01.00.00 |Denis Jackman | Final version based on the tutorials
20260903| 01.01.00 |Denis Jackman | Added pytest suite and Tests CI job, fixed the pylint/flake8 CI gate, removed the committed virtualenv, fixed a numpy bug tests caught, and fixed the malformed docs table
20260904| 01.02.00 |Denis Jackman | Added a scoring system with a local leaderboard, passive HP regeneration scaled by constitution, a character-naming prompt shown on the leaderboard, and fixed several tcod event-dispatch RuntimeWarnings
20260904| 01.02.01 |Denis Jackman | Fixed the game-over score display drifting 1 point above the leaderboard entry actually recorded for that run
20260904| 01.03.00 |Denis Jackman | Added an AWS-backed global leaderboard (API Gateway + Lambda + DynamoDB, deployed via CDK) alongside the local one, with silent fallback to the local file on any network/API failure
  |   |   |

## Links
* [Maturam Game Page](https://denisjackman.github.io/Maturam/)
* [Maturam Game Source Code](https://github.com/denisjackman/Maturam)
* [Maturam Game Wiki](https://github.com/denisjackman/Maturam/wiki)

## Tools
* [Scan PDF to Excel](https://www.pdftoexcelconverter.net/)
* [Pixlr - Online Sprite editor](https://pixlr.com/x/#editor)
* [RGB Colour Picker](https://www.colorspire.com/rgb-color-wheel/)

## References
* [Roguelike Dev on Reddit](https://www.reddit.com/r/roguelikedev/)
* [Roguelike tutorials](https://rogueliketutorials.com/)

## Status
* [![Pylint](https://github.com/denisjackman/Maturam/actions/workflows/pylint.yml/badge.svg)](https://github.com/denisjackman/Maturam/actions/workflows/pylint.yml)
* [![Tests](https://github.com/denisjackman/Maturam/actions/workflows/tests.yml/badge.svg)](https://github.com/denisjackman/Maturam/actions/workflows/tests.yml)
* [![pages-build-deployment](https://github.com/denisjackman/Maturam/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/denisjackman/Maturam/actions/workflows/pages/pages-build-deployment)

## Licence
![Creative Commons](docs/cc-zero.png)
