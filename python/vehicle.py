import math
from dataclasses import dataclass
from functools import wraps

from pysamp.player import Player
from pysamp.timer import set_timer
from pysamp.vehicle import Vehicle as BaseVehicle

from .libs.utils.consts import ID_NONE, NO_VEHICLE_OWNER, TIMER_ID_NONE
from .libs.utils.data import ServerMode


@dataclass
class VehicleTypes:
    LOWRIDER = "Лоурайдеры"
    OFFROAD = "Внедорожники"
    SERVICES = "Гос. службы"
    SEDAN = "Седаны"
    SPORT = "Спортивные"
    UNIVERSAL = "Универсалы"
    UNIQE = "Уникальные"


@dataclass
class VehicleData:
    """
    Key: id
    Values: (type, name, price)
    """
    data = {
        412: (VehicleTypes.LOWRIDER, "Voodoo", 1000),
        534: (VehicleTypes.LOWRIDER, "Remington", 1000),
        535: (VehicleTypes.LOWRIDER, "Slamvan", 1000),
        536: (VehicleTypes.LOWRIDER, "Blade", 1000),
        566: (VehicleTypes.LOWRIDER, "Tahoma", 1000),
        567: (VehicleTypes.LOWRIDER, "Savanna", 1000),
        575: (VehicleTypes.LOWRIDER, "Broadway", 1000),
        576: (VehicleTypes.LOWRIDER, "Tornado", 1000),

        400: (VehicleTypes.OFFROAD, "Landstalker", 5000),
        424: (VehicleTypes.OFFROAD, "BF Injection", 5000),
        444: (VehicleTypes.OFFROAD, "Monster", 5000),
        470: (VehicleTypes.OFFROAD, "Patriot", 5000),
        489: (VehicleTypes.OFFROAD, "Rancher", 5000),
        495: (VehicleTypes.OFFROAD, "Sandking", 5000),
        500: (VehicleTypes.OFFROAD, "Mesa", 5000),
        556: (VehicleTypes.OFFROAD, "Monster A", 5000),
        557: (VehicleTypes.OFFROAD, "Monster B", 5000),
        568: (VehicleTypes.OFFROAD, "Bandito", 5000),
        573: (VehicleTypes.OFFROAD, "Dune", 5000),
        579: (VehicleTypes.OFFROAD, "Huntley", 5000),

        407: (VehicleTypes.SERVICES, "Firetruck", 5000),
        416: (VehicleTypes.SERVICES, "Ambulance", 5000),
        420: (VehicleTypes.SERVICES, "Taxi", 5000),
        427: (VehicleTypes.SERVICES, "Enforcer", 5000),
        431: (VehicleTypes.SERVICES, "Bus", 5000),
        433: (VehicleTypes.SERVICES, "Barracks", 5000),
        437: (VehicleTypes.SERVICES, "Coach", 5000),
        438: (VehicleTypes.SERVICES, "Cabbie", 5000),
        490: (VehicleTypes.SERVICES, "FBI Rancher", 5000),
        523: (VehicleTypes.SERVICES, "HPV1000", 5000),
        528: (VehicleTypes.SERVICES, "FBI Truck", 5000),
        544: (VehicleTypes.SERVICES, "Firetruck LA", 5000),
        596: (VehicleTypes.SERVICES, "Police Car (LSPD)", 5000),
        597: (VehicleTypes.SERVICES, "Police Car (SFPD)", 5000),
        598: (VehicleTypes.SERVICES, "Police Car (LVPD)", 5000),
        599: (VehicleTypes.SERVICES, "Police Ranger", 5000),
        601: (VehicleTypes.SERVICES, "S.W.A.T", 5000),

        445: (VehicleTypes.SEDAN, "Admiral", 5000),
        504: (VehicleTypes.SEDAN, "Bloodring", 5000),
        401: (VehicleTypes.SEDAN, "Bravura", 5000),
        518: (VehicleTypes.SEDAN, "Buccaneer", 5000),
        527: (VehicleTypes.SEDAN, "Cadrona", 5000),
        542: (VehicleTypes.SEDAN, "Clover", 5000),
        507: (VehicleTypes.SEDAN, "Elegant", 5000),
        585: (VehicleTypes.SEDAN, "Emperor", 5000),
        419: (VehicleTypes.SEDAN, "Esperanto", 5000),
        526: (VehicleTypes.SEDAN, "Fortune", 5000),
        466: (VehicleTypes.SEDAN, "Glendale", 5000),
        492: (VehicleTypes.SEDAN, "Greenwood", 5000),
        474: (VehicleTypes.SEDAN, "Hermes", 5000),
        517: (VehicleTypes.SEDAN, "Majestic", 5000),
        410: (VehicleTypes.SEDAN, "Manana", 5000),
        551: (VehicleTypes.SEDAN, "Merit", 5000),
        516: (VehicleTypes.SEDAN, "Nebula", 5000),
        467: (VehicleTypes.SEDAN, "Oceanic", 5000),
        426: (VehicleTypes.SEDAN, "Premier", 5000),
        540: (VehicleTypes.SEDAN, "Previon", 5000),
        436: (VehicleTypes.SEDAN, "Primo", 5000),
        405: (VehicleTypes.SEDAN, "Sentinel", 5000),
        580: (VehicleTypes.SEDAN, "Stafford", 5000),
        550: (VehicleTypes.SEDAN, "Sunrise", 5000),
        549: (VehicleTypes.SEDAN, "Tampa", 5000),
        540: (VehicleTypes.SEDAN, "Vincent", 5000),
        491: (VehicleTypes.SEDAN, "Virgo", 5000),
        421: (VehicleTypes.SEDAN, "Washington", 5000),
        529: (VehicleTypes.SEDAN, "Willard", 5000),

        602: (VehicleTypes.SPORT, "Alpha", 5000),
        402: (VehicleTypes.SPORT, "Buffalo", 5000),
        429: (VehicleTypes.SPORT, "Banshee", 5000),
        541: (VehicleTypes.SPORT, "Bullet", 5000),
        496: (VehicleTypes.SPORT, "Blista Compact", 5000),
        415: (VehicleTypes.SPORT, "Cheetah", 5000),
        589: (VehicleTypes.SPORT, "Club", 5000),
        587: (VehicleTypes.SPORT, "Euros", 5000),
        562: (VehicleTypes.SPORT, "Elegy", 5000),
        565: (VehicleTypes.SPORT, "Flash", 5000),
        451: (VehicleTypes.SPORT, "Turismo", 5000),
        494: (VehicleTypes.SPORT, "Hotring Racer", 5000),
        502: (VehicleTypes.SPORT, "Hotring Racer", 5000),
        503: (VehicleTypes.SPORT, "Hotring Racer", 5000),
        411: (VehicleTypes.SPORT, "Infernus", 5000),
        559: (VehicleTypes.SPORT, "Jester", 5000),
        603: (VehicleTypes.SPORT, "Phoenix", 5000),
        475: (VehicleTypes.SPORT, "Sabre", 5000),
        506: (VehicleTypes.SPORT, "Super GT", 5000),
        560: (VehicleTypes.SPORT, "Sultan", 5000),
        558: (VehicleTypes.SPORT, "Uranus", 5000),
        477: (VehicleTypes.SPORT, "ZR-350", 5000),

        404: (VehicleTypes.UNIVERSAL, "Perenniel", 5000),
        418: (VehicleTypes.UNIVERSAL, "Moonbeam", 5000),
        458: (VehicleTypes.UNIVERSAL, "Solair", 5000),
        479: (VehicleTypes.UNIVERSAL, "Regina", 5000),
        561: (VehicleTypes.UNIVERSAL, "Stratum", 5000),

        406: (VehicleTypes.UNIQE, "Dumper", 5000),
        409: (VehicleTypes.UNIQE, "Stretch", 5000),
        423: (VehicleTypes.UNIQE, "Mr. Whoopee", 5000),
        428: (VehicleTypes.UNIQE, "Securicar", 5000),
        447: (VehicleTypes.UNIQE, "Seasparrow", 5000),
        495: (VehicleTypes.UNIQE, "Sandking", 5000),
        434: (VehicleTypes.UNIQE, "Hotknife", 5000),
        442: (VehicleTypes.UNIQE, "Romero", 5000),
        457: (VehicleTypes.UNIQE, "Caddy", 5000),
        483: (VehicleTypes.UNIQE, "Camper", 5000),
        485: (VehicleTypes.UNIQE, "Baggage", 5000),
        486: (VehicleTypes.UNIQE, "Dozer", 5000),
        508: (VehicleTypes.UNIQE, "Journey", 5000),
        525: (VehicleTypes.UNIQE, "Towtruck", 5000),
        530: (VehicleTypes.UNIQE, "Forklift", 5000),
        532: (VehicleTypes.UNIQE, "Combine Harvester", 5000),
        539: (VehicleTypes.UNIQE, "Vortex", 5000),
        545: (VehicleTypes.UNIQE, "Hustler", 5000),
        571: (VehicleTypes.UNIQE, "Kart", 5000),
        572: (VehicleTypes.UNIQE, "Mower", 5000),
        574: (VehicleTypes.UNIQE, "Sweeper", 5000),
        583: (VehicleTypes.UNIQE, "Tug", 5000),
        588: (VehicleTypes.UNIQE, "Hotdog", 5000),
    }


