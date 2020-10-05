echo "Creating mappings for the fields in the Geonames index..."
curl -XPUT "$2/geonames_postalcode" -H 'Content-Type: application/json' -d @geonames_postalcode_mapping.json


echo "Loading gazetteer into Elasticsearch..."
python geonames_postal_code_elasticsearch_loader.py $1 $2

echo "Done"