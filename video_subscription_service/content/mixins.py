from django.shortcuts import redirect
from django.contrib import messages


class CancelledPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user.subscription
        if user.status == "canceled":
            messages.info(
                request, "Your membership has been cancelled, please re-subscribe."
            )
            return redirect("content:course-list")
        return super().dispatch(request, *args, **kwargs)
