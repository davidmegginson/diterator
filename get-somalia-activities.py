import diterator.iterator, json, sys

activities = []

activity_iterator = diterator.iterator.Iterator({
    "country_code": "so",
    "year_min": 2020,
    "year_max": 2020,
})

for i, activity in enumerate(activity_iterator):
    activities.append({
        "identifier": activity.identifier,
        "title": str(activity.title),
        "description": str(activity.description),
        "humanitarian": activity.humanitarian,
        "orgs": {
            "reporting": {"name": str(activity.reporting_org), "type": activity.reporting_org.type},
            "funding": [{"name": str(org), "type": org.type} for org in activity.participating_orgs_by_role.get("1", [])],
            "accountable": [{"name": str(org), "type": org.type} for org in activity.participating_orgs_by_role.get("2", [])],
            "extending": [{"name": str(org), "type": org.type} for org in activity.participating_orgs_by_role.get("3", [])],
            "implementing": [{"name": str(org), "type": org.type} for org in activity.participating_orgs_by_role.get("4", [])],
        },
        "start_date": activity.start_date_actual if activity.start_date_actual else activity.start_date_planned,
        "end_date": activity.end_date_actual if activity.end_date_actual else activity.end_date_planned,
        "active": activity.is_active,
        "countries": [{"code": str(country), "percentage": country.percentage} for country in activity.recipient_countries],
        "locations": [str(location.name) for location in activity.locations],
        "sectors": {
            "oecd-dac5": [{"code": str(sector), "name": str(sector.narrative), "percentage": sector.percentage} for sector in activity.sectors_by_vocabulary.get("1", [])],
            "oecd-dac3": [{"code": str(sector), "name": str(sector.narrative), "percentage": sector.percentage} for sector in activity.sectors_by_vocabulary.get("2", [])],
            "ocha-clusters": [{"code": str(sector), "name": str(sector.narrative), "percentage": sector.percentage} for sector in activity.sectors_by_vocabulary.get("10", [])],
        },
    })

print(json.dumps(activities, indent=2))

print("Total", i, file=sys.stderr)
