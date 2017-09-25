# Caveats

This container entrypoint script assumes you have the following volume mounts:

* $logstash-filter-verifier-json-test-dir --> /etc/logstash/tests
* $logstash-config-dir --> /etc/logstash/conf.d/
* $logstash-pattern-dir --> /etc/logstash/patterns.d
