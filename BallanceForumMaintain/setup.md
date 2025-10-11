# 创建新账户

使用`sudo adduser flarum`命令创建名为flarum新用户，并设置密码，其余信息不填写直接回车。

然后，为了新用户能够使用`sudo`，需要使用文本编辑器打开`/etc/sudoers`文件，并添加以下行：`flarum ALL=(ALL) ALL`。有时候`/etc/sudoers`并不允许编辑，你需要转而在`/etc/sudoers.d`目录下创建单独的文件来定义特定用户或用户组的权限。需要注意：文件名应尽量以用户或用户组的名称命名，且不应包含`~`或`.`字符。文件的权限应设置为`0440`，以确保只有root用户可以读取和修改这些文件。

# SSH配置

## 生成密钥对

本机使用`ssh-keygen -t ed25519 -C "name@email.com"`生成SSH密钥对，文件名输入`flarum`，并设置密码。得到公钥文件`flarum.pub`和私钥文件`flarum`。

## 服务器部署

### 正规操作

使用WinSCP等工具，将公钥文件`xxx.pub`上传为服务器的`~/.ssh/authorized_keys`文件（注意一下该文件的权限，必须要是自己所有，否则sshd不认）。这个文件是每个用户一个的，也就是你不能用flarum的key来登录root。如果一个用户允许从多个key登录的话，就需要在这个文件里写入多行，就是简单地将每个公钥按回车join在一起，然后输出成`~/.ssh/authorized_keys`文件。

打开服务器的`/etc/ssh/sshd_config`文件并编辑如下设置：

```conf
# 修改默认端口（建议使用1024-65535之间的端口）
Port 2222  # 替换为你选择的新端口号

# 禁用密码认证
PasswordAuthentication no

# 禁用挑战响应认证
ChallengeResponseAuthentication no

# 启用公钥认证
PubkeyAuthentication yes

# 可选：禁用root用户直接登录（推荐）
PermitRootLogin no

# 可选：限制可登录的用户（如果需要）
AllowUsers your_username
```

使用`sudo systemctl restart sshd`重启SSH服务即可应用修改。

### 防变砖操作

为了防止服务器变成砖头，可以使用以下语法单独为某个用户启用对对应规则，以测试是否能够登录，如果登陆失败，还可以登录其他用户，避免服务器变成砖头。

```conf
Match User flarum
    PubkeyAuthentication yes
    PasswordAuthentication no
```

如果测试成功，则可以进入服务器，再按照上述的正规操作来修改。

## 本机部署

在配置好服务器只能使用证书登陆，禁止密码登陆后，我们需要显示指定我们登陆服务器时用的证书，一般来说会默认使用证书文件`~/.ssh/id_rsa`文件（Windows下的Home文件夹就是你自己的用户文件夹，在`C:\Users\<你的名字>`）。但对于我这种有很多个证书的人来说，这种情况就不适用，总不能每次登陆服务器都把要登录的那台服务器的私钥变成`~/.ssh/id_rsa`吧。所以最佳的解决方案就是编辑`~/.ssh/config`，让这个文件手动决定你使用哪个私钥来和服务器做验证。在`~/.ssh/config`文件中添加以下内容：

```conf
Host <服务器IP>
    HostName <服务器IP>
    User flarum
    IdentityFile ~/.ssh/id_ed25519_flarum
    IdentitiesOnly yes
    AddKeysToAgent yes
```

其中`<服务器IP>`要替换成你服务器的IP。最重要的是`User`写为你要登录的用户名，以及`IdentityFile`要指向你登陆用的私钥文件。其余选项不重要，我是从GitHub SSH登录上面抄下来的。配置好之后就可以使用SSH登录到你的远程服务器了，只需要输入你私钥的密码就行了。

如果后续还需要使用WinSCP配合私钥登录的话，需要将私钥再转为PuTTY的专有`PPK`格式，保存在本地以供使用。上网搜一下就有相关内容。

# 出入站规则

我们开始部署超TM安全的出入站规则。原本有两种部署方式，一种是iptables，一种是更加现代的ufw。最终我这里只留下的ufw的方式，有以下几个原因：

