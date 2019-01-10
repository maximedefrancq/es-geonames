
echo "Downloading Geonames gazetteer..."
wget http://download.geonames.org/export/zip/$1.zip

echo "Unpacking Geonames gazetteer..."
unzip $1.zip

echo "Creating mappings for the fields in the Postal Code Geonames index..."
curl -XPUT "$2/geonames_postalcode" -H 'Content-Type: application/json' -d @geonames_postalcode_mapping.json

echo "Loading gazetteer into Elasticsearch..."
python geonames_postal_code_elasticsearch_loader.py $1 $2

echo "Done"
