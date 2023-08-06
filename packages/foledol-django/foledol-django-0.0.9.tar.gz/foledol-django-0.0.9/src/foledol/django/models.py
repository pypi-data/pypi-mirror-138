from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

COLUMN_CRITERIA_NONE = 0
COLUMN_CRITERIA_EQUAL = 1
COLUMN_CRITERIA_NOT_EQUAL = 2
COLUMN_CRITERIA_LESS_THAN = 3
COLUMN_CRITERIA_LESS_THAN_OR_EQUAL = 4
COLUMN_CRITERIA_GREATER_THAN = 5
COLUMN_CRITERIA_GREATER_THAN_OR_EQUAL = 6
COLUMN_CRITERIA_CONTAINS = 7
COLUMN_CRITERIA_STARTS_WITH = 8
COLUMN_CRITERIA_ENDS_WITH = 9
COLUMN_CRITERIA_TRUE = 10
COLUMN_CRITERIA_FALSE = 11
COLUMN_CRITERIA_NULL = 12
COLUMN_CRITERIA_NOT_NULL = 13

COLUMN_TEXT_CRITERIA_SET = [
    COLUMN_CRITERIA_NONE,
    COLUMN_CRITERIA_EQUAL,
    COLUMN_CRITERIA_NOT_EQUAL,
    COLUMN_CRITERIA_CONTAINS,
    COLUMN_CRITERIA_STARTS_WITH,
    COLUMN_CRITERIA_ENDS_WITH,
    COLUMN_CRITERIA_NULL,
    COLUMN_CRITERIA_NOT_NULL
]

COLUMN_DATE_CRITERIA_SET = [
    COLUMN_CRITERIA_NONE,
    COLUMN_CRITERIA_EQUAL,
    COLUMN_CRITERIA_NOT_EQUAL,
    COLUMN_CRITERIA_CONTAINS,
    COLUMN_CRITERIA_STARTS_WITH,
    COLUMN_CRITERIA_ENDS_WITH,
    COLUMN_CRITERIA_NULL,
    COLUMN_CRITERIA_NOT_NULL
]

COLUMN_NUMBER_CRITERIA_SET = [
    COLUMN_CRITERIA_NONE,
    COLUMN_CRITERIA_EQUAL,
    COLUMN_CRITERIA_NOT_EQUAL,
    COLUMN_CRITERIA_LESS_THAN,
    COLUMN_CRITERIA_LESS_THAN_OR_EQUAL,
    COLUMN_CRITERIA_GREATER_THAN,
    COLUMN_CRITERIA_GREATER_THAN_OR_EQUAL,
    COLUMN_CRITERIA_NULL,
    COLUMN_CRITERIA_NOT_NULL
]

COLUMN_BOOLEAN_CRITERIA_SET = [
    COLUMN_CRITERIA_NONE,
    COLUMN_CRITERIA_TRUE,
    COLUMN_CRITERIA_FALSE
]

COLUMN_CRITERIA_SET = {
    COLUMN_CRITERIA_NONE: "(aucun)",
    COLUMN_CRITERIA_EQUAL: "égal à",
    COLUMN_CRITERIA_NOT_EQUAL: "différent de",
    COLUMN_CRITERIA_LESS_THAN: "plus petit que",
    COLUMN_CRITERIA_LESS_THAN_OR_EQUAL: "plus petit ou égal",
    COLUMN_CRITERIA_GREATER_THAN: "plus grand que",
    COLUMN_CRITERIA_GREATER_THAN_OR_EQUAL: "plus grand ou égal",
    COLUMN_CRITERIA_CONTAINS: "contient",
    COLUMN_CRITERIA_STARTS_WITH: "commence par",
    COLUMN_CRITERIA_ENDS_WITH: "termine par",
    COLUMN_CRITERIA_TRUE: "vrai",
    COLUMN_CRITERIA_FALSE: "faux",
    COLUMN_CRITERIA_NULL: "vide",
    COLUMN_CRITERIA_NOT_NULL: "non vide",
}


