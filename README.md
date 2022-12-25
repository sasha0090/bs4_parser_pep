# Парсер python.org ( ⓛ ω ⓛ )
 
Парсер доки питона с несколькими режимами работы. 

## Режимы работы

### whats-new
Собирает ссылки на статьи о нововведениях и достанете из них справочную информацию.

### latest-versions
Собирает информацию о версиях Python — номера, статус и ссылки на документацию.

### download
Скачивает архив с документацией Python на ваш локальный диск. В директорию ./src/downloads/

### pep
Посчитывает количество PEP в каждом статусе и общее количество PEP; данные о статусе документа беруться со страницы каждого PEP, а не из общей таблицы

### Дополнительные необязательные аргументы
***-h, --help*** — выводит вспомогательную информацию о работе парсера

***-c, --clear-cache*** — Удаляет кэш пред стартом

***-o {pretty,file}, --output {pretty,file}***  —  Дополнительные способы вывода данных. Параметр pretty выводит данные в терминале в оформленной таблице, параметр file сохраняет данные в csv файл.


## Запуск проекта
◾  Клонируйте репозиторий и перейти в него

◾  Установите и активируйте виртуальное окружение

◾  Установите зависимости из файла requirements.txt :
```
    pip install -r requirements.txt
```
◾  Через командную строку в директории src запустите скрипт:

    python main.py MOD -ARGS
Где MOD —   Название режима работы, а -ARGS  —  Перечисление необязательных аргументов

## Логирование
В проекте собираются логи с уровня INFO и сохраняются в директорию ./src/logs


## Автор
[Александр Телепин](https://github.com/sasha0090)