* ufw的默认规则就是非常安全的默认阻断所有入站连接，但保留本地回环的模式，所以省了我们很多事，不需要繁琐地去执行各种奇奇怪怪的iptables命令。
* 使用`iptables`配置比较繁琐，IPv4和IPv6还必须要分开配置。而`ufw`会自动帮你一起搞定IPv4和IPv6的配置。
* 后文还有更多需要配置的防火墙规则，使用`iptables`配置就显得非常蠢和麻烦，反观ufw就只需要几个命令就可以搞定。

执行以下命令配置超TM安全的出入站规则。

```sh
# 重置现有规则
sudo ufw reset

# 启用 UFW
sudo ufw enable

# 日志（可选）
sudo ufw logging on

# 允许本地回环通信（默认允许）
# 允许已建立连接（默认允许）

# 允许特定端口（HTTP, HTTPS, 2222）
sudo ufw allow 80/tcp
sudo ufw allow 80/udp
sudo ufw allow 443/tcp
sudo ufw allow 443/udp
sudo ufw allow 2222/tcp
sudo ufw allow 2222/udp
```

使用`sudo ufw status`可以查看当前防火墙状态（如规则和启用与否等）。使用`sudo ufw delete allow <你的规则>`可以删除已经输入的规则，比如你输错的时候。

# 安装Nginx

执行`sudo apt install nginx`安装Nginx。

默认装好的Nginx可以通过HTTP访问到Nginx默认页面，确认安装成功。如果你的服务器装了Apache2的话，请立即卸掉（Apache2的网站配置文件是人类能写的吗？），不然端口冲突，尤其是那些默认LAMP的服务器。

安装完成后可通过`sudo systemctl [start | stop | restart | enable | disable | status] nginx`来启动，停止，重启，开机自启，开机不自启，和查看Nginx状态。执行`sudo nginx -s reload`来重新加载配置文件，而不需要去重启Nginx服务。执行`sudo nginx -t`可以检查Nginx配置文件有无错误。

Nginx配置文件默认在`/etc/nginx`下，主配置是`nginx.conf`，通常具有特殊权限，一般不去改。然后你会看到它有两种不同的网站创建方式，一种是在`conf.d`文件夹下直接编写网站配置，Nginx的主配置文件默认会加载`/etc/nginx/conf.d`文件夹下的配置。另一种是`sites-available`和`sites-enabled`文件夹的组合，用户首先在`sites-available`里编写配置文件，然后通过软链接命令，将其链接到`sites-enabled`里，就算启用了网站，如果希望关闭网站，只需要删除软链接即可，这种方式更加适合多网站共存的情况。我们这里采用的是第一种方案。

# 安装PHP

## 安装

执行`sudo apt install php php-fpm`来安装PHP和PHP-FPM（就是Windows上那个CGI，全称是PHP fastCGI进程管理器）。安装好之后，我们可以同样使用systemctl命令，结合`php8.1-fpm`的unit名称，对PHP-FPM进行起停操作。

装PHP的时候需要注意一下，如果直接输入上面的话，不要无脑点Y键，看看装的包的列表，它有时会尝试给你装Apache2，至少我这里Ubuntu 22.04安装的时候是这样的。这是因为Ubuntu包解析的毛病，`php-fpm`只是一个指向`php<具体版本>-fpm`的Meta Package，然后`php<具体版本>-fpm`有一个适用于Apache2的可选依赖，然后Ubuntu解析这种结构的时候，会莫名其妙地把可选依赖解析成必须依赖，然后就把Apache2带进来了。解决方法是查这个Meta Package具体指向哪个包，我这里是`php8.1-fpm`，然后执行`sudo apt install php8.1 php8.1-fpm`来安装就好了，缺点是之后升级的时候不能享受到Meta Package的好处了。

安装完成后，执行`sudo apt install php-curl php-gd php-json php-mbstring php-mysql php-tokenizer php-zip`安装PHP插件，这些插件是Flarum需要的。

