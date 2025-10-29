from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView, UpdateView
)
from .forms import (
    WarehouseForm
)

from .models import (
    Warehouse
)

# Create your views here.
class Dashboard(TemplateView):
    template_name = 'layouts/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_sections = [
            {
                "label": "Elements",
                "items": [
                    {"name": "Buttons", "url": "elem-buttons.html"},
                    {"name": "Dropdown", "url": "elem-dropdown.html"},
                    {"name": "Icons", "url": "elem-icons.html"},
                ],
            },
            {
                "label": "Forms",
                "items": [
                    {"name": "Form Elements", "url": "form-elements.html"},
                ],
            },
            {
                "label": "Charts",
                "items": [
                    {"name": "ChartJS", "url": "chart-chartjs.html"},
                ],
            },
            {
                "label": "Tables",
                "items": [
                    {"name": "Basic Tables", "url": "table-basic.html"},
                ],
            },
        ]

        context['menu_sections'] = menu_sections

        return context

class ViewWarehouse(TemplateView):
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_sections = [
        {
            "label": "Inventory",
            "items": [
                {"name": "Warehouse", "url": "warehouseview"},
                {"name": "Stock", "url": "stockview"},
            ],
        },
        {
            "label": "Sales",
            "items": [
                {"name": "Orders", "url": "ordersview"},
                {"name": "Customers", "url": "customerview"},
            ],
        },
        ]

        context = {
            "title": "Master Data",
            "menu_sections": menu_sections,
        }

        return context
    
menu_sections = [
    {
        "title": "Master Data",
        "labels": [
            {
                "label": "Inventory",
                "label_icon":"<i class='ti ti-layout-grid me-2'></i>",
                "items": [
                    {"name": "Warehouse", "url": "warehouseview"},
                    {"name": "Zone", "url": "warehouseview"},
                ],
            },
        ],
    }
]

NEW_BUTTON = """
    <button type="button" class="nav-link btn btn-link text-secondary disabled">
        <i class="far fa-file"></i> New
    </button>
"""

EDIT_BUTTON = """
    <button type="button" class="nav-link btn btn-link text-secondary disabled">
        <i class="far fa-edit"></i> Edit
    </button>
"""

COPY_BUTTON = """
    <button type="button" class="nav-link btn btn-link text-secondary disabled">
        <i class="far fa-copy"></i> Copy
    </button>
"""

SAVE_BUTTON = """
    <button type="submit"
        name="action" value="save" class="btn btn-info btn-with-icon ">
        <i class="typcn typcn-input-checked"></i> Save
    </button>  
"""   
DELETE_BUTTON = """
    <button type="button" class="nav-link btn btn-link text-secondary disabled">
        <i class="far fa-trash-alt"></i> Delete
    </button>
"""   
               
class CreateWarehouse(TemplateView):
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_button = NEW_BUTTON
        edit_button = EDIT_BUTTON
        copy_button = COPY_BUTTON
        save_button = SAVE_BUTTON
        delete_button = DELETE_BUTTON

        context = {
            "page_title": "Manage Warehouse", 
            "menu_sections": menu_sections,
        }

        context['form'] = WarehouseForm
        context['navlink'] = f"""
            {new_button}
            {edit_button}
            {copy_button}
            {delete_button}
        """
        context['save_button'] = f"""
            {save_button}
        """
        context['navtab'] = f"""
            <a class="nav-link active" data-toggle="tab" href="#tab1"> Item Entry</a>
            <a class="nav-link" data-toggle="tab" href="#tab2">Item List</a>
        """

        items = Warehouse.objects.all()
        for item in items:
            url = f"{reverse('warehouseview')}?search={item.code}"
            item.onclick_attr = f'onclick="window.location.href=\'{url}\'"'

        context['items'] = items

        search_query = self.request.GET.get('search')
        copy_query = self.request.GET.get('copy')
        query = search_query or copy_query

        if query:
            new_button = f"""
                <button type="button"
                    onclick="window.location.href='{reverse('warehouseview')}'"
                    class="nav-link btn btn-link text-info">
                    <i class="far fa-file"></i> New
                </button>
            """
            try:
                obj = Warehouse.objects.get(code=query)
                form = WarehouseForm(instance=obj)
                if search_query:
                    # Jadikan semua field readonly
                    for field in form.fields.values():
                        field.widget.attrs['readonly'] = True
                        field.widget.attrs['placeholder'] = ""
                        # Aktifkan tombol edit (menuju halaman update)
                        edit_button = f"""
                            <button type="button"
                                onclick="window.location.href='{reverse('warehouseupdate', args=[obj.pk])}'"
                                class="nav-link btn btn-link text-info">
                                <i class="far fa-edit"></i> Edit
                            </button>
                        """
                        copy_button = f"""
                            <button type="button"
                                onclick="window.location.href='{reverse('warehouseview')}?copy={obj.code}'"
                                class="nav-link btn btn-link text-info">
                                <i class="far fa-copy"></i> Copy
                            </button>
                        """
                        delete_button = f"""
                            <button type="button"
                                onclick="window.location.href='{reverse('warehouseupdate', args=[obj.pk])}'"
                                class="nav-link btn btn-link text-danger">
                                <i class="far fa-trash-alt"></i> Delete
                            </button>
                        """
                        save_button = """
                            <button type="button"
                                class="btn btn-info btn-with-icon disabled">
                                <i class="typcn typcn-input-checked"></i> Save
                            </button>              
                        """

                context['form'] = form
            except Warehouse.DoesNotExist:
                context['form'] = WarehouseForm()
                context['error'] = "Data tidak ditemukan."
        else:
            context['form'] = WarehouseForm()

        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            form = WarehouseForm(request.POST)
            if form.is_valid():
                 form.save()

        return redirect(self.request.META.get('HTTP_REFERER'))
    
