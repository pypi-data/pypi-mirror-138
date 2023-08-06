from datetime import datetime

from django.test import TestCase

from tests.models import ModelTest
from jp_birthday.eras import JapanEra


class BirthdayTestEras(TestCase):
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

        self.era = JapanEra()

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")


class BirthdayTestErasJtw(TestCase):
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

        self.jtw = JapanEra().jtw

    def test__check_language_success(self):
        jp_era = "平成"
        l_type = self.jtw._check_language(jp_era)
        self.assertEqual(l_type, "kanji")

        jp_era = "ヘイセイ"
        l_type = self.jtw._check_language(jp_era)
        self.assertEqual(l_type, "katakana")

        jp_era = "へいせい"
        l_type = self.jtw._check_language(jp_era)
        self.assertEqual(l_type, "hiragana")

        jp_era = "heisei"
        l_type = self.jtw._check_language(jp_era)
        self.assertEqual(l_type, "english")

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
