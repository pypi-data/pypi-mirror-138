from enum import IntEnum
import struct
from typing import Any, Awaitable, Callable, Dict

from autobahn.asyncio.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions

from ..config import CONFIG
import c3loc.ingest as ingest
import c3loc.stats as stats

class C3AdvertType(IntEnum):
    SR = 0
    SLA = 1
    SSR = 2
    AUX = 3

def mac_from_path(path: str) -> str:
    leaf = path.split('/')[-1]
    return ":".join(leaf.split('_')[1:])

async def do_sr(conn, l_id: str, mac: str, payload: bytes, rssi: int) -> None:
    print(f"SR: {mac}, {payload.hex()}, {rssi}")
    if len(payload) < 8:
        stats.increment("Invalid SR Length")
        return
    version, rssi_cal, timestamp, status = struct.unpack('<BbIB', payload[1:8])
    battery_pct = status >> 1
    alarm_active = True if status & 1 else False;

    # print(f"\tversion: {version}, rssi_cal: {rssi_cal}, ts: {timestamp}, "
    #      f"batt_pct: {battery_pct}, alarm: {alarm_active}")

    stats.increment("SR Reports")
    t = await conn.fetchrow(
        'SELECT id, last_seen, (now() at time zone \'utc\'), alarm_active '
        'FROM tags WHERE mac = $1 AND type = \'SmartRelay\'', mac)
    if not t:
        stats.increment('New SR')
        t = await conn.fetch(
            'INSERT into tags (mac, type, battery_pct) '
            'VALUES ($1, \'SmartRelay\', $2) RETURNING '
            'id, last_seen, (now() at time zone \'utc\'), alarm_active',
            mac, battery_pct)
    t_id, t_lastseen, db_now, t_alarm = t[0], t[1], t[2], t[3]
    diff = (db_now - t_lastseen).seconds
    if diff > CONFIG['LAST_SEEN_RESOLUTION_SECS']:
        await conn.execute(
            'UPDATE tags SET last_seen = $1, battery_pct = $3 WHERE id = $2',
            db_now, t_id, battery_pct)

    # Service alarm
    if alarm_active:
        alarm = await conn.fetchrow(
            'UPDATE alarms SET last_ts = now() '
            'WHERE tag_id = $1 AND acknowledged = FALSE RETURNING id', t_id)
        if not alarm:
            stats.increment('New Alarm')
            await conn.execute(
                'INSERT INTO alarms (tag_id) VALUES ($1)', t_id)
    if t_alarm != alarm_active:
        stats.increment('Alarm State Updated')
        await conn.execute(
            'UPDATE tags SET alarm_active = $1 WHERE id = $2',
            alarm_active, t_id)

    if version == 1:
        # No current anchor
        stats.increment('Unanchored SR Packet')
        await conn.execute(
            'INSERT into log (tag_id, zone_id, listener_id, distance, '
            'variance, anchor_id, anchor_dist, anchor_ts_delta, reason)'
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
            t_id, listener_zone, self.listener_id,
            0, 0, None, None, None, 'STATUS')
        return

    if version != 2:
        stats.increment(f"Unknown SR version: {version}")
        return

    if not len(payload) == 15:
        stats.increment("Invalid SR Length")
        return

    n_id, a_delta, a_rssi, a_rssi_cal = struct.unpack('>IBbb', payload[-7:])
    a_dist = 10 ** ((a_rssi_cal - a_rssi)/(10 ** 3.2))  # TODO: path_loss

    # Reconstruct the iBeacon from the LA data
    major = n_id >> 16
    minor = n_id & 0xffff
    #print(f"n_id: {n_id} = {major}:{minor}")
    r = await conn.fetchrow(
        'SELECT id, zone_id FROM tags '
        'WHERE uuid = $1 AND major = $2 AND minor = $3',
        CONFIG['LA_UUID'], major, minor)
    if not r:
        stats.increment('New LA')
        r = await conn.fetchrow(
            'INSERT into tags (uuid, major, minor, type) '
            'VALUES ($1, $2, $3, \'LocationAnchor\') RETURNING id, zone_id',
            CONFIG['LA_UUID'], major, minor)
    (a_id, azone_id) = r[0], r[1]
    if not azone_id:
        stats.increment('Autocreated Zone (LA)')
        s = await conn.fetchrow(
            'INSERT INTO zones (name) VALUES ($1) RETURNING id',
            f'Near LA {major}:{minor}')
        azone_id = s[0]
        await conn.execute(
            'UPDATE tags SET zone_id = $1 WHERE id = $2',
            azone_id, a_id)
    await conn.fetch(
        'INSERT into log (tag_id, zone_id, listener_id, distance, '
        'variance, anchor_id, anchor_dist, anchor_ts_delta, reason)'
        'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        t_id, azone_id, l_id, 0,
        0, a_id, a_dist / 10,
        a_delta, 'STATUS')

async def do_sla(con, l_id: str, mac: str, payload: bytes, rssi: int) -> None:
    print(f"SLA: {mac}, {payload.hex()}, {rssi}")
    return

async def do_ssr(conn, l_id: str, mac: str, payload: bytes, rssi: int) -> None:
    print(f"SSR: {mac}, {payload.hex()}, {rssi}")
    return

async def do_aux(conn, l_id: str, mac: str, payload: bytes, rssi: int) -> None:
    print(f"AUX: {mac}, {payload.hex()}, {rssi}")
    await ingest.sensor(conn, mac, payload[1:])


DISPATCH: Dict[C3AdvertType, Callable[[Any, str, bytes, int], Awaitable[Any]]] = {
    C3AdvertType.SR: do_sr,
    C3AdvertType.SLA: do_sla,
    C3AdvertType.SSR: do_ssr,
    C3AdvertType.AUX: do_aux,
}

class WampHandler(ApplicationSession):
    db_pool = None

    def __init__(self, *args, **kwargs):
        assert self.db_pool, f"You must define {self.__class__}.db_pool before instantiation"
        ApplicationSession.__init__(self, *args, **kwargs)

    async def onJoin(self, details):
        print(f"Connected to router")

        async def on_manuf_c3wireless(i, details):
            #print(f"Got event {i}, {details}")
            payload = i['data'][0]
            if len(payload['data']) < 1:
                # Invalid C3 Wireless packet
                return
            ad_type = payload['data'][0]
            rssi = payload['rssi']
            l_id = i['listener_id']
            mac = mac_from_path(payload['path'])
            if ad_type not in DISPATCH:
                print(f"\tUnknown advert type {ad_type} from {mac}")
                return

            conn = await self.db_pool.acquire()
            await DISPATCH[ad_type](conn, l_id, mac, payload['data'], rssi)
            await self.db_pool.release(conn)


        def on_ibeacon(i, details):
            pass

        self.subscribe(on_manuf_c3wireless, 'com.c3wireless.listeners..manuf.c3wireless',
                       options=SubscribeOptions(details=True, match='wildcard'))

        self.subscribe(on_ibeacon, 'com.c3wireless.listeners..ibeacon',
                       options=SubscribeOptions(details=True, match='wildcard'))

    async def onDisconnect(self):
        pass
