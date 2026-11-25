#!/bin/sh
# 同步学マス剧情库：在一次性容器 story-sync 里下载三份来源、转换成 CSV（tools/story_sync/），
# 再在后端容器里运行 `eidolon story import-csv`。照 Eidolon-SC 的 deploy/story-sync.sh 写：
# 可以手动运行，也可以每周由 cron 或 Windows 的任务计划程序运行，安装方法见 README 的「剧情库」。
# 需要 docker compose；有 flock（util-linux）时加锁，防止两次同步重叠，没有时（Windows 的 Git Bash）不加锁。
#
# 输出追加到本目录的 logs/story-sync.log（可用 GAKUMAS_SYNC_LOG 改到别处）。
#
# 退出码（含义也写在每次同步的最后一行日志里）：
#   0  完全成功（三份来源都没更新时也是 0）
#   1  导入出错：缺少向量化服务的 key，或向量化中断（重新运行即可继续）
#   2  下载或转换出错，这次导入的是上次转换的那一份
#   3  下载或转换出错，而且没有可导入的剧情，这次没有导入
#   4  后端容器没有运行，或无法运行 docker compose
#   5  上一次同步还没结束，这次没有运行

set -u

root=$(cd "$(dirname "$0")" && pwd)
cd "$root" || exit 4
PATH=/usr/local/bin:/usr/bin:/bin:$PATH # cron 的 PATH 很短
# Git Bash 会把 /corpus/csv 这样的参数改写成 Windows 路径，传给容器就不对了
export MSYS_NO_PATHCONV=1
log=${GAKUMAS_SYNC_LOG:-$root/logs/story-sync.log}
mkdir -p "$root/logs" "$(dirname "$log")"
exec >>"$log" 2>&1

say() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

finish() {
  case $1 in
    0) meaning="完全成功" ;;
    1) meaning="导入出错：缺少向量化服务的 key，或向量化中断（重新运行即可继续）" ;;
    2) meaning="下载或转换出错：导入的是上次转换的那一份，下次同步再试" ;;
    3) meaning="下载或转换出错，而且没有可导入的剧情" ;;
    4) meaning="后端容器没有运行，或无法运行 docker compose" ;;
    5) meaning="上一次同步还没结束，这次没有运行" ;;
    *) meaning="未知" ;;
  esac
  say "==== 结束：退出码 $1（$meaning）"
  echo
  exit "$1"
}

say "==== 开始同步学マス剧情库（$root）"

if command -v flock >/dev/null; then
  exec 9>"$root/logs/story-sync.lock"
  if ! flock -n 9; then
    finish 5
  fi
fi

# 出错时（例如没有 docker 的权限）docker 自己的错误信息也写进日志
if [ -z "$(docker compose ps --status running --quiet backend)" ]; then
  say "后端容器没有运行（docker compose ps 里找不到运行中的 backend），先 docker compose up -d"
  finish 4
fi

say "下载和转换（docker compose run story-sync）"
docker compose run --rm --no-deps -T story-sync
fetch_code=$?
case $fetch_code in
  0 | 2) ;;
  3) finish 3 ;;
  *)
    say "docker compose run 以 $fetch_code 结束"
    finish 4
    ;;
esac

say "导入（docker compose exec backend eidolon story import-csv /corpus/csv）"
# -T：cron 里没有终端；PYTHONUNBUFFERED：进度日志和结果按实际顺序写进日志
docker compose exec -T -e PYTHONUNBUFFERED=1 backend eidolon story import-csv /corpus/csv
import_code=$?
case $import_code in
  0) ;;
  1) finish 1 ;;
  *)
    say "docker compose exec 以 $import_code 结束"
    finish 4
    ;;
esac
finish "$fetch_code"
