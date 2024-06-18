import random 
import string

file_object = open('pass.txt', 'a')
while True:
    def generate_password(length):
        characters = string.ascii_letters + string.digits

        password = ''.join(random.choice(characters) for i in range(length))
        return password
    password = generate_password(12)
    print(f'Ваш новый пароль: {password}')
    file_object.write("\n")
    file_object.write(password)
file_object.close()
