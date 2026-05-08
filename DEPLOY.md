# Panda App Deployment

This project can be deployed with Docker Compose on a 1Panel server.

## 1. Prepare the server

In 1Panel, install Docker if it is not already installed. You do not need to install MySQL separately for this Compose deployment, because MySQL runs as one of the containers.

Open the server firewall / cloud security group for:

- `8080` for the first test deployment
- `80` and `443` later when binding a domain through 1Panel

## 2. Upload or pull the project

Put the project on the server, for example:

```bash
cd /opt
git clone <your-repository-url> panda-app
cd /opt/panda-app
```

If you do not use Git yet, upload the project zip through 1Panel and extract it to `/opt/panda-app`.

## 3. Create environment config

```bash
cp .env.example .env
nano .env
```

Change all passwords and tokens before starting production services.

## 4. Start containers

```bash
docker compose up -d --build
```

Check status:

```bash
docker compose ps
docker compose logs -f backend
```

Open:

```text
http://<server-ip>:8080
```

Backend health check:

```text
http://<server-ip>:8080/health
```

## 5. Bind a domain later

After `http://<server-ip>:8080` works, create a reverse proxy site in 1Panel:

- Domain: your domain
- Proxy target: `http://127.0.0.1:8080`
- Enable HTTPS certificate after DNS is pointing to the server

## Common commands

Restart:

```bash
docker compose restart
```

Update after pulling new code:

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```
