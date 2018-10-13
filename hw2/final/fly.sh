#!/bin/sh
#
# This submits a job to the condor cluster for processing.

ls
./clean.sh
ls
condor_submit hw2.cmd
tail -f condor.log