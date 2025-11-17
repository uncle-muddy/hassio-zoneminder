# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2024-01-15

### Added
- Initial release of ZoneMinder Integration addon
- Full ZoneMinder API integration
- Automatic camera entity creation for all monitors
- Real-time motion detection event system
- Configurable polling intervals for events and monitor states
- Camera feed streaming support
- Monitor state tracking and updates
- Home Assistant event firing on motion detection
- Multi-architecture Docker support (aarch64, amd64, armhf, armv7, i386)
- Comprehensive documentation and examples
- SSL/TLS support with verification options
- Authentication with ZoneMinder API
- Monitor control capabilities
- Event history retrieval

### Features
- **Camera Integration**: View all ZoneMinder cameras in Home Assistant
- **Motion Events**: Automatic detection and Home Assistant event firing
- **Customizable Intervals**: Configure scan and event check frequencies
- **Secure Authentication**: Support for username/password authentication
- **Stream URLs**: Direct access to camera streams
- **Event Data**: Detailed information about detected events
- **Monitor Attributes**: Comprehensive monitor state and configuration tracking

### Configuration Options
- ZoneMinder host, port, and path configuration
- User authentication credentials
- SSL certificate verification toggle
- Scan interval for monitor state updates (1-3600 seconds)
- Event check interval for motion detection (5-300 seconds)

### Documentation
- Complete README with installation instructions
- Configuration examples for various setups
- Automation examples for common use cases
- Troubleshooting guide
- API reference documentation

### Technical Details
- Python 3.11 base
- Home Assistant Supervisor API integration
- Requests library for HTTP communication
- Support for ZoneMinder API v1.x
- Efficient polling with configurable intervals
- Error handling and logging

## Future Plans

### Upcoming Features
- [ ] MQTT support for real-time events
- [ ] Video clip downloads
- [ ] Advanced filtering options
- [ ] Zone-specific motion detection
- [ ] PTZ camera controls
- [ ] Event thumbnail previews
- [ ] Integration with Home Assistant notifications
- [ ] Custom event types and filters
- [ ] Historical event browser
- [ ] Performance monitoring
- [ ] Health check endpoints
- [ ] WebSocket support for real-time updates
- [ ] Advanced analytics and statistics
- [ ] Multi-server support
- [ ] Improved error recovery

### Known Issues
- None reported yet

### Contributing
Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

---

For more information, visit: https://github.com/uncle-muddy/hassio-zoneminder
