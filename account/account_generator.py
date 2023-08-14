import os.path
import sys
import calendar

from random import randrange
from datetime import date, timedelta


from password_generator import PasswordGenerator
from faker import Faker
from russian_names import RussianNames

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


MAX_TRIES = 5
CURRENT_FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))


class Account:
    def __init__(
            self,
            gender: str = "female",
            locale: str = "en_US",
            years: list | None = None,
            sms_api_code: str = "",
            proxy_host: str = "",
            proxy_pass: str = "",
            proxy_port: str = "",
            proxy_type: str = "",
            proxy_user: str = "",
            proxy_refresh: str = "",
    ) -> None:
        self.locale = locale
        self.gender = gender if gender in ["male", "female"] else "female"

        if not self.locale:
            self.locale = "en_US"
        fake = Faker()

        if self.locale == "en_US":
            self.first_name, self.last_name = fake.first_name_female(), fake.last_name_female()
            if self.gender == "male":
                self.first_name, self.last_name = fake.first_name_male(), fake.last_name_male()
        if self.locale == "ru_RU":
            gender_library_mapper = {
                None: 0,
                "female": 0,
                "male": 1
            }

            # Faker randomly swapping name with surname, fixed with this lib
            person = RussianNames()
            self.first_name = person._get_object(
                gender_library_mapper[self.gender],
                "name",
                person.name_reduction
            )
            self.last_name = person._get_object(
                gender_library_mapper[self.gender],
                "surname",
                person.name_reduction)

        self.password = self.generate_password()
        self.birthdate_year = ""
        self.birthdate_month = ""
        self.birthdate_day = ""
        self.set_random_birthdate(years)
        self.cookies = ""
        self.sms_api_code = sms_api_code
        self.login = ""
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_pass = proxy_pass
        self.proxy_user = proxy_user
        self.proxy_type = proxy_type
        self.proxy_refresh = proxy_refresh

    @staticmethod
    def generate_password(min_range: int = None, max_range: int = None) -> str:
        if min_range is None:
            min_range = randrange(7, 9)
        if max_range is None:
            max_range = randrange(12, 14)

        password = PasswordGenerator()
        password.minlen = min_range
        password.maxlen = max_range
        return password.generate()

    def set_random_birthdate(self, years: list | None = None) -> None:
        today = date.today()
        start_year = today.year - 66
        last_year = today.year - 18

        if years:
            start_year, last_year = years

        random_years = randrange(start_year, last_year)
        random_months = randrange(1, 12)
        random_date = today.replace(
            year=random_years,
            month=abs(today.month - random_months) if abs(today.month - random_months) != 0 else 2,
            day=1
        )

        random_days = randrange(1, 19)
        random_date -= timedelta(days=random_days)
        self.birthdate_year = random_date.year
        self.birthdate_month = calendar.month_abbr[random_date.month].lower()
        self.birthdate_day = random_date.day


if __name__ == "__main__":
    gender = "male"
    locale = "ru_RU"
    years = [1980, 1990]
    print(gender, locale, years)
    test_acc = Account(
        gender=gender,
        locale=locale,
        years=years,
        sms_api_code="88cf33cA49847b1fc7b6fd2e451be316",
        proxy_host="connect-ua.z-proxy.com",
        proxy_pass="5vc99ndtsr",
        proxy_port="7997",
        proxy_type="socks5",
        proxy_user="z_odl7xmqz",
        proxy_refresh="https://z-proxy.com/r/?h=5m1kqo"
    )
    # print(test_acc.birthdate_year, test_acc.birthdate_month, test_acc.birthdate_day)
    for k, v in test_acc.__dict__.items():
        print(k, v)
