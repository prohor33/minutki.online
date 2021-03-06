<img width="960" alt="Презентация2" src="https://user-images.githubusercontent.com/5472900/130338081-fb0639c7-7e2f-4cbc-8bb3-2940b2e5bc88.png">

Сделано за 1 сутки командой SberSquad в рамках хакатона LeadersOfDigital.

### Install extraction dependencies

```bash
$ pip install natasha==0.9.0 
$ pip install yargy==0.10.0 
$ pip install ipymarkup
$ pip install rutermextract 
```

## Сервис minutki.online
Сервис требует установки библитек с помощью следующей команды: 

```pip install streamlit numpy docx python-docx``` .  

Запуск сервиса выполняется следующим образом: 

```STREAMLIT_SERVER_PORT=80 streamlit run app.py --server.maxUploadSize=1028``` .

## Техническое описание

* Сервис позволяет загрузить файл в формате mp4 до 300mb
* После загрузки файла, отображается окно воспроизведения контента
* Алгоритмы AI начинают анализ файла сразу после загрузки
* Видеофайл преобразуется в нужный формат с помощью ffmpeg
* Видеофайл преобразуется в текст моделью speech2text (Vosk)
* На тексте отрабатывает глубинная нейронная сеть восстановления пунктуации на основе BERT
* Из текста с пунктуацией извлекается все термины и ключевые слова
* Извлекаются поручения, ответственные, сроки, заголовок, инициаторы встреч, участники и тема встречи
* Результат возвращается в виде json ниже

Формат ответа API:
```
{
    "cards": [
        {
            "assignment": {
                "text": "Построить модель извлечения текстов в соответствии с заданными тегами",
                "start": 1126,
                "end": 1197
            },
            "responsible": {
                "text": "Семён Петров",
                "start": 1210,
                "end": 1225
            },
            "date": {
                "text": "До пятнадцатого июля, две тысячи двадцать второго года",
                "start": 1229,
                "end": 1286
            }
        }
    ],
    "header": {
        "theme": "Обсуждение реализации проекта по распознаванию речи и извлечение из речи и извлечения из аудио дорожки, собрание или встречи, извлечение поручений, задач, каких-то примеров и прочего.",
        "meeting_initiator": "Сидоров Александр",
        "participants": "Сорокина Семён; Сидоров Александр"
    },
    "text": "у вас да добрый день, тема встречи обсуждение реализации проекта по распознаванию речи и извлечение из речи и извлечения из аудио дорожки, собрание или встречи, извлечение поручений, задач, каких-то примеров и прочего время начала встречи двадцать первая августа, две тысячи, двадцать первого года инициатор встречи сидоров александр навстречу присутствует сорокина семён сидоров александр, приступаем к обсуждению да здесь мы с тобой обсуждаем какие-то вопросы очень серьёзные, на про то, как мы строим, да да и в целом погода очень хорошая, неплохо не жертвуя, холодно погулять бы мы сидим в монитора, смотрим окей, но что тогда давай, я там сейчас по итогам да начнём по итогам обсуждения постановили так задача номер один, выбор движка для распознавания речи, например, сова или воск, ответственные прохор глотки, срок до двадцать второго августа, две тысячи двадцать первого года, конец задачи, задача номер два, пост процессинг, пост обработка текстов на выходе после движка распознавания речи, ответственный иванов пётр, срок двадцать первая августа, две тысячи двадцать первого года, конец задачи, поручение номер три построить модель извлечения текстов в соответствии с заданными тегами, ответственная семён петров, срок до пятнадцатого июля, две тысячи двадцать второго года, конец поручению все большое спасибо за встречу"
}
```
