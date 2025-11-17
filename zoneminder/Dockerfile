ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    ffmpeg \
    && ln -sf python3 /usr/bin/python

# Copy requirements and install Python packages
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Copy addon files
COPY run.sh zoneminder_integration.py /
RUN chmod a+x /run.sh

WORKDIR /
CMD [ "/run.sh" ]
