# Use a Debian base image
FROM debian:bullseye

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    perl \
    lsb-release && \
    apt-get clean

# Add GLPI-Agent repository and install the GLPI Agent
COPY ./ .
RUN perl ./glpi-agent-1.11-linux-installer.pl

# Expose necessary ports (if needed)
EXPOSE 62354

# Define entrypoint
CMD ["sh", "./entrypoint.sh"]
