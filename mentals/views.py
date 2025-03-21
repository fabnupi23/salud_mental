from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CrearCitas
from .models import Appointment
from django.utils import timezone


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": "Usuario existente"
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": "Contraseña no coincide"
                })

@login_required #Decorador
def citas_completadas(request):
    # Filtrar citas completadas y que pertenezcan al usuario actual
    citas = Appointment.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted')
    return render(request, 'citas.html', {'citas': citas})

@login_required
# Definir la función 'agendar' que maneja solicitudes relacionadas con la agenda de citas
def agendar(request):
    # Verificar si el método de la solicitud es GET
    if request.method == 'GET':
        # Renderizar la plantilla 'agenda_citas.html' y enviar un formulario vacío para crear citas
        return render(request, 'agenda_citas.html', {
            'form': CrearCitas()  # Formulario para agendar citas
        })
    # Verificar si el método de la solicitud es POST
    elif request.method == 'POST':
        try:
            # Crear una instancia del formulario con los datos enviados en la solicitud
            form = CrearCitas(request.POST)
            # Verificar si los datos del formulario son válidos
            if form.is_valid():
                # Crear un objeto de agenda, pero no guardar todavía en la base de datos
                new_agenda = form.save(commit=False)
                # Asignar al campo 'user' el usuario que está realizando la solicitud
                new_agenda.user = request.user
                # Verificar si el campo 'date' no tiene un valor
                if not new_agenda.date:
                    # Asignar la fecha y hora actual al campo 'date'
                    new_agenda.date = timezone.now()
                # Guardar el nuevo objeto de agenda en la base de datos
                new_agenda.save()
                # Redirigir al detalle de la cita recién creada
                return redirect('cita_detail', cita_id=new_agenda.id)
            else:
                # Lanzar un error si los datos del formulario no son válidos
                raise ValueError("Datos inválidos")
        except ValueError as e:
            # Renderizar la plantilla 'agenda_citas.html' con el formulario vacío y un mensaje de error
            return render(request, 'agenda_citas.html', {
                'form': CrearCitas(),
                'error': str(e)  # Mostrar el error en la página
            })
        except Exception as e:
            # Devolver una respuesta de error genérica si ocurre un error inesperado
            return HttpResponse(f"Ha ocurrido un error inesperado: {e}", status=500)
    else:
        # Responder con un error 405 si el método de la solicitud no está permitido
        return HttpResponse("Método no permitido", status=405)

@login_required
# Definir la función 'cita_detail' para manejar la visualización y edición de una cita específica
def cita_detail(request, cita_id):
    try:
        # Buscar la cita correspondiente al ID proporcionado o devolver un error 404 si no existe
        cita = get_object_or_404(Appointment, pk=cita_id, user=request.user)

        # Manejar la solicitud si el método HTTP es GET
        if request.method == 'GET':
            # Crear un formulario prellenado con los datos de la cita existente
            form = CrearCitas(instance=cita)
            # Renderizar la plantilla 'cita_detail.html' con la cita y el formulario
            return render(request, 'cita_detail.html', {'cita': cita, 'form': form})
        
        # Manejar la solicitud si el método HTTP es POST
        elif request.method == 'POST':
            # Crear un formulario con los datos enviados por el usuario, asociándolo a la cita existente
            form = CrearCitas(request.POST, instance=cita)
            # Verificar si los datos del formulario son válidos
            if form.is_valid():
                # Guardar los cambios realizados en la cita
                form.save()
                # Redirigir al usuario a la lista de citas después de guardar los cambios
                return redirect('citas')
            else:
                # Si el formulario no es válido, volver a renderizar la plantilla con un mensaje de error
                return render(request, 'cita_detail.html', {
                    'cita': cita,          # Pasar la cita para mostrar sus detalles
                    'form': form,          # Enviar el formulario con errores para corregirlos
                    'error': 'Por favor, proveer datos válidos'  # Mensaje de error para el usuario
                })
        
        # Si el método HTTP no es GET ni POST, devolver una respuesta con error 405 (Método no permitido)
        else:
            return HttpResponse("Método no permitido", status=405)

    except Appointment.DoesNotExist:
        # Manejar el caso en que la cita no se encuentra en la base de datos
        return HttpResponse("La cita solicitada no existe.", status=404)
    
    except Exception as e:
        # Manejar cualquier otro error inesperado
        return HttpResponse(f"Ha ocurrido un error inesperado: {e}", status=500)

@login_required
def complete_task(request, cita_id):
    task = get_object_or_404(Appointment, pk=cita_id, user=request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('citas')

@login_required
def delete_task(request, cita_id):
    task = get_object_or_404(Appointment, pk=cita_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('citas')

            
@login_required
def citas(request):
    cit = Appointment.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'citas.html', {'citas': cit})       

    
@login_required
def seguimiento(request):
    return render(request, 'seguimiento.html')


@login_required
def recursos(request):
    return render(request, 'recursos_autoayuda.html')


@login_required
def telepsicologia(request):
    return render(request, 'telepsicologia.html')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        
        else:
            login(request, user)
            return redirect('/')
        
        

@login_required
def signout(request):
    logout(request)
    return redirect("/")