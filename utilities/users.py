import json
import random
import string


class User:
    @staticmethod
    def generate_user_data(name, surname, phone_number):
        user = {
            "firstName": name,
            "lastName": surname,
            "phone": phone_number
        }
        return json.dumps(user)

    @staticmethod
    def generate_random_characters(num_of_chars):
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(num_of_chars))

    @staticmethod
    def generate_random_phone_number(num_of_digits=9):
        return '+48 ' + ''.join(random.SystemRandom().choice(string.digits) for _ in range(num_of_digits))
