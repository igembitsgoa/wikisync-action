Integrate WikiSync into your Github Actions workflow

![License: MIT](https://img.shields.io/github/license/igembitsgoa/wikisync-action?style=for-the-badge) 
![GitHub release](https://img.shields.io/github/v/release/igembitsgoa/wikisync-action?style=for-the-badge)

# Github Action for iGEM WikiSync

iGEM WikiSync is a Python package that allows you to automatically upload your iGEM wiki at once. It uploads all the files and replaces all local URLs in your code with `igem.org` URLs. You can find more information about WikiSync [here](https://igem-wikisync.readthedocs.io).

[![igembitsgoa/igem-wikisync - GitHub](https://gh-card.dev/repos/igembitsgoa/igem-wikisync.svg)](https://github.com/igembitsgoa/igem-wikisync)

This Github Action allows you to integrate WikiSync into your workflow, to set up continuous deployment for your wiki.

This example illustrates how to use it:

```yaml
- name: iGEM WikiSync
  uses: igembitsgoa/wikisync-action@v0.3
  with:
    team: 'BITSPilani-Goa_India'
    source: 'dist'
    build: 'igem'
  env:
    IGEM_USERNAME: ${{ secrets.IGEM_USERNAME }}
    IGEM_PASSWORD: ${{ secrets.IGEM_PASSWORD }}
```

## Parameters
1. `team`: Your iGEM team name.
1. `source`: Folder containing the wiki to be uploaded.
1. `build`: Folder where your modified wiki will be stored before deployment. 

Your iGEM username and password must be provided as Github Secrets. Read more about Secrets [here](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets).

Please read the following sections about requirements and keeping track of uploads carefully before using this Action.


# Requirements

Since WikiSync is a Python library, it requires Python to be set up in your runner.

Here is a complete workflow which illustrates this:

```yaml

name: Build and Deploy

on:
  push:
    branches: [ master ]

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2.3.1
        with:
          persist-credentials: false

      # Steps to build your Wiki 
      # (using webpack/react/whatever)

      - name: Set up Python 3.7
        uses: actions/setup-python@v2
        with:
          python-version: 3.7

      - name: iGEM WikiSync
        uses: igembitsgoa/wikisync-action@v0.2
        with:
          team: 'BITSPilani-Goa_India'
          source: 'dist'
          build: 'igem'
        env:
          IGEM_USERNAME: ${{ secrets.IGEM_USERNAME }}
          IGEM_PASSWORD: ${{ secrets.IGEM_PASSWORD }}

```

# Keeping Track of Uploads

WikiSync keeps track of files it has previously uploaded in a file called `upload_map.yml` in your root directory. It also creates `wikisync.log` where it writes a stepwise log of each activity.

In order to make sure that you retain the upload map and the log file, it is necessary that your CI workflow commits these changes back to your repo. If this step is avoided, the action will upload every single file every time you run it.

Here is a complete workflow which illustrates this: 

```yaml
name: Build and Deploy

on:
  push:
    branches: [ master ]

jobs:  
  main:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2.3.1
        with:
          persist-credentials: false
      
      # Steps to build your Wiki
      # (using webpack/react/whatever)

      - name: Set up Python 3.7
        uses: actions/setup-python@v2
        with:
          python-version: 3.7

      - name: iGEM WikiSync
        uses: igembitsgoa/wikisync-action@v0.2
        with:
          team: 'BITSPilani-Goa_India'
          source: 'dist'
          build: 'igem'
        env:
          IGEM_USERNAME: ${{ secrets.IGEM_USERNAME }}
          IGEM_PASSWORD: ${{ secrets.IGEM_PASSWORD }}

      - name: Add Changes to Git
        run: git add upload_map.yml wikisync.log dist igem
        # It is recommended that you add the source and 
        # the build folder along with the upload map and
        # log file. Read note below.

      - name: Commit Changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git commit -m "Successfully built and deployed to iGEM [no-ci]" || echo "No changes to commit"

      - name: Push Changes to Github
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}

```

> **Note:**  This is helpful in order to keep track of the changes WikiSync makes as well as to compare the appearance of your wiki locally or on Github Pages, with that on iGEM servers. Sometimes extra CSS/JS overrides might be necessary to make your Wiki look right, since iGEM displays it within a container.

In case pushing back to your repo is not possible for you, this Action prints the upload map in the Action log by default. You can manually copy and paste this into `upload_map.yml`, but this is highly discouraged. 

# Help, Issues and Feature Requests

In case this Action doesn't work as expected, or you need help getting it to work, please reach out by raising an issue [here](https://github.com/igembitsgoa/wikisync-action/issues).

# Collaboration

Using this Action or submitting issues and pull requests can count towards a collaboration for our teams. Please give us a shoutout at [@igem_bits](https://instagram.com/igem_bits) on Instagram if WikiSync has made your iGEM experience easier! For contibuting to this software or discussing further collaborations, please reach out to us at igembitsgoa@gmail.com.
