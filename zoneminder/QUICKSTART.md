# Quick Start Guide - ZoneMinder Home Assistant Addon

Get up and running with ZoneMinder in Home Assistant in under 10 minutes!

## ⚡ Quick Installation

### 1. Prepare Your ZoneMinder Server (2 minutes)

Make sure you know:
- ✅ ZoneMinder URL (e.g., `http://192.168.1.100`)
- ✅ Port (usually `80` for HTTP, `443` for HTTPS)
- ✅ Path (usually `/zm`)
- ✅ Username and password

### 2. Install the Addon (3 minutes)

1. In Home Assistant, go to: **Settings** → **Add-ons** → **Add-on Store**
2. Click **⋮** (menu) → **Repositories**
3. Add: `https://github.com/uncle-muddy/hassio-zoneminder`
4. Find "ZoneMinder Integration" and click **Install**

### 3. Configure (2 minutes)

1. Click on the installed addon
2. Go to **Configuration** tab
3. Enter your details:
   ```yaml
   zm_host: "http://192.168.1.100"
   zm_port: 80
   zm_path: "/zm"
   zm_user: "admin"
   zm_password: "your_password"
   ```
4. Click **Save**

### 4. Start the Addon (1 minute)

1. Toggle **Start on boot** to ON
2. Click **Start**
3. Check the **Log** tab - you should see:
   ```
   Successfully authenticated with ZoneMinder
   Found X monitors
   Integration running...
   ```

### 5. View Your Cameras (2 minutes)

1. Edit your dashboard
2. Add a **Grid Card**
3. Add **Picture Entity** cards for each camera:
   - Entity: `camera.zoneminder_[camera_name]`
   - Camera View: Live

Done! 🎉

## 🚀 First Automation

Create a motion alert in 60 seconds:

1. Go to **Settings** → **Automations & Scenes**
2. Click **Create Automation**
3. Use this YAML:

```yaml
alias: Motion Alert
trigger:
  - platform: event
    event_type: zoneminder_motion_detected
action:
  - service: notify.mobile_app_your_phone
    data:
      title: Motion Detected
      message: "{{ trigger.event.data.monitor_name }}"
```

## 📱 Mobile Dashboard

Quick mobile-friendly view:

```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.zoneminder_front_door
    camera_view: live
  
  - type: horizontal-stack
    cards:
      - type: button
        entity: camera.zoneminder_front_door
        name: Front
        tap_action:
          action: more-info
      - type: button
        entity: camera.zoneminder_back_yard
        name: Back
        tap_action:
          action: more-info
```

## 🔧 Common Issues

### Can't connect?
- Check ZoneMinder is running
- Verify URL, port, and credentials
- Try `zm_ssl_verify: false` for self-signed certs

### No cameras showing?
- Check ZoneMinder has enabled monitors
- Restart the addon
- Look in **Developer Tools** → **States** for `camera.zoneminder_*`

### No motion events?
- Set monitors to "Modect" mode in ZoneMinder
- Lower `event_check_interval` to `5`
- Test by triggering motion in ZoneMinder

## 📚 Full Documentation

For detailed setup, advanced features, and troubleshooting:
- **INSTALLATION.md** - Complete installation guide
- **README.md** - Full documentation
- **LOVELACE_EXAMPLES.md** - Dashboard examples
- **example_automations.yaml** - Automation templates

## 🎯 Next Steps

1. ✅ Set up notifications for motion
2. ✅ Create night mode automation
3. ✅ Add cameras to dashboard
4. ✅ Configure zones in ZoneMinder
5. ✅ Set up remote access

Need help? Check the full documentation or open an issue on GitHub!
