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
            real_labels = []
            user_labels = []
            for annotation in annotations:
                real_labels.append([annotation.sample.real_pitch, annotation.sample.real_secondary])
                user_labels.append([annotation.pitch, annotation.secondary])
            progress = (
                100 * len([0 for annotation in annotations if annotation.pitch != "NONE"]) / len(samples)
                if len(samples)
                else None
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
                else None
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
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE" and annotation.sample.real_secondary == "NONE"
                    ]
                )
                if len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE" and annotation.sample.real_secondary == "NONE"
                    ]
                )
                else None
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
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE" and annotation.sample.real_secondary != "NONE"
                    ]
                )
                if len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE" and annotation.sample.real_secondary != "NONE"
                    ]
                )
                else None
            )
            pitch_accuracy = (
                100
                * len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE" and annotation.sample.real_pitch == annotation.pitch
                    ]
                )
                / len([0 for annotation in annotations if annotation.pitch != "NONE"])
                if len([0 for annotation in annotations if annotation.pitch != "NONE"])
                else None
            )
            secondary_accuracy = (
                100
                * len(
                    [
                        0
                        for annotation in annotations
                        if annotation.pitch != "NONE" and annotation.sample.real_secondary == annotation.secondary
                    ]
                )
                / len([0 for annotation in annotations if annotation.pitch != "NONE"])
                if len([0 for annotation in annotations if annotation.pitch != "NONE"])
                else None
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
                    "pitch_accuracy": pitch_accuracy,
                    "secondary_accuracy": secondary_accuracy,
                    "real_labels": real_labels,
                    "user_labels": user_labels,
                }
            )

    mean_statistics = {}
    excluded_users = []
    for user_idx, element in enumerate(all_statistics):
        for key, value in element.items():
            if "_labels" in key:
                break

            if key != "user":
                if key not in mean_statistics:
                    mean_statistics[key] = {}
                    mean_statistics[key]["list"] = []
                mean_statistics[key]["list"].append(value)
                if value is None:
                    excluded_users.append(user_idx)

    for key in mean_statistics.keys():
        mean_statistics[key]["mean"] = np.mean(
            [v for idx, v in enumerate(mean_statistics[key]["list"]) if idx not in excluded_users]
        )
        mean_statistics[key]["std"] = np.std(
            [v for idx, v in enumerate(mean_statistics[key]["list"]) if idx not in excluded_users]
        )
        del mean_statistics[key]["list"]

    statistics = {"all": all_statistics, "average": mean_statistics}
    return statistics
