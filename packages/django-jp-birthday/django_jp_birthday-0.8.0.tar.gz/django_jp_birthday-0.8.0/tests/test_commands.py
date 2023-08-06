# -*- coding: utf-8 -*-

from datetime import datetime
from io import StringIO

# from django.core.exceptions import FieldError

# from django.db import models
from django.test import TestCase
from django.core.management import call_command

# from jp_birthday.fields import BirthdayField

from tests.models import ModelTest


class BirthdayTest(TestCase):
    def setUp(self):
        self.birthdays = ["2001-01-01", "2000-01-02", "2002-12-31"]
        for birthday in self.birthdays:
            ModelTest.objects.create(
                birthday=datetime.strptime(birthday, "%Y-%m-%d").date()
            )

    def test_get_zodiac(self):

        out = StringIO()
        call_command(
            "jp_birthday",
            "jp_birthday.ModelTest",
            params={
                "id": 1,
                "method": "get_zodiac",
            },
            verbosity=1,
            stdout=out,
        )
        self.assertIn("巳", out.getvalue())

    def test_get_jp_era_birthdays(self):

        out = StringIO()
        call_command(
            "jp_birthday",
            "jp_birthday.ModelTest",
            params={"method": "get_jp_era_birthdays", "args": {"jp_era": "heisei"}},
            verbosity=1,
            stdout=out,
        )
        self.assertIn("JpBirthdayQuerySet", out.getvalue())
        for i in range(1, len(self.birthdays) + 1):
            self.assertIn("({0})".format(str(i)), out.getvalue())

    def test_error_model(self):
        out = StringIO()
        call_command(
            "jp_birthday",
            "jp_birthday.ModelHogeTest",
            params={"id": 1, "params": "get_zodiac"},
            verbosity=1,
            stdout=out,
        )
        self.assertIn("is not an ordered model, try:", out.getvalue())

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
