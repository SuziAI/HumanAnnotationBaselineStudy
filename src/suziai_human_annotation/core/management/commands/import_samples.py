import json
import os

from django.core.files import File
from django.core.management.base import BaseCommand

from suziai_human_annotation.core.models import Sample


class Command(BaseCommand):
    help = "Generate Sample instances from a JSON file containing image paths and metadata."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-file",
            type=str,
            required=True,
            help="The JSON file containing sample data.",
        )

    def handle(self, *args, **options):
        data_file = options["data_file"]

        # Validate path
        if not os.path.isfile(data_file):
            self.stderr.write(self.style.ERROR(f"The file {data_file} does not exist."))
            return

        # Load JSON data
        try:
            with open(data_file) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Error decoding JSON file: {e}"))
            return

        created_samples = []

        for entry in data:
            try:
                image_path = entry["image_path"]
                image_path = os.path.join(os.path.dirname(data_file), image_path)
                real_name = os.path.basename(image_path)
                real_pitch = entry["annotation"]["pitch"] if entry["annotation"]["pitch"] is not None else "NONE"
                real_secondary = (
                    entry["annotation"]["secondary"] if entry["annotation"]["secondary"] is not None else "NONE"
                )
                group = entry["group"] if entry["group"] is not None else 0
            except KeyError:
                self.stderr.write(self.style.WARNING(f"Skipping entry with missing data: {entry}"))
                continue

            if not os.path.isfile(image_path):
                self.stderr.write(self.style.WARNING(f"Image file not found: {image_path}. Skipping entry."))
                continue

            # Create the Sample instance
            with open(image_path, "rb") as image_file:
                Sample.objects.update_or_create(
                    real_name=real_name,
                    defaults={
                        "image": File(image_file, name=os.path.basename(image_path)),
                        "real_pitch": real_pitch,
                        "real_secondary": real_secondary,
                        "group": group,
                    },
                )
                created_samples.append(real_name)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {len(created_samples)} Sample(s): {', '.join(created_samples)}")
        )
