FROM ubuntu:24.04

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		curl \
		net-tools \
		python3 \
		sudo \
		vim \
	&& rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash --groups sudo coder \
	&& echo "coder ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/coder \
	&& chmod 0440 /etc/sudoers.d/coder

USER coder

RUN printf '%s\n' \
	"PS1='\\[\\033[1;36m\\]\\h \\[\\033[1;34m\\]\\W\\[\\033[0;35m\\] \\[\\033[1;36m\\]$ \\[\\033[0m\\]'" \
	>> /home/coder/.bashrc