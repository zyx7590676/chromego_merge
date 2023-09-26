## 简介

**注意：clash内核无法使用这些节点，你要用clashmeta**
<details>
  <summary>点击展开/折叠</summary>

提取并聚合chromego中的节点，并套上warp，让你感受白嫖加隐私的快乐体验，当然普通clash无法使用这些节点，我也不喜欢被别人抓取节点到免费节点池里
完全是面向chromego写的，所以很多地方都写死了。套上warp的原因是方便看一些chromego不让看的网址，比如p开头的x开头的
chromego如果更新我会及时修改代码保证代码可用，如果更新不及时请提issues

</details>

## 为什么要套上warp
<details>
  <summary>点击展开/折叠</summary>
首先chromego屏蔽了很多网站，包括你喜欢的p开头的网站，套上warp可以突破这一层限制。

第二我并不喜欢使用机场等服务，原因就是机场主或者节点主完全知道你访问的网站，虽然有一层https加密，但是他们还是可以知道你访问的域名已经你连接的时间，套上warp之后，他们只能看到一串加密流量。

第三，我为什么要提取节点出来，不仅仅是因为方便管理，可以在一个配置文件中切换不同的节点。而且是因为我并不喜欢使用他们所提供的客户端，虽然chromego所提供的客户端并没有什么问题，但是我还是喜欢自己常用的客户端。

</details>

## 如何修改为自己的warp节点
可以用warp+机器人和提取wg节点替换掉配置文件中的wg信息
[warp提取wireguard网站](https://replit.com/@misaka-blog/wgcf-profile-generator)
[warp+机器人](https://t.me/generatewarpplusbot)

## 订阅链接分享(无需翻墙版-托管自netlify）
### 不套warp版本（clashmeta-全平台通用-节点最全）
```
https://mareep.netlify.app/sub/merged_proxies.yaml
```
### 套warp版本（clashmeta-全平台通用-节点最全)
```
https://mareep.netlify.app/sub/merged_warp_proxies.yaml
```
### shadowrocket订阅链接-节点较全
```
https://mareep.netlify.app/sub/shadowrocket_base64.txt
```
### nekoray订阅链接-节点较不全
```
https://mareep.netlify.app/sub/neko_base64.txt
```
## 订阅链接分享（需要翻墙版-托管自github）
<details>
  <summary>点击展开/折叠</summary>
  
### 不套warp版本（clashmeta
```
https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/merged_proxies.yaml
```
### 套warp版本（clashmeta
```
https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/merged_warp_proxies.yaml
```
### shadowrocket订阅链接-ios客户端
```
https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/shadowrocket_base64.txt
```
### nekoray订阅链接-Windows客户端
```
https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/neko_base64.txt
```
</details>


## 致谢
[Alvin9999](https://github.com/Alvin9999/pac2/tree/master)

## 其他订阅
chromego中的clash节点(量很大，可用性未知)
```
https://fastly.jsdelivr.net/gh/jsvpn/jsproxy@dev/baitai/20200329/1302338.md
```
ermaozi

clash订阅链接：https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml

v2ray订阅链接：https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt


