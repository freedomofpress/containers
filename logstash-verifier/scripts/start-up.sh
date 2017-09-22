#!/bin/bash
#
#
set -e

LOGSTASH_PATH=/usr/share/logstash/bin

/sbin/paxctl -cm /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 2> /dev/null

cd /etc/logstash/conf.d/ || exit

# Exclude multiline and input and output logs
rm /tmp/all &> /dev/null || true

# Gather up all configs except for input/output lines (num in the 01/9x range)
find ./ -type f -name '*conf' -not -name '01*' -not -name '9*' | sort -n | xargs cat >> /tmp/all

if [ "$2" = "all" ]; then
    CONFIG_PATH=/tmp/
else
    CONFIG_PATH=/etc/logstash/conf.d/
fi

/usr/local/bin/logstash-filter-verifier --logstash-path=$LOGSTASH_PATH/logstash \
    "/etc/logstash/tests/$1" "${CONFIG_PATH}/$2"
