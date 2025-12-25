export interface APODData {
  date: string;
  title: string;
  explanation: string;
  url: string;
  hdurl?: string;
  media_type: 'image' | 'video';
  copyright?: string;
}

export interface MarsPhoto {
  id: number;
  sol: number;
  earth_date: string;
  camera_name: string;
  camera_full_name: string;
  rover_name: string;
  img_src: string;
}

export interface NearEarthObject {
  id: string;
  name: string;
  nasa_jpl_url: string;
  estimated_diameter_min_m: number;
  estimated_diameter_max_m: number;
  is_potentially_hazardous: boolean;
  close_approach_date: string;
  miss_distance_km: number;
  relative_velocity_kph: number;
}

export interface HistoricalEvent {
  year: number;
  title: string;
  description: string;
  category?: string;
  wikipedia_url?: string;
  image_url?: string;
}

export interface HistoricalFigure {
  name: string;
  year: number;
  description: string;
  event_type: 'birth' | 'death';
  wikipedia_url?: string;
}

export interface HistoricalWeather {
  date: string;
  location_name?: string;
  latitude: number;
  longitude: number;
  temperature_max_c: number;
  temperature_min_c: number;
  temperature_mean_c: number;
  precipitation_mm: number;
  weather_code: number;
  weather_description: string;
  sunrise?: string;
  sunset?: string;
  daylight_hours?: number;
}

export interface TemporalContext {
  date: string;

  // Space
  apod?: APODData;
  mars_photos: MarsPhoto[];
  near_earth_objects: NearEarthObject[];

  // History
  historical_events: HistoricalEvent[];
  notable_births: HistoricalFigure[];
  notable_deaths: HistoricalFigure[];
  year_fact?: string;

  // Weather
  weather?: HistoricalWeather;
  weather_comparison: Record<number, HistoricalWeather>;

  // Insights
  cosmic_perspective?: string;
  day_summary?: string;
}
