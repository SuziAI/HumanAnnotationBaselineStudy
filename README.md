# Suzipu Human Annotation Baseline Study GUI

This software is intended to be used in a user study for determining the human baseline performance of classifying *suzipu* 俗字谱 notation.
In this Django-based web-app, each individual user can annotate the provided samples which are taken from the Shanghai MS edition of *Baishidaoren Gequ* 白石道人歌曲.
The annotations and all timestamps corresponding to user actions are collected in a database. Later, the data can be evaluated to gain the average human accuracy
in the classification task and the time used.

## How to import the sample data into the database
Run the following command:

`docker compose run django python manage.py import_samples --data-file /app/sample_data/dataset_grouped.json`
