from django import template
from urllib.parse import quote_plus
from django.db.models.fields.files import FieldFile
from django.utils.dateformat import format
import datetime, os
import base64

register = template.Library()

@register.filter
def get_field_value(obj, attr_name):
    # Mengambil nilai field dari objek model berdasarkan nama field (attr_name)
    # Ambil value dari dict atau object
    if isinstance(obj, dict):
        value = obj.get(attr_name, None)
    else:
        value = getattr(obj, attr_name, None)
    #  Menangani FieldFile (misalnya ImageField atau FileField pada model)
    if isinstance(value, FieldFile):
        return os.path.basename(value.name)
    # Menangani datetime (mengonversi menjadi format yang lebih mudah dibaca)
    if isinstance(value, datetime.datetime):
        return format(value, 'd-m-Y H:i')
    # Menangani date (mengonversi menjadi format yang lebih mudah dibaca)
    if isinstance(value, datetime.date):
        # return value.strftime('%d-%b-%Y').upper()
        return format(value, 'd-m-Y')
    # Menangani boolean (mengonversi menjadi 'Yes'/'No')
    if isinstance(value, bool):
        return "YES" if value else "NO"
    # Menangani None (mengonversi menjadi '--')
    if value is None:
        return "--"
    return value

@register.filter
def split_words(value):
    return value.split()

@register.filter
def get_item(dictionary, key):
    return dictionary[key]

@register.filter
def startswith(value, arg):
    """Mengembalikan True jika 'value' dimulai dengan 'arg'."""
    if value:
        return value.startswith(arg)
    return False

@register.filter
def to_abjad(n):
    """Convert 1 -> A, 2 -> B, ..., 27 -> AA, 28 -> AB, etc."""
    result = ''
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result