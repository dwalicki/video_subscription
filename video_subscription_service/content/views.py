from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CancelledPermissionMixin
from django.db.models import Exists, OuterRef
from .models import Course, Video, Subscription


class CourseListView(generic.ListView):
    template_name = "content/course_list.html"
    queryset = Course.objects.all()


class CourseDetailView(generic.DetailView):
    template_name = "content/course_detail.html"
    queryset = Course.objects.all()


class VideoDetailView(LoginRequiredMixin, CancelledPermissionMixin, generic.DetailView):
    template_name = "content/video_detail.html"

    def get_object(self):
        return get_object_or_404(
            Video.objects.annotate(
                has_permission=Exists(
                    Subscription.objects.filter(
                        user=self.request.user,
                        pricing__course__videos__id=OuterRef("id"),
                    )
                )
            ).filter(
                slug=self.kwargs["video_slug"],
                course__slug=self.kwargs["slug"],
            )
        )
