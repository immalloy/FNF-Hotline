import json
import os
import urllib.request

GAME_ID = 8694
TOP_SUBS_URL = f'https://gamebanana.com/apiv12/Game/{GAME_ID}/TopSubs'

_config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

def _load_config():
    with open(_config_path, encoding='utf-8') as f:
        cfg = json.load(f)

    periods = []
    labels = {}
    colors = {}
    for key, opts in cfg['periods'].items():
        if opts.get('enabled', True):
            periods.append(key)
            labels[key] = {'emoji': opts['emoji'], 'name': opts['name']}
            colors[key] = int(opts['color'].lstrip('#'), 16)

    return periods, labels, colors, cfg.get('max_per_period', 3), cfg.get('blacklist', [])

PERIODS, LABELS, COLORS, MAX_PER_PERIOD, BLACKLIST = _load_config()

def _is_blacklisted(mod):
    name = (mod.get('_sName') or '').lower()
    author = (mod.get('_aSubmitter', {}).get('_sName') or '').lower()
    for term in BLACKLIST:
        if term.lower() in name or term.lower() in author:
            return True
    return False

def fetch_top_subs():
    req = urllib.request.Request(TOP_SUBS_URL, headers={'User-Agent': 'Funkin-Hotline/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())

    result = {p: [] for p in PERIODS}
    for item in data:
        period = item.get('_sPeriod')
        if period in PERIODS and len(result[period]) < MAX_PER_PERIOD:
            if not _is_blacklisted(item):
                result[period].append(item)
    return result

def get_mod_key(mod):
    if not mod:
        return None
    return f'{mod["_sPeriod"]}:{mod["_idRow"]}'

def get_state_key(mods):
    key = {}
    for p in PERIODS:
        ids = [get_mod_key(m) for m in mods[p] if m]
        key[p] = ','.join(ids) if ids else None
    return key

def get_label(period):
    return LABELS.get(period, {'emoji': '', 'name': period})

def get_color(period):
    return COLORS.get(period, 0x5865f2)
