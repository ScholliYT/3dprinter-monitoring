# 3dprinter-monitoring
Monitoring my 3D printer


## Installation

Install python dependencies
`pip install paho-mqtt minimalmodbus`

Run the script periodically via crontab to report information to Datacake by placing this line into `crontab -e`.  
`*/5 * * * * python3 /home/pi/git/3dprinter-monitoring/datacake_monitoring.py`
