import os
import uuid


def filename_generator(prefix):
    def generate_unique_filename(instance, filename):
        unique_id = uuid.uuid4()
        extension = os.path.splitext(filename)[1] or ".bin"
        new_filename = f"{unique_id}{extension}"
        return os.path.join(prefix, new_filename)

    generate_unique_filename.deconstruct = lambda: (
        f"{filename_generator.__module__}.{filename_generator.__name__}",
        [prefix],
        {},
    )

    return generate_unique_filename
