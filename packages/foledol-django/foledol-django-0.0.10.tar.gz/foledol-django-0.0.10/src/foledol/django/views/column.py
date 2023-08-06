from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from foledol.django.logger import log
from foledol.django.tools.field import TextField, IntegerField, BooleanField, DateField, FloatField
from foledol.django.tools.form import Form
from foledol.django.tools.handlers import confirm
from foledol.django.utils import pop_path, get_path, get_param, get_integer, error, new_context
from .grid import get_field
from .grids import grid_renumber

from ..models import Column, Grid, COLUMN_CRITERIA_SET, COLUMN_TEXT_CRITERIA_SET, COLUMN_DATE_CRITERIA_SET, \
    COLUMN_NUMBER_CRITERIA_SET, COLUMN_BOOLEAN_CRITERIA_SET


class ColumnForm(Form):
    def __init__(self, context):
        super().__init__(context, [
            TextField('label', "Libellé", min_length=1),
            IntegerField('criteria', "Critère"),
            TextField('value', "Valeur"),
            IntegerField('order', "Ordre"),
            IntegerField('width', "Largeur"),
            BooleanField('hidden', "Masquer"),
        ])


def column_form(request, column):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    action = get_path(request, context, column, 'column', space='django')

    grid_id = get_integer(request, 'grid_id', 0)
    if grid_id > 0:
        grid = Grid.objects.all().get(id=grid_id)
    context['grid_id'] = grid.id

    if column:
        context['column'] = column

    fields = grid.fields() if grid else []
    context['fields'] = fields

    context['criteria_set'] = COLUMN_CRITERIA_SET

    form = ColumnForm(context)
    form.read(request.POST, column)
    if action == 'update':
        # TODO: fix the issue on BooleanField (Read)
        form.field('hidden').value = 'hidden' in request.POST

    order = (grid.column_set.count() + 1) * 10 if grid else 10

    criteria = get_integer(request, 'criteria', column.criteria if column else 0)
    context['criteria'] = criteria

    if len(action) > 0:
        form.validate()

    if context['error']:
        context['error'] = "Veuillez corriger les erreurs ci-dessous"

    label = get_param(request, context, 'label', None)
    if label and column:
        field = get_field(column.label, fields)
        if isinstance(field, TextField):
            if criteria not in COLUMN_TEXT_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec un texte"
        if isinstance(field, DateField):
            if criteria not in COLUMN_DATE_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec une date"
        if isinstance(field, FloatField) or isinstance(field, IntegerField):
            if criteria not in COLUMN_NUMBER_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec un nombre"
        if isinstance(field, BooleanField):
            if criteria not in COLUMN_BOOLEAN_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec un booléen"

    if not action or context['error']:
        context['action'] = 'update' if column else 'create'
        return render(request, 'column.html', context)

    if action == 'create':
        column = Column(grid=grid)
    form.save(column)
    if not column.order:
        column.order = order
    column.save()
    if grid:
        grid_renumber(grid)
    log(column.id, 'column', action, request.user, form.old_values, form.new_values)

    return HttpResponseRedirect(context['back'] + '?path=' + pop_path(request))


@login_required
def column_create(request):
    return column_form(request, None)


@login_required
def column_update(request, pk):
    column = Column.objects.filter(id=pk).first()
    return column_form(request, column) if column else error(request)


@login_required
def column_delete(request, pk):
    def prepare(context):
        column = Column.objects.get(id=pk)
        context['title'] = _('delete_column_title').format(column)
        context['cancel'] = reverse('django:column_update', kwargs={'pk': pk})
        context['message'] = _('delete_column_message').format(column)
        return column

    def execute(column):
        column.delete()
        grid_renumber(column.grid)

    return confirm(request, 'delete', prepare, execute, reverse('django:columns'))
