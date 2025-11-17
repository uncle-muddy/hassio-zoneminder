#!/usr/bin/env python3
"""ZoneMinder Integration for Home Assistant."""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ZoneMinderAPI:
    """Interface to ZoneMinder API."""
    
    def __init__(self, host: str, port: int, path: str, user: str, password: str, ssl_verify: bool = True):
        """Initialize the ZoneMinder API connection."""
        self.host = host
        self.port = port
        self.path = path
        self.user = user
        self.password = password
        self.ssl_verify = ssl_verify
        self.base_url = f"{host}:{port}{path}/api"
        self.session = requests.Session()
        self.token = None
        self.monitors = {}
        
    def login(self) -> bool:
        """Authenticate with ZoneMinder."""
        try:
            login_url = f"{self.base_url}/host/login.json"
            data = {
                "user": self.user,
                "pass": self.password
            }
            
            response = self.session.post(
                login_url,
                data=data,
                verify=self.ssl_verify,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get('access_token') or result.get('token')
                logger.info("Successfully authenticated with ZoneMinder")
                return True
            else:
                logger.error(f"Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def get_monitors(self) -> Dict:
        """Fetch all monitors from ZoneMinder."""
        try:
            url = f"{self.base_url}/monitors.json"
            headers = {}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            
            response = self.session.get(
                url,
                headers=headers,
                verify=self.ssl_verify,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                monitors = {}
                
                for monitor in data.get('monitors', []):
                    mon_data = monitor.get('Monitor', {})
                    mon_id = mon_data.get('Id')
                    monitors[mon_id] = {
                        'id': mon_id,
                        'name': mon_data.get('Name'),
                        'enabled': mon_data.get('Enabled') == '1',
                        'function': mon_data.get('Function'),
                        'width': mon_data.get('Width'),
                        'height': mon_data.get('Height'),
                    }
                
                self.monitors = monitors
                logger.info(f"Found {len(monitors)} monitors")
                return monitors
            else:
                logger.error(f"Failed to get monitors: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting monitors: {e}")
            return {}
    
    def get_monitor_stream_url(self, monitor_id: str) -> str:
        """Get the stream URL for a monitor."""
        return f"{self.host}:{self.port}{self.path}/cgi-bin/nph-zms?mode=jpeg&monitor={monitor_id}&scale=100"
    
    def get_events(self, monitor_id: Optional[str] = None, since: Optional[datetime] = None) -> List[Dict]:
        """Get events from ZoneMinder."""
        try:
            url = f"{self.base_url}/events.json"
            headers = {}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            
            params = {}
            if monitor_id:
                params['MonitorId'] = monitor_id
            if since:
                params['StartTime'] = since.strftime('%Y-%m-%d %H:%M:%S')
            
            response = self.session.get(
                url,
                headers=headers,
                params=params,
                verify=self.ssl_verify,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                for event in data.get('events', []):
                    evt_data = event.get('Event', {})
                    events.append({
                        'id': evt_data.get('Id'),
                        'monitor_id': evt_data.get('MonitorId'),
                        'name': evt_data.get('Name'),
                        'cause': evt_data.get('Cause'),
                        'start_time': evt_data.get('StartTime'),
                        'end_time': evt_data.get('EndTime'),
                        'length': evt_data.get('Length'),
                        'frames': evt_data.get('Frames'),
                        'alarm_frames': evt_data.get('AlarmFrames'),
                    })
                
                return events
            else:
                logger.error(f"Failed to get events: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return []
    
    def set_monitor_state(self, monitor_id: str, function: str) -> bool:
        """Set the state of a monitor (Modect, Monitor, Record, etc.)."""
        try:
            url = f"{self.base_url}/monitors/{monitor_id}.json"
            headers = {'Content-Type': 'application/json'}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            
            data = {
                "Monitor": {
                    "Function": function
                }
            }
            
            response = self.session.put(
                url,
                headers=headers,
                json=data,
                verify=self.ssl_verify,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Set monitor {monitor_id} to {function}")
                return True
            else:
                logger.error(f"Failed to set monitor state: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting monitor state: {e}")
            return False


class HomeAssistantAPI:
    """Interface to Home Assistant API."""
    
    def __init__(self):
        """Initialize Home Assistant API connection."""
        self.supervisor_token = os.environ.get('SUPERVISOR_TOKEN')
        self.ha_url = "http://supervisor/core/api"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.supervisor_token}',
            'Content-Type': 'application/json'
        })
    
    def fire_event(self, event_type: str, event_data: Dict) -> bool:
        """Fire an event in Home Assistant."""
        try:
            url = f"{self.ha_url}/events/{event_type}"
            response = self.session.post(url, json=event_data, timeout=5)
            
            if response.status_code in [200, 201]:
                logger.debug(f"Fired event: {event_type}")
                return True
            else:
                logger.error(f"Failed to fire event: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error firing event: {e}")
            return False
    
    def update_sensor(self, entity_id: str, state: str, attributes: Dict = None) -> bool:
        """Update a sensor state in Home Assistant."""
        try:
            url = f"{self.ha_url}/states/{entity_id}"
            data = {
                "state": state,
                "attributes": attributes or {}
            }
            
            response = self.session.post(url, json=data, timeout=5)
            
            if response.status_code in [200, 201]:
                logger.debug(f"Updated sensor: {entity_id}")
                return True
            else:
                logger.error(f"Failed to update sensor: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating sensor: {e}")
            return False


class ZoneMinderIntegration:
    """Main integration class."""
    
    def __init__(self):
        """Initialize the integration."""
        self.zm_api = ZoneMinderAPI(
            host=os.environ.get('ZM_HOST'),
            port=int(os.environ.get('ZM_PORT', 80)),
            path=os.environ.get('ZM_PATH', '/zm'),
            user=os.environ.get('ZM_USER'),
            password=os.environ.get('ZM_PASSWORD'),
            ssl_verify=os.environ.get('ZM_SSL_VERIFY', 'true').lower() == 'true'
        )
        self.ha_api = HomeAssistantAPI()
        self.scan_interval = int(os.environ.get('SCAN_INTERVAL', 30))
        self.event_check_interval = int(os.environ.get('EVENT_CHECK_INTERVAL', 10))
        self.last_event_check = {}
        self.running = True
    
    def setup(self) -> bool:
        """Set up the integration."""
        logger.info("Setting up ZoneMinder integration...")
        
        # Authenticate with ZoneMinder
        if not self.zm_api.login():
            logger.error("Failed to authenticate with ZoneMinder")
            return False
        
        # Get monitors
        monitors = self.zm_api.get_monitors()
        if not monitors:
            logger.error("No monitors found")
            return False
        
        # Create sensor entities for each monitor
        for monitor_id, monitor in monitors.items():
            entity_id = f"camera.zoneminder_{monitor['name'].lower().replace(' ', '_')}"
            self.ha_api.update_sensor(
                entity_id,
                "idle",
                {
                    "friendly_name": monitor['name'],
                    "monitor_id": monitor_id,
                    "enabled": monitor['enabled'],
                    "function": monitor['function'],
                    "stream_url": self.zm_api.get_monitor_stream_url(monitor_id),
                    "width": monitor['width'],
                    "height": monitor['height'],
                }
            )
            
            # Initialize last event check
            self.last_event_check[monitor_id] = datetime.now() - timedelta(seconds=self.event_check_interval)
        
        logger.info("ZoneMinder integration setup complete")
        return True
    
    def check_events(self):
        """Check for new events and fire Home Assistant events."""
        for monitor_id in self.zm_api.monitors.keys():
            since = self.last_event_check.get(monitor_id)
            if not since:
                continue
            
            events = self.zm_api.get_events(monitor_id=monitor_id, since=since)
            
            for event in events:
                # Fire Home Assistant event
                self.ha_api.fire_event(
                    "zoneminder_motion_detected",
                    {
                        "monitor_id": monitor_id,
                        "monitor_name": self.zm_api.monitors[monitor_id]['name'],
                        "event_id": event['id'],
                        "event_name": event['name'],
                        "cause": event['cause'],
                        "start_time": event['start_time'],
                        "frames": event['frames'],
                        "alarm_frames": event['alarm_frames'],
                    }
                )
                
                logger.info(f"Motion detected on monitor {monitor_id}: {event['name']}")
                
                # Update camera sensor state
                entity_id = f"camera.zoneminder_{self.zm_api.monitors[monitor_id]['name'].lower().replace(' ', '_')}"
                self.ha_api.update_sensor(
                    entity_id,
                    "motion_detected",
                    {
                        "last_event_id": event['id'],
                        "last_event_time": event['start_time'],
                        "last_event_cause": event['cause'],
                    }
                )
            
            self.last_event_check[monitor_id] = datetime.now()
    
    def update_monitor_states(self):
        """Update monitor states from ZoneMinder."""
        monitors = self.zm_api.get_monitors()
        
        for monitor_id, monitor in monitors.items():
            entity_id = f"camera.zoneminder_{monitor['name'].lower().replace(' ', '_')}"
            self.ha_api.update_sensor(
                entity_id,
                monitor['function'].lower(),
                {
                    "enabled": monitor['enabled'],
                    "function": monitor['function'],
                }
            )
    
    def run(self):
        """Run the integration."""
        if not self.setup():
            logger.error("Setup failed, exiting...")
            return
        
        last_monitor_update = time.time()
        last_event_check = time.time()
        
        logger.info("Integration running...")
        
        try:
            while self.running:
                current_time = time.time()
                
                # Check for events
                if current_time - last_event_check >= self.event_check_interval:
                    self.check_events()
                    last_event_check = current_time
                
                # Update monitor states
                if current_time - last_monitor_update >= self.scan_interval:
                    self.update_monitor_states()
                    last_monitor_update = current_time
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")


if __name__ == "__main__":
    integration = ZoneMinderIntegration()
    integration.run()
