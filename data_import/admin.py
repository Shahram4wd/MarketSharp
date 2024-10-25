from django.contrib import admin
from .models import *

@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email1', 'source', 'company_id', 'is_active', 'creation_date')
    search_fields = ('first_name', 'last_name', 'email1', 'source', 'company_id')
    list_filter = ('is_active', 'source', 'has_dnc_phone', 'has_dne_email')
    ordering = ('-creation_date',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_initial', 'last_name', 'title', 'source', 'company_id', 'contact_phone_id', 'primary_address_id')
        }),
        ('Email Information', {
            'fields': ('email1', 'email1_can_mail', 'email2', 'email2_can_mail', 'email3', 'email3_can_mail')
        }),
        ('Website Information', {
            'fields': ('website1', 'website2', 'website3')
        }),
        ('Additional Information', {
            'fields': ('income_code', 'age_code', 'structure_age_code', 'year_home_built', 'marital_status', 'length_of_residence', 'style_of_home')
        }),
        ('Status and Sync Data', {
            'fields': ('is_active', 'qb_sync_date', 'qb_id', 'last_update', 'created_date', 'has_dnc_phone', 'has_dne_email')
        }),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email1', 'source', 'company_id', 'is_active', 'creation_date')
    search_fields = ('first_name', 'last_name', 'email1', 'source', 'company_id')
    list_filter = ('is_active', 'source', 'has_dnc_phone', 'has_dne_email')
    ordering = ('-creation_date',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_initial', 'last_name', 'title', 'source', 'company_id', 'contact_phone_id', 'primary_address_id')
        }),
        ('Email Information', {
            'fields': ('email1', 'email1_can_mail', 'email2', 'email2_can_mail', 'email3', 'email3_can_mail')
        }),
        ('Website Information', {
            'fields': ('website1', 'website2', 'website3')
        }),
        ('Additional Information', {
            'fields': ('income_code', 'age_code', 'structure_age_code', 'year_home_built', 'marital_status', 'length_of_residence', 'style_of_home')
        }),
        ('Status and Sync Data', {
            'fields': ('is_active', 'qb_sync_date', 'qb_id', 'last_update', 'created_date', 'has_dnc_phone', 'has_dne_email')
        }),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'owner', 'email', 'phone', 'address_city', 'address_state')
    search_fields = ('name', 'owner', 'email', 'address_city', 'phone')
    list_filter = ('address_state', 'time_zone')
    ordering = ('-name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'owner', 'number', 'address_line1', 'address_line2', 'address_city', 'address_state', 'address_zip')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'fax', 'website', 'contact_name', 'contact_title')
        }),
        ('Additional Information', {
            'fields': ('time_zone',)
        }),
    )

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email1', 'source', 'company_id', 'is_active', 'creation_date')
    search_fields = ('first_name', 'last_name', 'email1', 'source', 'company_id')
    list_filter = ('is_active', 'source', 'has_dnc_phone', 'has_dne_email')
    ordering = ('-creation_date',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_initial', 'last_name', 'title', 'source', 'company_id', 'contact_phone_id', 'primary_address_id')
        }),
        ('Email Information', {
            'fields': ('email1', 'email1_can_mail', 'email2', 'email2_can_mail', 'email3', 'email3_can_mail')
        }),
        ('Website Information', {
            'fields': ('website1', 'website2', 'website3')
        }),
        ('Additional Information', {
            'fields': ('income_code', 'age_code', 'structure_age_code', 'year_home_built', 'marital_status', 'length_of_residence', 'style_of_home')
        }),
        ('Status and Sync Data', {
            'fields': ('is_active', 'qb_sync_date', 'qb_id', 'last_update', 'created_date', 'has_dnc_phone', 'has_dne_email')
        }),
    )

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'status', 'sale_date', 'is_active', 'last_update')
    search_fields = ('name', 'type', 'status', 'contact_id', 'inquiry_id')
    list_filter = ('status', 'type', 'is_active')
    ordering = ('-last_update',)

    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'status', 'contact_id', 'inquiry_id', 'appointment_id')
        }),
        ('Address Information', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'zip')
        }),
        ('Date Information', {
            'fields': ('start_date', 'sale_date', 'completed_date')
        }),
        ('Additional Information', {
            'fields': ('structure_value_code', 'note', 'exported_to_guild_quality', 'is_active', 'last_update', 'created_date')
        }),
    )

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'contact_id', 'due_date', 'is_active', 'last_update')
    search_fields = ('type', 'contact_id', 'assign_to_employee_id', 'scheduled_by_employee_id')
    list_filter = ('is_active', 'type')
    ordering = ('-last_update',)

    fieldsets = (
        (None, {
            'fields': ('contact_id', 'name', 'type', 'due_date', 'completed_date', 'reminder_minutes', 'notes')
        }),
        ('Employee Assignment', {
            'fields': ('assign_to_employee_id', 'scheduled_by_employee_id', 'reminder_dismissed')
        }),
        ('Status and Sync Data', {
            'fields': ('is_active', 'last_updated_by', 'last_update', 'created_by', 'created_date')
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email1', 'source', 'company_id', 'is_active', 'creation_date')
    search_fields = ('first_name', 'last_name', 'email1', 'source', 'company_id')
    list_filter = ('is_active', 'source', 'has_dnc_phone', 'has_dne_email')
    ordering = ('-creation_date',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_initial', 'last_name', 'title', 'source', 'company_id', 'contact_phone_id', 'primary_address_id')
        }),
        ('Email Information', {
            'fields': ('email1', 'email1_can_mail', 'email2', 'email2_can_mail', 'email3', 'email3_can_mail')
        }),
        ('Website Information', {
            'fields': ('website1', 'website2', 'website3')
        }),
        ('Additional Information', {
            'fields': ('income_code', 'age_code', 'structure_age_code', 'year_home_built', 'marital_status', 'length_of_residence', 'style_of_home')
        }),
        ('Status and Sync Data', {
            'fields': ('is_active', 'qb_sync_date', 'qb_id', 'last_update', 'created_date', 'has_dnc_phone', 'has_dne_email')
        }),
    )

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'inquiry_date', 'contact_id', 'division', 'is_active', 'last_update')
    search_fields = ('description', 'contact_id', 'division', 'job_site_city', 'job_site_zip')
    list_filter = ('is_active', 'division', 'inquiry_status_id')
    ordering = ('-last_update',)

    fieldsets = (
        (None, {
            'fields': ('contact_id', 'description', 'inquiry_date', 'set_date', 'division', 'is_active')
        }),
        ('Job Site Information', {
            'fields': ('job_site_address_line1', 'job_site_address_line2', 'job_site_city', 'job_site_state', 'job_site_zip', 'job_site_directions')
        }),
        ('Source Information', {
            'fields': ('inquiry_source_primary_id', 'inquiry_source_secondary_id', 'promoter_id', 'canvasser_id', 'telemarketer_id', 'set_by_id')
        }),
        ('Status and Sync Data', {
            'fields': ('inquiry_status_id', 'last_update_by', 'last_update', 'created_by', 'created_date')
        }),
    )