class UpdateWarehouse(UpdateView):
    template_name = 'pages/create.html'
    model = Warehouse
    form_class = WarehouseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_button = NEW_BUTTON
        edit_button = EDIT_BUTTON
        copy_button = COPY_BUTTON
        save_button = SAVE_BUTTON
        delete_button = DELETE_BUTTON
        
        search_query = self.request.GET.get('search')
        copy_query = self.request.GET.get('copy')

        # Pilih salah satu query yang tersedia
        query = search_query or copy_query
        if query:
            try:
                obj = Warehouse.objects.get(code=search_query)
                form = WarehouseForm(instance=obj)
                # Jadikan semua field readonly
                if search_query:
                    # Jadikan semua field readonly
                    
                    for field in form.fields.values():
                        field.widget.attrs['readonly'] = True
                        field.widget.attrs['placeholder'] = ""
                        # Aktifkan tombol edit (menuju halaman update)
                        edit_button = f"""
                            <button type="button"
                                    onclick="window.location.href='{reverse('warehouseupdate', args=[obj.pk])}'"
                                    class="nav-link btn btn-link text-info">
                                <i class="far fa-edit"></i> Edit
                            </button>
                        """
                        copy_button = f"""
                            <button type="button"
                                    onclick="window.location.href='{reverse('warehouseview')}?copy={obj.code}'"
                                    class="nav-link btn btn-link text-info">
                                <i class="far fa-copy"></i> Copy
                            </button>
                        """
                        save_button = """
                            <button type="button"
                                class="btn btn-info btn-with-icon disabled">
                                <i class="typcn typcn-input-checked"></i> Save
                            </button>              
                        """

                context['form'] = form
            except Warehouse.DoesNotExist:
                context['form'] = WarehouseForm()
                context['error'] = "Data tidak ditemukan."

        new_button = f"""
            <button type="button"
                onclick="window.location.href='{reverse('warehouseview')}'"
                class="nav-link btn btn-link text-info">
                <i class="far fa-file"></i> New
            </button>
        """

        delete_button = f"""
            <button type="button"
                onclick="window.location.href='{reverse('warehouseview')}'"
                class="nav-link btn btn-link text-danger">
                <i class="far fa-trash-alt"></i> Delete
            </button>
        """

        context['menu_sections'] = menu_sections
        items = Warehouse.objects.all()
        for item in items:
            url = f"{reverse('warehouseview')}?search={item.code}"
            item.onclick_attr = f'onclick="window.location.href=\'{url}\'"'

        context['items'] = items

        context['navtab'] = f"""
            <a class="nav-link btn-with-icon active" data-toggle="tab" href="#tab1"><i class=" typcn typcn-spanner-outline"></i> Entry View</a>
            <a class="nav-link btn-with-icon" data-toggle="tab" href="#tab2"><i class=" typcn typcn-zoom-outline"></i> Data Preview</a> 
            """
        context['navlink'] = f"""
            {new_button}
            {edit_button}
            {copy_button}
            {delete_button}
        """
        context['save_button'] = f"""
            {save_button}
        """
        return context
    
    def get_success_url(self):
        # Ambil kode warehouse dari instance yang baru disimpan
        code = self.object.code
        base_url = reverse('warehouseview')
        return f"{base_url}?search={code}"
