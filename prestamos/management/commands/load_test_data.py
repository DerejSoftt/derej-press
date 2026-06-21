from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from prestamos.models import Cliente, Prestamo, Ingreso, RecibosAnulados
from random import choice, randint, uniform


CLIENTES = [
    {
        "nombres": "María",
        "apellidos": "Rodríguez",
        "numero_identificacion": "001-1234567-8",
        "genero": "female",
        "nacionalidad": "Dominicana",
        "telefono_principal": "809-555-0101",
        "telefono_secundario": "849-555-0101",
        "direccion": "Calle Las Flores #12, Ensanche Ozama",
        "ciudad": "Santo Domingo",
        "provincia": "SD",
        "tipo_cuenta": "ahorro",
        "ingresos_mensuales": Decimal("45000.00"),
        "empleador": "Ministerio de Educación",
        "telefono_laboral": "809-555-1001",
        "banco_principal": "Banco Popular",
        "numero_cuenta": "1234567890",
    },
    {
        "nombres": "Juan Carlos",
        "apellidos": "Pérez",
        "numero_identificacion": "002-2345678-9",
        "genero": "male",
        "nacionalidad": "Dominicana",
        "telefono_principal": "809-555-0202",
        "telefono_secundario": None,
        "direccion": "Av. Independencia #45, Gazcue",
        "ciudad": "Santo Domingo",
        "provincia": "DN",
        "tipo_cuenta": "corriente",
        "ingresos_mensuales": Decimal("85000.00"),
        "empleador": "Grupo Corripio",
        "telefono_laboral": "809-555-2002",
        "banco_principal": "Banco de Reservas",
        "numero_cuenta": "0987654321",
    },
    {
        "nombres": "Ana",
        "apellidos": "Santos de la Cruz",
        "numero_identificacion": "003-3456789-0",
        "genero": "female",
        "nacionalidad": "Dominicana",
        "telefono_principal": "829-555-0303",
        "telefono_secundario": "809-555-0303",
        "direccion": "Calle Principal #8, Villa Olga",
        "ciudad": "Santiago",
        "provincia": "SA",
        "tipo_cuenta": "ahorro",
        "ingresos_mensuales": Decimal("32000.00"),
        "empleador": "Clínica Corominas",
        "telefono_laboral": "809-555-3003",
        "banco_principal": "Banco Santa Cruz",
        "numero_cuenta": "4567890123",
    },
    {
        "nombres": "Pedro Antonio",
        "apellidos": "Martínez",
        "numero_identificacion": "004-4567890-1",
        "genero": "male",
        "nacionalidad": "Dominicana",
        "telefono_principal": "809-555-0404",
        "telefono_secundario": None,
        "direccion": "Carretera Luperón #78, Playa Dorada",
        "ciudad": "Puerto Plata",
        "provincia": "PU",
        "tipo_cuenta": "corriente",
        "ingresos_mensuales": Decimal("65000.00"),
        "empleador": "Hoteles Meliá",
        "telefono_laboral": "809-555-4004",
        "banco_principal": "Banco Popular",
        "numero_cuenta": "5678901234",
    },
    {
        "nombres": "Rosa",
        "apellidos": "Jiménez",
        "numero_identificacion": "005-5678901-2",
        "genero": "female",
        "nacionalidad": "Dominicana",
        "telefono_principal": "829-555-0505",
        "telefono_secundario": "849-555-0505",
        "direccion": "Calle Duarte #33, Zona Colonial",
        "ciudad": "Santo Domingo",
        "provincia": "DN",
        "tipo_cuenta": "ahorro",
        "ingresos_mensuales": Decimal("28000.00"),
        "empleador": "Farmacia Popular",
        "telefono_laboral": "809-555-5005",
        "banco_principal": "Banco BHD",
        "numero_cuenta": "6789012345",
    },
    {
        "nombres": "Luis",
        "apellidos": "García",
        "numero_identificacion": "006-6789012-3",
        "genero": "male",
        "nacionalidad": "Dominicana",
        "telefono_principal": "809-555-0606",
        "telefono_secundario": None,
        "direccion": "Av. San Martín #15, Los Prados",
        "ciudad": "Santo Domingo",
        "provincia": "DN",
        "tipo_cuenta": "corriente",
        "ingresos_mensuales": Decimal("95000.00"),
        "empleador": "Induveca",
        "telefono_laboral": "809-555-6006",
        "banco_principal": "Banco de Reservas",
        "numero_cuenta": "7890123456",
    },
    {
        "nombres": "Carmen",
        "apellidos": "Vargas",
        "numero_identificacion": "007-7890123-4",
        "genero": "female",
        "nacionalidad": "Dominicana",
        "telefono_principal": "829-555-0707",
        "telefono_secundario": "809-555-0707",
        "direccion": "Calle 27 de Febrero #22, Los Jardines",
        "ciudad": "San Cristóbal",
        "provincia": "SC",
        "tipo_cuenta": "ahorro",
        "ingresos_mensuales": Decimal("38000.00"),
        "empleador": "Ayuntamiento de San Cristóbal",
        "telefono_laboral": "809-555-7007",
        "banco_principal": "Banco Popular",
        "numero_cuenta": "8901234567",
    },
    {
        "nombres": "Miguel",
        "apellidos": "Hernández",
        "numero_identificacion": "008-8901234-5",
        "genero": "male",
        "nacionalidad": "Dominicana",
        "telefono_principal": "809-555-0808",
        "telefono_secundario": None,
        "direccion": "Calle Proyecto #5, Los Maestros",
        "ciudad": "La Vega",
        "provincia": "VE",
        "tipo_cuenta": "corriente",
        "ingresos_mensuales": Decimal("52000.00"),
        "empleador": "Agroindustrial La Vega",
        "telefono_laboral": "809-555-8008",
        "banco_principal": "Banco Santa Cruz",
        "numero_cuenta": "9012345678",
    },
    {
        "nombres": "Diana",
        "apellidos": "Castillo",
        "numero_identificacion": "009-9012345-6",
        "genero": "female",
        "nacionalidad": "Dominicana",
        "telefono_principal": "829-555-0909",
        "telefono_secundario": "849-555-0909",
        "direccion": "Av. España #100, Los Paseos",
        "ciudad": "Santo Domingo Este",
        "provincia": "SDE",
        "tipo_cuenta": "ahorro",
        "ingresos_mensuales": Decimal("41000.00"),
        "empleador": "Pinturas Tropical",
        "telefono_laboral": "809-555-9009",
        "banco_principal": "Banco BHD",
        "numero_cuenta": "0123456789",
    },
    {
        "nombres": "Roberto",
        "apellidos": "Almonte",
        "numero_identificacion": "010-0123456-7",
        "genero": "male",
        "nacionalidad": "Dominicana",
        "telefono_principal": "809-555-1010",
        "telefono_secundario": None,
        "direccion": "Calle José Martí #55, El Millón",
        "ciudad": "Santo Domingo",
        "provincia": "DN",
        "tipo_cuenta": "corriente",
        "ingresos_mensuales": Decimal("120000.00"),
        "empleador": "Teleperformance",
        "telefono_laboral": "809-555-0010",
        "banco_principal": "Banco de Reservas",
        "numero_cuenta": "1122334455",
    },
]

