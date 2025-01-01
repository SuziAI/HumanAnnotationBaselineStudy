from django.contrib.auth import get_user_model

import numpy as np

from suziai_human_annotation.core.models import Action, Annotation, Sample

User = get_user_model()


def build_statistics():
    all_statistics = []
    for user in User.objects.all():
        if user.username != "admin":
            samples = Sample.objects.filter(group=user.id % 2)
            annotations = Annotation.objects.filter(user=user)
            timestamps = sorted([action.timestamp for action in Action.objects.filter(annotation__in=annotations)])
            timestamp_increments = [
                (timestamps[idx + 1] - timestamps[idx]).total_seconds() / 60 for idx in range(len(timestamps) - 1)
            ]
            progress = (
                100 * len([0 for annotation in annotations if annotation.pitch != "NONE"]) / len(samples)
                if len(samples)
                else 0
            )
            total_accuracy = (
                100
                * len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE"
                        and annotation.sample.real_pitch == annotation.pitch
                        and annotation.sample.real_secondary == annotation.secondary
                    ]
                )
                / len([0 for annotation in annotations if annotation.pitch != "NONE"])
                if len([0 for annotation in annotations if annotation.pitch != "NONE"])
                else 0
            )
            simple_accuracy = (
                100
                * len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE"
                        and annotation.secondary == "NONE"
                        and annotation.sample.real_pitch == annotation.pitch
                        and annotation.sample.real_secondary == annotation.secondary
                    ]
                )
                / len(
                    [0 for annotation in annotations if annotation.pitch != "NONE" and annotation.secondary == "NONE"]
                )
                if len(
                    [0 for annotation in annotations if annotation.pitch != "NONE" and annotation.secondary == "NONE"]
                )
                else 0
            )
            composite_accuracy = (
                100
                * len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE"
                        and annotation.secondary != "NONE"
                        and annotation.sample.real_pitch == annotation.pitch
                        and annotation.sample.real_secondary == annotation.secondary
                    ]
                )
                / len(
                    [0 for annotation in annotations if annotation.pitch != "NONE" and annotation.secondary != "NONE"]
                )
                if len(
                    [0 for annotation in annotations if annotation.pitch != "NONE" and annotation.secondary != "NONE"]
                )
                else 0
            )

            all_statistics.append(
                {
                    "user": user.username,
                    "total_time": sum(timestamp_increments) / 60,
                    # if an increment between actions is more than 5 minutes, count it as 5 minutes
                    "real_time": sum([increment if increment < 5 else 5 for increment in timestamp_increments]) / 60,
                    "progress": progress,
                    "total_accuracy": total_accuracy,
                    "simple_accuracy": simple_accuracy,
                    "composite_accuracy": composite_accuracy,
                }
            )

    mean_statistics = {}
    for element in all_statistics:
        for key, value in element.items():
            if key != "user":
                if key not in mean_statistics:
                    mean_statistics[key] = {}
                    mean_statistics[key]["list"] = []
                mean_statistics[key]["list"].append(value)

    for key in mean_statistics.keys():
        mean_statistics[key]["mean"] = np.mean(mean_statistics[key]["list"])
        mean_statistics[key]["std"] = np.std(mean_statistics[key]["list"])
        del mean_statistics[key]["list"]

    statistics = {"all": all_statistics, "average": mean_statistics}
    return statistics
