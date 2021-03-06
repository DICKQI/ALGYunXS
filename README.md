# ALGYun v1.1

## 简介
ALGYun 是基于python语言开发，web前端使用react开发，小程序端使用Taro框架开发的集学生二手交易，学生互帮互助信息，学生兼职信息发布等于一体的多功能平台

## 技术选型
    环境：ubuntu 16.04 + nginx 1.10.3 + uwsgi 2.0.17.1
    
    后端：python3.6（服务器运行环境） + django 2.1.2 + mysql + redis
    
    web前端：React
    
    小程序端：NervJS/taro
    
    静态文件存放：阿里云OSS
    
    计划开发：Android端，IOS端

## 分支说明
#### master分支：在服务器稳定运行的版本
#### dev分支：开发中分支，大体稳定运行的版本，但仍存在不确定的Bug
#### 其他分支：为各个开发者自己使用的分支

## 其他说明

web前端代码链接为:https://github.com/zhcxk1998/AlgYun-front-end

taro端代码链接为:https://github.com/zhcxk1998/ALGYun-Taro


# 项目功能介绍
### 基础介绍
### 主账户模块
    1.基础信息
        （1）邮箱
        （2）密码
        （3）昵称
        （4）年龄
        （5）头像
        （6）学号，真实姓名
    2.以邮箱（包括邮箱认证）作为账户唯一标识（由于手机号认证需要购买验证码服务，所以暂时弃用）
    3.注册使用哈希算法对用户输入的密码进行加密，注册后会自动生成9位数ID
    4.对外显示用户以用户名（nickname）
    5.用户可以使用ID和邮箱登录
    6.用户身份（权限）功能
        （1）总管理员（全站最高权限）
        （2）market,helps,ptj模块管理员
        （3）普通用户（由邮箱是否已认证分为两种）
        （4）黑名单用户（登录后限制一切功能，只能联系总管理员解锁）
    7.教务验证功能
        （1）通过正方教务系统（es）的接口来验证，并且更新账户的学号和真实姓名
        （2）被封禁的学号将永远无法作为注册此网站
    8.信用分功能（尚未完善）
    9.密码重置、找回功能（由邮箱验证身份）
    10.消息通知功能集成
        （1）订单提醒
        （2）评论提醒
    11.可以查看用户的评价（二手商品）
    12.收藏功能（尚未完善）
    13.关注用户功能
    14.用户浏览记录功能
    15.第三方登录功能，第三方账号绑定（开发中）
        （1）支持微信登录（未开发）
        （2）支持微博登录（未开发）
### 二手市场模块
    1.商品发布，修改，删除等基本功能
    2.商品分类（由管理员管理）
    3.商品留言
    4.商品留言点赞（会防止重复点赞）
    5.商品下单购买功能（面对面交易）
        （1）自己不能下单自己的商品
        （2）信用分低于480分的同学无法下单
        （3）下单前购买者需要输入收货地址
        （4）订单成功创建之后，会生成以"时间+id"为订单号的订单
        （5）订单成功创建后，商品会显示已售出，并且系统发出通知（站内通知，邮件）告知商品所有者
        （6）订单创建后，会处于"未确认"状态，购买者可以在下单的时候指定最迟确认时间（60分钟），此时订单可以被购买者或者商品所有人取消
        （7）成功确认订单后，订单会生成最迟确认收货时间，为订单确认起的15天（1296000秒），到时系统会自动确认收货
        （8）购买者可以在自动确认收货时间前确认收货，完成订单
        （9）购买过程中保证买家权利
    6.商品退货功能（开发中）
        （1）需要订单"未确认收货"情况下才能退货
        （2）退货过程中保证卖家权利
    7.订单（互相）评论功能（开发中）
### 互助信息模块
    1.文章发布、修改、删除等基本功能
    2.文章标签功能
        （1）普通用户在新建文章的时候可以创建新标签或者选择旧标签
        （2）标签列表会显示热度前十的列表，点击对应的列表会显示对应的文章
    3.文章附图（一张）
    4.文章评论功能
    5.文章评论点赞
    6.文章点赞功能
    7.文章分类（由管理员管理）
