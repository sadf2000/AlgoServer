import requests,time,json

class AlgoServer:
  def __init__(self, Cookie, ID):

    self.Cookie = Cookie
    self.ID = ID
    urll = f"https://learn.algoritmika.org/api/v1/projects/info/{ID}"
    self.header={'cookie': Cookie,'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}  # Рекомендуется актуальный User-Agent
    try:
      r = requests.get(urll, headers=self.header)
      r = r.json()
    except:
      print(r.text)
    try:
      try:
        LId = int(r["data"]["meta"]["scratchId"])
      except:
        LId = int(r["data"]["meta"]["projectId"])
    except:
      LId = None
      print(f"Скретч и пайтон проект не был найден, в ID:{self.ID}. LId=None")
    self.LocalID = LId
    #Константы
    self.urlParseComment = f"https://learn.algoritmika.org/api/v1/projects/comment/{ID}"
    self.urlPython = f"https://learn.algoritmika.org/api/v1/python/save?id={self.LocalID}"
    self.urlDescChanger = f"https://learn.algoritmika.org/api/v1/projects/update/{ID}"
    self.urlScratch = f"https://learn.algoritmika.org/api/v1/scratch/save-project/{self.LocalID}"
    self.urlLoadScratch = f"https://learn.algoritmika.org/api/v1/scratch/load/{self.LocalID}"
    self.urlLoadPython = f"https://learn.algoritmika.org/api/v1/python/preview?id={self.LocalID}"
    
    self.Name = ""
    self.Message = ""
    self.source = ''
    self.titlee = ''
    self.projectContent = ''
  def ParseComment(self):
    try:
      response = requests.get(self.urlParseComment+"?page=1&perPage=1&sort=-created_at",headers=self.header)
      response.raise_for_status()
      a = response.json()
    
      try:
        self.Name = a["data"]["items"][0]["author"]["name"]
        self.Message = a["data"]["items"][0]["message"]
        self.ID = a["data"]["items"][0]["author"]["id"]
        print(self.Name)
        print(self.Message)
      except (KeyError, IndexError, TypeError) as e:
        print(f"Ошибка при парсинге JSON(нету комментария): {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

  def ParseComments(self, lengthComment):
    try:
      try:
        response = requests.get(self.urlParseComment+f"?page=1&perPage={lengthComment}&sort=-created_at",headers=self.header)
        response.raise_for_status()
        a = response.json()
        result = {}
        #print(a)
        try:
          for i in range(lengthComment):
          #print(i+1)
            self.Name = a["data"]["items"][i]["author"]["name"]
            self.Message = a["data"]["items"][i]["message"]
            self.ID = a["data"]["items"][i]["author"]["id"]
            self.IDM = a["data"]["items"][i]["id"]
            result[self.IDM] = [self.ID,self.Name,self.Message]
          #print(self.Name, self.ID)
          #print(self.Message)
          #print(result)
        except (KeyError, IndexError, TypeError) as e:
          print(f"Ошибка при парсинге JSON(нету комментария): {e}")
      except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
    except:
      print("Ошибка инициализации")
    return result
  
  def ParseScratch(self): 
      try:
            response = requests.get(self.urlLoadScratch, headers=self.header)
            response.raise_for_status()
            try:  
              result = json.dumps(response.json(), indent=4, ensure_ascii=False)  # Красивый вывод JSON
            except json.JSONDecodeError:
                print("Ответ не является JSON, вывод текста:")
                print(response.text)  # Если не JSON, выводим как текст
      except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе ParseScratch: {e}")
      return result

  def ParsePython(self): 
    a = requests.get(self.urlLoadPython, headers=self.header).json()
    return a["data"]["content"]

  def SimpleRGet(self,url):
    try:
      r = requests.get(url,headers=self.header)
      r.raise_for_status()
      print(r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе SimpleRGet: {e}")
    return r.text

  def ChangePyProject(self,titlee,source):
    try:
      r = requests.post(self.urlPython, headers=self.header, json={"content": source, "name": titlee})
      r.raise_for_status()  # Проверяем на HTTP ошибки
      print(r, r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangePyProject: {e}")

  def ChangeScratchProject(self,projectContent):
    try:
      r = requests.post(self.urlScratch, headers=self.header, json={"projectContent": json.dumps(projectContent)})
      r.raise_for_status()  # Проверяем на HTTP ошибки
      print(r, r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangeScratchProject: {e} \n {r.text}")

  def ChangeDescProject(self,titlee,desc,preview,Remix):
    try:
      r = requests.post(self.urlDescChanger, headers=self.header, json={
        "title":titlee,
        "description":desc,
        "isRemixEnabled":Remix,
        "previewName":preview})
      r.raise_for_status()  # Проверяем на HTTP ошибки
      print(r, r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangeDescProject: {e}")

      
  time.sleep(0.5) #Включена задержка, рекомендовано для стабильности сервера алгоритмики

class GetCookie:
  def __init__(self,login,password):
    self.login = login  # Добавлено сохранение логина и пароля
    self.password = password
    urlLogin = 'https://learn.algoritmika.org/s/auth/api/e/student/auth'
    try:
        response = requests.post(urlLogin, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},  # Рекомендуется актуальный User-Agent
                                     json={"login": str(login), "password": str(password)})
        response.raise_for_status()  # Проверяем на HTTP ошибки
        a = response.json()
        self.Id = a["item"]["studentId"]
        lollol = ""
        if "item" in a:
          for key,value in a["item"].items():
            lollol+=str(key)  # Ключ тоже нужно приводить к строке
            lollol+="="
            lollol+=str(value)
            lollol+=";"
          self.cookie = lollol  # Сохраняем куки как атрибут класса
        else:
          print("Не удалось получить куки. Проверьте логин и пароль.")
          self.cookie = None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе GetCookie: {e}")
        print(response.text)
        print(login, password)
        self.cookie = None
    except (KeyError, TypeError, ValueError) as e:
        print(f"Ошибка при парсинге JSON в GetCookie: {e}")
        self.cookie = None

class BuildScratch:
  def __init__(self,projectContent):
    self.projectContentJSON = json.loads(projectContent)
  #Берет со сцены все переменные и листы

  def getLists(self):
    a = self.projectContentJSON
    lists = a["targets"][0]["lists"]
    #print(lists)
    return lists

  def getVariables(self): 
    a = self.projectContentJSON
    variables = a["targets"][0]["variables"]
    #print(variables)
    return variables

  def Variable(self, idd,name,value):
    a = self.projectContentJSON
    a["targets"][0]["variables"][idd] = [name,value]

  def List(self, idd,name,value):
    a = self.projectContentJSON
    a["targets"][0]["lists"][idd] = [name,value]

  def DebugPrint(self):
    a = self.projectContentJSON
    print(json.dumps(a, indent=4, ensure_ascii=False))

  def delVariable(self,idd):
    try:
      del self.projectContentJSON["targets"][0]["variables"][idd]
    except (KeyError, TypeError) as e:
      print(f"Error deleting variable: {e}")
  def delList(self,idd):
    try:
      del self.projectContentJSON["targets"][0]["lists"][idd]
    except (KeyError, TypeError) as e:
      print(f"Error deleting variable: {e}")
