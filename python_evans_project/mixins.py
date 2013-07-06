from django.core.exceptions import ImproperlyConfigured, PermissionDenied


class OwnerOrSuperUserRequiredMixin:
    owner_path = "user"

    def check_permission(self, request):
        if request.user.is_staff:
            return True  # Superusers are allowed to do anything

        obj = (hasattr(self, 'get_object') and self.get_object()
               or getattr(self, 'object', None))

        if not hasattr(obj, self.owner_path):
            raise ImproperlyConfigured("'OwnerOrSuperUserRequiredMixin' requires "
                                       "'owner_path' attribute to be set to object's user path"
                                       "(e.g. owner)")

        user = getattr(obj, self.owner_path)
        if user == request.user:
            return True  # The current user is the owner, he has permission
        else:
            return False

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        allowed = self.check_permission(request)
        if not allowed:
            raise PermissionDenied()
        return super(OwnerOrSuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)
