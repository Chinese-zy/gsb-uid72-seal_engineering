起页面（基础镜像按 digest 钉死；启动先跑 migrate.sql 迁移，空库再灌 data/seed.json 样例）：

docker compose up --build

页面从 http://127.0.0.1:8762 进。对外入口是 / 、/api/seals 、/health ，不要换。

本机单机开发可另跑 python app.py ，默认听 8761；核对不要打这个口。

核对打容器里起来的那个（映射到 8762），夹具只读，绝不回写：

python check.py

连不上、HTTP 状态非 200、ok 不为真或行数据与 data/expected.json 不一致时，check.py 以非零退出；可用 TARGET 环境变量覆盖地址。

库表在 migrate.sql ，容器启动时由 bootstrap.py 自动执行；data/seed.json 只在 seals 表为空时播种，迁移或播种失败启动即失败。
健康检查由 healthcheck.py 打容器内 /health ，确认口真的听上了，不再只看进程在不在。