DEPARTAMENTOS = ["ayuntamiento", "ferquido", "choga", "financiamiento", "personal"]
METODOS_PAGO_PRESTAMO = ["efectivo", "transferencia", "cheque"]
METODOS_PAGO_INGRESO = ["EFECTIVO", "TARJETA", "TRANSFERENCIA", "CHEQUE"]
TIPOS_PAGO = ["COMPLETO", "ABONO"]
MOTIVOS_ANULACION = ["ERROR_MONTO", "RECIBO_DUPLICADO", "SOLICITUD_CLIENTE", "ERROR_SISTEMA"]


class Command(BaseCommand):
    help = "Carga datos de prueba en la base de datos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Elimina los datos existentes antes de cargar (no afecta auth.User)",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=5,
            help="Número de clientes a crear (default: 5, max: 10)",
        )

    def handle(self, *args, **options):
        count = min(options["count"], len(CLIENTES))

        if options["clear"]:
            self._clear_data()

        clientes = self._create_clientes(count)
        prestamos = self._create_prestamos(clientes)
        self._create_ingresos(prestamos)
        self._create_recibos_anulados(prestamos)

        self.stdout.write(self.style.SUCCESS(
            f"\nDatos de prueba cargados exitosamente:"
            f"\n  Clientes: {len(clientes)}"
            f"\n  Préstamos: {len(prestamos)}"
            f"\n  Ingresos: {len(Ingreso.objects.filter(anulado=False))}"
            f"\n  Recibos anulados: {len(RecibosAnulados.objects.all())}"
        ))

    def _clear_data(self):
        self.stdout.write("Eliminando datos existentes...")
        RecibosAnulados.objects.all().delete()
        Ingreso.objects.all().delete()
        Prestamo.objects.all().delete()
        Cliente.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Datos eliminados."))

    def _create_clientes(self, count):
        self.stdout.write(f"Creando {count} clientes...")
        clientes = []
        for data in CLIENTES[:count]:
            cliente, created = Cliente.objects.get_or_create(
                numero_identificacion=data["numero_identificacion"],
                defaults=data,
            )
            clientes.append(cliente)
            if created:
                self.stdout.write(f"  + {cliente.nombres} {cliente.apellidos}")
            else:
                self.stdout.write(f"  = {cliente.nombres} {cliente.apellidos} (ya existe)")
        return clientes

    def _create_prestamos(self, clientes):
        self.stdout.write("Creando préstamos...")
        prestamos = []
        today = date.today()

        prestamo_data = [
            {"departamento": "personal", "monto": Decimal("50000.00"), "metodo_pago": "efectivo", "dias_atras": 0, "estado": "ACTIVO"},
            {"departamento": "personal", "monto": Decimal("150000.00"), "metodo_pago": "transferencia", "dias_atras": 15, "estado": "ACTIVO"},
            {"departamento": "ayuntamiento", "monto": Decimal("200000.00"), "metodo_pago": "cheque", "dias_atras": 60, "estado": "VENCIDO"},
            {"departamento": "ferquido", "monto": Decimal("75000.00"), "metodo_pago": "efectivo", "dias_atras": 0, "estado": "ACTIVO"},
            {"departamento": "choga", "monto": Decimal("120000.00"), "metodo_pago": "transferencia", "dias_atras": 30, "estado": "ACTIVO"},
            {"departamento": "financiamiento", "monto": Decimal("300000.00"), "metodo_pago": "cheque", "dias_atras": 90, "estado": "VENCIDO"},
            {"departamento": "personal", "monto": Decimal("25000.00"), "metodo_pago": "efectivo", "dias_atras": 0, "estado": "ACTIVO"},
            {"departamento": "ayuntamiento", "monto": Decimal("80000.00"), "metodo_pago": "transferencia", "dias_atras": 5, "estado": "ACTIVO"},
        ]

        for i, data in enumerate(prestamo_data):
            cliente = clientes[i % len(clientes)]
            fecha_despacho = today - timedelta(days=data["dias_atras"] + 30)
            prestamo, created = Prestamo.objects.get_or_create(
                numero_factura=f"FAC-{i+1:04d}",
                defaults={
                    "cliente": cliente,
                    "monto": data["monto"],
                    "fecha_despacho": fecha_despacho,
                    "fecha_vencimiento": fecha_despacho + timedelta(days=30),
                    "metodo_pago": data["metodo_pago"],
                    "departamento": data["departamento"],
                    "estado": data["estado"],
                    "telefono": cliente.telefono_principal,
                },
            )
            prestamos.append((prestamo, created))
            if created:
                self.stdout.write(f"  + {prestamo} ({data['departamento']}, ${data['monto']})")
            else:
                self.stdout.write(f"  = {prestamo} (ya existe)")

        return prestamos

    def _create_ingresos(self, prestamos):
        self.stdout.write("Creando ingresos (pagos)...")
        ingresos = []
        today = date.today()
        recibo_count = 1

        for prestamo, was_created in prestamos[:5]:
            if not was_created:
                continue
            num_pagos = randint(1, 3)
            for j in range(num_pagos):
                monto_pago = prestamo.monto / Decimal(str(num_pagos))
                monto_pago = monto_pago.quantize(Decimal("0.01"))
                fecha_pago = prestamo.fecha_despacho + timedelta(days=(j + 1) * 10)

                ingreso, created = Ingreso.objects.get_or_create(
                    no_recibo=f"REC-{recibo_count:04d}",
                    defaults={
                        "prestamo": prestamo,
                        "monto_pago": monto_pago,
                        "fecha_pago": min(fecha_pago, today),
                        "metodo_pago": choice(METODOS_PAGO_INGRESO),
                        "tipo_pago": choice(TIPOS_PAGO),
                        "notas": f"Pago {j + 1} de {num_pagos} para {prestamo}",
                    },
                )
                if created:
                    ingresos.append(ingreso)
                recibo_count += 1

        self.stdout.write(f"  {len(ingresos)} ingresos creados")
        return ingresos

    def _create_recibos_anulados(self, prestamos):
        self.stdout.write("Creando recibos anulados...")
        anulados = []

        recibos_data = [
            {
                "no_recibo": "ANU-0001",
                "monto_pago": Decimal("25000.00"),
                "dias_pago": -5,
                "metodo_pago": "EFECTIVO",
                "tipo_pago": "ABONO",
                "motivo": "ERROR_MONTO",
                "notas_anulacion": "Error en el monto registrado por el cajero",
            },
            {
                "no_recibo": "ANU-0002",
                "monto_pago": Decimal("50000.00"),
                "dias_pago": -10,
                "metodo_pago": "TRANSFERENCIA",
                "tipo_pago": "COMPLETO",
                "motivo": "RECIBO_DUPLICADO",
                "notas_anulacion": "Recibo duplicado generado por error del sistema",
            },
        ]

        for i, data in enumerate(recibos_data):
            prestamo = prestamos[i % len(prestamos)][0]
            fecha_pago = date.today() + timedelta(days=data["dias_pago"])
            fecha_anulacion = fecha_pago + timedelta(days=1)

            obj, created = RecibosAnulados.objects.get_or_create(
                no_recibo=data["no_recibo"],
                defaults={
                    "prestamo": prestamo,
                    "monto_pago": data["monto_pago"],
                    "fecha_pago": fecha_pago,
                    "metodo_pago": data["metodo_pago"],
                    "tipo_pago": data["tipo_pago"],
                    "notas": f"Pago anulado correspondiente a {prestamo}",
                    "fecha_registro": timezone.now(),
                    "motivo_anulacion": data["motivo"],
                    "notas_anulacion": data["notas_anulacion"],
                    "fecha_anulacion": fecha_anulacion,
                    "anulado_por": None,
                },
            )
            if created:
                anulados.append(data["no_recibo"])

        self.stdout.write(f"  {len(anulados)} recibos anulados creados")
