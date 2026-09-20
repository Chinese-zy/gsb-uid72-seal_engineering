docker compose up --build

页面从 http://127.0.0.1:8762 进。对外入口是 / 、/api/seals 、/health ，不要换。

本机另开一个口看页面：python app.py ，它听 8761。
启动会先跑 migrate.sql 建表，库没就绪 /health 返回 503，编排探活打到真口上。
核对用 python check.py ：它打容器对外的 8762（可用 CHECK_TARGET 改），
先灌 data/seed.json 的样例，再拿读出的数和 data/expect.json 对，
不一致或够不到服务都退出非零。核对只读数据文件，不回写。
核对以全新部署为准，重复灌样例会判不一致；重置用 docker compose up --build --force-recreate 。
