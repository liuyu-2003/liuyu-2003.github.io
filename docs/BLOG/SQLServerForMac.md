# 如何在Mac上使用SQL Server

设备：MacBook Air M1



1. 下载docker
   https://www.docker.com/

2. 获取Azure SQL Edge镜像
   https://hub.docker.com/_/microsoft-azure-sql-edge

   终端输入命令

   `docker pull mcr.microsoft.com/azure-sql-edge`

3. 终端输入命令

   ```docker run -e "ACCEPT_EULA=1" -e "MSSQL_SA_PASSWORD=SQLsqlserver1234" -e "MSSQL_PID=Developer" -e "MSSQL_USER=SA" -p 1433:1433 --name SQL -d mcr.microsoft.com/azure-sql-edge ```

   

   若提示`docker: invalid reference format: repository name must be lowercase.See 'docker run --help'.`就不要复制，手敲一份

4. 终端输入`docker ps`检查是否正在运行

5. 下载Azure Data Studio
   https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio

6. 在Azure Data Studio中连接

   连接类型：Microsoft SQL Server

   输入类型：参数

   服务器：localhost

   身份验证类型：SQL登录

   用户名：SA

   密码：SQLsqlserver1234

   数据库：默认值

   加密：强制（True）

   信任服务器证书：True

   服务器组：默认值

   名称：SQL





PS:请自行更改密码、容器名称和username