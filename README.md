# ZoneMinder Integration for Home Assistant

A Home Assistant addon that integrates ZoneMinder security camera system, providing camera feeds, event monitoring, and motion detection triggers.

## Features

- **Camera Feed Display**: View all ZoneMinder camera streams in Home Assistant
- **Motion Detection Events**: Automatically trigger Home Assistant automations when motion is detected
- **Event Monitoring**: Access ZoneMinder events and recordings
- **Monitor Control**: Control monitor states (Modect, Record, Monitor, etc.)
- **Real-time Updates**: Configurable polling intervals for events and monitor states

## Installation

### Method 1: Add Repository (Recommended)

1. Open Home Assistant
2. Navigate to **Settings** → **Add-ons** → **Add-on Store**
3. Click the three dots menu (⋮) in the top right
4. Select **Repositories**
5. Add this repository URL: `https://github.com/uncle-muddy/hassio-zoneminder`
6. Click **Add**
7. Find "ZoneMinder Integration" in the add-on store
8. Click **Install**

### Method 2: Manual Installation

1. Copy the addon files to your Home Assistant addons directory:
   ```
   /addons/zoneminder/
   ├── config.yaml
   ├── Dockerfile
   ├── requirements.txt
   ├── run.sh
   ├── zoneminder_integration.py
   └── README.md
   ```

2. Restart Home Assistant
3. Navigate to **Settings** → **Add-ons** → **Add-on Store**
4. Find "ZoneMinder Integration" under "Local add-ons"
5. Click **Install**

## Configuration

### Basic Configuration

After installation, configure the addon with your ZoneMinder details:

```yaml
zm_host: "http://192.168.1.100"
zm_port: 80
zm_path: "/zm"
zm_user: "admin"
zm_password: "your_password"
zm_ssl_verify: true
scan_interval: 30
event_check_interval: 10
```

### Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `zm_host` | string | Yes | - | ZoneMinder server URL (http:// or https://) |
| `zm_port` | integer | Yes | 80 | ZoneMinder server port |
| `zm_path` | string | Yes | /zm | Path to ZoneMinder installation |
| `zm_user` | string | Yes | - | ZoneMinder username |
| `zm_password` | string | Yes | - | ZoneMinder password |
| `zm_ssl_verify` | boolean | No | true | Verify SSL certificates |
| `scan_interval` | integer | No | 30 | Monitor state update interval (seconds) |
| `event_check_interval` | integer | No | 10 | Event check interval (seconds) |

### Example Configuration

For a ZoneMinder instance at `https://cameras.myhouse.com:8443/zoneminder`:

```yaml
zm_host: "https://cameras.myhouse.com"
zm_port: 8443
zm_path: "/zoneminder"
zm_user: "homeassistant"
zm_password: "SecurePassword123"
zm_ssl_verify: true
scan_interval: 30
event_check_interval: 5
```

## Usage

### Camera Entities

After starting the addon, camera entities will be automatically created for each ZoneMinder monitor:

- Entity ID format: `camera.zoneminder_[monitor_name]`
- Example: `camera.zoneminder_front_door`

Each camera entity includes:
- Current state (idle, motion_detected, recording, etc.)
- Stream URL for viewing the feed
- Monitor configuration (width, height, function)
- Last event information

### Viewing Camera Feeds

Add cameras to your Lovelace dashboard:

```yaml
type: picture-entity
entity: camera.zoneminder_front_door
camera_view: live
```

Or use a camera grid:

```yaml
type: grid
cards:
  - type: picture-entity
    entity: camera.zoneminder_front_door
    camera_view: live
  - type: picture-entity
    entity: camera.zoneminder_back_yard
    camera_view: live
  - type: picture-entity
    entity: camera.zoneminder_garage
    camera_view: live
```

### Motion Detection Events

The addon fires a `zoneminder_motion_detected` event when motion is detected on any monitor.

#### Event Data

```yaml
event_type: zoneminder_motion_detected
data:
  monitor_id: "1"
  monitor_name: "Front Door"
  event_id: "12345"
  event_name: "Front Door-1"
  cause: "Motion"
  start_time: "2024-01-15 14:30:25"
  frames: "150"
  alarm_frames: "45"
```

### Creating Automations

#### Example 1: Turn on Lights When Motion Detected

```yaml
automation:
  - alias: "Front Door Motion - Lights On"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
        event_data:
          monitor_name: "Front Door"
    action:
      - service: light.turn_on
        target:
          entity_id: light.front_porch
      - service: notify.mobile_app
        data:
          title: "Motion Detected"
          message: "Motion detected at front door"
```

