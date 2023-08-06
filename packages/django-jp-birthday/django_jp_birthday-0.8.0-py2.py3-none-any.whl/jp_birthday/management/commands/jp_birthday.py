from django.apps import apps
from django.core.management import BaseCommand, CommandError

# from django.db import models

from jp_birthday.models import BaseBirthdayModel


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, nargs="*")
        parser.add_argument(
            "--params",
            type=dict,
            nargs="?",
            default={"id": 1, "method": "", "args": {}},
        )

    def handle(self, *args, **options):
        """
        Sometimes django-ordered-models ordering goes wrong, for various reasons,
        try re-ordering to a working state.
        """
        # self.verbosity = options["verbosity"]
        self.params = options["params"]

        base_birthday_models = [
            m._meta.label for m in apps.get_models() if issubclass(m, BaseBirthdayModel)
        ]
        candidates = "\n   {}".format("\n   ".join(base_birthday_models))

        print("base_birthday_models", base_birthday_models)
        for model_name in options["model_name"]:
            if model_name not in base_birthday_models:
                self.stdout.write(
                    "Model '{}' is not an ordered model, try: {}".format(
                        model_name, candidates
                    )
                )
                break

            model = apps.get_model(model_name)
            # if not issubclass(model, BaseBirthdayModel):
            #     raise CommandError(
            #         "{} does not inherit from OrderedModel or OrderedModelBase".format(
            #             str(model)
            #         )
            #     )

            try:
                results = self.run_method(model, self.params)
                self.stdout.write("handle")
                self.stdout.write(str(results))
            except Exception as e:
                raise e

    def run_method(self, model: str, params: dict, *args, **options):

        results = None
        method = params["method"]
        if method:
            pk = params["id"] if "id" in params else None
            if pk:
                m = model.objects.filter(id=pk).first()
                if method in dir(m):
                    results = getattr(m, method)()
            else:
                args = params["args"]
                results = getattr(model.objects, method)(**args)
        return results
