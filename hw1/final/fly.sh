#!/bin/sh
#
# This submits a job to the condor cluster for processing.

./clean.sh
condor_submit condor.cmd
tail -f condor.log