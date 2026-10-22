# CVE-2026-109618/619修复

PHP于2026年10月20日爆出CVE-2026-109618/619漏洞，服务器采用的版本还是Ubuntu包管理器提供的PHP 8.1，因此被迫更新。

## 用户友好维护告知页面

在维护过程中，服务器总是需要宕机一会。由于是PHP侧的问题，Nginx侧仍能正常工作，因此展示一个用户友好的维护告知非常必要。

### 维护告知网页

新建文件：`/var/www/maintenance/maintenance.html`，填入以下AI生成内容：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>系统维护中 / Under Maintenance</title>
<style>
  body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
      "PingFang SC", "Microsoft YaHei", sans-serif;
    line-height: 1.7;
    color: #333;
    background: #fff;
  }
  .box {
    max-width: 520px;
    width: 100%;
  }
  h1 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 12px;
  }
  p {
    margin: 0 0 10px;
    color: #555;
  }
  hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 28px 0;
  }
</style>
</head>
<body>
  <div class="box">
    <h1>系统维护中</h1>
    <p>我们正在进行系统更新与维护，以应对PHP CVE-2026-109618/619漏洞。</p>
    <p>服务暂时不可用，请稍后再试。给您带来的不便，敬请谅解。</p>

    <hr>

    <h1>Under Maintenance</h1>
    <p>We are performing scheduled system maintenance to deal with PHP CVE-2026-109618/619 issue.</p>
    <p>The service is temporarily unavailable. Please try again later.</p>
    <p>We apologize for any inconvenience.</p>
  </div>
</body>
</html>
```

然后执行`sudo chown -R www-data:www-data /var/www/maintenance`命令，把整个文件夹的权限切给`www-data`，使得Nginx可以读取。

### Nginx配置

新建文件：`/etc/nginx/snippets/maintenance.conf`，填入以下AI生成内容：

```conf
# /etc/nginx/snippets/maintenance.conf
# 存在开关文件时自动进入维护模式（每个请求判断，无需 reload）
if (-f /etc/nginx/maintenance.on) {
    return 503;
}

# 改为指向命名 location
error_page 503 @maintenance;

location @maintenance {
    root /var/www/maintenance;
    try_files /maintenance.html =503;

    internal;                      # 禁止用户直接访问该 URL
    add_header Cache-Control "no-store, no-cache, must-revalidate" always;
    add_header Retry-After 3600 always;
    add_header X-Robots-Tag "noindex, nofollow" always;
}
```

然后在主站文件`/etc/nginx/conf.d/flarum.conf`中按如下方式引入该片段：

```conf
server {
    # HTTPS块。省略其内容...
    listen 443;

    include /etc/nginx/snippets/maintenance.conf;   # ← 引入维护逻辑
}

server {
    # HTTP块。AI说要在这里加，但是我这里只有一个302跳转，所以我没加。
    listen 80;

    # include /etc/nginx/snippets/maintenance.conf;   # ← 引入维护逻辑
}
```

### 上线页面

执行以下内容检查Nginx配置文件格式，然后重载配置。

```sh
# 语法检查
sudo nginx -t
# 加载配置
sudo systemctl reload nginx
```

在上线之后，就可以通过控制单个文件`/etc/nginx/maintenance.on`的存在来控制维护，即：

- 开启维护：`sudo touch /etc/nginx/maintenance.on`（立即生效）
- 结束维护：`sudo rm /etc/nginx/maintenance.on`（立即恢复，无需 reload）

## 更新PHP

由于服务器用的Ubuntu版本中的包管理器中提供的PHP是早已经End of Life的PHP 8.1，所以我们只能转而使用PHP官方推荐的方式来安装：官方提供的Ubuntu PPA。

首先添加添加官方的PPA源：

```sh
# Add the ondrej/php repository.
sudo apt update
sudo apt install -y software-properties-common
sudo LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php -y
sudo apt update

# Install PHP.
sudo apt install -y php8.3
```

然后停止PHP 8.1的服务，并禁止自动启动：

```sh
sudo systemctl stop php8.1-fpm
sudo systemctl disable php8.1-fpm
```

然后从这个PPA里安装PHP 8.3。因为主仓库里没有同名的包，所以应该不需要：

```sh
sudo apt install php8.3 php8.3-fpm php8.3-common php8.3-curl php8.3-gd php8.3-mbstring php8.3-mysql php8.3-zip php8.3-intl php8.3-xml php8.3-bcmath php8.3-soap
```

启动PHP 8.3并设置开机自启：

```sh
sudo systemctl start php8.3-fpm
sudo systemctl enable php8.3-fpm
```

到这里似乎应当再把PHP 8.1卸载了，但是我使用`php -v`等命令检查，系统直接认了新安装的PHP 8.3。为了防止删除PHP 8.1再搞出什么Bug，因此我就没有删除。

## 适配新PHP

由于是跨小版本更新，一些配置文件需要进行更新。

### 查找PHP-FPM Socket

使用配置阶段相同的方式查找PHP-FPM Socket。在`/etc/php/8.3/fpm/pool.d/www.conf`找到配置文件，使用`cat www.conf | grep listen`筛选出监听端口的配置，得到`listen = /run/php/php8.3-fpm.sock`字样。

### 更新Nginx配置

主站文件`/etc/nginx/conf.d/flarum.conf`中的PHP-FPM Socket路径，测试并上线。

### Composer

Composer经过检测可以正常运行（其实我只测了`composer --help`和`composer --version`，懒了）

## Flarum配置

### 屏蔽弃用警告

Flarum要求编辑`/etc/php/8.3/fpm/php.ini`文件，修改如下字段，来屏蔽预期内的弃用通知，防止它们填满日志或意外暴露给访客：

```ini
error_reporting = E_ALL & ~E_DEPRECATED & ~E_USER_DEPRECATED
```

修改完后重启PHP-FPM：`sudo systemctl reload php8.3-fpm`

## 清除缓存

执行`php flarum cache:clear`清除Flarum缓存。

## 收尾

删除Nginx的维护标志文件，然后访问网址，一切正常。看后台的PHP版本也已经更新。
