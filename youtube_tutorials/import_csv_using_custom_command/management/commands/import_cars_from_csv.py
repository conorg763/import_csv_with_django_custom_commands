import csv

from django.core.management.base import BaseCommand

from import_csv_using_custom_command.forms import CarForm


class Command(BaseCommand):
    help = ("imports cars from a local csv file. Expects columns make,model,variant,year")

    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0,1,2,3

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs=1, type=str)

    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", self.NORMAL)
        self.file_path = options["file_path"][0]
        self.prepare()
        self.main()
        self.finalise()

    def prepare(self):
        self.imported_counter = 0
        self.skipped_counter = 0

    def main(self):
        if self.verbosity >= self.NORMAL:
            self.stdout.write("=== Importing Cars === ")

        with open(self.file_path, mode="r") as f:
            reader = csv.DictReader(f)
            for index, row_dict in enumerate(reader):
                form = CarForm(data=row_dict)
                if form.is_valid():
                    car = form.save()
                    if self.verbosity >= self.NORMAL:
                        self.stdout.write(f" - {car}\n")
                    self.imported_counter +=1
                else:
                    if self.verbosity >= self.NORMAL:
                        self.stderr.write(f"Errors importing cars"
                                          f"{row_dict['make']} - {row_dict['model']}:\n"
                                          )
                        self.stderr.write(f"{form.errors.as_json()}\n")
    def finalise(self):
        if self.verbosity >= self.NORMAL:
            self.stdout.write(f"-------------\n")
            self.stdout.write(f"Cars imported: {self.imported_counter}\n")
            self.stdout.write(f"Cars skipped: {self.skipped_counter}\n\n")


