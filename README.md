Требования к окружению: 
pymysql, bcrypt, dotenv, pydantic, fastapi, jose 
  Сначала поднимаем MySql в контейнере:
docker run -d \                                                                                                                                  
  --name mysql-atk \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=atk \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=pass \
  -p 3306:3306 \
  mysql:8.0
В проекте запускаем выполнение сценария создания и заполнения бд:
python setup_db.py
Запускаем проект:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Swagger UI доступен на http://localhost:8000/docs#/
Доступные данные для авторизации:
user1:user1pw, user2:user2pw, user3:user3pw
В окне авторизации игнорировать поля client_id и client_sercet.
<img width="639" height="587" alt="image" src="https://github.com/user-attachments/assets/2e38e105-0ba2-43c0-a575-3ed99ee48cfb" />
Проверка работоспособности:
<img width="713" height="967" alt="image" src="https://github.com/user-attachments/assets/0211b792-77b0-407d-bb0a-568bb6057416" />
<img width="1419" height="966" alt="image" src="https://github.com/user-attachments/assets/fe01f57a-d394-449c-930d-12ed9a700e2d" />
<img width="718" height="631" alt="image" src="https://github.com/user-attachments/assets/bc37fab5-25fe-4b2f-8b47-1df648d38998" />
<img width="391" height="296" alt="image" src="https://github.com/user-attachments/assets/1e271191-00c0-40f9-b196-bbb1e05d2c59" />
<img width="429" height="296" alt="image" src="https://github.com/user-attachments/assets/7ed189df-31f4-4178-b416-37f3e96ab86f" />
<img width="659" height="502" alt="image" src="https://github.com/user-attachments/assets/ee61c449-3b4d-436a-902a-48e611ae8e14" />
<img width="716" height="610" alt="image" src="https://github.com/user-attachments/assets/6a723096-391d-4d32-b8b3-56b4e8b2ed4a" />
<img width="374" height="336" alt="image" src="https://github.com/user-attachments/assets/ffc151a8-ee3a-4fbf-9de9-91a3bacc55f9" />
<img width="713" height="606" alt="image" src="https://github.com/user-attachments/assets/7cdecd01-5d91-4876-b631-305d45ba3ca3" />
<img width="380" height="487" alt="image" src="https://github.com/user-attachments/assets/27868089-68d8-4b6a-93f5-86b5ed971814" />
