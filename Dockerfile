FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive
ARG HOST_UID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git openssh-client curl ca-certificates \
    python3 python3-venv python3-pip python3-dev tmux nano less sudo \
    && rm -rf /var/lib/apt/lists/*

# Ubuntu 24.04 images already include user "ubuntu" (UID 1000).
# If your WSL user ID differs, align it so file ownership matches.
RUN if [ "${HOST_UID}" != "1000" ]; then \
      usermod -u ${HOST_UID} ubuntu && groupmod -g ${HOST_UID} ubuntu; \
    fi \
 && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu

USER ubuntu
WORKDIR /workspace

# Create ~/.ssh as "ubuntu" so the ssh-keys volume isn't owned by root
RUN mkdir -p /home/ubuntu/.ssh && chmod 700 /home/ubuntu/.ssh

RUN python3 -m venv /home/ubuntu/venv
ENV PATH="/home/ubuntu/venv/bin:$PATH"
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["sleep", "infinity"]