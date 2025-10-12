# 服务器安全修正

在配置完成并跑了几周之后，根据维护人员反馈，对服务器增加了一些额外的安全配置。

## No Referrer

Referrer Policy决定了网站的同源设定，根据维护人员反馈，希望将其设置成No Referrer来防止任何潜在的泄露。修改`/etc/nginx/conf.d/flarum.conf`，在`server`块中添加`add_header Referrer-Policy "no-referrer";`的语句，就可以添加上这个特性。

比较奇怪的是，我这里设置后，再打开前端页面，发现请求里有两个Referrer Policy设置，一个是服务器的`no-referrer`，另一个是`same-origin`，查了一圈不知道是从哪里来的。个人感觉是Cloudflare带来的，因为站点是用Cloudflare反向代理的。所以设置的时候，其实应该也可以从Cloudflare里设置。

## 仅限Cloudflare连接

站点使用Cloudflare连接之后，可以大幅减轻被DDoS的可能性。然而经过维护人员调查后发现，如果直接按IP地址连接，则也能显示出网页，只是HTTPS验证失败罢了。这很危险，如果一个程序一直在扫描IP中是否有网站，这个程序就很可能扫到我们的服务器然后绕开Cloudflare对我们的服务器进行打击。所以解决方案是：只允许Cloudflare连接到我们的网站。为了实现这一解决方案，有两种不同的方法：一种是使用Linux防火墙来限制只允许Cloudflare连接到我们服务器的网站相关端口。另一种是配置Nginx来只允许Cloudflare连接。

