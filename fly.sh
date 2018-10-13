#!/bin/sh
#
# This submits a job to the condor cluster for processing.

ls
./clean.sh
ls
condor_submit condor.cmd
tail -f condor.log