@dataclass
class VehicleRGBAColors:
    rgba = (
        0x000000FF, 0xF5F5F5FF, 0x2A77A1FF, 0x840410FF, 0x263739FF, 0x86446EFF, 0xD78E10FF, 0x4C75B7FF, 0xBDBEC6FF, 0x5E7072FF,
        0x46597AFF, 0x656A79FF, 0x5D7E8DFF, 0x58595AFF, 0xD6DAD6FF, 0x9CA1A3FF, 0x335F3FFF, 0x730E1AFF, 0x7B0A2AFF, 0x9F9D94FF,
        0x3B4E78FF, 0x732E3EFF, 0x691E3BFF, 0x96918CFF, 0x515459FF, 0x3F3E45FF, 0xA5A9A7FF, 0x635C5AFF, 0x3D4A68FF, 0x979592FF,
        0x421F21FF, 0x5F272BFF, 0x8494ABFF, 0x767B7CFF, 0x646464FF, 0x5A5752FF, 0x252527FF, 0x2D3A35FF, 0x93A396FF, 0x6D7A88FF,
        0x221918FF, 0x6F675FFF, 0x7C1C2AFF, 0x5F0A15FF, 0x193826FF, 0x5D1B20FF, 0x9D9872FF, 0x7A7560FF, 0x989586FF, 0xADB0B0FF,
        0x848988FF, 0x304F45FF, 0x4D6268FF, 0x162248FF, 0x272F4BFF, 0x7D6256FF, 0x9EA4ABFF, 0x9C8D71FF, 0x6D1822FF, 0x4E6881FF,
        0x9C9C98FF, 0x917347FF, 0x661C26FF, 0x949D9FFF, 0xA4A7A5FF, 0x8E8C46FF, 0x341A1EFF, 0x6A7A8CFF, 0xAAAD8EFF, 0xAB988FFF,
        0x851F2EFF, 0x6F8297FF, 0x585853FF, 0x9AA790FF, 0x601A23FF, 0x20202CFF, 0xA4A096FF, 0xAA9D84FF, 0x78222BFF, 0x0E316DFF,
        0x722A3FFF, 0x7B715EFF, 0x741D28FF, 0x1E2E32FF, 0x4D322FFF, 0x7C1B44FF, 0x2E5B20FF, 0x395A83FF, 0x6D2837FF, 0xA7A28FFF,
        0xAFB1B1FF, 0x364155FF, 0x6D6C6EFF, 0x0F6A89FF, 0x204B6BFF, 0x2B3E57FF, 0x9B9F9DFF, 0x6C8495FF, 0x4D8495FF, 0xAE9B7FFF,
        0x406C8FFF, 0x1F253BFF, 0xAB9276FF, 0x134573FF, 0x96816CFF, 0x64686AFF, 0x105082FF, 0xA19983FF, 0x385694FF, 0x525661FF,
        0x7F6956FF, 0x8C929AFF, 0x596E87FF, 0x473532FF, 0x44624FFF, 0x730A27FF, 0x223457FF, 0x640D1BFF, 0xA3ADC6FF, 0x695853FF,
        0x9B8B80FF, 0x620B1CFF, 0x5B5D5EFF, 0x624428FF, 0x731827FF, 0x1B376DFF, 0xEC6AAEFF, 0x000000FF,
        0x177517FF, 0x210606FF, 0x125478FF, 0x452A0DFF, 0x571E1EFF, 0x010701FF, 0x25225AFF, 0x2C89AAFF, 0x8A4DBDFF, 0x35963AFF,
        0xB7B7B7FF, 0x464C8DFF, 0x84888CFF, 0x817867FF, 0x817A26FF, 0x6A506FFF, 0x583E6FFF, 0x8CB972FF, 0x824F78FF, 0x6D276AFF,
        0x1E1D13FF, 0x1E1306FF, 0x1F2518FF, 0x2C4531FF, 0x1E4C99FF, 0x2E5F43FF, 0x1E9948FF, 0x1E9999FF, 0x999976FF, 0x7C8499FF,
        0x992E1EFF, 0x2C1E08FF, 0x142407FF, 0x993E4DFF, 0x1E4C99FF, 0x198181FF, 0x1A292AFF, 0x16616FFF, 0x1B6687FF, 0x6C3F99FF,
        0x481A0EFF, 0x7A7399FF, 0x746D99FF, 0x53387EFF, 0x222407FF, 0x3E190CFF, 0x46210EFF, 0x991E1EFF, 0x8D4C8DFF, 0x805B80FF,
        0x7B3E7EFF, 0x3C1737FF, 0x733517FF, 0x781818FF, 0x83341AFF, 0x8E2F1CFF, 0x7E3E53FF, 0x7C6D7CFF, 0x020C02FF, 0x072407FF,
        0x163012FF, 0x16301BFF, 0x642B4FFF, 0x368452FF, 0x999590FF, 0x818D96FF, 0x99991EFF, 0x7F994CFF, 0x839292FF, 0x788222FF,
        0x2B3C99FF, 0x3A3A0BFF, 0x8A794EFF, 0x0E1F49FF, 0x15371CFF, 0x15273AFF, 0x375775FF, 0x060820FF, 0x071326FF, 0x20394BFF,
        0x2C5089FF, 0x15426CFF, 0x103250FF, 0x241663FF, 0x692015FF, 0x8C8D94FF, 0x516013FF, 0x090F02FF, 0x8C573AFF, 0x52888EFF,
        0x995C52FF, 0x99581EFF, 0x993A63FF, 0x998F4EFF, 0x99311EFF, 0x0D1842FF, 0x521E1EFF, 0x42420DFF, 0x4C991EFF, 0x082A1DFF,
        0x96821DFF, 0x197F19FF, 0x3B141FFF, 0x745217FF, 0x893F8DFF, 0x7E1A6CFF, 0x0B370BFF, 0x27450DFF, 0x071F24FF, 0x784573FF,
        0x8A653AFF, 0x732617FF, 0x319490FF, 0x56941DFF, 0x59163DFF, 0x1B8A2FFF, 0x38160BFF, 0x041804FF, 0x355D8EFF, 0x2E3F5BFF,
        0x561A28FF, 0x4E0E27FF, 0x706C67FF, 0x3B3E42FF, 0x2E2D33FF, 0x7B7E7DFF, 0x4A4442FF, 0x28344EFF
    )


