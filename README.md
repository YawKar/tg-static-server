# What's that?
Y'all now the drill, this is a dead simple static resource server over telegram.

No authentication & authorization is a feature!

No pagination is a feature! (maybe I'll make pagination later).

I used base85+SHA256 for relative paths to bypass the 64-byte constraint on telegram callback data.

# How to run my instance?
## Docker executable
Assuming you want to share your `~/Music` directory.
```bash
git clone git@github.com:YawKar/tg-static-server.git && cd tg-static-server
mkdir -p secrets && echo "your telegram bot api token" > secrets/telegram_token.secret
docker build -t bot .
docker run -v ~/Music:/Music bot --api-token $(cat secrets/telegram_token.secret) --root-dir /Music
```
## On host machine
Assuming you want to hack things and test it out. (Add pagination maybe...)
```bash
git clone git@github.com:YawKar/tg-static-server.git && cd tg-static-server
mkdir -p secrets && echo "your telegram bot api token" > secrets/telegram_token.secret
# hacking goes here
make requirements
python bot/main.py --api-token $(cat secrets/telegram_token.secret) --root-dir ~/Music
```

# Frequently questioned answers ;D
- Why `$(cat secrets/telegram_token.secret)`?
  - I ripped the skeleton of this project from another one of mine and there I used docker compose secrets management feature.

# Caveats
- Idk if it's safe to put any kind of directory symlinks into the mounted volume.
- Idk about telegram api limitations regarding network bandwidth, file size or anything else.
- Idk about how secure it is to check if a user is allowed to change dir by simply finding out
if the path specified in the callback is relative to the root dir.
