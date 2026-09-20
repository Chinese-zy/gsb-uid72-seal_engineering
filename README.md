docker compose up --build

页面从 http://127.0.0.1:8762 进。对外入口是 / 、/api/seals 、/health ，不要换。

本机另开一个口看页面：python app.py ，它听 8761。
核对用 python check.py 。
库表在 migrate.sql ，说明在这里，启动不会自己跑。
