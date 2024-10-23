FROM bitnami/spark:latest

USER root
# RUN apt-get update && apt-get install -y openjdk-11-jdk
# ENV SPARK_SUBMIT_OPTIONS="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0"

ADD postgresql-42.2.23.jar /opt/spark/jars/
RUN chmod 644 /opt/spark/jars/postgresql-42.2.23.jar

# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# ENV PATH="$JAVA_HOME/bin:$PATH"