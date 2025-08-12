# progres-logo-fix

mitmproxy addon that automatically captures the `etablissementId` from `/dias` API responses and rewrites `/logoEtablissement/undefined` requests to use the correct ID for **progres.mesrs.dz**.

## Features
- captures `etablissementId` dynamically from `/dias` API call.
- holds `/logoEtablissement/undefined` requests until the ID is known.
- automatically rewrites the request with the correct ID.

## Requirements
- Python 3.8+
- mitmproxy (`pip install mitmproxy`)
- Device or emulator configured to use mitmproxy as HTTP/HTTPS proxy.
- mitmproxy CA certificate installed on the device (visit `http://mitm.it` while proxying).

## Installation
1. Clone this repo or download the script.
2. Save the script as `auto_fix_logo_request.py`.

## Usage
```bash
mitmproxy -s fix_logo_progres.py
- Run the app while your device is proxied through mitmproxy.
- The addon will log when it captures the ID
- Requests to /logoEtablissement/undefined will be rewritten automatically

```
## Legal Notice
This tool is intended for authorized debugging and testing only. Ensure you have permission before intercepting or modifying traffic.