@dataclass
class VehicleIDs:
    cars = (
        412,
        534,
        535,
        536,
        566,
        567,
        575,
        576,
        400,
        424,
        444,
        470,
        489,
        495,
        500,
        556,
        557,
        568,
        573,
        579,
        407,
        416,
        420,
        427,
        431,
        433,
        437,
        438,
        490,
        523,
        528,
        544,
        596,
        597,
        598,
        599,
        445,
        504,
        401,
        518,
        527,
        542,
        507,
        585,
        419,
        526,
        466,
        492,
        474,
        517,
        410,
        551,
        516,
        467,
        426,
        540,
        436,
        405,
        580,
        550,
        549,
        540,
        491,
        421,
        529,
        602,
        402,
        429,
        541,
        496,
        415,
        589,
        587,
        562,
        565,
        451,
        494,
        502,
        503,
        411,
        559,
        603,
        475,
        506,
        560,
        558,
        477,
        404,
        418,
        458,
        479,
        561,
        406,
        409,
        423,
        428,
        434,
        442,
        457,
        483,
        485,
        486,
        508,
        525,
        530,
        532,
        539,
        545,
        571,
        572,
        574,
        583,
        588,
    )


@dataclass(frozen=True)
class VehicleComponents:
    exhaust = {
        "Upswept": 1018,
        "Twin": 1019,
        "Large": 1020,
        "Medium": 1021,
        "Small": 1022,
    }
    wheels = {
        "Shadow": 1073,
        "Mega": 1074,
        "Rimshine": 1075,
        "Wires": 1076,
        "Classic": 1077,
        "Twist": 1078,
        "Cutter": 1079,
        "Switch": 1080,
        "Grove": 1081,
        "Import": 1082,
        "Dollar": 1083,
        "Trance": 1084,
        "Atomic": 1085,
        "Stereo": 1086,
        "Ahab": 1096,
        "Virtual": 1097,
        "Access": 1098
    }
    hydraulics: int = 1087
    nitro_x2: int = 1009
    nitro_x5: int = 1008
    nitro_x10: int = 1010
    paint_jobs = {
        483: (0),
        534: (0, 1, 2),
        535: (0, 1, 2),
        536: (0, 1, 2),
        558: (0, 1, 2),
        559: (0, 1, 2),
        560: (0, 1, 2),
        561: (0, 1, 2),
        562: (0, 1, 2),
        565: (0, 1, 2),
        567: (0, 1, 2),
        575: (0, 1),
        576: (0, 1, 2)
    }
    spoilers = {
        565: {
            "Alien": 1049,
            "X-Flow": 1050
        },
        561: {
            "Alien": 1058,
            "X-Flow": 1060
        },
        560: {
            "Alien": 1138,
            "X-Flow": 1139
        },
        562: {
            "Alien": 1146,
            "X-Flow": 1147
        },
        559: {
            "Alien": 1162,
            "X-Flow": 1158
        },
        558: {
            "Alien": 1164,
            "X-Flow": 1163
        }
    }
    front_bumper = {
        534: {
            "Chrome": 1117,
        },
        565: {
            "Alien": 1153,
            "X-Flow": 1152
        },
        561: {
            "Alien": 1155,
            "X-Flow": 1157
        },
        559: {
            "Alien": 1160,
            "X-Flow": 1173
        },
        558: {
            "Alien": 1166,
            "X-Flow": 1165
        },
        560: {
            "Alien": 1169,
            "X-Flow": 1170
        },
        562: {
            "Alien": 1171,
            "X-Flow": 1172
        },
        575: {
            "Chrome": 1174,
            "Slamin": 1175
        },
        534: {
            "Chrome": 1179,
            "Slamin": 1185
        },
        536: {
            "Chrome": 1182,
            "Slamin": 1181
        },
        567: {
            "Chrome": 1189,
            "Slamin": 1188
        },
        576: {
            "Chrome": 1191,
            "Slamin": 1190
        }
    }
    rear_bumper = {
        560: {
            "Alien": 1141,
            "X-Flow": 1140
        },
        562: {
            "Alien": 1149,
            "X-Flow": 1148
        },
        565: {
            "Alien": 1150,
            "X-Flow": 1151
        },
        561: {
            "Alien": 1154,
            "X-Flow": 1156
        },
        559: {
            "Alien": 1159,
            "X-Flow": 1161
        },
        558: {
            "Alien": 1168,
            "X-Flow": 1167
        },
        575: {
            "Chrome": 1176,
            "Slamin": 1177
        },
        534: {
            "Chrome": 1180,
            "Slamin": 1178
        },
        536: {
            "Chrome": 1184,
            "Slamin": 1183
        },
        567: {
            "Chrome": 1187,
            "Slamin": 1186
        },
        576: {
            "Chrome": 1191,
            "Slamin": 1193
        }
    }


