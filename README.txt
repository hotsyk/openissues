Openissues - is a fork of the opentodo task management system designed to create simple open issue management system

Main differences from the opentodo:
 * Localizations
 * Thread comments
 * Estimates for the tasks
 * Iterations and planning of the releases
 * Task types
 * Markdown instead of the cuted html
 * Task workflow - possibility to define user as the project manager and all tasks will be returned to him instead of the task author after the finishing
 * Scrum charts
 * Actual time for the task tracking 
 * Integration with the kava (@42cc project)


       opentodo - Система управления задачами на Django Framework


Новое в версии 0.91 (31 марта 2009)
====================================

+ Теперь для перехода к задаче из списка достаточно кликнуть по ряду таблицы (не обязательно по названию задачи)
+ Ссылки для автоматической вставки html-тегов в textarea (описание задач и проектов, комментарии)

Также переработан парсинг html, исправлены ошибки. Библиотека BeautifulSoap больше не используется.

Исправлен баг - при ответе на комментарий его автору не приходило уведомление по почте.

Теперь в настройках MEDIA_URL не имеет значения, есть слэш в конце или нет, все корректно работает в любом случае.


Новое в версии 0.9 (22 марта 2009)
====================================

+ Разграничение доступа пользователей к проектам
+ Фильтр - по автору, исполнителю, статусу, названию задачи
+ Ответ на комментарии - при ответе автор комментария получает уведомление по e-mail
+ Разметка текста - в описании проектов, задач и тексте комментариев разрешены некоторые html-теги


Ссылки
=========

* Описание, инструкция по установке, релизы: http://code.google.com/p/opentodo/

* Домашняя страница проекта: http://opentodo.ru/

* Онлайн демо: http://demo.opentodo.ru/

* Исходный код на GitHub: http://github.com/mgrigoriev/opentodo/


Лицензия: GNU General Public License v3

Автор: Михаил Григорьев <mgrigoriev@gmail.com>

