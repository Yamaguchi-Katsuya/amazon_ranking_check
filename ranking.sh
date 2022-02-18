#!/bin/sh

# sh ranking.sh 実行時間 実行間隔
# e.g. sh ranking.sh 481 60(1時間ごとに8時間実行480分 + 1とすることで8時間フルで実行させる)
COMMAND="python3 main.py"
START_TIME=$(date +%s)
LIMIT_MINUTES=$(($1*60))
SLEEP_MINUTES=$(($2*60))
echo "実行時間: $1分"
echo "実行間隔: $2分"
is_end=0

while [ "$is_end" -eq 0 ];
do
  current_time=$(date +%s)
  run_time=$((current_time - START_TIME))
  if [ "$run_time" -gt "$LIMIT_MINUTES" ]; then
    is_end=1
    echo 'プログラムを終了します。'
  else
    echo "ランキングチェックします。\n"
    echo `date`
    eval "$COMMAND"
    sleep "$SLEEP_MINUTES"
  fi
done
