### Kintro Web

Very simple, tiny flask app to trigger kintro cli in an environment where we cannot ensure python dependencies


### Sonarr Usage


#### Dependencies (available on linuxserver sonarr containers)
`jq` and `curl`

#### Copy the below to somewhere in sonarr /config, ex /config/scripts/kintro.sh and ensure it is executable (chmod +x /config/scripts/kintro.sh)

##### Replace {IP:PORT} with your kintro-web instance
```bash
#!/bin/bash

env

echo "Series: ${sonarr_series_title}"
echo "Season: ${sonarr_episodefile_seasonnumber}"
echo "Episode(s) #${sonarr_episodefile_episodecount}: ${sonarr_episodefile_episodenumbers}"

SHOW_AND_SEASON_URL=$(printf %s "${sonarr_series_title}/${sonarr_episodefile_seasonnumber}" | jq -s -R -r @uri)
for episode in $(echo ${sonarr_episodefile_episodenumbers} | tr "," "\n"); do
    echo "Handling episode: ${episode}"
    echo "Command: curl -XPOST http://{IP:PORT}/episode/${SHOW_AND_SEASON_URL}/${episode}"
    curl -XPOST http://{IP:PORT}/episode/${SHOW_AND_SEASON_URL}/${episode}
done
```

Settings > Connect > Custom Script

Name: kintro

Triggers: On Import | On Upgrade

Path: Full Path to your script, ex /config/scripts/kintro.sh
