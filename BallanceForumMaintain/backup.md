# 服务器备份

根据服务器维护人员要求，为了确保论坛数据的绝对安全，今后希望可以定时将论坛数据进行备份。论坛维护人员提出了几点要求：

1. 定时将全部论坛数据备份成一个tar包并压缩。
2. 提供一个JSON格式的清单文件来表示这个tar包的基本信息（例如SHA256摘要，和创建时间等）
3. 打开一个仅允许他自己的服务器连接的HTTP服务，他通过轮询机制同步论坛数据到另一个具有更大硬盘的服务器上。

根据这些要求，我们设计了接下来的备份流程。

## 准备工作

### mysqldump专用账户

Flarum的部分数据是存储在MySQL数据库中的，然而我们不希望粗暴地使用和Flarum运行时使用的同一个用户来将这些数据Dump出来，因为这样可能会增加数据泄露的风险。因此我们希望创建一个专门用于Flarum数据库Dump的新用户，该用户仅拥有有限的权限，刚好满足mysqldump的执行。执行以下命令来创建一个名为`flarum_dumper`的新用户：

```sql
-- 创建Dump专用用户，以指定的密码，和mysql_native_password验证模式。
-- 该用户仅允许从localhost登录。
CREATE USER 'flarum_dumper'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
-- 仅授予Dump用户对论坛数据库的有限权限，使之刚好满足mysqldump的需求。
-- 这些权限只有从localhost登陆时才会授予。
GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER ON flarum.* TO 'flarum_dumper'@'localhost';
GRANT PROCESS ON *.* TO 'flarum_dumper'@'localhost';
-- 在不重启MySQL服务器的情况下应用权限。
FLUSH PRIVILEGES;
```

有关授予的权限，通过查询MySQL文档可知：

> mysqldump requires at least the SELECT privilege for dumped tables, SHOW VIEW for dumped views, TRIGGER for dumped triggers, LOCK TABLES if the --single-transaction option is not used, PROCESS if the --no-tablespaces option is not used, and the RELOAD or FLUSH_TABLES privilege with --single-transaction if both gtid_mode=ON and gtid_purged=ON|AUTO. Certain options might require other privileges as noted in the option descriptions. 
> 
> --events: Include Event Scheduler events for the dumped databases in the output. This option requires the EVENT privileges for those databases. 

配合后文的导出脚本，这些权限是导出所必须的最小权限。其中PROCESS权限由于其特性，只能在全部数据库上进行授予。

## 备份脚本

备份脚本将被存放在`/usr/local/bin/flarum_backup.sh`，这是UNIX系统存放用户自编译程序的地方，非常适合备份脚本存放。存放后需要检查其是否有执行权限（尤其是其所有者和后文Systemd中设置的执行者不同时）。

```sh
#!/bin/bash
echo "开始备份Ballance论坛系统..."

# 设置脚本出错就退出
# -e表示一旦脚本中有命令的返回值为非0，则脚本立即退出，后续命令不再执行。
# -u表示当脚本中使用未定义的变量时，立即退出并报错。
# -o pipefail用于确保在管道中的任何命令失败时，整个管道会以非零退出码退出。默认情况下，Bash只会返回管道中最后一个命令的退出码，而忽略中间命令的失败。
set -euo pipefail

# 配置变量
BACKUP_DIR="/var/www/flarum_backups"
BACKUP_ARCHIVE_NAME="flarum_backup.tar.xz"
BACKUP_MANIFEST_NAME="flarum_backup.json"
BACKUP_ARCHIVE_PASSWORD="VeryStrongPassword"
MYSQL_USER="flarum_dumper"
MYSQL_PASSWORD="VeryStrongPassword"
MYSQL_DATABASE="flarum"
FLARUM_DATA_DIR="/var/www/flarum"
MEILISEARCH_DATA_DIR="/var/lib/meilisearch"

# 临时目录的申请与自动清理
TEMP_DIR=$(mktemp -d)
echo "已申请临时目录：$TEMP_DIR"
cleanup() {
    rm -rf "$TEMP_DIR"
    echo "已销毁临时目录"
}
trap cleanup EXIT

# 确保存档文件和清单文件所在文件夹存在
mkdir -p "$BACKUP_DIR"
# 在临时目录中构建存档文件中的文件夹结构
echo "于临时目录中创建存档文件结构..."
mkdir -p "$TEMP_DIR/mysql"
mkdir -p "$TEMP_DIR/meilisearch" 
mkdir -p "$TEMP_DIR/flarum"

# 备份 MySQL
echo "导出MySQL数据库..."
mysqldump \
	--single-transaction \
	--routines \
	--triggers \
	--events \
	--hex-blob \
	--set-gtid-purged=OFF \
	-u"$MYSQL_USER" \
	-p"$MYSQL_PASSWORD" \
	--databases "$MYSQL_DATABASE" > "$TEMP_DIR/mysql/flarum_dump.sql"

# 创建软链接
echo "链接Meilisearch数据..."
ln -s "$MEILISEARCH_DATA_DIR" "$TEMP_DIR/meilisearch/data"
echo "链接Flarum数据..."
ln -s "$FLARUM_DATA_DIR" "$TEMP_DIR/flarum/data"

# 创建压缩包并加密
echo "创建压缩且加密的存档..."
# -c指令表示压缩。-h指令表示跟随软链接打包所有文件。
tar -ch -C "$TEMP_DIR" . | xz -6 --threads=0 | openssl enc -aes-256-cbc -pbkdf2 -pass pass:$BACKUP_ARCHIVE_PASSWORD -out "${BACKUP_DIR}/${BACKUP_ARCHIVE_NAME}"

# 生成备份描述文件
# sha256sum会以名为FIPS-180-2的格式输出，形似07f2b5a17427064a4dc9f1ef59f853cace91eeb5662da6bf83813e38be97f971 *FAQ.md
# 使用cut命令以空白分割，并取第一项，即可获得需要的内容。
echo "生成存档描述文件..."
TIMESTAMP=$(date +%s)
DIGEST=$(sha256sum "${BACKUP_DIR}/${BACKUP_ARCHIVE_NAME}" | cut -d' ' -f1)
# 直接拼接JSON输出
cat > "${BACKUP_DIR}/${BACKUP_MANIFEST_NAME}" << EOF
{
	"timestamp": $TIMESTAMP,
	"digest": "$DIGEST"
}
EOF

echo "Ballance论坛系统备份完成"
echo "存档文件: ${BACKUP_DIR}/${BACKUP_ARCHIVE_NAME}"
echo "存档描述文件: ${BACKUP_DIR}/${BACKUP_MANIFEST_NAME}"
```

