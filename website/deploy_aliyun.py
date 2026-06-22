from __future__ import annotations

import os
import posixpath
import tarfile
import time
from pathlib import Path

import paramiko


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DEPLOY_TMP = ROOT / "deploy_tmp"
ARCHIVE = DEPLOY_TMP / "python_tutorial_site.tar.gz"


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


def make_archive() -> None:
    if not PUBLIC.exists():
        raise SystemExit("public/ does not exist. Run website/build_site.py first.")
    DEPLOY_TMP.mkdir(exist_ok=True)
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with tarfile.open(ARCHIVE, "w:gz") as tar:
        for item in PUBLIC.iterdir():
            tar.add(item, arcname=item.name)
    print(f"archive={ARCHIVE} bytes={ARCHIVE.stat().st_size}")


def connect() -> paramiko.SSHClient:
    host = required_env("DEPLOY_HOST")
    user = os.environ.get("DEPLOY_USER", "root")
    password = required_env("DEPLOY_PASSWORD")
    port = int(os.environ.get("DEPLOY_PORT", "22"))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=host,
        port=port,
        username=user,
        password=password,
        timeout=30,
        banner_timeout=30,
        auth_timeout=30,
    )
    return client


def run(client: paramiko.SSHClient, command: str, timeout: int = 300) -> None:
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    if out:
        print(out)
    if err:
        print(err)
    if exit_code != 0:
        raise SystemExit(f"Remote command failed with exit code {exit_code}: {command}")


def upload(client: paramiko.SSHClient) -> str:
    remote_archive = f"/tmp/python_tutorial_site_{int(time.time())}.tar.gz"
    sftp = client.open_sftp()
    try:
        sftp.put(str(ARCHIVE), remote_archive)
    finally:
        sftp.close()
    return remote_archive


def deploy(client: paramiko.SSHClient, remote_archive: str) -> None:
    quoted_archive = remote_archive.replace("'", "'\\''")
    command = f"""
set -e
if ! command -v nginx >/dev/null 2>&1; then
  if command -v dnf >/dev/null 2>&1; then dnf install -y nginx;
  elif command -v yum >/dev/null 2>&1; then yum install -y nginx;
  else echo "No dnf/yum package manager found" >&2; exit 1;
  fi
fi
mkdir -p /var/www/python-tutorial
rm -rf /var/www/python-tutorial/*
tar -xzf '{quoted_archive}' -C /var/www/python-tutorial
cat > /etc/nginx/conf.d/python_tutorial.conf <<'EOF'
server {{
    listen 80;
    server_name 39.106.48.40;
    root /var/www/python-tutorial;
    index index.html;
    charset utf-8;
    client_max_body_size 64m;

    location / {{
        try_files $uri $uri/ /index.html;
    }}

    location ~* \\.(?:png|jpg|jpeg|gif|css|js|html|json|py|md|csv|txt|zip|xlsx|docx|pptx)$ {{
        try_files $uri =404;
        expires 7d;
        add_header Cache-Control "public";
    }}
}}
EOF
if command -v firewall-cmd >/dev/null 2>&1; then
  firewall-cmd --permanent --add-service=http >/dev/null 2>&1 || true
  firewall-cmd --reload >/dev/null 2>&1 || true
fi
chown -R nginx:nginx /var/www/python-tutorial 2>/dev/null || true
nginx -t
systemctl enable nginx
systemctl restart nginx
rm -f '{quoted_archive}'
printf 'deployed to /var/www/python-tutorial\\n'
"""
    run(client, command, timeout=600)


def main() -> None:
    make_archive()
    client = connect()
    try:
        remote_archive = upload(client)
        print(f"uploaded={posixpath.basename(remote_archive)}")
        deploy(client, remote_archive)
    finally:
        client.close()


if __name__ == "__main__":
    main()