#### Example 2: Send Notification for Any Camera

```yaml
automation:
  - alias: "ZoneMinder Motion Alert"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
    action:
      - service: notify.mobile_app
        data:
          title: "Security Alert"
          message: "Motion detected on {{ trigger.event.data.monitor_name }}"
```

#### Example 3: Trigger Recording on Specific Monitor

```yaml
automation:
  - alias: "Start Recording on Motion"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
        event_data:
          monitor_name: "Driveway"
    action:
      - service: camera.record
        target:
          entity_id: camera.zoneminder_driveway
        data:
          duration: 30
```

#### Example 4: Conditional Actions Based on Time

```yaml
automation:
  - alias: "Night Motion Alert"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
    condition:
      - condition: time
        after: "22:00:00"
        before: "06:00:00"
    action:
      - service: light.turn_on
        target:
          entity_id: light.all_lights
        data:
          brightness: 255
      - service: notify.mobile_app
        data:
          title: "Night Motion Alert"
          message: "Motion detected on {{ trigger.event.data.monitor_name }} at night!"
          data:
            priority: high
```

### Using Camera States in Conditions

```yaml
automation:
  - alias: "Alert on Motion During Away"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
    condition:
      - condition: state
        entity_id: alarm_control_panel.home_alarm
        state: "armed_away"
    action:
      - service: notify.mobile_app
        data:
          title: "Security Breach"
          message: "Motion detected while away: {{ trigger.event.data.monitor_name }}"
```

### Displaying Recent Events

Create a sensor to track recent events:

```yaml
template:
  - sensor:
      - name: "ZoneMinder Last Event"
        state: >
          {{ state_attr('camera.zoneminder_front_door', 'last_event_time') }}
        attributes:
          event_id: >
            {{ state_attr('camera.zoneminder_front_door', 'last_event_id') }}
          cause: >
            {{ state_attr('camera.zoneminder_front_door', 'last_event_cause') }}
```

## Troubleshooting

### Addon Won't Start

1. Check the addon logs: **Settings** → **Add-ons** → **ZoneMinder Integration** → **Log**
2. Verify ZoneMinder credentials and URL are correct
3. Ensure ZoneMinder API is enabled and accessible
4. Check network connectivity between Home Assistant and ZoneMinder

### No Motion Events

1. Verify monitors are in "Modect" or "Mocord" mode in ZoneMinder
2. Check that motion detection is properly configured in ZoneMinder
3. Reduce `event_check_interval` for more frequent checks
4. Review ZoneMinder logs for event generation

### Camera Feeds Not Displaying

1. Verify the stream URL is accessible from Home Assistant
2. Check ZoneMinder authentication settings
3. Ensure Home Assistant can access the ZoneMinder server
4. Try using IP address instead of hostname if DNS issues exist

### High CPU Usage

1. Increase `scan_interval` and `event_check_interval`
2. Reduce number of active monitors
3. Optimize ZoneMinder configuration

## Advanced Configuration

### Custom Event Filtering

You can filter events by specific criteria in your automations:

```yaml
automation:
  - alias: "High Priority Motion Only"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
    condition:
      - condition: template
        value_template: >
          {{ trigger.event.data.alarm_frames | int > 20 }}
    action:
      - service: notify.mobile_app
        data:
          title: "High Activity Alert"
          message: "Significant motion on {{ trigger.event.data.monitor_name }}"
```

### Integration with Other Systems

Use the motion events to trigger other smart home systems:

```yaml
automation:
  - alias: "Motion to Security System"
    trigger:
      - platform: event
        event_type: zoneminder_motion_detected
    action:
      - service: mqtt.publish
        data:
          topic: "security/motion"
          payload: >
            {
              "monitor": "{{ trigger.event.data.monitor_name }}",
              "time": "{{ trigger.event.data.start_time }}"
            }
```

## API Reference

### Events

#### zoneminder_motion_detected

Fired when motion is detected on any monitor.

**Data:**
- `monitor_id`: Monitor ID in ZoneMinder
- `monitor_name`: Human-readable monitor name
- `event_id`: ZoneMinder event ID
- `event_name`: Event name
- `cause`: Event cause (usually "Motion")
- `start_time`: Event start timestamp
- `frames`: Total frames in event
- `alarm_frames`: Number of frames with motion

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/uncle-muddy/hassio-zoneminder/issues
- Home Assistant Community: https://community.home-assistant.io/

## License

MIT License - See LICENSE file for details

## Credits

Created for the Home Assistant community. Special thanks to the ZoneMinder and Home Assistant teams.
