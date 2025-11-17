# Installation Guide for ZoneMinder Home Assistant Addon

This guide will walk you through installing and configuring the ZoneMinder integration for Home Assistant.

## Prerequisites

Before you begin, ensure you have:

1. **Home Assistant** installed and running (version 2024.1.0 or later)
2. **ZoneMinder** server installed and accessible
3. **ZoneMinder API** enabled (usually enabled by default)
4. Valid **ZoneMinder credentials** (username and password)
5. Network connectivity between Home Assistant and ZoneMinder

## Step 1: Prepare ZoneMinder

### 1.1 Enable API Access

1. Log into your ZoneMinder web interface
2. Navigate to **Options** → **System**
3. Ensure **OPT_USE_API** is enabled
4. Note your ZoneMinder URL, port, and path

### 1.2 Create Dedicated User (Recommended)

For security, create a dedicated Home Assistant user:

1. In ZoneMinder, go to **Options** → **Users**
2. Click **Add New User**
3. Set username: `homeassistant`
4. Set a strong password
5. Set permissions:
   - **Enabled**: Yes
   - **Stream**: View
   - **Events**: View
   - **Monitors**: View
6. Save the user

### 1.3 Test API Access

Test that the API is accessible:

```bash
# Replace with your ZoneMinder details
curl -X POST http://192.168.1.100/zm/api/host/login.json \
  -d "user=homeassistant&pass=yourpassword"
```

You should receive a JSON response with a token or access_token.

## Step 2: Install the Addon

### Method A: Via Repository (Recommended)

1. Open Home Assistant web interface
2. Navigate to **Settings** → **Add-ons**
3. Click **Add-on Store** (bottom right)
4. Click the three-dot menu (⋮) in the top right
5. Select **Repositories**
6. Add this URL: `https://github.com/yourusername/hassio-zoneminder`
7. Click **Add** → **Close**
8. Refresh the add-on store page
9. Find **ZoneMinder Integration** in the list
10. Click on it and then click **Install**

### Method B: Manual Installation

1. Connect to your Home Assistant server via SSH or file share
2. Navigate to the addons directory:
   ```bash
   cd /addons
   ```
3. Create the addon directory:
   ```bash
   mkdir zoneminder
   cd zoneminder
   ```
4. Copy all addon files to this directory:
   - config.yaml
   - Dockerfile
   - build.yaml
   - requirements.txt
   - run.sh
   - zoneminder_integration.py
   - README.md

5. Set proper permissions:
   ```bash
   chmod +x run.sh
   ```

6. Restart Home Assistant
7. Navigate to **Settings** → **Add-ons** → **Add-on Store**
8. Refresh the page
9. Find **ZoneMinder Integration** under "Local add-ons"
10. Click **Install**

## Step 3: Configure the Addon

### 3.1 Basic Configuration

1. After installation, click on **ZoneMinder Integration**
2. Go to the **Configuration** tab
3. Enter your ZoneMinder details:

```yaml
zm_host: "http://192.168.1.100"
zm_port: 80
zm_path: "/zm"
zm_user: "homeassistant"
zm_password: "your_secure_password"
zm_ssl_verify: true
scan_interval: 30
event_check_interval: 10
```

### 3.2 Configuration Examples

#### Local Network Installation
```yaml
zm_host: "http://192.168.1.100"
zm_port: 80
zm_path: "/zm"
zm_user: "homeassistant"
zm_password: "SecurePass123"
zm_ssl_verify: true
scan_interval: 30
event_check_interval: 10
```

#### Remote HTTPS Installation
```yaml
zm_host: "https://cameras.mydomain.com"
zm_port: 443
zm_path: "/zoneminder"
zm_user: "homeassistant"
zm_password: "SecurePass123"
zm_ssl_verify: true
scan_interval: 60
event_check_interval: 15
```

#### Self-Signed Certificate
```yaml
zm_host: "https://192.168.1.100"
zm_port: 8443
zm_path: "/zm"
zm_user: "homeassistant"
zm_password: "SecurePass123"
zm_ssl_verify: false  # Disable for self-signed certs
scan_interval: 30
event_check_interval: 10
```

### 3.3 Understanding Configuration Options

| Option | Description | Tips |
|--------|-------------|------|
| `zm_host` | ZoneMinder server URL | Include http:// or https:// |
| `zm_port` | Server port | Usually 80 (HTTP) or 443 (HTTPS) |
| `zm_path` | Installation path | Usually /zm or /zoneminder |
| `zm_user` | Username | Use dedicated user for security |
| `zm_password` | Password | Use strong, unique password |
| `zm_ssl_verify` | Verify SSL certs | Set false for self-signed certs |
| `scan_interval` | Monitor update frequency | 30-60 sec recommended |
| `event_check_interval` | Event check frequency | 5-15 sec recommended |

## Step 4: Start the Addon

1. Click the **Info** tab
2. Toggle **Start on boot** to enabled
3. Click **Start**
4. Monitor the **Log** tab for startup messages

Expected log output:
```
Starting ZoneMinder integration...
Connecting to ZoneMinder at http://192.168.1.100:80/zm
Successfully authenticated with ZoneMinder
Found 4 monitors
ZoneMinder integration setup complete
Integration running...
```

## Step 5: Verify Camera Entities

### 5.1 Check Entity Creation

1. Navigate to **Settings** → **Devices & Services**
2. Look for camera entities starting with `camera.zoneminder_`
3. Each ZoneMinder monitor should have a corresponding entity

