CREATE TABLE ad_clicks (
  ad_id INTEGER,
  user_id INTEGER,
  click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  clicked BOOLEAN
);