### 日志与记录模块
    1.登录日志
        （1）记录账户登录的IP
        （2）记录账户登录的时间和登录端（web或小程序）
    2.商品浏览记录
    3.互助文章浏览记录
    4.IP访问记录
        （1）通过djanog中间件记录IP的访问时间，IP的访问次数
        （2）当同一个IP在5分钟内访问接口的次数高于300次，将会自动锁定IP，此IP将在第二天0点之前无法访问网站的所有接口
    5.黑名单功能，黑名单IP将无法访问所有接口，解锁需要联系网站总管理员
### 兼职信息模块
    1.兼职信息的发布、修改等基本功能（需要通过认证的用户才能发布信息）
    2.其余功能开发中
### 公告与反馈模块
    1.公告新建（由总管理员操作）
    2.首页显示公告
    3.意见反馈
### 自动执行模块
    1.原理
        （1）通过apps模块，编程好不对前端开放的接口，使用django对数据库进行操作
        （2）写好python脚本，使用requests库，对接口进行访问
        （3）使用linux的crontab进行定时以上写好的python脚本
    2.目前写好的自动脚本
        （1）每5分钟自动清零无锁的ip的"5分钟访问频数"
        （2）每1分钟查看是否有自动确认的订单，或者需要取消的订单
        （3）每天0点解锁锁定的ip
    3.未来需要实现的自动化功能
        （1）自动计算信用分
        （2）。。。。。。
### 搜索引擎模块（开发中）
    这是一个专门为ALG智慧校园设计的搜索引擎
    技术选型有Whoosh引擎, django-haystack框架, jieba组件
    haystack是django的一个开源框架，支持Whoosh等多种强大的搜索引擎
    搜索引擎使用Whoosh，这是一个由纯Python实现的全文搜索引擎，没有二进制文件等，比较小巧，配置比较简单，当然性能自然略低。
    但是Whoosh自带的是英文分词的支持，对中文分词不够友好，所以我们使用jieba作为中文分词的组件
### 有闲--顺风帮模块（开发中）
    有闲是一个同学们顺路帮助（代取，代办）的平台。同学们可以通过在这里发单，接单，让生活变得更加便捷，同时可以让同学们赚取少许外快。
    我们旨在让同学们的生活变得更加的便利，充分利用起每一滴时间，将时间变得更有价值。
    1.每一位通过学生认证的同学，并且信用分在510分以上，都可以在有闲发单
    2.每一位通过学生认证的同学，并且信用分在510分以上，都可以去有闲接单
    4.有闲的主要功能，就类似于滴滴顺风车。当需要购买一些外卖无法买到的食物、需要去比较远的地方办事情取东西等等可以托人代办的事情，都可以在有闲上发单，当有同学顺路愿意帮助的时候，可以接单，同时获取一定的报酬
    5.有闲内有与ALG智慧校园主账户关联的副账户，用户可以设置本人常用路线，如宿舍—教学楼，设置空闲的时间，系统会根据设置的信息，自动推荐最优最合适的单子给用户。
    6.当然，如果用户愿意公开自己的设置信息，需要帮忙的同学看到后可以直接私聊询问是否愿意帮忙，并且愿意支付合适的价格。
    
# 关于Settings.py中的配置
### ALG_email_config.json中的数据格式为：
    "EMAIL_USE_SSL": true,
    "EMAIL_HOST": "smtp.mail.com",
    "EMAIL_PORT": 465,
    "EMAIL_HOST_USER": "your_email@mail.com",
    "EMAIL_HOST_PASSWORD": "your_email_password",
    "EMAIL_FROM": "your sign"
### database_config.json中的数据格式为：
    "ENGINE": "django.db.backends.mysql",
    "NAME": "your_database_name",
    "USER": "your_database_username",
    "PASSWORD": "your_database_password",
    "HOST": "localhost",
    "PORT": 3306
### ossConfig.json中的数据格式为：
    "ACCESS_KEY_ID": "your access key id",
    "ACCESS_KEY_SECRET": "you access key secret",
    "END_POINT": "oss-cn-shenzhen-internal.aliyuncs.com",
    "BUCKET_NAME": "your bucket name",
    "BUCKET_ACL_TYPE": "public-read-write",
    "DEFAULT_FILE_STORAGE": "aliyun_oss2_storage.backends.AliyunMediaStorage"
