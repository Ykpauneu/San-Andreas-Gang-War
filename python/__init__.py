from pysamp import (
    on_gamemode_init,
    send_rcon_command,
    set_game_mode_text,
    enable_stunt_bonus_for_all,
    manual_vehicle_engine_and_lights,
    disable_interior_enter_exits,
    show_player_markers,
    create_3d_text_label,
    set_world_time,
    send_client_message_to_all,
    show_name_tags
)
from datetime import datetime
from zoneinfo import ZoneInfo
from pysamp.gangzone import Gangzone
from pysamp.textdraw import TextDraw
from pysamp.timer import set_timer
from pystreamer import register_callbacks
from pystreamer.dynamiccp import DynamicCheckpoint
from pystreamer.dynamicpickup import DynamicPickup
from pydpc.driftcounter.callbacks import register as register_drift_callbacks
from pydpc.driftcounter.drift import Drift
from pydpc.driftcounter import *
from .libs.gang import GangZoneData
from .libs.gangzones import GangZones
from .libs.player import Player
from .libs.vehicle import Vehicle
from .libs.utils.data import *
from .libs.database import DataBase
from .libs.commands import *
from .libs.textdraws import TextDraws
from .libs.objects import Objects
from .libs import __version__
from .libs.fun.math import MathTest
import random
encode()

@on_gamemode_init
def on_ready() -> None:
    DataBase.create_metadata()
    register_callbacks()
    register_drift_callbacks()
    drift_set_global_check()
    drift_set_update_delay(8)
    drift_set_start_end_delay(60)
    drift_set_minimal_angle(15.5)
    drift_set_minimal_speed(25.5)
    drift_set_divider(1000)
    drift_set_damage_check()
    enable_stunt_bonus_for_all(False)
    manual_vehicle_engine_and_lights()
    disable_interior_enter_exits()
    show_name_tags(True)
    show_player_markers(1)
    send_rcon_command(f"name {ServerInfo.name}")
    send_rcon_command(f"language {ServerInfo.language}")
    send_rcon_command(f"game.map {ServerInfo.map}")
    set_game_mode_text(ServerInfo.gamemode)
    create_3d_text_label("Grove Street Families", 0x009900FF, 2514.3403, -1691.5911, 14.0460, 10, 0, test_line_of_sight=True)
    create_3d_text_label("The Ballas", 0xCC00FFFF, 2022.9318, -1120.2645, 26.4210+1, 10, 0, test_line_of_sight=True)
    create_3d_text_label("Los Santos Vagos", 0xffcd00FF, 2756.3645,-1182.8091, 69.4035+1, 10, 0, test_line_of_sight=True)
    create_3d_text_label("Varios Los Aztecas", 0x00B4E1FF, 2185.7717, -1815.2280, 13.5469, 10, 0, test_line_of_sight=True)
    create_3d_text_label("The Rifa", 0x6666FFFF, 2787.0764,-1926.1918, 13.5469+1, 10, 0, test_line_of_sight=True)
    DataBase.create_gangzones()
    TextDraws.load()
    Objects.load()
    GangZones.load()
    gangzones = DataBase.load_gangzones_order_by()
    if gangzones:
        for gangzone in gangzones:
            GangZoneData(
                gangzone.id,
                gangzone.gang_id,
                gangzone.color,
                gangzone.gang_atk_id,
                gangzone.gang_def_id,
                gangzone.gang_atk_score,
                gangzone.gang_def_score,
                gangzone.capture_cooldown,
                gangzone.is_capture,
                gangzone.capture_time
            )
    print("GangZone's registry:")
    for id, value in GangZoneData._registry.items():
        print(f"\tID: {id} | Inst: {value}")

    vehicles = DataBase.load_vehicles_order_by()
    if vehicles:
        for vehicle in vehicles:
            if vehicle.virtual_world != ServerMode.freeroam_world:
                veh = Vehicle.create(
                    vehicle.model_id,
                    vehicle.x,
                    vehicle.y,
                    vehicle.z,
                    vehicle.rotation,
                    vehicle.color1,
                    vehicle.color2,
                    vehicle.delay,
                    vehicle.virtual_world,
                    add_siren=vehicle.add_siren,
                )
                veh.set_info(
                    owner=vehicle.owner,
                    engine=vehicle.engine,
                    lights=vehicle.lights,
                    doors=vehicle.doors
                )

    print("Vehicle's registry:")
    for id, value in Vehicle._registry.items():
        print(f"\tID: {id} | Inst: {value}")

    print(f"Loaded: {len(GangZoneData._registry.items())} gangzones")
    print(f"Loaded: {len(Vehicle._registry.items())} vehicles")
    print(f"Loaded: {ServerInfo.name_short} (v{__version__})")
    print("Created by: Ykpauneu & Rein.")
    time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
    ServerInfo.current_time = time
    set_world_time(ServerInfo.current_time.hour)
    set_timer(every_second, 1000, True)

