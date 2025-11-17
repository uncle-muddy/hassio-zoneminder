#!/usr/bin/with-contenv bashio

bashio::log.info "Starting ZoneMinder integration..."

# Get configuration
export ZM_HOST=$(bashio::config 'zm_host')
export ZM_PORT=$(bashio::config 'zm_port')
export ZM_PATH=$(bashio::config 'zm_path')
export ZM_USER=$(bashio::config 'zm_user')
export ZM_PASSWORD=$(bashio::config 'zm_password')
export ZM_SSL_VERIFY=$(bashio::config 'zm_ssl_verify')
export SCAN_INTERVAL=$(bashio::config 'scan_interval')
export EVENT_CHECK_INTERVAL=$(bashio::config 'event_check_interval')

bashio::log.info "Connecting to ZoneMinder at ${ZM_HOST}:${ZM_PORT}${ZM_PATH}"

# Start the Python integration
python3 /zoneminder_integration.py