## 运行时用户与权限配置

接下来要去查找PHP-FPM的监听端口，PHP-FPM在Linux上有两种方式，一种是以`127.0.0.1:9000`，通过网络暴露接口，另一种是通过UNIX Sock来暴露接口。我这里推荐在Linux上使用UNIX Sock来暴露接口，因为安全。这种方式即使没有ufw进行防御，也能保证服务器安全（不过实际上只有你脑残地把监听设置为`0.0.0.0:9000`时才有巨大危险）。我们这里安装完之后，转到`/etc/php/8.1`下，用`find . -name *.conf`可以找到有`/etc/php/8.1/fpm/pool.d/www.conf`这样一个配置文件，使用`cat www.conf | grep listen`筛选出监听端口的配置，得到`listen = /run/php/php8.1-fpm.sock`字样，立即转到相应位置查看权限，发现该文件所有者是`www-data`，可以得出PHP-FPM的执行用户是`www-data`，这个用户我们后面会用到。

然后我们可以开始准备网站的容器了。转到`/var/www`中，新建一个文件夹`flarum`作为我们站点的根文件夹。然后在其中创建一个`index.php`，并写入以下内容，该文件用于测试我们的PHP是否安装完成：

```php
<?php
phpinfo();
?>
```

我们需要保证PHP-FPM，Nginx，我们自己之间可以相互访问。最好的方法是将PHP-FPM和Nginx设置为同一用户，我们再加入那个用户的组。我们在上文找到了PHP-FPM的执行用户，是`www-data`。那么我们应该确保：

* Nginx配置文件`/etc/nginx/nginx.conf`中的`user`字段配置为`www-data`。
* 对于我们自己，执行`sudo usermod -a -G www-data flarum`将自己也添加入`www-data`组中，以方便未来网站的操作
    - 分配完成后可以用`groups flarum`检查`flarum`分配进入的用户组。
    - 需要注意加入组后要重新登陆，才能应用自己的组权限。
* `sudo chown -R www-data:www-data /var/www/flarum`来将网站文件夹所有权分配给Nginx的执行用户，前面的`www-data`是用户名，后面的`www-data`是用户组。
* `sudo chmod -R 774 /var/www/flarum`改变权限，确保这个网站文件夹只能Nginx执行用户能访问到。

## 验证

接下来可以验证是否已经安装完成PHP。在`/etc/nginx/conf.d`文件夹先清空所有文件（比如默认的`default.conf`，或者你直接在上面测也行），再新建`flarum.conf`,编写如下内容：

```conf
server {
    listen  80;
    server_name  <你的域名>;
    root    /var/www/flarum;
    index index.php;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+.php)(/.+)$;
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_index index.php;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

其中`<你的域名>`需要替换为你网站的域名。`fastcgi_pass`是我们刚才了解到的PHP-FPM UNIX Sock地址。

最后登录到`http://<你的域名>/index.php`就可以看到PHP成功的结果了。

# 安装MySQL

## 安装

执行`sudo apt install mysql-server-8.0`来安装MySQL。这个命令会一起安装服务端和客户端。安装完成后，建议立即运行`sudo mysql_secure_installation`进行一个安全的初始化，在初始化过程中会提示你要不要启用`VALIDATE PASSWORD PLUGIN`，这是一个密码安全度验证模块，用于检验你设置的用户密码（例如下文创建用户时的密码）安不安全而已。开关都无所谓，因为实际上并不会输入root密码，因为MySQL对root用户采用了一个特殊的操作，使得只能从本机登录root用户；而其他新建的用户又可以限制只能本地登录。所以除非你有从外网登录本机MySQL的需求，否则这个模块开启与否都无所谓。

## 建立数据库与用户

初始化完毕后，使用`sudo mysql`打开MySQL控制台。接下来我们创建用户和数据库。执行以下命令：

```sql
-- 创建论坛数据库
CREATE DATABASE flarum;
-- 创建论坛数据库用户，以指定的密码，和mysql_native_password验证模式。
CREATE USER 'flarum_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
-- 授予论坛数据库用户以论坛数据库的全部权限。
GRANT ALL ON flarum.* TO 'flarum_user'@'localhost';
```

