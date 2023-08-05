from datetime import datetime

from django.test import TestCase

from tests.models import ModelTest


class BirthdayTestModels(TestCase):
    @classmethod
    def setup_class(self):
        """テストclass実行の前処理"""

        print("setup_class")

    def setUp(self):
        self.meiji = ["1905-1-2", "1905-1-1", "1905-2-1", "1905-2-2"]
        self.showa = ["1980-7-7", "1975-1-1"]
        self.heisei = ["2000-01-02", "2001-01-01", "2002-12-31"]

        self.birthdays = self.meiji + self.showa + self.heisei
        for birthday in self.birthdays:
            model_test = ModelTest(
                birthday=datetime.strptime(birthday, "%Y-%m-%d").date()
            )
            model_test.save()

    def test_default(self):

        self.assertEqual(len(ModelTest._meta.fields), 3)
        self.assertTrue(hasattr(ModelTest, "birthday"))
        self.assertEqual(ModelTest.objects.all().count(), len(self.birthdays))

    def test_month(self):
        model_tests = ModelTest.objects.all()
        for m in model_tests:
            month = m.birthday.month
            self.assertEqual(month, m.birthday_month)

    def test_month_day(self):
        model_tests = ModelTest.objects.all()
        for m in model_tests:
            month = m.birthday.month
            day = m.birthday.day

            month = "0" + str(month) if 10 > month else str(month)
            day = "0" + str(day) if 10 > day else str(day)

            self.assertEqual(month + "-" + day, m.birthday_month_day)

    def test_get_wareki_birthday(self):
        model_tests = ModelTest.objects.all()
        for m in model_tests:
            month = m.birthday.month
            day = m.birthday.day

            wareki_birthday = m.get_wareki_birthday()

            wareki_month = int(wareki_birthday.split("-")[2])
            wareki_day = int(wareki_birthday.split("-")[3])

            self.assertEqual(month, wareki_month)
            self.assertEqual(day, wareki_day)

    def test_get_wareki_birthdays(self):
        wareki_birthdays = ModelTest.objects.get_wareki_birthdays("heisei")
        for m in wareki_birthdays:
            birthday = str(m.birthday)
            self.assertTrue(birthday in self.heisei)

        wareki_birthdays = ModelTest.objects.get_wareki_birthdays("へいせい")
        for m in wareki_birthdays:
            birthday = str(m.birthday)
            self.assertTrue(birthday in self.heisei)

        wareki_birthdays = ModelTest.objects.get_wareki_birthdays("平成")
        for m in wareki_birthdays:
            birthday = str(m.birthday)
            self.assertTrue(birthday in self.heisei)

    def test_get_age(self):
        model_tests = ModelTest.objects.all()
        for m in model_tests:
            age = m.get_age()
            self.assertTrue("int" in str(type(age)))

    def test_get_zodiac(self):
        def get_zodiac(year: int):
            zodiacs = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
            num = (year + 8) % 12
            return zodiacs[num]

        model_tests = ModelTest.objects.all()
        for m in model_tests:
            zodiac = m.get_zodiac()
            year = m.birthday.timetuple().tm_year

            self.assertEqual(zodiac, get_zodiac(year))

    def test_get_jp_era_range(self):
        # 平成
        heisei_birthdays = [
            datetime.strptime(b, "%Y-%m-%d").date() for b in self.heisei
        ]

        model_tests = ModelTest.objects.filter(birthday__in=heisei_birthdays)
        for m in model_tests:
            year = m.get_jp_era_range()
            self.assertEqual(year, 31)

        # 昭和
        showa_birthdays = [datetime.strptime(b, "%Y-%m-%d").date() for b in self.showa]

        model_tests = ModelTest.objects.filter(birthday__in=showa_birthdays)
        for m in model_tests:
            year = m.get_jp_era_range()
            print("year", year)
            self.assertEqual(year, 64)

        # 明治
        meiji_birthdays = [datetime.strptime(b, "%Y-%m-%d").date() for b in self.meiji]

        model_tests = ModelTest.objects.filter(birthday__in=meiji_birthdays)
        for m in model_tests:
            year = m.get_jp_era_range()
            self.assertEqual(year, 45)

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