@admin.register(ActivityReference)
class ActivityReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_id', 'is_active', 'created_date_utc', 'last_update_utc')
    search_fields = ('name', 'company_id')
    list_filter = ('is_active',)
    ordering = ('-last_update_utc',)

    fieldsets = (
        (None, {
            'fields': ('company_id', 'name', 'inquiry_required', 'appointment_required', 'is_active')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_date_utc', 'last_update_by', 'last_update_utc')
        }),
    )

@admin.register(ActivityResult)
class ActivityResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_id', 'confirmed', 'is_active', 'last_update', 'created_date')
    search_fields = ('name', 'company_id')
    list_filter = ('is_active', 'confirmed', 'count_as_appt_confirmed')
    ordering = ('-last_update',)

    fieldsets = (
        (None, {
            'fields': ('company_id', 'name', 'email_success', 'email_failure', 'confirmed', 'is_active')
        }),
        ('Counts', {
            'fields': ('count_as_appt_confirmed', 'count_as_appt_created', 'count_as_contacted')
        }),
        ('Audit Information', {
            'fields': ('last_update_by', 'last_update', 'created_by', 'created_date')
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_id', 'line1', 'city', 'state', 'zip', 'is_active')
    search_fields = ('line1', 'city', 'state', 'zip', 'contact_id')
    list_filter = ('state', 'is_active')
    ordering = ('-city',)

    fieldsets = (
        (None, {
            'fields': ('contact_id', 'line1', 'line2', 'city', 'state', 'zip', 'county', 'country')
        }),
        ('Additional Information', {
            'fields': ('carrier_route', 'cass', 'latitude', 'longitude', 'zip4', 'dpbc2', 'bar_code')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'inquiry_id', 'salesperson1_id', 'appointment_date', 'is_active', 'created_date')
    search_fields = ('id', 'type', 'inquiry_id', 'salesperson1_id')
    list_filter = ('is_active', 'type')
    ordering = ('-created_date',)

    fieldsets = (
        (None, {
            'fields': ('type', 'inquiry_id', 'salesperson1_id', 'salesperson2_id', 'set_by_id', 'result_id')
        }),
        ('Appointment Details', {
            'fields': ('appointment_date', 'set_date', 'issued_date', 'subject', 'note', 'result_reason')
        }),
        ('Status and Tracking', {
            'fields': ('is_active', 'last_update', 'last_update_by', 'created_date', 'created_by')
        }),
    )

from django.contrib import admin
from .models import AppointmentResult

@admin.register(AppointmentResult)
class AppointmentResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'presentation', 'sold', 'is_active')
    search_fields = ('name', 'id')
    list_filter = ('presentation', 'sold', 'is_active')
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Status', {
            'fields': ('presentation', 'sold', 'is_active')
        }),
    )

@admin.register(ContactPhone)
class ContactPhoneAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'cell_phone', 'work_phone', 'home_phone')
    search_fields = ('contact_id', 'cell_phone', 'work_phone', 'home_phone')
    ordering = ('contact_id',)

    fieldsets = (
        (None, {
            'fields': ('contact_id',)
        }),
        ('Phone Information', {
            'fields': (
                'assistant_phone', 'work_fax', 'cell_phone', 'company_phone',
                'home_phone2', 'home_fax', 'pager', 'work_phone2', 'company_fax',
                'home_phone', 'work_phone', 'other_phone', 'cell_phone2', 'other_phone2'
            )
        }),
    )