其中`password`是你新建的用户的密码。我这里新建的用户名是`flarum_user`，可以随意改名。后面的`@'localhost'`指示这个用户只能从本机登录，这相对安全。与之相对的是`@'%'`，它代表允许从任何IP登录到MySQL数据库，很危险，除非你知道你在做什么，否则不要用。

全部执行成功后，输入`exit`退出，之后就可以通过`mysql -u flarum_user -p`输入密码后登录新创建的用户，然后使用`SHOW DATABASES;`显示所有数据库来检查结果。

## 验证

我们可以在安装Flarum前，验证从Nginx，到PHP，再到MySQL道路的通畅性，先尽可能消除一些潜在错误。首先进入数据库，执行以下命令插入表和数据：

```sql
-- 创建一个名为todo_list的测试表。
CREATE TABLE flarum.todo_list (
   item_id INT AUTO_INCREMENT,
   content VARCHAR(255),
   PRIMARY KEY(item_id)
);
-- 在测试表中插入几行内容。
INSERT INTO flarum.todo_list (content) VALUES ("My first important item");
INSERT INTO flarum.todo_list (content) VALUES ("My first important item");
INSERT INTO flarum.todo_list (content) VALUES ("My first important item");
-- 确认数据已成功保存到您的表中（会在输出中看到插入的数据）。
SELECT * FROM flarum.todo_list;
```

退出控制台，打开`/var/www/flarum/index.php`，编写以下内容：

```php
<?php
$user = "flarum_user";
$password = "password";
$database = "flarum";
$table = "todo_list";

try {
  $db = new PDO("mysql:host=localhost;dbname=$database", $user, $password);
  echo "<h2>TODO</h2><ol>"; 
  foreach($db->query("SELECT content FROM $table") as $row) {
    echo "<li>" . $row['content'] . "</li>";
  }
  echo "</ol>";
} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}
```

保存。最后登录到`http://<你的域名>/index.php`，页面应该显示在测试表中插入的内容。如果数据库连接有问题，它会抛出异常。

验证完毕后，为了还原验证前的状态，你需要：

* 清空`/var/www/flarum/index.php`或填充无用数据。
* MySQL执行`DROP TABLE IF EXISTS flarum.todo_list;`以删除测试表。

# 安装Composer

执行`sudo apt install composer`来安装Composer。Composer应该是需要一些额外PHP模块才能运行的，但包管理器应该写明了这些依赖了。

唯一需要注意的是，绝对不要使用Composer的1.x版本。Composer的1.x版本对于依赖解析的功能异常孱弱，会吃掉非常多的内存。就拿Flarum来说，添加了大约7-8个插件后，其解析依赖时所吃掉的内容就高达2 GB之多，这对于内存寸土寸金的小型服务器而言是无法承受的。我一开始是在一台内存只有512 MB的Ubuntu 20.04 LTS上进行安装的，最终因无法忍受高额的内存消耗而放弃。

如果你不幸只能安装1.x版本的Composer，那么Composer装依赖的时候可能会显示`Killed`，通常就是内存不足造成的。一种解决方法是编辑`/etc/php/8.1/fpm/php.ini`文件，将`memory_limit`改大一些，比如`512MB`。可以使用`cat /etc/php/8.1/fpm/php.ini | grep memory_limit -n`命令来快速确认行号。另一种解决方案是直接执行`php -d memory_limit=-1 /usr/bin/composer require <你的依赖> -vvv`来执行。其中`/usr/bin/composer`是Composer的位置，可以用`whereis composer`确认。`php -d memory_limit=-1`用于解除php内存限制。`-vvv`用于显示详细信息，方便你确认执行时在哪里崩溃了（基本上都是加载JSON时把自己内存撑爆了）。

