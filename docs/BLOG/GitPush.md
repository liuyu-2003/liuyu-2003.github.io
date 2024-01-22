# 解决git push报错问题
报错：Failed to connect to github.com port 443 after ***** ms: Couldn‘t connect to server

原因：网络问题,terminal->ping github.com不通->DNS被污染了

解决：改dns为1.1.1.1


PS: 

```nslookup github.com 1.1.1.1```返回的ip地址应该和之前返回的ip不同才对，
谷歌的8.8.8.8就被污染了，返回的和国内dns服务器一样。