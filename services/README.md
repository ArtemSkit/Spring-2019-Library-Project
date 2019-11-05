# Technical Details

In order for this service to work, both `flask.service` and `mytestlib.service` systemd files need to be running, per the following command:

```bash
sudo systemctl start flask
sudo systemctl start mytestlib
```