class Vehicle(BaseVehicle):
    _registry: dict = {}
    player_vehicles: dict[int, "Vehicle"] = {}
    def __init__(self, vehicle_id: int):
        super().__init__(vehicle_id)
        self.owner = NO_VEHICLE_OWNER
        self.engine = 0
        self.lights = 0
        self.doors = 0
        self.repair_timer = TIMER_ID_NONE

    @classmethod
    def from_registry_native(cls, vehicle: BaseVehicle) -> "Vehicle":
        if isinstance(vehicle, int):
            vehicle_id = vehicle

        if isinstance(vehicle, BaseVehicle):
            vehicle_id = vehicle.id

        vehicle = cls._registry.get(vehicle_id)
        if not vehicle:
            cls._registry[vehicle_id] = vehicle = cls(vehicle_id)

        return vehicle

    @classmethod
    def using_registry(cls, func):
        @wraps(func)
        def from_registry(*args, **kwargs):
            args = list(args)
            args[0] = cls.from_registry_native(args[0])
            return func(*args, **kwargs)

        return from_registry

    @classmethod
    def get_from_registry(cls, id: int) -> "Vehicle":
        return cls._registry[id]

    @classmethod
    def delete_registry(cls, vehicle: BaseVehicle) -> None:
        del cls._registry[vehicle.id]

    @classmethod
    def create(
        cls,
        model: int,
        x: float,
        y: float,
        z: float,
        rotation: float,
        color1: int,
        color2: int,
        respawn_delay: int,
        mode: int,
        add_siren: bool = False,
    ) -> "Vehicle":
        veh = super().create(model, x, y, z, rotation, color1, color2, respawn_delay, add_siren=add_siren)
        veh.set_virtual_world(mode)
        return cls.from_registry_native(veh)

    def set_info(self, owner: str = "", engine: int = 0, lights: int = 0, doors: int = 0) -> "Vehicle":
        self.owner = owner,
        self.engine = engine
        self.lights = lights
        self.doors = doors

    def set_owner(self, owner: str):
        self.owner = owner

    @property
    def is_car(self) -> bool:
        return self.get_model() in VehicleIDs.cars

    @classmethod
    def remove_unused_player_vehicle(cls, player_id: int, vehicle: "Vehicle") -> None:
        cls.delete_registry(vehicle)
        del cls.player_vehicles[player_id]
        if vehicle.is_valid():
            vehicle.destroy()

    def repair_ex(self) -> None:
        self.repair()
        self.repair_timer = ID_NONE

@Vehicle.on_damage_status_update
@Vehicle.using_registry
def on_vehicle_damage_status(vehicle: Vehicle, player: Player) -> None:
    if vehicle.repair_timer == ID_NONE:
        return set_timer(vehicle.repair_ex, 1500, False)
