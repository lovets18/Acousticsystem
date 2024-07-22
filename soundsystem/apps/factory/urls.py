from django.urls import path

from . import views

app_name = "factory"
urlpatterns = [
    path("", views.index, name="index"),
    path("add_project/", views.add_project, name="add_project"),
    path("create_project/", views.create_project, name="create_project"),
    path("<int:project_id>/", views.detail, name="detail"),
    path("measure/<int:measure_id>/", views.render_measure, name="render_measure"),
    path("<int:project_id>/addmeasure/", views.addmeasure, name="addmeasure"),
    # path('<int:project_id>/create_measure/', views.create_measure, name='create_measure'),
    # path('<int:project_id>/add_measure_/', views.model_form_upload, name='add_measure_'),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("plot_line/", views.plot_line, name="plot_line"),
    path("test", views.test, name="test"),
]
