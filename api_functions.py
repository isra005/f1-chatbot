# api_functions.py
import requests
import json

# ========================================
# API HELPER FUNCTIONS
# ========================================

def get_json_response(url):
    """
    Makes API request and returns JSON data.
    Handles errors gracefully.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

# ========================================
# FUNCTION 1: Get Last Race Results
# ========================================

def get_last_race_results():
    """
    Gets the results of the most recent F1 race.
    
    Returns:
        dict with winner, race name, date, top 3
    """
    url = "http://ergast.com/api/f1/current/last/results.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch race data"}
    
    try:
        race = data['MRData']['RaceTable']['Races'][0]
        results = race['Results']
        
        # Extract top 3
        top_3 = []
        for i in range(min(3, len(results))):
            driver = results[i]['Driver']
            top_3.append({
                "position": results[i]['position'],
                "driver": f"{driver['givenName']} {driver['familyName']}",
                "team": results[i]['Constructor']['name']
            })
        
        return {
            "race_name": race['raceName'],
            "date": race['date'],
            "circuit": race['Circuit']['circuitName'],
            "winner": top_3[0]['driver'] if top_3 else "Unknown",
            "top_3": top_3
        }
    except (KeyError, IndexError) as e:
        return {"error": f"Failed to parse race data: {e}"}

# ========================================
# FUNCTION 2: Get Next Race
# ========================================

def get_next_race():
    """
    Gets information about the next upcoming race.
    
    Returns:
        dict with race name, date, circuit, country
    """
    url = "http://ergast.com/api/f1/current/next.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch next race data"}
    
    try:
        race = data['MRData']['RaceTable']['Races'][0]
        
        return {
            "race_name": race['raceName'],
            "date": race['date'],
            "time": race.get('time', 'TBA'),
            "circuit": race['Circuit']['circuitName'],
            "country": race['Circuit']['Location']['country']
        }
    except (KeyError, IndexError) as e:
        return {"error": f"Failed to parse next race data: {e}"}

# ========================================
# FUNCTION 3: Get Driver Standings
# ========================================

def get_driver_standings(year='current'):
    """
    Gets current driver championship standings.
    
    Args:
        year: Season year (default: 'current')
    
    Returns:
        list of drivers with positions, points, wins
    """
    url = f"http://ergast.com/api/f1/{year}/driverStandings.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch standings"}
    
    try:
        standings_list = data['MRData']['StandingsTable']['StandingsLists'][0]
        standings = standings_list['DriverStandings']
        
        results = []
        for driver in standings[:10]:  # Top 10
            results.append({
                "position": driver['position'],
                "driver": f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
                "team": driver['Constructors'][0]['name'],
                "points": driver['points'],
                "wins": driver['wins']
            })
        
        return {
            "season": standings_list['season'],
            "standings": results
        }
    except (KeyError, IndexError) as e:
        return {"error": f"Failed to parse standings: {e}"}

# ========================================
# FUNCTION 4: Get Constructor Standings
# ========================================

def get_constructor_standings(year='current'):
    """
    Gets current constructor (team) championship standings.
    
    Args:
        year: Season year (default: 'current')
    
    Returns:
        list of constructors with positions, points, wins
    """
    url = f"http://ergast.com/api/f1/{year}/constructorStandings.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch constructor standings"}
    
    try:
        standings_list = data['MRData']['StandingsTable']['StandingsLists'][0]
        standings = standings_list['ConstructorStandings']
        
        results = []
        for team in standings:
            results.append({
                "position": team['position'],
                "constructor": team['Constructor']['name'],
                "nationality": team['Constructor']['nationality'],
                "points": team['points'],
                "wins": team['wins']
            })
        
        return {
            "season": standings_list['season'],
            "standings": results
        }
    except (KeyError, IndexError) as e:
        return {"error": f"Failed to parse constructor standings: {e}"}

# ========================================
# FUNCTION 5: Get Driver Info
# ========================================

def get_driver_info(driver_id):
    """
    Gets information about a specific driver.
    
    Args:
        driver_id: Driver's last name (lowercase, e.g., 'hamilton')
    
    Returns:
        dict with driver details
    """
    url = f"http://ergast.com/api/f1/drivers/{driver_id}.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch driver info"}
    
    try:
        driver = data['MRData']['DriverTable']['Drivers'][0]
        
        return {
            "full_name": f"{driver['givenName']} {driver['familyName']}",
            "code": driver.get('code', 'N/A'),
            "number": driver.get('permanentNumber', 'N/A'),
            "nationality": driver['nationality'],
            "birth_day": driver['dateOfBirth'],
            "url": driver['url']
        }
    except (KeyError, IndexError):
        return {"error": "Driver not found"}

# ========================================
# FUNCTION 6: Get Race Schedule
# ========================================

def get_race_schedule(year='current'):
    """
    Gets the full race calendar for a season.
    
    Args:
        year: Season year (default: 'current')
    
    Returns:
        list of races with dates and locations
    """
    url = f"http://ergast.com/api/f1/{year}.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch race schedule"}
    
    try:
        races = data['MRData']['RaceTable']['Races']
        
        schedule = []
        for race in races:
            schedule.append({
                "round": race['round'],
                "race_name": race['raceName'],
                "date": race['date'],
                "circuit": race['Circuit']['circuitName'],
                "country": race['Circuit']['Location']['country']
            })
        
        return {
            "season": year,
            "total_races": len(schedule),
            "races": schedule
        }
    except (KeyError, IndexError) as e:
        return {"error": f"Failed to parse schedule: {e}"}

# ========================================
# FUNCTION 7: Get Specific Race Winner
# ========================================

def get_race_winner(year, round_number):
    """
    Gets the winner of a specific race.
    
    Args:
        year: Season year
        round_number: Race number in season (1-23)
    
    Returns:
        dict with winner info
    """
    url = f"http://ergast.com/api/f1/{year}/{round_number}/results.json"
    data = get_json_response(url)
    
    if not data:
        return {"error": "Could not fetch race results"}
    
    try:
        race = data['MRData']['RaceTable']['Races'][0]
        winner = race['Results'][0]
        driver = winner['Driver']
        
        return {
            "race_name": race['raceName'],
            "date": race['date'],
            "winner": f"{driver['givenName']} {driver['familyName']}",
            "team": winner['Constructor']['name']
        }
    except (KeyError, IndexError):
        return {"error": "Race not found or not completed yet"}