export interface Entry {
  id: string;
  user_id: string;
  entry_date: string;
  title?: string;
  content: string;
  content_html?: string;
  mood?: string;
  mood_score?: number;
  word_count?: number;
  writing_time_seconds?: number;
  latitude?: number;
  longitude?: number;
  location_name?: string;
  tags: string[];
  is_private: boolean;
  created_at: string;
  updated_at: string;
}

export interface EntryMemory {
  entry: Entry;
  years_ago: number;
}

export interface CreateEntryInput {
  entry_date: string;
  title?: string;
  content: string;
  mood?: string;
  mood_score?: number;
  latitude?: number;
  longitude?: number;
  location_name?: string;
  tags?: string[];
}