class Log(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='actor')
    ref = models.CharField(max_length=64, default='')
    model = models.CharField(max_length=64, default='')
    date = models.DateTimeField(auto_now_add=True, editable=True, null=True, blank=True)
    diff = models.TextField(default='')
    action = models.CharField(max_length=64, default='')
    transaction = models.CharField(max_length=64, default='', null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def author(self):
        return self.user.username if self.user else '(admin)'


class LogItem(models.Model):
    log = models.ForeignKey(Log, on_delete=models.DO_NOTHING, null=True, related_name='items')
    key = models.CharField(max_length=128, default='')
    old = models.CharField(max_length=128, default='', null=True)
    new = models.CharField(max_length=128, default='', null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)


class GridTable:
    def __init__(self, label, fields, manager, table, url, reports=[]):
        self.label = label
        self.fields = fields
        self.manager = manager
        self.table = table
        self.url = url
        self.reports = reports


class Grid(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    table = models.CharField(max_length=255, default='', null=True, blank=True)
    comment = models.CharField(max_length=255, default='', null=True, blank=True)
    filter_by = models.CharField(max_length=512, default='', null=True, blank=True)
    group_by = models.BooleanField(default=False)
    distinct = models.BooleanField(default=False)
    show_on_home = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.name)

    def table_as_str(self):
        return settings.GRID_TABLES[self.table].label if self.table in settings.GRID_TABLES else ''

    def fields(self):
        return settings.GRID_TABLES[self.table].fields if self.table in settings.GRID_TABLES else None


class Column(models.Model):
    grid: Grid = models.ForeignKey(Grid, on_delete=models.DO_NOTHING, null=True)

    label = models.CharField(max_length=255, default='', null=True, blank=True)
    value = models.CharField(max_length=255, default='', null=True, blank=True)
    criteria = models.IntegerField(default=COLUMN_CRITERIA_EQUAL)
    width = models.IntegerField(default=80, null=True, blank=True)
    order = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def label_as_str(self):
        fields = self.grid.fields() if self.grid else None
        for field in fields:
            if field.key == self.label:
                return field.label
        return self.label

    def label_with_operator(self, op):
        return str(self.label) + '__' + op

    def criteria_as_str(self):
        return COLUMN_CRITERIA_SET[self.criteria]

    def filter(self, objects):
        try:
            if self.criteria == COLUMN_CRITERIA_NOT_EQUAL:
                return objects.exclude(Q(**{self.label: self.value}))
            elif self.criteria == COLUMN_CRITERIA_EQUAL:
                return objects.filter(Q(**{self.label: self.value}))
            elif self.criteria == COLUMN_CRITERIA_LESS_THAN:
                return objects.filter(Q(**{self.label_with_operator('lt'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_LESS_THAN_OR_EQUAL:
                return objects.filter(Q(**{self.label_with_operator('lte'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_GREATER_THAN:
                return objects.filter(Q(**{self.label_with_operator('gt'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_GREATER_THAN_OR_EQUAL:
                return objects.filter(Q(**{self.label_with_operator('gte'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_CONTAINS:
                return objects.filter(Q(**{self.label_with_operator('contains'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_STARTS_WITH:
                return objects.filter(Q(**{self.label_with_operator('startswith'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_ENDS_WITH:
                return objects.filter(Q(**{self.label_with_operator('endswith'): self.value}))
            elif self.criteria == COLUMN_CRITERIA_TRUE:
                return objects.filter(Q(**{self.label: True}))
            elif self.criteria == COLUMN_CRITERIA_FALSE:
                return objects.filter(Q(**{self.label: False}))
            elif self.criteria == COLUMN_CRITERIA_NULL:
                return objects.filter(Q(**{self.label_with_operator('isnull'): True}))
            elif self.criteria == COLUMN_CRITERIA_NOT_NULL:
                return objects.filter(
                    Q(**{self.label_with_operator('isnull'): False})
                ).exclude(Q(**{self.label_with_operator('exact'): ''}))
        except Exception as ex:
            print("ERROR:" + str(ex))
        return objects

