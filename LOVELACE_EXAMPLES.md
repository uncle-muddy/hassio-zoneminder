# Lovelace Dashboard Configuration for ZoneMinder

## Camera Grid View

Add this to your Lovelace dashboard to display all ZoneMinder cameras:

```yaml
type: vertical-stack
cards:
  # Header Card
  - type: markdown
    content: |
      # ZoneMinder Security Cameras
      Monitor your property with live camera feeds
  
  # Status Bar
  - type: horizontal-stack
    cards:
      - type: entity
        entity: sensor.zoneminder_active_monitors
        name: Active Cameras
        icon: mdi:cctv
      
      - type: entity
        entity: sensor.zoneminder_motion_status
        name: Motion Status
        icon: mdi:motion-sensor
      
      - type: entity
        entity: sensor.zoneminder_last_motion
        name: Last Motion
        icon: mdi:clock-outline
  
  # Camera Grid
  - type: grid
    columns: 2
    square: false
    cards:
      - type: picture-entity
        entity: camera.zoneminder_front_door
        camera_view: live
        name: Front Door
        show_state: true
        show_name: true
        tap_action:
          action: more-info
      
      - type: picture-entity
        entity: camera.zoneminder_back_yard
        camera_view: live
        name: Back Yard
        show_state: true
        show_name: true
        tap_action:
          action: more-info
      
      - type: picture-entity
        entity: camera.zoneminder_garage
        camera_view: live
        name: Garage
        show_state: true
        show_name: true
        tap_action:
          action: more-info
      
      - type: picture-entity
        entity: camera.zoneminder_driveway
        camera_view: live
        name: Driveway
        show_state: true
        show_name: true
        tap_action:
          action: more-info
```

## Single Camera Full View

For a detailed view of a single camera with controls:

```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.zoneminder_front_door
    camera_view: live
    aspect_ratio: 16x9
  
  - type: entities
    entities:
      - entity: camera.zoneminder_front_door
        name: Camera Status
      
      - type: attribute
        entity: camera.zoneminder_front_door
        attribute: function
        name: Mode
      
      - type: attribute
        entity: camera.zoneminder_front_door
        attribute: last_event_time
        name: Last Event
      
      - type: attribute
        entity: camera.zoneminder_front_door
        attribute: last_event_cause
        name: Event Cause
```

## Motion Detection Dashboard

Create a dedicated motion detection monitoring dashboard:

```yaml
type: vertical-stack
cards:
  # Motion Status Banner
  - type: conditional
    conditions:
      - entity: sensor.zoneminder_motion_status
        state: "Motion Detected"
    card:
      type: markdown
      content: |
        ## ⚠️ MOTION DETECTED ⚠️
      card_mod:
        style: |
          ha-card {
            background-color: rgba(255, 0, 0, 0.3);
            color: white;
          }
  
  # Recent Events Timeline
  - type: entities
    title: Recent Motion Events
    entities:
      - entity: camera.zoneminder_front_door
        secondary_info: last-changed
      - entity: camera.zoneminder_back_yard
        secondary_info: last-changed
      - entity: camera.zoneminder_garage
        secondary_info: last-changed
      - entity: camera.zoneminder_driveway
        secondary_info: last-changed
  
  # Event History (using custom card - requires installation)
  - type: custom:logbook-card
    entity: camera.zoneminder_front_door
    hours_to_show: 24
    title: Motion History - Front Door
```

## Compact Camera Strip

For a space-saving horizontal camera strip:

```yaml
type: horizontal-stack
cards:
  - type: picture-entity
    entity: camera.zoneminder_front_door
    camera_view: live
    show_name: false
    show_state: false
    tap_action:
      action: more-info
  
  - type: picture-entity
    entity: camera.zoneminder_back_yard
    camera_view: live
    show_name: false
    show_state: false
    tap_action:
      action: more-info
  
  - type: picture-entity
    entity: camera.zoneminder_garage
    camera_view: live
    show_name: false
    show_state: false
    tap_action:
      action: more-info
  
  - type: picture-entity
    entity: camera.zoneminder_driveway
    camera_view: live
    show_name: false
    show_state: false
    tap_action:
      action: more-info
```

## Security Overview Dashboard

Complete security monitoring dashboard:

