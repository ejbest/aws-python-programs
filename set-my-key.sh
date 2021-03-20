#!/usr/bin/env bash
set -x
git config --global user.name "EJ Best"
git config --global user.email "erich.ej.best@gmail.com"
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_san5

