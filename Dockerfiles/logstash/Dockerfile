ARG ELK_VERSION=7.13.0

# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash:${ELK_VERSION}
RUN logstash-plugin install logstash-output-mongodb
# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