如果Composer的内存无论如何都不够，可以尝试在本地先安装一个工程，记得执行`composer require`的时候带上`--no-install`参数（然而这个参数是2.x才有的，2.x基本不会出现内存不够的情况），这样就只会更新`composer.lock`文件（类似于`Cargo.lock`，存放已经解析完毕的，已经决定好的依赖及其版本）和`composer.json`文件（类似`Cargo.toml`，存放项目的依赖），而不会下载需要的文件。然后把`composer.lock`文件和`composer.json`文件上传到服务器，执行`composer install`，会方便很多。相当于把依赖解析的步骤放在本地完成了。

# 安装Flarum

## 安装本体

在`/var/www/flarum`文件夹下，执行`composer create-project flarum/flarum:^1.8.0 .`安装Flarum本体。

需要注意的是，安装完本体后，最好再对`/var/www/flarum`文件夹执行上文所述的`chown`和`chmod`操作，因为Composer是在当前用户凭证下拉出来的文件，权限可能不是期望的，会导致Flarum在初始化页面报告权限错误。

## Nginx配置

安装完Flarum之后就可以配置Nginx了，这样就可以访问到网页了。编辑`/etc/nginx/conf.d/flarum.conf`文件内容如下：

```conf
server {
    listen       80;
    server_name  <你的域名>;
    
    # 这个是一定要的，不然就没法去掉index.php的尾部，而且网站还会出错。
    index index.php;
    root /var/www/flarum/public;
    
    error_log /var/log/nginx/flarum.error;
    access_log /var/log/nginx/flarum.access;

    include /var/www/flarum/.nginx.conf;

    # PHP代理配置
    location ~ \.php$ {
        fastcgi_split_path_info ^(.+.php)(/.+)$;
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

保存并重启Nginx后，输入`http://<你的域名>`应该就可以看到Flarum的初始化页面了。抓紧时间进行初始化，防止其他人恶意访问。初始化页面主要是填写数据库连接内容，例如数据库名，数据库用户名，数据库用户密码，以及数据库表前缀。这个前缀是Flarum在数据库里建表时，给每个表加的一个前缀，我这里填的是`fl_`，然后Flarum初始化的时候就会把每个表都加一个`fl_`前缀。不过如果用户名或者密码输入错了也不要过于担心，可以在`/var/www/flarum/config.php`里再次修改的，没必要重装。

据其他人反馈，有时候Flarum花费了过多时间操作，导致超过了PHP设置的最大执行时间，最终导致初始化失败。解决方案是编译`php.ini`中的`max_execution_time`，将其设置为`max_execution_time = -1`，代表不限时，等Flarum初始化完毕后再改回原值。

我这里还遇到一个比较奇葩的情况。我是先在一台配置比较垃圾的Ubuntu 20.04 LTS上装好了一个Flarum，域名都绑定，HTTPS都配置好了。结果发现内存太少跑不动Composer，于是被迫换了一台新机器，新机器就是一开始提到的Ubuntu 22.04 LTS。换完之后Flarum也照样装好了，然后域名也切换到了这台新机器的IP上，结果进入后台面板，无论点哪个选项进行配置，都会提示我配置失败请刷新页面再试。最终通过更改`config.php`中的调试模式（记得分析完错误后把调试模式关了，不然不安全），输出了具体的报错内容，才知道是因为什么原因。解决方案很简单，就是清空浏览器数据就好了。原因是我在那台Ubuntu 20.04 LTS上配置的Flarum里没有退出登录，导致浏览器把那个已经死掉的Flarum的登录信息应用到现在这个新的Flarum中了，因为两边域名是一样的。然而新旧数据肯定不通用啊，于是就导致了这个错误。所以如果你也遇到了这个奇葩Bug，可以这么解决。

## 额外插件

在Flarum安装的根目录执行`composer require flarum-lang/chinese-simplified`安装中文语言包，这是最重要的插件。安装完成后可以在插件面板里打开，并将中文锁定为默认语言。

确认语言插件工作正常后，接下来就是使用`composer require <插件名>`安装以下常用插件：