编写完成后，需要记得替换文件开头的那些变量的值。然后可以尝试运行一次，确定可以运行。

## Systemd服务

折腾完这些，我们需要把这个脚本注册成Systemd服务，且让其定期执行。

### 创建服务

创建服务文件`/etc/systemd/system/flarum-backup.service`，就像配置Meilisearch时一样。

由于mysqldump需要MySQL启动后才能连接，所以我们需要等待MySQL的服务后才能启动备份服务。服务类型是oneshot而不是simple，因为我们是瞬时执行，而非持续执行。同时不需要失败重启策略，不然脚本失败了就反复循环重启循环失败了。

```
[Unit]
Description=Flarum Backup
Requires=mysql.service
After=mysql.service

[Service]
Type=oneshot
WorkingDirectory=/var/www/flarum_backups
ExecStart=/usr/local/bin/flarum_backup.sh
User=flarum
Group=flarum
```

### 创建定时器

创建定时器文件`/etc/systemd/system/flarum-backup.timer`。

```
[Unit]
Description=Flarum Backup Timer (every 3 days)
Requires=flarum-backup.service

[Timer]
OnCalendar=Mon,Thu *-*-* 04:00:00 Asia/Shanghai
Persistent=true
RandomizedDelaySec=3600

[Install]
WantedBy=timers.target
```

其中，`Mon,Thu *-*-* 04:00:00 Asia/Shanghai`表示在每周一和每周四的UTF+8的凌晨4点进行定时器操作。由于Systemd的设计，做不到每隔N天备份一次这种定时操作，只能如此。选择这两个时间点是考虑正常情况下，周末较为活跃，以及UTF+8凌晨四点人数较少的情况。

### 启用定时器

设置完成后，就可以执行以下命令设置定时器的自启动和启动计时器了。

```sh
sudo systemctl enable flarum-backup.timer
sudo systemctl start flarum-backup.timer
```

## Nginx站点配置

新建Nginx配置文件`/etc/nginx/conf.d/flarum_backup.conf`。其中`61.61.61.61`要改成自己服务器的IP地址。

```
server {
    listen 6145;
    server_name 61.61.61.61;
    
    root /var/www/flarum_backups;
    
    # 安全设置
    autoindex off;
    disable_symlinks on;

    # 设置日志
    access_log /var/log/nginx/flarum_backups.access;
    error_log /var/log/nginx/flarum_backups.error;
    
    location / {
        # 仅允许访问指定文件
        location = /flarum_backup.tar.xz {
            alias /var/www/flarum_backups/flarum_backup.tar.xz;
            default_type application/octet-stream;
            add_header Content-Disposition "attachment; filename=flarum_backup.tar.xz";
        }

        location = /flarum_backup.json {
            alias /var/www/flarum_backups/flarum_backup.json;
            default_type application/json;
        }

        # 其他所有请求返回 404
        return 404;
    }

    # 防范路径遍历（双重保险）
    location ~ \.\. {
        return 403;
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
}
```

配置完成后检查一下有没有错误，然后重载Nginx服务器。

## 配置ufw防火墙

执行以下命令来只允许维护人员的服务器访问这个服务器，其中的`16.16.16.16`需要替换成维护人员服务器的IP地址。

```sh
# 允许指定 IP 访问 6145 端口
sudo ufw allow from 16.16.16.16 to any port 6145 proto tcp comment Flarum-Backup
```
