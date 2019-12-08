import django
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "HospitalSystem.settings"
django.setup()


from django.db.models import get_app, get_models

from Finance.models import *
from User.models import *
from Laboratory.models import *
from Medicine.models import *
from Outpatient.models import *
from Reservation.models import *


def generateSerializers():
    app = get_app("User")
    for model in get_models(app):
        print(model.name)


def generateViewSets():
    pass


if __name__ == "__main__":
    generateSerializers()
    pass
