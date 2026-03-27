select *
from {{ ref('stg_open_meteo_weather') }}
where wind_speed_10m is not null
  and (wind_speed_10m < 0 or wind_speed_10m > 75)