* `fof/upload:"*"`：允许用户上传文件。
* `fof/nightmode:"*"`：网页夜间模式。
* `fof/default-user-preferences:"*"`：用户默认设置（比如默认把邮件发送关掉。
* `fof/frontpage`：加精。
* `fof/doorman:"*"`：邀请码机制。
* `darkle/fancybox`：点击图片放大查看。
* `fof/profile-image-crop:"*"`：上传头像时允许裁剪。
* `fof/polls:"*"`：投票。
* `fof/filter:"*"`：违禁词屏蔽。
* `fof/linguist`：多语言翻译插件。有些时候默认的翻译并不总是令人满意，或者某些地方没有被翻译，可以通过这个插件修改。
* `ziiven/flarum-post-number`：楼层号码显示
* `pipecraft/flarum-ext-id-slug`：以ID显示帖子链接，而不是文字。
* `league/flysystem-aws-s3-v3:"1.*"`：以AWS S3协议存储用户上传的文件。
* `the-turk/flarum-stickiest:"^3.0.0"`：超级置顶，解决Flarum默认置顶看完之后会不在第一位的设计问题。
* `clarkwinkelmann/flarum-ext-emojionearea`：表情选项器。
* `wvbdev/tieba-stickers`：贴吧表情。
* `meilisearch/meilisearch-php:"0.23.*"`：Meilisearch插件的依赖
* `clarkwinkelmann/flarum-ext-scout`：Meilisearch插件
* `antoinefr/flarum-ext-money`：站内货币功能
* `ziiven/flarum-daily-check-in`：每日签到

# 安装Certbot

接下来就是配置HTTPS了，小站肯定是直接用Let's Encrypt的服务了。于是就选择了Certbot。本质上来说，如果你使用Cloudflare来代理你的网站，你的网站其实不需要申请HTTPS证书，Cloudflare会自动帮你加上HTTPS（当然，是Cloudflare帮你包了一层）。然而这种方式下，Cloudflare和你的服务器之间的通信仍然是HTTP，可窃取和替换的，所以我还是坚持为服务器加上HTTPS。

## 安装

首先是确保服务器上已经安装了Certbot和Nginx。如果没有安装，可以使用以下命令进行安装：`sudo apt install certbot python3-certbot-nginx`。其中`certbot`是本体，`python3-certbot-nginx`应该是配合修改Nginx配置文件的库。

Let's Encrypt的Certbot是一个挑战式Bot，目的在于确认你拥有这个域名。通常而言，Certbot自启一个Web服务器，然后部署一个随机文件（只有Let's Encrypt知道这个文件的内容），然后Let's Encrypt再到你的域名下试图访问这个文件，访问到了就确认你拥有这个域名，就签发证书。

## 获取证书

然后就是使用Certbot获取SSL证书并自动配置Nginx：`sudo certbot --nginx -d <你的域名>`。在运行上述命令时，Certbot可能会提示您选择一个或多个域名，并询问是否希望将所有流量重定向到HTTPS。一般选择重新定向，这样Certbot会自动修改你的Nginx配置文件。尽管我不怎么信任Certbot会正确修改我的Nginx配置（Nginx配置千千万万，它是怎么找到我网站配置的？），但还是偷了个懒让Certbot自动帮我搞定Nginx配置了，之后查看了一下Certbot修改后的配置文件确认无误。

Certbot安装证书后，就可以通过访问`https://<你的域名>`来验证网站是否已启用HTTPS。以及访问`http://<你的域名>`看是否会重定向到HTTPS网站上。

使用Certbot不需要关闭Nginx。如果你用完Certbot后，使用`sudo systemctl status nginx`查看状态发现状态为停止，且重启失败，那么可能是Certbot暴力地直接运行了Nginx，而非通过systemd来启动Nginx。此时请`sudo killall nginx`干掉所有Nginx进程，然后再使用systemctl重启Nginx。如果还是失败，请`sudo lsof -i:80`或`sudo lsof -i:443`检查端口被哪个程序占用了。

## 自动续订证书

Certbot会设置一个定时任务，定期检查您的证书是否需要更新。您可以通过以下命令查看Certbot的定时任务：`sudo systemctl status certbot.timer`。如果需要手动更新证书，可以使用以下命令：`sudo certbot renew --dry-run`

