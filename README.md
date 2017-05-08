# Falcon Versioning [![Build Status](https://travis-ci.org/FreakinFacu/falcon_versioning.svg?branch=master)](https://travis-ci.org/FreakinFacu/falcon_versioning) [![codecov](https://codecov.io/gh/FreakinFacu/falcon_versioning/branch/master/graph/badge.svg)](https://codecov.io/gh/FreakinFacu/falcon_versioning)


A versioning plugin for Falcon Framework (Link here)

## Goals
* No changes to resources
* Allow version branching
* Allow default versions
* Keep the interface similar to Falcon's

## How to use
* Define versions with parent versions and default
* Pass to falcon.API as router and middleware
* app.add_route now takes a required version param

## Error handling

## Version Parsing
* Mention both parsers that are included

## Why it needs to be passed as router AND middleware

