#!/usr/bin/python
# Homebrew Cleaner
# Author: Fang2hou

import commands
import re

ignoreList = [
    "telnet",
    "aria2",
    "zsh",
    "you-get",
    "ffmpeg",
    "libav",
    "wget",
    "go",
    "node",
    "python",
    "python3",
    "vim",
    "ruby",
    "imagemagick",
    "gnuplot",
]

def IsListed(formula):
    for listedFormula in ignoreList:
        if listedFormula == formula:
            return True
    return False

def SetDeps(formula):
    depString = commands.getoutput('brew deps ' + formula)
    depList = depString.split("\n")
    if depList != [""]:
        for ignoreDeps in depList:
            if not IsListed(ignoreDeps):
                ignoreList.append(ignoreDeps)
                SetDeps(ignoreDeps)

def GetAllFormulae():
    formulaString = commands.getoutput('brew list')
    formulaList = re.split("\t|\n", formulaString)
    return formulaList

def Main():
    loopList = ignoreList[:]
    for formula in loopList:
        SetDeps(formula)

    loopList = GetAllFormulae()

    for formula in loopList:
        if not IsListed(formula):
            commands.getoutput('brew uninstall --ignore-dependencies ' + formula)

Main()