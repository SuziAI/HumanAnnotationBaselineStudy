from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "suziai_human_annotation/core/home.html"

    def get_context_data(self, **kwargs):
        # Add custom data to the context
        context = super().get_context_data(**kwargs)
        context["message"] = "Welcome to the Home Page!"
        return context
