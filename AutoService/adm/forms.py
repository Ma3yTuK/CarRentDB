from django import forms
from . import models
from django.utils.translation import gettext as _
from polls import db_requests



class AdminUserCreateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    def role_choice():
        return  [ (role["id"], role["name"]) for role in db_requests.execQuery(db_requests.filter("roles")) ]

    role = forms.TypedChoiceField(coerce=int, choices=role_choice)
    email = forms.CharField(label=_("email"), max_length=256)
    password = forms.CharField(label=_("password"), widget=forms.PasswordInput())
    first_name = forms.CharField(label=_("first name"), max_length=32)
    last_name = forms.CharField(label=_("last name"), max_length=32)

    table = "users"

    def clean(self):
        cleaned_data = super().clean()
        if db_requests.execQuery(db_requests.filter("users", email=cleaned_data["email"])):
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("users",
            email = cleaned_data["email"],
            password = cleaned_data["password"],
            first_name = cleaned_data["first_name"],
            last_name = cleaned_data["last_name"],
            id_role = cleaned_data["role"]
        ))


class AdminUserUpdateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    def role_choice():
        return  [ (role["id"], role["name"]) for role in db_requests.execQuery(db_requests.filter("roles")) ]

    id = forms.IntegerField(disabled=True)
    role = forms.TypedChoiceField(coerce=int, choices=role_choice)
    email = forms.CharField(label=_("email"), max_length=128)
    first_name = forms.CharField(label=_("first name"), max_length=32)
    last_name = forms.CharField(label=_("last name"), max_length=32)

    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial

        users = db_requests.execQuery(db_requests.filter("users", email=cleaned_data["email"]))
        if users and users[0]["id"] != cleaned_data["id"]:
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.updateTable("users", cleaned_data["id"],
            email = cleaned_data["email"],
            first_name = cleaned_data["first_name"],
            last_name = cleaned_data["last_name"],
            id_role = cleaned_data["role"]
        ))


class AdminEmployeeCreateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    def user_choice():
        return  [ (user["id"], user["first_name"]) for user in db_requests.execQuery(db_requests.filter("users")) ]

    def branch_choice():
        return  [ (branch["id"], branch["address"]) for branch in db_requests.execQuery(db_requests.filter("branches")) ]

    id_user = forms.TypedChoiceField(coerce=int, choices=user_choice)
    id_branch = forms.TypedChoiceField(coerce=int, choices=branch_choice)

    table = "employees"

    def clean(self):
        cleaned_data = super().clean()
        if db_requests.execQuery(db_requests.filter("employees", id_user=cleaned_data["id_user"])):
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("employees",
            id_user = cleaned_data["id_user"],
            id_branch = cleaned_data["id_branch"]
        ))


class AdminEmployeeUpdateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    def user_choice():
        return  [ (user["id"], user["first_name"]) for user in db_requests.execQuery(db_requests.filter("users")) ]

    def branch_choice():
        return  [ (branch["id"], branch["address"]) for branch in db_requests.execQuery(db_requests.filter("branches")) ]

    id_user = forms.TypedChoiceField(coerce=int, choices=user_choice)
    id_branch = forms.TypedChoiceField(coerce=int, choices=branch_choice)
    id = forms.IntegerField(disabled=True)

    table = "employees"

    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        employees = db_requests.execQuery(db_requests.filter("employees", id_user=cleaned_data["id_user"]))
        if employees and employees[0].id != cleaned_data["id"]:
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.updateTable("employees", cleaned_data["id"],
            id_user = cleaned_data["id_user"],
            id_branch = cleaned_data["id_branch"]
        ))


class AdminJobCreateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    name = forms.CharField(max_length=32)
    salary = forms.IntegerField()

    table = "jobs"

    def clean(self):
        cleaned_data = super().clean()
        if db_requests.execQuery(db_requests.filter("jobs", name=cleaned_data["name"])):
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("jobs",
            name = cleaned_data["name"],
            salary = cleaned_data["salary"]
        ))


class AdminJobUpdateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    name = forms.CharField(max_length=32)
    salary = forms.IntegerField()
    id = forms.IntegerField(disabled=True)

    table = "employees"

    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        jobs = db_requests.execQuery(db_requests.filter("jobs", name=cleaned_data["name"]))
        if jobs and jobs[0].id != cleaned_data["id"]:
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.updateTable("jobs", cleaned_data["id"],
            name = cleaned_data["name"],
            salary = cleaned_data["salary"]
        ))


class AdminMarkCreateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    name = forms.CharField(max_length=32)

    table = "marks"

    def clean(self):
        cleaned_data = super().clean()
        if db_requests.execQuery(db_requests.filter("marks", name=cleaned_data["name"])):
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("marks",
            name=cleaned_data["name"]
        ))


class AdminMarkUpdateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    name = forms.CharField(max_length=32)
    id = forms.IntegerField(disabled=True)

    table = "marks"

    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        marks = db_requests.execQuery(db_requests.filter("marks", name=cleaned_data["name"]))
        if marks and marks[0].id != cleaned_data["id"]:
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.updateTable("marks", cleaned_data["id"],
            name=cleaned_data["name"]
        ))


