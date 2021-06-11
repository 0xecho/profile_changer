# Telegram Profile Picture Changer

Is the little green dot not enough for you to announce your presence on the ever-growing telegram platform? 

No worries, python comes to the rescue. 

This little script can change your profile picture according to your online status. Configure it with your api_hash, api_id, and give it 2 images (one for when you are online, one for when you are offline) and **Boom** you are good to go.

## Installation

Just clone this repository where ever you want and configure this little linux service I wrote (more configs for pm2 etc.. will be coming)

```bash
[Unit]
Description=Telegram profile picture changer based on your status
After=network.target
Wants=network-online.target
[Service]
Restart=always
Type=simple
ExecStart=/usr/bin/python3 /path/to/main.py
Environment='API_HASH=[API HASH HERE]' 'ONLINE_IMAGE_PATH=[ ONLINE_IMAGE_PATH HERE ]' 'API_ID=[ API ID HERE ]' 'OFFLINE_IMAGE_PATH=[ OFFLINE_IMAGE_PATH HERE ]'
[Install]
WantedBy=multi-user.target

```
