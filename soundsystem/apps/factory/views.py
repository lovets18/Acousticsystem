from smtplib import SMTPAuthenticationError

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView
from .forms import *

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import Project, Measure
from .process_1d import get_polar_data

from django.core.mail import send_mail

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import plot

# from matplotlib import pylab
# from pylab import *
# import PIL, PIL.Image
# import io
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# import matplotlib
# matplotlib.use('Agg')


def index(request):
    projects_list = Project.objects.order_by('-update_date')[:5]
    return render(request, 'factory/list.html', {'projects_list': projects_list})


def detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        raise Http404('Проект не найден')
    measures_list = project.measure_set.order_by('-id')  # [:size]
    intensity = project.track_intensity()
    fig = px.line(intensity, x="date", y="intensity", title='mean measure intensity')
    story = plot(fig, output_type="div")
    return render(
        request,
        'factory/detail.html',
        {'project': project, 'measures': measures_list, 'intensity': intensity, 'story': story})


def signal(project, measure):
    send_mail(
        'Отклоение оборудования от нормальноего режима работы',
        f'В рамках проекта {project} при измерении {measure} было обнаружено отклонение шума, '
        f'издаваемого оборудованием от нормального режима работы.',
        'lovets1818@gmail.com',
        ['lovtsov2001@bk.ru'],
        fail_silently=False,
    )


def addmeasure(request, project_id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(id=project_id)
        except:
            raise Http404('Проект не найден')

        # print(request.FILES['data'].read())

        from django.core.files.base import ContentFile
        file = request.FILES['data']
        processed_data = get_polar_data(
            file,
            # int(request.POST['direct_start']),
            # int(request.POST['direct_stop'])
        )
        content = processed_data.to_csv(index=False)
        temp_file = ContentFile(content.encode('utf-8'), 'processed.csv')

        print(type(request.FILES['data']))

        start = int(request.POST['direct_start'])
        stop = int(request.POST['direct_stop'])
        mean_intensity = processed_data.query(
            '@start <= phi <= @stop'
        ).r.mean()
        now = timezone.now()
        project.update_date = now
        project.save()
        project.measure_set.create(
            author_name=request.user, # request.POST['author_name'],
            measure_name=request.POST['measure_name'],
            date=now,
            data=request.FILES['data'],
            processed_data=temp_file,
            direct_start=start,
            direct_stop=stop,
            mean_intensity=mean_intensity
        )
        minimal = project.min_intensity
        maximum = project.max_intensity
        if mean_intensity > maximum or mean_intensity < minimal:
            print('Отклонение от нормального режима работы')
            try:
                signal(project, request.POST['measure_name'])
            except SMTPAuthenticationError:
                print('not authenticated email')
        # return redirect(f'factory:detail/{project_id}')
        return HttpResponseRedirect(reverse('factory:detail', args=(project_id, )))
    else:
        form = MeasureForm()
    return render(request, 'factory/addmeasure.html', {
        'form': form
    })


def render_measure(request, measure_id):
    try:
        measure = Measure.objects.get(id = measure_id)
    except:
        raise Http404('Проект не найден')
    # import plotly.express as px
    # from plotly.offline import plot

    df = pd.read_csv(measure.processed_data)
    max_range = df.r.max()
    fig = px.line_polar(df,
                        r="r",
                        theta="phi",
                        line_close=True,
                        animation_frame="iter",
                        range_r=[0, max_range * 1.1],
                        start_angle=0,
                        direction='counterclockwise',
                        width=1200, height=380,
                        )
    sound = plot(fig, output_type="div")
    df_copy = df.copy()
    df_copy['y'] = 1
    fig2 = px.density_heatmap(
        df_copy, y="y", z="r", x="phi",
        animation_frame="iter",
        histfunc="avg", nbinsx=50,
        color_continuous_scale=px.colors.sequential.Jet,
        labels={'phi':'угол', 'y':'', 'r':'интенсивность'},
        width=1200, height=380,
        )
    fig2.update_xaxes(autorange="reversed")
    fig2.update_yaxes(showticklabels=False)
    heatmap = plot(fig2, output_type="div")
    context = {'plot_div': sound, 'plot_heatmap': heatmap, 'measure': measure}
    return render(request, 'factory/render_measure.html', context)


def create_measure(request, project_id):
    return redirect(f'factory:detail/{project_id}')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'factory/register.html'

    success_url = reverse_lazy('factory:login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'factory/login.html'
    # success_url = reverse_lazy('factory:login')


def logout_user(request):
    logout(request)
    return redirect('factory:login')


def add_project(request):
    return render(request, 'factory/add_project.html')


def create_project(request):
    project = Project(
        project_name=request.POST['project_name'],
        project_description=request.POST['project_description'],
        create_date=timezone.now(),
        update_date=timezone.now(),
        is_monitored='monitoring' in request.POST.keys(),
    )

    project.save()
    return redirect('factory:index')


def test(request):
    return HttpResponse('test')


def model_form_upload(request, project_id):
    if request.method == 'POST':

        try:
            project = Project.objects.get(id=project_id)
        except:
            raise Http404('Проект не найден')

        # project.measure_set.create()
        print(request.FILES['data'].read())

        project.measure_set.create(
            author_name=request.POST['author_name'],
            measure_name=request.POST['measure_name'],
            date=timezone.now(),
            data=request.FILES['data'],  # POST['measure_data'],
        )

        # form = MeasureForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        #
        return redirect('factory:index')
    else:
        form = MeasureForm()
    return render(request, 'factory/add_measure_.html', {
        'form': form
    })


def plot_line(request):
    # import plotly.express as px
    from plotly.offline import plot
    # df = px.data.wind()
    # fig = px.line_polar(df, r="frequency", theta="direction", color="strength", line_close=True,
    #                     color_discrete_sequence=px.colors.sequential.Plasma_r)
    df = px.data.gapminder()
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                     size="pop", color="continent", hover_name="country", facet_col="continent",
                     log_x=True, size_max=45, range_x=[100, 100000], range_y=[25, 90])

    # fig = get_polar_plot()

    # canvas = FigureCanvasAgg(fig)
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format='png')
    # plt.close(fig)
    sound = plot(fig, output_type="div")
    context = {'plot_div': sound}
    # return HttpResponse(buffer.getvalue(), content_type='image/png')
    return render(request, 'factory/plot_line.html', context)
