from app.cloud_api import get_dns_zones_list

def get_zone_id_if_owned_by_user(zone: str, user: str) -> str:
    """
    Validate zone ownership and return the zone ID
    """
    # Get all zones for the user
    user_zones = get_dns_zones_list(user)
    zones_dict = {zone['zone_id']: zone['name'] for zone in user_zones}

    zone_id = (
        zone if zone in zones_dict.keys()
        else next(
            (z_id for z_id, z_name in zones_dict.items() if z_name == zone),
            ""
        )
    )
    return zone_id
    