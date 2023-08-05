# Software Systems Laboratory Metrics Project

> A helper package to install all Software Systems Laboratory Metrics tools

![[https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)
![[https://img.shields.io/badge/DOI-Example-red](https://img.shields.io/badge/DOI-Example-red)](https://img.shields.io/badge/DOI-Example-red)
![[https://img.shields.io/badge/build-Example-red](https://img.shields.io/badge/build-Example-red)](https://img.shields.io/badge/build-Example-red)
![[https://img.shields.io/badge/license-BSD--3-yellow](https://img.shields.io/badge/license-BSD--3-yellow)](https://img.shields.io/badge/license-BSD--3-yellow)

## Table of Contents

- [Software Systems Laboratory Metrics Project](#software-systems-laboratory-metrics-project)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
    - [Shell Software](#shell-software)
    - [Python Software](#python-software)
  - [Bundled Projects](#bundled-projects)
  - [How To Use](#how-to-use)

## About

The Software Systems Laboratory (SSL) Metrics Project is a collection of `python` tools that can be used on any Git and/or GitHub to generate longitudinal graphs of classical metrics. They can also be modified by outside teams or individuals for usage of their own personal projects.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project and the greater SSL Metrics project, the following software packages are **required**:

### Operating System

All tools developed for the greater SSL Metrics project **must target** Mac OS and Linux. SSL Metrics software is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

It is recomendded to develop on Mac OS or Linux. However, if you are on a Windows machine, you can use WSL to develop as well.

### Shell Software

- `git`
- `wc`

### Python Software

> The software listed in this section is meant for developing tools

All listed Python software assumes that you have downloaded and installed **Python 3.9.6** or greater.

- `black`
- `build`
- `isort`
- `pylint`

You can install all of the Python software with this one-liner:

`pip install --upgrade black build isort pip pylint`

## Bundled Projects

This projects bundles the following `python` projects into one `pip` installable:

- [Git Bus Factor](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-bus-factor)
- [Git Commits LOC](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc)
- [Git Productivity](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-productivity)
- [GitHub Issues](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues)
- [GitHub Issue Density](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issue-density)
- [GitHub Issue Spoilage](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issue-spoilage)
- [GitHub Repository Searcher](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-repository-searcher)
- [JSON Converter](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-json-converter)
- [Metric Badges](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-badges)

## How To Use

For informaton on how to use each of the respective projects, see their respective GitHub pages.

You can install all of the Python software with this one-liner:

`pip install --upgrade pip ssl-metrics-meta`
