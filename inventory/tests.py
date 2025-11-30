from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Gemstone, EntryMovement, ExitMovement, AdjustmentMovement

class ExampleTestCase(TestCase):
    def setUp(self):
        create_users()
    
    # CP001 Test correct entry with the "surtidor" role
    def test_valid_entry(self):
        create_mock_gemstone()

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

    # CP002 Test incorrect entry with the "surtidor" role
    def test_invalid_entry(self):
        create_mock_gemstone()

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

        # Register empty gemstone entry
        movement_count_before = EntryMovement.objects.count()
        response = client.post('/inventory/entry/A1234/')
        gemstone_after = Gemstone.objects.get(pk="A1234")
        self.assertEqual(required_gemstone, gemstone_after, f"La piedra preciosa fué modificada con una entrada inválida")

        # Confirm movement was NOT stored on the database
        movement_count_after = EntryMovement.objects.count()
        self.assertEqual(movement_count_before, movement_count_after, f"Se registró un movimiento cuando no se realizó ningún cambio")

    # CP003 Test correct exit with the "surtidor" role
    def test_valid_exit(self):
        create_mock_gemstone()

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

        # Register gemstone exit
        expected_ammount = required_gemstone.ammount_available - 20
        context = {'ammount': 20, 'destination': 'prod'}
        response = client.post('/inventory/exit/A1234/', context)
        new_ammount = Gemstone.objects.get(pk="A1234").ammount_available
        self.assertEqual(new_ammount, expected_ammount, f"Fallo en la entrada de material, la cantidad registrada es: {new_ammount} y debería ser: {expected_ammount}")

        # Redirect user to the dashboard
        self.assertEqual(response.url, '/', f"Fallo en el redireccionamiento, el usuario fué redireccionado a: {response.url}")

        # Confirm movement was stored on the database
        try: movement = ExitMovement.objects.order_by('pk').last()
        except: movement = None
        self.assertNotEqual(movement, None, "No se guardó ningún movimiento en la base de datos")
        self.assertEqual(movement.type, "exit", f"El tipo de movimiento debe ser 'exit', pero se guardó como {movement.type}")
        self.assertEqual(movement.ammount, 20.0, f"La cantidad modificada fué 20, pero se guardó {movement.ammount}")

    # CP004 Test incorrect exit with the "surtidor" role
    def test_invalid_exit(self):
        create_mock_gemstone()

        # Assert preconditions
        try: required_user = User.objects.get(username='surtidor')
        except: required_user = None
        self.assertNotEqual(required_user, None, "Precondición fallida: Usuario surtidor no existe")

        try: required_gemstone = Gemstone.objects.get(pk="A1234")
        except: required_gemstone = None
        self.assertNotEqual(required_gemstone, None, "Precondición fallida: Piedra A1234 no existe")
        required_gemstone.ammount_available = 10.0
        required_gemstone.save()

        # Log in as "surtidor"
        client = Client()
        context = {
            'username': 'surtidor',
            'password': 'surtidor',
        }
        response = client.post('/users/login/', context)
        self.assertEqual(response.status_code, 302, "Iniciar sesión con estas credenciales debería redireccionarte al dashboard de materiales")

        # Register invalid gemstone exit
        movement_count_before = ExitMovement.objects.count()
        context = {'ammount': 20, 'destination': 'prod'}
        response = client.post('/inventory/exit/A1234/', context)
        gemstone_after = Gemstone.objects.get(pk="A1234")
        self.assertEqual(required_gemstone, gemstone_after, f"La piedra preciosa fué modificada con una entrada inválida")

        # Confirm movement was NOT stored on the database
        movement_count_after = ExitMovement.objects.count()
        self.assertEqual(movement_count_before, movement_count_after, f"Se registró un movimiento cuando no se realizó ningún cambio")
    
    #CP005 Test correct adjustment with the "Asistente" role
    def test_valid_adjustment(self):
        create_mock_gemstone()

        # Assert preconditions
        try: required_user = User.objects.get(username='asistente')
        except: required_user = None
        self.assertNotEqual(required_user, None, "Precondición fallida: Usuario asistente no existe")

        try: required_gemstone = Gemstone.objects.get(pk="A1234")
        except: required_gemstone = None
        self.assertNotEqual(required_gemstone, None, "Precondición fallida: Piedra A1234 no existe")
        required_gemstone.ammount_available = 200.0
        required_gemstone.save()

        # Log in as "asistente"
        client = Client()
        context = {
            'username': 'asistente',
            'password': 'asistente',
        }
        response = client.post('/users/login/', context)
        self.assertEqual(response.status_code, 302, "Iniciar sesión con estas credenciales debería redireccionarte al dashboard de materiales")

        # Make valid adjustment
        context = {'ammount':195.0, 'motive':'damage'}
        response = client.post('/inventory/adjustment/A1234/', context)
        gemstone_after = Gemstone.objects.get(pk="A1234")
        self.assertEqual(gemstone_after.ammount_available, 195.0, f"La cantidad disponible debería ser 195.0, pero fué {gemstone_after.ammount_available}")
        
        # Confirm movement was stored on the database
        try: movement = AdjustmentMovement.objects.order_by('pk').last()
        except: movement = None
        self.assertNotEqual(movement, None, "No se guardó ningún movimiento en la base de datos")
        self.assertEqual(movement.type, "adjustment", f"El tipo de movimiento debe ser 'adjustment', pero se guardó como {movement.type}")
        self.assertEqual(movement.ammount, 195.0, f"La cantidad modificada fué 195.0, pero se guardó {movement.ammount}")
    
    #CP006 Test incorrect Adjustment with the "Asistente" role
    def test_invalid_adjustment(self):
        create_mock_gemstone()

        # Assert preconditions
        try: required_user = User.objects.get(username='asistente')
        except: required_user = None
        self.assertNotEqual(required_user, None, "Precondición fallida: Usuario asistente no existe")

        try: required_gemstone = Gemstone.objects.get(pk="A1234")
        except: required_gemstone = None
        self.assertNotEqual(required_gemstone, None, "Precondición fallida: Piedra A1234 no existe")

        # Log in as "asistente"
        client = Client()
        context = {
            'username': 'asistente',
            'password': 'asistente',
        }
        response = client.post('/users/login/', context)
        self.assertEqual(response.status_code, 302, "Iniciar sesión con estas credenciales debería redireccionarte al dashboard de materiales")

        # Register invalid gemstone adjustment
        movement_count_before = AdjustmentMovement.objects.count()
        context = {'ammount':195.0, 'motive':''}
        response = client.post('/inventory/exit/A1234/', context)
        gemstone_after = Gemstone.objects.get(pk="A1234")
        self.assertEqual(required_gemstone, gemstone_after, f"La piedra preciosa fué modificada con una entrada inválida")

        # Confirm movement was NOT stored on the database
        movement_count_after = AdjustmentMovement.objects.count()
        self.assertEqual(movement_count_before, movement_count_after, f"Se registró un movimiento cuando no se realizó ningún cambio")
    
    #CP007, CP008  
    def test_user_permissions():
        pass

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

def create_mock_gemstone():
    ruby = Gemstone.objects.create(id="A1234", type='Rubí', name='Rubí Rojo', ammount_available=80.0)
    ruby.save()