# AlgoServer

GetCookie("логин", пароль)
- базовая команда получает куки для дальнейших действий

AlgoServer(куки аккаунта, айди проекта) 
- вторая базовая команда, на чем происходит взаимодействие с любым проектом

Что бы инициализировать работу над проектом надо написать простые команды:
accCookie = GetCookie("логин", пароль)
AlgoServer(accCookie.cookie, айди проекта)

#Или

accCookie = GetCookie("логин", пароль).cookie
AlgoServer(accCookie, айди проекта)

ОТ AlgoServer идёт команды:
acc = GetCookie("логин", пароль)
Serv = AlgoServer(acc.cookie, айди проекта)


Serv.ParseComment() #Парcит первый комментарий и возвращает Serv.Name, Serv.Message, Serv.ID
a = Serv.ParseComments(длина сообщений)# так же что и ParseComment но возвращает список

print(a)
"""
----------------
{"айди сообщение":{"айди юзера","Имя", "Сообщение"}, и тд}
"""

Serv.ParsePython() #Парсит твой пайтон проект
Serv.ChangePyProject("Название", "Код") #Вставляет изменненный код


Serv.ChangeDescProject("Название проекта","описание","preview твоего проекта, лучше ставить на auto",включить - 1; выключить - 0 ремикс)


Serv.SimpleRGet() #Простой http GET запрос



EmptyProject = Serv.ParseScratch() #Парсит твой скретч проект

Source = BuildScratch(EmptyProject) #Спокойно берет код твоего проекта что бы легче взаимодействовать

Source.DebugPrint() #Выводит в json обертке весь проект, что бы прочитать, что внутри

Lists = Source.getLists() #Получает список всех доступных листов со сцены в скретче
#Например:
#{"*34cer+wr-v":{"Пользователи",["Daniil","Sanya228"]}, "Zl/q*css":{"Пароли":["1002134","12312312"]}}
# А если
Variables = Source.getVariables()
#Получим:
#{"qpr/cw*-sf":{"Coins",5}, и тд}
#Что за рандомные символы в переменных скретча, это идентификатор, что бы получить переменную
#Также можно создавать и изменять созданные новые листы и переменные
Source.Variable("gems","gems",5)#ID, имя переменной, значение
Source.List("*34cer+wr-v", "Пользователи", ["Daniil","Sanya228","ScratchCat"])#Добавляем нового пользователя
Source.Variable("test","test","sucess")

#Если мы хотим удалить переменную в скретче или лист, используем ключевой del, например:
Source.delVariable("gems")#В данном случае надо указать ID, и он удалит полностью
Source.delList("*34cer+wr-v")

#Если мы хотим увидеть результат из Source.projectContentJSON , выводим в ChangeScratchProject():
ChangeScratchProject(Source.projectContentJSON)

#Теперь зайдите в ваш скретч проект должно заработать

Документация AlgoServer, [03.07.2025 5:44]
Это пока всё от версии AlgoServer 2.1 Beta

Документация AlgoServer, [03.07.2025 5:52]
Так же не забудьте когда скачаете AlgoServer, поставить рядом с вашим скриптом, который импортирует версию AlgoServer. Например должна быть такая структура

——-Мои сервера
—AlgoServerLibBetaV21.py
---MyCode.py

И в MyCode.py пишем название библиотеки:
from AlgoServerLibBetaV21 import * #Важно всё зависит от названии библиотеки, которую вы скачиваете!