### 5.2 Test Camera View

1. Go to **Developer Tools** → **States**
2. Search for `camera.zoneminder_`
3. Click on a camera entity
4. Click **More Info** to view the camera feed

## Step 6: Create Automations

### 6.1 Basic Motion Alert

1. Navigate to **Settings** → **Automations & Scenes**
2. Click **Create Automation** → **Start with an empty automation**
3. Add trigger:
   - Type: **Event**
   - Event Type: `zoneminder_motion_detected`
4. Add action:
   - Type: **Call Service**
   - Service: `notify.mobile_app_your_phone`
   - Data:
     ```yaml
     title: Motion Detected
     message: Motion on {{ trigger.event.data.monitor_name }}
     ```
5. Save with name "ZoneMinder Motion Alert"

### 6.2 Import Example Automations

Copy the examples from `example_automations.yaml` to your configuration:

1. Open the `example_automations.yaml` file
2. Copy desired automations
3. Paste into your `automations.yaml` file
4. Adjust entity IDs to match your setup
5. Reload automations: **Developer Tools** → **YAML** → **Automations**

## Step 7: Add to Dashboard

### 7.1 Simple Camera View

1. Edit your dashboard
2. Add a new card
3. Select **Picture Entity**
4. Choose a ZoneMinder camera entity
5. Set **Camera View** to "Live"

### 7.2 Multi-Camera Grid

1. Edit your dashboard
2. Add a new card
3. Select **Grid Card**
4. Set columns to 2
5. Add multiple Picture Entity cards for each camera

See `LOVELACE_EXAMPLES.md` for more dashboard configurations.

## Step 8: Advanced Setup (Optional)

### 8.1 Enable HTTPS in ZoneMinder

For secure remote access:

1. Set up reverse proxy (Nginx/Apache)
2. Configure SSL certificate
3. Update addon configuration with https:// URL

### 8.2 Optimize Performance

```yaml
# For remote access
scan_interval: 60
event_check_interval: 15

# For local network
scan_interval: 30
event_check_interval: 5
```

### 8.3 Custom Event Filters

Create input_boolean helpers for toggling features:

```yaml
input_boolean:
  zm_motion_alerts:
    name: ZoneMinder Motion Alerts
    icon: mdi:bell
  
  zm_night_mode:
    name: ZoneMinder Night Mode
    icon: mdi:weather-night
```

## Troubleshooting

### Addon Won't Start

**Check logs:**
1. Go to addon page
2. Click **Log** tab
3. Look for error messages

**Common issues:**
- Wrong credentials → Verify username/password
- Wrong URL → Check host, port, and path
- Network issue → Ensure Home Assistant can reach ZoneMinder
- API disabled → Enable API in ZoneMinder settings

**Fix authentication:**
```bash
# Test from Home Assistant terminal:
curl -X POST http://YOUR_ZM_HOST/zm/api/host/login.json \
  -d "user=YOUR_USER&pass=YOUR_PASS"
```

### No Camera Entities

**Verify monitors exist:**
1. Log into ZoneMinder
2. Check that monitors are enabled
3. Restart the addon

**Check entity registry:**
1. Go to **Developer Tools** → **States**
2. Search for "zoneminder"
3. Entities should appear after successful startup

### Motion Events Not Working

**Check ZoneMinder settings:**
1. Ensure monitors are in "Modect" or "Mocord" mode
2. Verify motion detection is configured
3. Test by triggering motion in camera view

**Reduce check interval:**
```yaml
event_check_interval: 5  # Check more frequently
```

**Check event generation:**
1. Open ZoneMinder web interface
2. Go to **Events** page
3. Verify events are being created

### Poor Camera Performance

**Optimize settings:**
```yaml
scan_interval: 60  # Reduce API calls
```

**In ZoneMinder:**
1. Lower resolution for less critical cameras
2. Adjust frame rate (10-15 FPS sufficient)
3. Enable hardware acceleration if available

### SSL Certificate Errors

**For self-signed certificates:**
```yaml
zm_ssl_verify: false
```

**For proper certificates:**
1. Ensure certificate is valid
2. Check certificate chain is complete
3. Verify hostname matches certificate

## Getting Help

If you encounter issues:

1. **Check the logs** in the addon Log tab
2. **Review documentation** in README.md
3. **Search existing issues** on GitHub
4. **Ask on forums**:
   - Home Assistant Community
   - ZoneMinder Forums
5. **Create GitHub issue** with:
   - Addon version
   - Home Assistant version
   - ZoneMinder version
   - Configuration (sanitized)
   - Error logs

## Next Steps

After successful installation:

1. ✅ Configure motion detection automations
2. ✅ Set up dashboard cameras
3. ✅ Create notification rules
4. ✅ Test event triggers
5. ✅ Optimize performance settings
6. ✅ Set up remote access (if needed)
7. ✅ Configure backup and monitoring

## Updating the Addon

When updates are available:

1. Go to **Settings** → **Add-ons**
2. Click **ZoneMinder Integration**
3. If update available, click **Update**
4. Review changelog
5. Click **Restart** after update

## Uninstallation

To remove the addon:

1. Go to **Settings** → **Add-ons**
2. Click **ZoneMinder Integration**
3. Click **Uninstall**
4. Confirm removal
5. Manually remove any automations/dashboard cards

Camera entities will be automatically removed.

---

**Congratulations!** Your ZoneMinder integration is now set up and ready to use.
