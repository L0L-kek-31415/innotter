class SerializersMixin:
    def get_serializer_class(self):
        return self.serializer_action_classes.get(
            self.action, super().get_serializer_class()
        )

    def check_permissions(self, request):
        handler = getattr(self, request.method.lower(), None)
        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(
                handler.__name__
            )
        super().check_permissions(request)
