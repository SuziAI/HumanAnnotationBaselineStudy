from django.db import models


class PitchChoices(models.TextChoices):
    NONE = "NONE", "none"
    HE = "HE", "he"
    SI = "SI", "si"
    YI = "YI", "yi"
    SHANG = "SHANG", "shang"
    GOU = "GOU", "gou"
    CHE = "CHE", "che"
    GONG = "GONG", "gong"
    FAN = "FAN", "fan"
    LIU = "LIU", "liu"
    WU = "WU", "wu"
    GAO_WU = "GAO_WU", "gao wu"


class SecondaryChoices(models.TextChoices):
    ADD_NONE = "NONE", "none"
    ADD_DA_DUN = "DA_DUN", "da dun"
    ADD_XIAO_ZHU = "XIAO_ZHU", "xiao zhu"
    ADD_DING_ZHU = "DING_ZHU", "ding zhu"
    ADD_DA_ZHU = "DA_ZHU", "da zhu"
    ADD_ZHE = "ZHE", "zhe"
    ADD_YE = "YE", "ye"
