# ✨Dingtalk-playback-download
> 钉钉直播回放下载脚本
> 编码:UTF-8
#### 本脚本可用于下载钉钉禁止下载的直播回放

## 🎇使用教程
#### https://blog.muna.uk/archives/dingtalk-downloads.html

***

## 更新日志
### 2025/01/07 版本更新
- **支持通过浏览器控制台抓包而无需降级钉钉或安装抓包工具（思路来源：https://www.bilibili.com/video/BV1EC41147fY/）**
- 增加了 Windows 和 Linux 系统的 FFmpeg 安装脚本（源 https://github.com/BtbN/FFmpeg-Builds）
- 改进了执行 curl 命令时潜在的安全性问题
- 增加了 FFmpeg 安装状态检测，支持 ffmpeg 不配置环境变量同目录内调用
- 修复了出现直播暂停时导致片段缺失的问题
- 新增 FFmpeg 安装指引
- 新增了 M3U8 来源：浏览器调试控制台
### 2023/07/20 版本更新
- 移除了对 wget 的依赖
- 增加了对手机端抓包下载的适配
### 2022/07/02 版本更新
- 适配linux系统
- 自动检测下载错误的ts片段并重新下载
- 优化错误日至的写出
- 优化逻辑

***

## 🎇支持列表
- 1.群直播回放
- 2.在线课堂