class AdminVehicleCreateForm(forms.Form):

    def branch_choice():
        return  [ (branch["id"], branch["address"]) for branch in db_requests.execQuery(db_requests.filter("branches")) ]

    def mark_choice():
        return  [ (mark["id"], mark["name"]) for mark in db_requests.execQuery(db_requests.filter("marks")) ]

    id_branch = forms.TypedChoiceField(coerce=int, choices=branch_choice)
    id_mark = forms.TypedChoiceField(coerce=int, choices=mark_choice)
    type = forms.CharField(max_length=32)
    model = forms.CharField(max_length=32)
    price = forms.IntegerField()
    is_available = forms.BooleanField(required=False)

    table = "vehicles"

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("vehicles",
            id_branch = cleaned_data["id_branch"],
            id_mark = cleaned_data["id_mark"],
            type = cleaned_data["type"],
            model = cleaned_data["model"],
            price = cleaned_data["price"],
            is_available = cleaned_data["is_available"]
        ))


class AdminVehicleUpdateForm(forms.Form):

    def branch_choice():
        return  [ (branch["id"], branch["address"]) for branch in db_requests.execQuery(db_requests.filter("branches")) ]

    def mark_choice():
        return  [ (mark["id"], mark["name"]) for mark in db_requests.execQuery(db_requests.filter("marks")) ]

    id_branch = forms.TypedChoiceField(coerce=int, choices=branch_choice)
    id_mark = forms.TypedChoiceField(coerce=int, choices=mark_choice)
    type = forms.CharField(max_length=32)
    model = forms.CharField(max_length=32)
    price = forms.IntegerField()
    is_available = forms.BooleanField(required=False)
    id = forms.IntegerField(disabled=True)

    table = "vehicles"

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        db_requests.execQuery(db_requests.updateTable("vehicles", cleaned_data["id"],
            id_branch = cleaned_data["id_branch"],
            id_mark = cleaned_data["id_mark"],
            type = cleaned_data["type"],
            model = cleaned_data["model"],
            price = cleaned_data["price"],
            is_available = cleaned_data["is_available"]
        ))


class AdminInsuranceCreateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    def vehicle_choice():
        return  [ (vehicle["id"], vehicle["model"]) for vehicle in db_requests.execQuery(db_requests.filter("vehicles")) ]

    id_vehicle = forms.TypedChoiceField(coerce=int, choices=vehicle_choice)
    insurance_start = forms.DateTimeField()
    insurance_end = forms.DateTimeField()
    info = forms.CharField(max_length=1024)

    table = "insurances"

    def clean(self):
        cleaned_data = super().clean()
        if db_requests.execQuery(db_requests.filter("insurances", id_vehicle=cleaned_data["id_vehicle"])):
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("insurances",
            id_vehicle = cleaned_data["id_vehicle"],
            insurance_start = cleaned_data["insurance_start"],
            insurance_end = cleaned_data["insurance_end"],
            info = cleaned_data["info"]
        ))


class AdminInsuranceUpdateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    def vehicle_choice():
        return  [ (vehicle["id"], vehicle["model"]) for vehicle in db_requests.execQuery(db_requests.filter("vehicles")) ]

    id_vehicle = forms.TypedChoiceField(coerce=int, choices=vehicle_choice)
    insurance_start = forms.DateTimeField()
    insurance_end = forms.DateTimeField()
    info = forms.CharField(max_length=1024)
    id = forms.IntegerField(disabled=True)

    table = "insurances"

    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        marks = db_requests.execQuery(db_requests.filter("insurances", id_vehicle=cleaned_data["id_vehicle"]))
        if insurances and insurances[0].id != cleaned_data["id"]:
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.updateTable("insurances", cleaned_data["id"],
            id_vehicle = cleaned_data["id_vehicle"],
            insurance_start = cleaned_data["insurance_start"],
            insurance_end = cleaned_data["insurance_end"],
            info = cleaned_data["info"]
        ))


class AdminBranchCreateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    address = forms.CharField(max_length=512)

    table = "branches"

    def clean(self):
        cleaned_data = super().clean()
        if db_requests.execQuery(db_requests.filter("branches", address=cleaned_data["address"])):
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.insertIntoTable("branches",
            address = cleaned_data["address"]
        ))


class AdminBranchUpdateForm(forms.Form):
    error_messages = {
        'exists': _("Exists"),
    }

    address = forms.CharField(max_length=512)
    id = forms.IntegerField(disabled=True)

    table = "branches"

    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        branches = db_requests.execQuery(db_requests.filter("branches", address=cleaned_data["addresss"]))
        if branches and branches[0].id != cleaned_data["id"]:
            raise forms.ValidationError(
                self.error_messages['exists'],
                code='exists',
            )
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        db_requests.execQuery(db_requests.updateTable("branches", cleaned_data["id"],
            address = cleaned_data["address"]
        ))