from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from Backend.services.weather_service import WeatherService

router = APIRouter(tags=["Weather"])
weather_service = WeatherService()

@router.get("/weather")
async def get_weather(
    city: Optional[str] = Query(None, description="City name (e.g. New Delhi, Mumbai, Fresno)"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate")
):
    try:
        if lat is not None and lon is not None:
            data = await weather_service.get_weather_by_coords(lat, lon)
        elif city:
            data = await weather_service.get_weather_by_city(city)
        else:
            # Default to New Delhi if unspecified
            data = await weather_service.get_weather_by_city("New Delhi")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather: {str(e)}")

@router.get("/weather/forecast")
async def get_weather_forecast(
    city: Optional[str] = Query(None, description="City name (e.g. New Delhi, Pune, Nashik)"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate")
):
    try:
        data = await weather_service.get_3_day_forecast(latitude=lat, longitude=lon, city_name=city)
        return {"forecast": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch 3-day forecast: {str(e)}")