```yaml
title: Security
path: security
icon: mdi:shield-home
badges:
  - entity: sensor.zoneminder_active_monitors
  - entity: sensor.zoneminder_motion_status
  - entity: alarm_control_panel.home_alarm

cards:
  # Quick Status
  - type: glance
    title: Camera Status
    columns: 4
    entities:
      - entity: camera.zoneminder_front_door
        name: Front
      - entity: camera.zoneminder_back_yard
        name: Back
      - entity: camera.zoneminder_garage
        name: Garage
      - entity: camera.zoneminder_driveway
        name: Drive
  
  # Live Feeds
  - type: grid
    title: Live Camera Feeds
    columns: 2
    square: false
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
      
      - type: picture-entity
        entity: camera.zoneminder_driveway
        camera_view: live
  
  # Event Log
  - type: logbook
    title: Security Events
    hours_to_show: 24
    entities:
      - camera.zoneminder_front_door
      - camera.zoneminder_back_yard
      - camera.zoneminder_garage
      - camera.zoneminder_driveway
  
  # Quick Actions
  - type: entities
    title: Quick Actions
    entities:
      - entity: input_boolean.motion_alerts
        name: Enable Motion Alerts
      
      - entity: input_boolean.night_mode
        name: Night Mode
      
      - type: button
        name: View All Recordings
        icon: mdi:video-box
        tap_action:
          action: url
          url_path: "http://your-zoneminder-server/zm"
```

## Mobile Optimized View

For mobile devices, use this simpler layout:

```yaml
type: vertical-stack
cards:
  # Status Summary
  - type: entities
    entities:
      - sensor.zoneminder_motion_status
      - sensor.zoneminder_last_motion
  
  # Camera Carousel (swipe between cameras)
  - type: picture-entity
    entity: camera.zoneminder_front_door
    camera_view: live
    aspect_ratio: 16x9
  
  # Quick Camera Selector
  - type: horizontal-stack
    cards:
      - type: button
        entity: camera.zoneminder_front_door
        name: Front
        icon: mdi:door
        tap_action:
          action: more-info
      
      - type: button
        entity: camera.zoneminder_back_yard
        name: Back
        icon: mdi:home
        tap_action:
          action: more-info
      
      - type: button
        entity: camera.zoneminder_garage
        name: Garage
        icon: mdi:garage
        tap_action:
          action: more-info
```

## Advanced: Custom Button Card Configuration

Using the custom button-card (requires HACS installation):

```yaml
type: custom:button-card
entity: camera.zoneminder_front_door
name: Front Door
show_state: true
show_last_changed: true
state:
  - value: 'motion_detected'
    color: red
    icon: mdi:motion-sensor-alert
  - value: 'idle'
    color: green
    icon: mdi:cctv
  - value: 'recording'
    color: orange
    icon: mdi:record-rec
styles:
  card:
    - height: 120px
  icon:
    - width: 60px
    - height: 60px
  name:
    - font-size: 16px
    - font-weight: bold
tap_action:
  action: more-info
hold_action:
  action: url
  url_path: "http://your-zoneminder-server/zm/index.php?view=watch&mid=1"
```

## Integration with Picture Elements Card

For interactive floor plan integration:

```yaml
type: picture-elements
image: /local/floorplan.png
elements:
  # Front Door Camera
  - type: state-icon
    entity: camera.zoneminder_front_door
    tap_action:
      action: more-info
    style:
      top: 20%
      left: 50%
  
  # Back Yard Camera
  - type: state-icon
    entity: camera.zoneminder_back_yard
    tap_action:
      action: more-info
    style:
      top: 80%
      left: 50%
  
  # Garage Camera
  - type: state-icon
    entity: camera.zoneminder_garage
    tap_action:
      action: more-info
    style:
      top: 50%
      left: 10%
  
  # Motion Indicator
  - type: conditional
    conditions:
      - entity: sensor.zoneminder_motion_status
        state: "Motion Detected"
    elements:
      - type: state-badge
        entity: sensor.zoneminder_motion_status
        style:
          top: 5%
          left: 5%
```

## Tips for Best Performance

1. **Use JPEG streams** rather than MJPEG for better performance
2. **Limit simultaneous streams** on mobile devices (2-3 max)
3. **Use lower resolution** for thumbnail views
4. **Enable caching** in ZoneMinder settings
5. **Consider using a reverse proxy** for remote access
6. **Use conditional cards** to hide inactive cameras
7. **Implement tabs** for large camera deployments

## Recommended HACS Cards

For enhanced functionality, install these custom cards:

- **button-card**: Advanced button styling
- **card-mod**: Custom CSS styling
- **layout-card**: Advanced layouts
- **auto-entities**: Dynamic entity lists
- **lovelace-swipe-navigation**: Swipe between views
- **frigate-card**: Advanced camera card (can be adapted)
