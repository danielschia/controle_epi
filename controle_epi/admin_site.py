from django.contrib.admin import AdminSite


class SuperuserAdminSite(AdminSite):
    site_header = "Controle EPI Admin"
    site_title = "Controle EPI Admin"
    index_title = "Administração - Controle de EPI"

    def has_permission(self, request):
        """Allow access only to active superusers.

        By default Django's AdminSite checks for is_active and is_staff. We restrict
        this further to require is_superuser so regular staff (e.g., Gerentes) can't access /admin.
        """
        return bool(request.user and request.user.is_active and request.user.is_superuser)


admin_site = SuperuserAdminSite(name="superuser_admin")
