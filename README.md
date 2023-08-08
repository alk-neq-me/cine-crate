# cine-crate

## Install

```sh
# docker for redis
sudo docker run --name cine-crate-redis -p 6379:6379 redis:latest && sudo docker rm cine-crate-redis
```

```sh
# setup server
cd server
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

```sh
# setup client
cd ../mobile
yarn
yarn expo start
```
