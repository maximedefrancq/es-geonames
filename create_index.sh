
echo "Downloading Geonames gazetteer..."
wget http://download.geonames.org/export/dump/$1.zip

echo "Unpacking Geonames gazetteer..."
unzip $1.zip

echo "Creating mappings for the fields in the Geonames index..."
curl -XPUT "$2/geonames" -H 'Content-Type: application/json' -d @geonames_mapping.json

echo "Loading gazetteer into Elasticsearch..."
python geonames_elasticsearch_loader.py $1 $2

echo "Done"
