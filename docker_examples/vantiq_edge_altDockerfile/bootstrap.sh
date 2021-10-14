#!/usr/bin/env bash

#If python is already install then skip the onboarding steps and just start Vantiq.
if type -P python > /dev/null; then
  /opt/vantiq/bin/vantiq.sh
else
  (/wait-for-it.sh localhost:8080 -t 600; sleep 15; python /vantiqedge_bootstrap.py) &
  apt update && \
  apt install -y python python-pip && \
  pip install requests pyOpenSSL && \
  /opt/vantiq/bin/vantiq.sh
fi