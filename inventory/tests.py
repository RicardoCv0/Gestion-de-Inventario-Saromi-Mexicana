from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Gemstone, EntryMovement, ExitMovement, AdjustmentMovement

class ExampleTestCase(TestCase):
    def setUp(self):
        create_users()

    # CP001 Validate correct entry with the "surtidor" role
    def test_valid_entry(self):
        prepare_test_one()

        # Assert preconditions
        try: required_user = User.objects.get(username='surtidor')
        except: required_user = None
        self.assertNotEqual(required_user, None, "Precondición fallida: Usuario surtidor no existe")

        try: required_gemstone = Gemstone.objects.get(pk="A1234")
        except: required_gemstone = None
        self.assertNotEqual(required_gemstone, None, "Precondición fallida: Piedra A1234 no existe")

        # Log in as "surtidor"
        client = Client()
        context = {
            'username': 'surtidor',
            'password': 'surtidor',
        }
        response = client.post('/users/login/', context)
        self.assertEqual(response.status_code, 302, "Iniciar sesión con estas credenciales debería redireccionarte al dashboard de materiales")

        # Register gemstone entry
        expected_ammount = required_gemstone.ammount_available + 50
        context = {'ammount': 50}
        response = client.post('/inventory/entry/A1234/', context)
        new_ammount = Gemstone.objects.get(pk="A1234").ammount_available
        self.assertEqual(new_ammount, expected_ammount, f"Fallo en la entrada de material, la cantidad registrada es: {new_ammount} y debería ser: {expected_ammount}")

        # Redirect user to the dashboard
        self.assertEqual(response.url, '/', f"Fallo en el redireccionamiento, el usuario fué redireccionado a: {response.url}")

        # Confirm movement was stored on the database
        try: movement = EntryMovement.objects.order_by('pk').last()
        except: movement = None
        self.assertNotEqual(movement, None, "No se guardó ningún movimiento en la base de datos")
        self.assertEqual(movement.type, "entry", f"El tipo de movimiento debe ser 'entry', pero se guardó como {movement.type}")
        self.assertEqual(movement.ammount, 50.0, f"La cantidad modificada fué 50, pero se guardó {movement.ammount}")

    # CP002 Validate invalid entry with the "surtidor" role
    #def test_valid_entry(self):
    #    pass


def create_users():
    # Definir Usuario Gerente
    gerente = User.objects.create(username='gerente')
    gerente.set_password('gerente')
    gerente.userprofile.role = "gerente"
    gerente.save()

    # Definir Usuario Supervisor
    supervisor = User.objects.create(username='supervisor')
    supervisor.set_password('supervisor')
    supervisor.userprofile.role = "supervisor"
    supervisor.save()

    # Definir Usuario Surtidor
    surtidor = User.objects.create(username='surtidor')
    surtidor.set_password('surtidor')
    surtidor.userprofile.role = "surtidor"
    surtidor.save()

    # Definir Usuario Asistente
    asistente = User.objects.create(username='asistente')
    asistente.set_password('asistente')
    asistente.userprofile.role = "asistente"
    asistente.save()

def prepare_test_one():
    ruby = Gemstone.objects.create(id="A1234", type='Rubí', name='Rubí Rojo', ammount_available=100.0)
    ruby.save()