# sibur_competition_code

## Как запустить
1. Собрать контейнер
  ```
  docker build --rm -f  Dockerfile -t sibur:latest .
  ```
2. Запустить контейнер. Примонтировав папку с данными `/data`
  ```
  docker run -v <dir_path>/output_data:/output_data sibur:latest
  ```
3. В примонтированной папке `/output_data` найти решения `first_track_result.csv` и `second_track_result.csv` для первой и второй задачи соответсвенно.
