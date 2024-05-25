## Setup

Create a file called config.ini inside the jamcito directory. The content of the file should be the following ids:

```ini
[DEFAULT]
jam server=<The JAM server id>
test server = <Test server id>
jam general chat = <The JAM general chat id>
test general chat = <The Test general chat id>
token=<The discord token for the bot>
```


## Start the bot

```bash
poetry run service-run
```

## To install it as a service

### Ubuntu

Run this in the root of the project

```bash
$ poetry shell
$ which service-run
```

We should have something like 
```
/home/gerardo/.cache/pypoetry/virtualenvs/jamcito-tXdIXVmH-py3.8/bin/service-run
```

Now create the service file to `/etc/systemd/system/jamcito.service` with the following content:

```ini
[Unit]
Description=Jamcito

[Service]
ExecStart=/home/gerardo/.cache/pypoetry/virtualenvs/jamcito-tXdIXVmH-py3.8/bin/service-run

[Install]
WantedBy=multi-user.target
```
Using The binary path we got before as `ExectStart`

Now you can start the service
```bash
sudo systemctl start example-service
```