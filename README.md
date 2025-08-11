# 📅 ios-calendar-supplement/针对ios日历的补充

## 🧭 介绍

本项目旨在补充 iOS/macOS 系统日历中缺失的节日、纪念日信息，  
内容缺少对比基于 MIUI 系统日历的节日库（含中西方节日、节气、法定节假日）对比校验后补充完善，确保覆盖全面性。
支持导入至 Apple 日历、Outlook、Google Calendar 等标准日历客户端。

- 📌 兼容格式：`iCalendar (.ics)`
- 📆 类型覆盖：阳历节日（如愚人节、护士节）、纪念日（如七七事变）、动态节日（如父亲节、母亲节等）
- 🌍 数据来源：常用纪念日资料

---

## 🛠 自建订阅

如你希望自建 `.ics` 发布服务以供他人订阅

这里提供一下nginx配置文件：
```
# HTTP → HTTPS 重定向
server {
    listen 80;
    server_name calendar.example.com;
    return 301 https://$host$request_uri;
}

# HTTPS 服务
server {
    listen 443 ssl;
    server_name calendar.example.com;

    ssl_certificate     /path/to/protected/fullchain.pem;
    ssl_certificate_key /path/to/protected/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    root /var/www/calendar/;
    index index.html;

    # .ics日历文件处理
    location ~* \.ics$ {
        default_type text/calendar;
        try_files $uri =404;
    }

}

```

文件大致目录结构：
```
/
└── var/
    └── www/
        └── calendar/                    # 网站根目录
            ├── index.html               # 主页面
            └── calendar-supplement.ics  # 日历文件
```

---

## 📎 订阅地址（如不想搭建，可以使用下列链接订阅）

- 📌 订阅链接：  [点击跳转到订阅页面](https://calendar.cliboy.xyz/)

- 📋 手动添加方法（以 iPhone （ios18）为例）：
  打开日历 → 点击下方中部日历 → 左下角添加日历 → 添加订阅日历 → 填入订阅链接 → 点击订阅

- 💻 macOS / Outlook 同样支持 `.ics` 网络订阅

---

## ✅ TODO（第一阶段）

- [x] 添加母亲节、父亲节（动态节日）
- [x] 加入重要纪念日（如七七事变、九一八等）
- [x] 自动化构建和发布脚本（GitHub Actions）
- [x] 增加节气时间提示
      
至此，项目初期规划的开发任务已全面顺利完成（后续将视实际需求发展情况，会考虑是否启动新的规划阶段）

---

## ❤️ 致谢

感谢 MIUI 自带日历提供的灵感，欢迎 PR 补充其他节日内容。  
如你觉得项目有用，欢迎 Star ✨ 或分享给他人一起使用。