## 更改Flarum模式

如果Flarum在切换HTTPS后打不开（一般来说都是打不开），转到`/var/www/flarum/config.php`把里面`url`的`http`改为`https`。

# 安装Meilisearch

Flarum对于中文搜索的支持非常垃圾，应该是完全没有分词导致的，你必须要输入全名才能搜到对应帖子，非常的垃圾。好在Flarum社区有几种解决方案。其中一种方案是魔改MySQL数据库的`ngram_token_size`来暴力分词，但过于Hack；也有用Elasticsearch这种正统搜索方案的，但是资源消耗太多（Java写的，你说呢？）。原本一番调研下来后决定使用Sonic的，结果发现Sonic从2024年开始就开摆了，遂转而选择Meilisearch，后者仍在持续跟新，且二者均为Rust编写，具有极大的部署便利性。

该部分内容基于两个帖子来进行部署的（如果无法访问了就去Internet Archive查看网页备份）：

* https://discuss.flarum.org.cn/d/3994
* https://forum.gitzaai.com/d/79-%E7%94%A8-meilisearch-%E6%9B%BF%E4%BB%A3-flarum-%E7%9A%84%E4%B8%AD%E6%96%87%E6%90%9C%E7%B4%A2%E5%8A%9F%E8%83%BD

## 下载和安装

首先就是下载Meilisearch的最新版，我这里采用的时我安装时的最新版1.22.1。我发现他的Github Release页面中不仅提供了Linux可执行程序，还提供了打包好的Debian包（`.deb`文件），于是我就下载了Debian包形式的文件，因为我的服务器是Ubuntu的，而且我希望采用Debian包后，它可以帮我自动配置好systemd（虽然后面发现没帮我配置就是了）。

用wget下载完成后，直接使用`sudo dpkg -i meilisearch.deb`安装这个包，安装很顺利，没有任何错误。

## 配置Systemd

安装好之后发现并没有给我配置好systemd，于是乎被迫手动配置。官方文档中是使用`cat << EOF > /etc/systemd/system/meilisearch.service`加上文件内容的方式写入的，但是我没有权限，即使用了sudo也是。于是我就直接暴力`sudo nano /etc/systemd/system/meilisearch.service`，然后把内容粘贴进去了。不过这个预设配置文件不能直接用，我做了一点小修改，写在下面，你可以直接粘下面这段进去，就不需要从官方那再拿一遍然后自己改了。

```
[Unit]
Description=Meilisearch
After=systemd-user-sessions.service

[Service]
Type=simple
WorkingDirectory=/var/lib/meilisearch
ExecStart=/usr/bin/meilisearch --no-analytics --config-file-path /etc/meilisearch.toml
User=flarum
Group=flarum
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

主要改动的部分是以下几点：

* `User`和`Group`从`meilisearch`改为了我自己的用户`flarum`，因为这俩用户并不存在，后文在改文件夹权限的时候会提示无效用户，索性改成自己得了。
* `--no-analytics`选项用于关闭Meilisearch的匿名数据收集。
* Meilisearch可执行路径改为了`/usr/bin/meilisearch`，因为在我服务器上就是这个位置，可以用`whereis meilisearch`来确定具体位置在哪。
* `WorkingDirectory`没改，但是很重要。Meilisearch的数据都会放在这里（如果不改配置文件的情况下），这个目录我们一会再新建。

## 工作目录

转到`/var/lib`，使用`sudo mkdir meilisearch`新建文件夹。然后立即使用`sudo chown -R flarum:flarum /var/lib/meilisearch`将文件夹所有者转给自己，因为默认所有者是root。如果你需要用其他用户来运行Meilisearch，就转给运行的用户，然后把自己加到那个用户组里，不然Meilisearch会缺权限。

## 配置文件

首先根据官网上的文档，执行`curl https://raw.githubusercontent.com/meilisearch/meilisearch/latest/config.toml > /etc/meilisearch.toml`（权限不足就先输出到别的地方然后`sudo mv`进去），把预设配置文件下载下来。然后使用`sudo nano /etc/meilisearch.toml`更改它，主要注重这些项目：

