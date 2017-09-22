FROM docker.elastic.co/logstash/logstash:5.5.0

# Set pax flags accordingly - this was kind of annoying to fix
# I initially tried to setfattr on the files but they didnt stick post-build
# also tried setuid flags on the /bin/paxflags binary -- no dice. Chowning java
# to logstash user was the path of least resistance here :shrug:
USER root
RUN yum install attr -y && yum clean all
ADD paxflags /bin/paxflags
RUN chown logstash:logstash `realpath /etc/alternatives/java` && \
    chmod +x /bin/paxflags && \
    sed -i 's!#\!/bin/bash -e!#\!/bin/bash -e\n/bin/paxflags!g' /usr/local/bin/docker-entrypoint

# Set default user back to logstash
USER logstash
