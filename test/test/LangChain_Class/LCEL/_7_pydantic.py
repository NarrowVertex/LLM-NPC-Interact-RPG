from pydantic import BaseModel

#일반 객체 생성
class User:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

user1 = User(name="Joe",age=32, email="joe@gmail.com")
print(user1.name)

user2 = User(name="Joe",age="bar", email="joe@gmail.com")
print(user2.age)



# #Pydantic 객체 생성
# class pUser(BaseModel):
#     name: str
#     age: int
#     email: str

# user1_p = pUser(name="Jane", age=32, email="jane@gmail.com")
# print(user1_p.model_json_schema())

# #잘못된 데이터 - 에러 발생
# user2_p = pUser(name="Jane", age="bar", email="jane@gmail.com")
# print(user2_p.model_json_schema())