* `env`：一定要改为`production`
* `http_addr`：除非端口冲突，不然一般不需要改。
* `master_key`：Meilisearch的主密钥，一定要设置。你可以**在工作目录下**（不然你就等着一大堆垃圾文件输出到你当前目录吧）直接执行`meilisearch`，它会给你在输出中给你自动生成一个安全的主密钥，可以直接拿来用。
* `no_analytics`：设置为`true`好像也能禁用数据收集呢（我写这篇文章的时候才发现，那我之前改命令行干嘛）？

## 启动和获取Flarum用密钥

执行`sudo systemctl enable meilisearch`设置开机启动，执行`sudo systemctl start meilisearch`启动Meilisearch。

然后按照教程，执行如下命令（把`MASTER_KEY`换成上一步中的主密钥）：

```sh
curl \
  -X GET 'http://localhost:7700/keys' \
  -H 'Authorization: Bearer MASTER_KEY'
```

然后就能得到一个JSON输出，简单拿出来格式化一下，找到名为`Default Admin API Key`里面的`key`的对应值，就是一会要填入的密钥。

## 设置Flarum

配合Meilisearch的相关插件在上一步已经安装完毕了，所以可以直接进入Flarum后台，启用Scout Search扩展。Driver选择Meilisearch；Index name prefix (optional)随便填，我填了`blc`；Meilisearch Host填写主机端口；Meilisearch Key填写为上一步获取的密钥。然后应用就可以了。

填写主机端口Meilisearch Host的时候需要注意，许多教程里让你保持默认（也就是连接`127.0.0.1:7700`），或者是让你直接填写这个地址和端口。但在我这里，这么填写一开始可以，但是不知道为什么，在某次维护后发生了在论坛里搜索和AT用户的时候持续报错的情况，分析报错日志的时候出现了很多Scout Search插件以及Meilisearch的字样，错误中包含`Invalid URL: scheme is missing in "//127.0.0.1:7700/indexes/blcusers/search". Did you forget to add "http(s)://"?`等字样。于是就把这个字段填写为了`http://127.0.0.1:7700`，这样就不会出现问题了，我建议你也那么填。

最后转到服务器SSH中，在Flarum论坛根目录下执行`php flarum scout:import-all`，把当前现有的数据导入到Meilisearch中。

# 存储服务

论坛的上传服务有3种模式，一种是存储在本地，一种是Imgur图床，最后一种是接入AWS S3存储桶服务，选择后两者就不需要在本地消耗过多存储空间了。Imgur图床是肯定不能接受的，因为需要国内访问，所以之剩下AWS S3存储桶选项。原计划为了防止外部流量打击，导致一夜之间AWS S3的流量被用完，转而决定使用兼容AWS S3协议的Cloudflare R2存储桶服务，但是没有境外支付手段遂作罢。转而决定在本地搭建Minio来实现存储服务，然而Minio于五月份暴雷，删除了整个Web管理功能。最终在各种妥协和思量下，决定还是直接把数据存储在服务器本地算了（绕了一圈又回来了）。

存储在本地发配置就很简单了，就直接打开FOF Upload插件，然后配置就好了。分别设置如下项目，以允许图片，压缩包和Ballance特有的NMO地图上传：

* `^image\/(jpeg|png|gif|webp|avif|bmp|tiff|svg\+xml)$`：允许图片。设置为本地；完整图片预览模板。
* `^application\/octet-stream$`：允许Ballance地图。设置为本地；默认文件下载模板。
* `^application\/(x-(7z|rar|zip)-compressed|zip|x-(bzip2|gzip|tar)|pdf)$`：允许压缩包。设置为本地；默认文件下载模板。

同时，为了服务器承载力度考虑，设置最大上传数值为2MiB。同时根据下方的提示，修改了`/etc/nginx/conf.d/flarum.conf`，在server块里设置了`client_max_body_size 2m;`的限制（我PHP的限制是比2MiB大的，所以不需要改）。