无论采用哪一种方案，首先需要知道Cloudflare的反向代理IP都有哪些，这个可以通过查阅[Cloudflare的文档](https://www.cloudflare.com/ips/)来知晓。

### 方案一

如果选用方法一，则可以执行如下语句来配置ufw：

```sh
# IPv4
sudo ufw allow from 103.21.244.0/22 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 103.22.200.0/22 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 103.31.4.0/22 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 104.16.0.0/12 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 108.162.192.0/18 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 131.0.72.0/22 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 141.101.64.0/18 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 162.158.0.0/15 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 172.64.0.0/13 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 173.245.48.0/20 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 188.114.96.0/20 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 190.93.240.0/20 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 197.234.240.0/22 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 198.41.128.0/17 to any port 443 proto tcp comment Cloudflare

# IPv6
sudo ufw allow from 2400:cb00::/32 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 2606:4700::/32 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 2803:f800::/32 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 2405:b500::/32 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 2405:8100::/32 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 2a06:98c0::/29 to any port 443 proto tcp comment Cloudflare
sudo ufw allow from 2c0f:f248::/32 to any port 443 proto tcp comment Cloudflare
```

执行完毕后应当就只能通过Cloudflare连接到站点了。当然，如果Cloudflare更新了他的IP列表，这里也都得跟着改，非常不便，所以这里介绍一下维护人员编写的Python脚本，可以自动获取IP地址列表并批量设置ufw。

```python
import requests
import subprocess
import re

def run(args):
    print(">", " ".join(args))
    subprocess.run(args)

for line in subprocess.run(["ufw", "status"], stdout=subprocess.PIPE).stdout.decode().split("\n"):
    if "Cloudflare" not in line:
        continue
    print(line)
    cidr_ptn = re.compile(r'[0-9\.a-f:]+/[0-9]+')
    for entry in line.strip().split(" "):
        if not cidr_ptn.match(entry):
            continue
        run("ufw delete allow from".split(" ") + [entry] + "to any port 443 proto tcp".split(" "))

ips = requests.get("https://www.cloudflare.com/ips-v4/").text.strip().split("\n") + requests.get("https://www.cloudflare.com/ips-v6/").text.strip().split("\n")
for ip in ips:
    run("ufw allow from".split(" ") + [ip] + 'to any port 443 proto tcp comment Cloudflare'.split(" "))

run("ufw status".split(" "))
```

### 方案二

如果选择方法二，可以首先创建一个文件`/etc/nginx/cloudflare.conf`并写入如下内容：

```
# /etc/nginx/cf.conf

# IPv4
allow 103.21.244.0/22;
allow 103.22.200.0/22;
allow 103.31.4.0/22;
allow 104.16.0.0/12;
allow 108.162.192.0/18;
allow 131.0.72.0/22;
allow 141.101.64.0/18;
allow 162.158.0.0/15;
allow 172.64.0.0/13;
allow 173.245.48.0/20;
allow 188.114.96.0/20;
allow 190.93.240.0/20;
allow 197.234.240.0/22;
allow 198.41.128.0/17;

# IPv6
allow 2400:cb00::/32;
allow 2606:4700::/32;
allow 2803:f800::/32;
allow 2405:b500::/32;
allow 2405:8100::/32;
allow 2a06:98c0::/29;
allow 2c0f:f248::/32;

# Deny all other traffic
deny all;
```

然后修改`/etc/nginx/conf.d/flarum.conf`，在`server`块中添加`include /etc/nginx/cloudflare.conf;`，重启Nginx服务器即可。不过我没有试验过这种方法，不确保正确性。

## Cloudflare真实IP

在使用了Cloudflare反向代理了网站之后，所有来源IP就被Cloudflare包了一层隐藏起来了。所以Nginx日志里记录到的全是Cloudflare服务器的地址。Flarum中用户登录IP也是Cloudflare服务器的地址。然而维护人员想知道访问网站的人的真实IP地址，以看看是谁在尝试攻击网站。这部分需要解决两个问题，首先我们解决Nginx中的IP问题。

### Nginx中的真实IP

解决方案同样也已经被Cloudflare写好了，查阅[Cloudflare文档](https://developers.cloudflare.com/support/troubleshooting/restoring-visitor-ips/restoring-original-visitor-ips/#nginx-1)就能知道怎么做。

首先确保Nginx已经开启了`ngx_http_realip_module`模块，可以通过`nginx -V`来确认是否开启（查看里面`with`开头的命令行参数），我这里是开启的状态，所以我就不需要再折腾。然后按照文档修改`/etc/nginx/conf.d/flarum.conf`在`server`块中添加如下语句：

```
set_real_ip_from 192.0.2.1;
real_ip_header X-Forwarded-For;
```

当然，这么做之后，是可以获取到真实IP了，但日志里显示的仍然是Cloudflare的IP，解决方案就是新建一种日志格式，使用我们获取到的真实IP来取代默认的IP显示。仍然是在`/etc/nginx/conf.d/flarum.conf`文件里，写入如下代码，并同时修改`access_log`语句。但是需要注意，`log_format`语句不能写在`server`块里，要写在`server`块的上面。

```
log_format cloudflare_log '$http_x_forwarded_for - $remote_user - [$time_local]'
                          '"$request" $status $body_bytes_sent'
                          '"$http_referer" "$http_user_agent"';

# 这是我们之前的server块
server {
    # 此处省略15字...

    # 在后面加上cloudflare_log以使用我们新定义的输出格式来输出日志
    access_log /var/log/nginx/flarum.access cloudflare_log;
}
```

`log_format`语句定义了一种新日志输出格式，我们在其中使用`$http_x_forwarded_for`变量来获取真实IP。这个日志输出格式就是Nginx默认的`combined`格式，将其中的IP改为真实IP的结果。如果你的Nginx服务器使用其他输出格式，你也需要进行对应的改动。

### Flarum中的真实IP

Flarum真是太刁了，这种反向代理检测功能都没写代码里。Flarum是直接获取地址，完全不考虑X-Forwarded-For的值的。而利用Flarum Middleware解决这一问题的插件也是好几年前更新的且issue里一大堆问题的东西。所以我打算直接跳过从Flarum这个麻烦的东西，直接从代理服务器那边下手解决这个问题。

刚才的解决方案中，我们已经拿到了真实的IP地址，问题是怎么把他强制设置给Nginx，解决方案如下，在PHP反向代理中设置这些内容。

```
# 这是原本的location块
location ~ \.php$ {
    # 这些语句不变
    fastcgi_split_path_info ^(.+.php)(/.+)$;
    fastcgi_pass unix:/run/php/php8.1-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;

    # 新建一个变量用于容纳真实IP地址。
    # 它的值为X-Forwarded-For中的值。
    # 如果没有X-Forwarded-For，则设置为这个请求来源的IP地址。
    set $flarum_addr $remote_addr;
    if ($http_x_forwarded_for) {
        set $flarum_addr $http_x_forwarded_for;
    }

    # 保持这个导入语句
    include fastcgi_params;

    # 覆盖掉上面导入语句中对FastCGI参数设置的语句。
    # 把远程地址强制设置为我们的变量。
    fastcgi_param  REMOTE_ADDR        $flarum_addr;
}
```

这样一来，我们就可以强行把真实地址喂到Flarum嘴里，让Flarum里也能显示用户的真实地址了。