def every_second():
    for gangzone in GangZoneData._registry.values():
        if gangzone.capture_cooldown != 0:
            gangzone.capture_cooldown -= 1

        if gangzone.capture_cooldown == 0:
            DataBase.save_gangzone(
                gangzone.gangzone_id,
                capture_cooldown=0
            )

        if gangzone.is_capture:
            if gangzone.capture_time != 0:
                gangzone.capture_time -= 1
                Player.update_capture_textdraw(gangzone)

            else:
                Player.end_capture(gangzone)

    if ServerInfo.current_time.hour != datetime.now(tz=ZoneInfo("Europe/Moscow")).hour:
        ServerInfo.current_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        if ServerInfo.current_time.hour == 0:
            DataBase.create_analytics()

        set_world_time(ServerInfo.current_time.hour)
        send_client_message_to_all(Colors.ad, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        send_client_message_to_all(Colors.ad, f"Наш сайт: {{{Colors.link_hex}}}sanandreasonline.github.io")
        send_client_message_to_all(Colors.ad, f"Наш Discord: {{{Colors.link_hex}}}discord.gg/yn2EcNJywH")
        send_client_message_to_all(Colors.ad, f"Наш IP: {{{Colors.cmd_hex}}}213.226.126.237:7777")
        send_client_message_to_all(Colors.ad, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if ServerInfo.change_name_and_adverb != 0:
        ServerInfo.change_name_and_adverb -= 1

    else:
        send_rcon_command(f"name {random.choice(ServerInfo.name_timer)}")
        ServerInfo.change_name_and_adverb = 7200

    if ServerInfo.send_math != 0:
        ServerInfo.send_math -= 1

    else:
        MathTest.send_math_test()
        ServerInfo.send_math = 1800

@Player.on_connect
@Player.using_registry
def on_player_connect(player: Player) -> None:
    player.on_connect_handle()


@Player.on_disconnect
@Player.using_registry
def on_player_disconnect(player: Player, reason: int) -> None:
    player.on_disconnect_handle()

@Player.on_request_class
@Player.using_registry
def on_player_request_class(player: Player, class_id: int) -> None:
    player.on_request_class_handle(class_id)

@Player.on_spawn
@Player.using_registry
def on_player_spawn(player: Player) -> None:
    player.on_spawn_handle()

@Player.on_death
@Player.using_registry
def on_player_death(player: Player, killer: Player, reason: int) -> None:
    killer = Player.from_registry_native(killer)
    player.on_death_handle(killer, reason)

@Player.on_text
@Player.using_registry
def on_player_text(player: Player, text: str) -> None:
    player.on_text_handle(text)
    return False

@DynamicPickup.on_player_pick_up
@Player.using_registry
def on_player_pick_up_pickup(player: Player, pickup: DynamicPickup) -> None:
    player.on_pick_up_pickup_handle(pickup)

@DynamicCheckpoint.on_player_enter
@Player.using_registry
def on_player_enter_checkpoint(player: Player, checkpoint: DynamicCheckpoint) -> None:
    player.on_enter_checkpoint_handle(checkpoint)

@Player.on_update
@Player.using_registry
def on_player_update(player: Player) -> None:
    player.on_update_handle()

@Player.on_give_damage
@Player.using_registry
def on_player_give_damage(player: Player, issuer: Player, amount: float, weapon_id: int, body_part) -> None:
    issuer = Player.from_registry_native(issuer)
    player.on_damage_handler(issuer, amount, weapon_id, body_part)

@Player.on_key_state_change
@Player.using_registry
def on_player_key_state_change(player: Player, new_keys: int, old_keys: int) -> None:
    player.on_key_state_change_handle(new_keys, old_keys)

@Player.on_state_change
@Player.using_registry
def on_player_state_change(player: Player, new_state: int, old_state: int) -> None:
    player.on_state_change_handle(new_state, old_state)


@Player.on_click_textdraw
@Player.using_registry
def on_player_click_textdraw(player: Player, clicked: TextDraw) -> None:
    player.on_click_textdraw_handle(clicked)

@Player.on_click_map
@Player.using_registry
def on_player_click_map(player: Player, x: float, y: float, z: float) -> None:
    player.on_click_map_handle(x, y, z)

@Drift.on_start
@Player.using_registry
def on_player_start_drift(player: Player) -> None:
    player.on_start_drift_handle()

@Drift.on_update
@Player.using_registry
def on_player_drift_update(player: Player, value: int, combo: int, flag_id: int, distance: float, speed: float) -> None:
    player.on_drift_update_handle(value, combo, flag_id, distance, speed)

@Drift.on_end
@Player.using_registry
def on_player_end_drift(player: Player, value: int, combo: int, reason: int) -> None:
    player.on_end_drift_handle(value, combo, reason)

@Vehicle.on_death
@Vehicle.using_registry
def on_vehicle_death(vehicle: Vehicle, killer: Player) -> None:
    killer = Player.from_registry_native(killer)
    vehicle.on_death_handle(killer)

@Vehicle.on_damage_status_update
@Vehicle.using_registry
def on_vehicle_damage_status_update(vehicle: Vehicle, player: Player) -> None:
    player = Player.from_registry_native(player)
    vehicle.on_damage_status_handle(player)