@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_id', 'contact_type', 'is_active')
    search_fields = ('contact_id', 'contact_type')
    list_filter = ('is_active',)
    ordering = ('id',)

    fieldsets = (
        (None, {
            'fields': ('contact_id', 'contact_type')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'contact_id')
    search_fields = ('name', 'value', 'contact_id')
    list_filter = ('name',)
    ordering = ('id',)

    fieldsets = (
        (None, {
            'fields': ('name', 'value', 'contact_id')
        }),
    )

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type_id', 'is_active', 'company_id')
    search_fields = ('name', 'product_type_id', 'company_id')
    list_filter = ('is_active', 'company_id')
    ordering = ('id',)

    fieldsets = (
        (None, {
            'fields': ('name', 'product_type_id', 'company_id')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'company_id')
    search_fields = ('name', 'company_id')
    list_filter = ('is_active',)
    ordering = ('id',)

    fieldsets = (
        (None, {
            'fields': ('name', 'company_id')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(ProductInterest)
class ProductInterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'inquiry_id', 'product_type_id', 'price_quoted', 'is_active', 'last_update')
    search_fields = ('inquiry_id', 'product_type_id', 'product_detail_id')
    list_filter = ('is_active',)
    ordering = ('-last_update',)

    fieldsets = (
        (None, {
            'fields': ('inquiry_id', 'product_type_id', 'product_detail_id')
        }),
        ('Details', {
            'fields': ('price_quoted', 'last_update')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'company_id', 'last_update')
    search_fields = ('name', 'company_id')
    list_filter = ('is_active',)
    ordering = ('-last_update',)

    fieldsets = (
        (None, {
            'fields': ('name', 'company_id')
        }),
        ('Status', {
            'fields': ('is_active', 'last_update')
        }),
    )


@admin.register(InquiryStatus)
class InquiryStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_id', 'is_active', 'last_update_utc', 'created_date_utc')
    search_fields = ('name', 'company_id', 'created_by')
    list_filter = ('is_active',)
    ordering = ('-last_update_utc',)

    fieldsets = (
        (None, {
            'fields': ('name', 'company_id', 'is_active')
        }),
        ('Audit Information', {
            'fields': ('last_update_by', 'last_update_utc', 'created_by', 'created_date_utc')
        }),
    )


@admin.register(InquirySourcePrimary)
class InquirySourcePrimaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_id', 'is_active')
    search_fields = ('name', 'id', 'company_id')
    list_filter = ('is_active',)
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'company_id')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(InquirySourceSecondary)
class InquirySourceSecondaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'inquiry_source_primary_id', 'company_id', 'is_active')
    search_fields = ('name', 'inquiry_source_primary_id', 'company_id')
    list_filter = ('is_active',)
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'inquiry_source_primary_id', 'company_id', 'is_active')
        }),
    )