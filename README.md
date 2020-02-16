# 保持迅雷快鸟在线提速 -XlNetAcc Keeper
在家中的NAS，软路由，能够保持提速的Python脚本（前提你开了加速会员）

# 使用方法
* 把本项目Clone下来
* 安装必要的Python3库 `pip3 install requests-toolbelt requests`
* 把getCookies.js内的js脚本在浏览器的控制台中执行，获取到一串base64文本，保存到cookies.txt
* chmox +x ./kuainiao.sh & ./kuainiao.sh
* 完成

# 效果
<img src="./static/run.png" width = "800" align=center />
<img src="./static/result.png" width = "800" align=center />

# ISSUES
* 出现`#日期`，这样格式的消息，则视为加速成功
* 默认用户心跳包15分钟一次,1.5小时更新加速一次.
* 如果出现网络错误,那可能因为有两点，①你暴力刷API,导致服务器Banned了你，建议你冷却技能。②你的Cookie失效了，请更新Cookie，一般不可能，除非你在浏览器注销?
* 如果出现`speedup server already speed up`的提示，那么请隔日再来把，你用官方客户端也加速不了，这个是因为你路由器重新拨号导致旧的IP加速没下线，so,需要等24小时等迅雷那边自动释放?
* 可以用PM2,service,systemctl去让随系统自启动
* 项目本质只是封装网页版的快鸟加速API
