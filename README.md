# My Project

This repository contains the source code for a project that includes functionality for scheduling tasks, fetching the latest news, and interacting with Telegram. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Linux Service Setup](#linux-service-setup)
- [Modules](#modules)
- [License](#license)

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Configuration
Make sure to configure the environment variables needed for your project. You can use the `.env.example` file as a template. Copy it to .env and update the values accordingly.

```bash
cp .env.example .env
```

## Environment Variables
`BOT_TOKEN`: Your Telegram bot API key.
`SECRET_KEY`: Encryption key.

## Usage
You can start the application by running the appropriate Python scripts. Here is an example of how to run the main components:
For the regular bot polling:
```bash
python telegram_utils.py
```

For the scheduled tasks:
```bash
python schedule_utils.py
```

## Linux Service Setup
To set up the project as a service on a Linux system, you need to create two service files: `nieuwsbot.service` and `nieuwsbot-schedule.service`.

### nieuwsbot.service
Create a file named `nieuwsbot.service` with the following content:

```ini
[Unit]
Description=NieuwsBot

[Service]
ExecStart=/your/path/to/nieuwsbot/venv/bin/python /your/path/to/nieuwsbot/telegram_utils.py
WorkingDirectory=/your/path/to/nieuwsbot
Restart=always
User=root

[Install]
WantedBy=default.target
```

### nieuwsbot-schedule.service
Create a file named `nieuwsbot-schedule.service` with the following content:

```ini
[Unit]
Description=NieuwsBot Schedule

[Service]
ExecStart=/your/path/to/nieuwsbot/venv/bin/python /your/path/to/nieuwsbot/schedule_utils.py
WorkingDirectory=/your/path/to/nieuwsbot
Restart=always
User=root

[Install]
WantedBy=default.target
```

### Enabling the Services
1. Copy the `nieuwsbot.service` and `nieuwsbot-schedule.service` files to the `/etc/systemd/system` directory.

```bash
sudo cp nieuwsbot.service /etc/systemd/system/
sudo cp nieuwsbot-schedule.service /etc/systemd/system/
```

2. Reload the systemd daemon.

```bash
sudo systemctl daemon-reload
```

3. Enable and start the services.

```bash
sudo systemctl enable nieuwsbot.service
sudo systemctl start nieuwsbot.service
sudo systemctl enable nieuwsbot-schedule.service
sudo systemctl start nieuwsbot-schedule.service
```

## Modules
### latest_news.py
This module fetches the latest news using a specified news API.

### schedule_utils.py
This module contains utilities for scheduling tasks using the schedule library.

### telegram_utils.py
This module provides utilities for interacting with Telegram using the telebot library.

### Requirements
The project requires the following Python packages:

- feedparser
- telebot
- schedule
- latest_news
- Fernet
- ratelimit
- cryptography

## License
This project is licensed under the Custom License. See the [LICENSE](LICENSE) file for more details.