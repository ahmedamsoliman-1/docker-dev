#!/bin/bash

mkdir submodule
cd submodule
git clone https://github.com/airbytehq/airbyte.git
cd airbyte
./run-ab-platform.sh
