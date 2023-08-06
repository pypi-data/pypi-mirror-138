# Python Client Library for the EMS API

This project is a client library for the EMS API that is generated using [AutoRest](https://github.com/Azure/autorest). It is intended to be a direct mirror of the routes and models exposed by the EMS API. This makes the package suitable for purpose-built projects that want to use the low-level API routes directly with minimal effort.

For data science and exploratory use, consider using the [emsPy](https://github.com/ge-flight-analytics/emspy) package instead.

## Getting Started

### Install via pip

```bash
pip install emsapi
```

### Create an API client

In your code, create an API client object using an endpoint, username, and password:

```python
from emsapi import emsapi

user = "..."
password = "..."
url = "https://ems.efoqa.com/api/"

client = emsapi.create(user, password, url)
```

### Retrieve EMS system id

If the EMS system id is not known, it should be retrieved before any further requests:

```python
ems_id = client.find_ems_system_id('ems-server-name')
```

### Access routes on the API client

Different routes are exposed as members of the `client` object created in the previous step. These routes match the sections in the `API Explorer` documentation in the web UI. Most of them need the ems system id (see previous step).

```python
# The routes exposed by the client:
client.analytic
client.analytic_set
client.asset
client.database
client.ems_profile
client.ems_system
client.navigation
client.parameter_set
client.profile
client.tableau
client.trajectory
client.transfer
client.upload
client.weather
```

## Examples

### Handling errors

Check for and handle error messages from any route

```python
import logging

response = client.analytic.get_analytic_group_contents(ems_id)
if client.is_error(response):
    message = client.get_error_message(response)
    logging.error(message)
```

### Analytic query

Query a time-series parameter for a flight

```python
# List the root analytic group contents
groups = client.analytic.get_analytic_group_contents(ems_id)

# Query a specific analytic
flight = 123
altitude_id = "H4sIAAAAAAAEAG2Q0QuCMBDG34P+B/HdbZVUiApBPQT2kgi9rrn0YM7aZvbnN5JVUvdwfHD34/vu4iPXrbjTs+D7kksDF+DKezRC6ggSvzbmGmHc9z3qF6hVFZ4TMsOnQ5azmjc0AKkNlYz7A/Mm9GusUUkNZa00ijLj+BCTFd6UgApF/XQ68bx4SMHVvkyd1GjX6KytgFER46+FEZBfObOZ2db6eBBJEIlvVGfz4P+LhYRbZ29NyVCzgJD1MgitDIhrrj6+P/h04obj36VPLpuOeVIBAAA="

# Pull out altitude with 100 samples through the file.
query = {
    "select": [
        {
            "analyticId": altitudeId
        }
    ],
    "size": 100
}

altitude = client.analytic.get_query_results(ems_id, flight, query)
```

### Database query

Query and print the top 20 flight ids with a valid takeoff and landing

```python
query = {
  "select": [
    {
      "fieldId": "[-hub-][field][[[ems-core][entity-type][foqa-flights]][[ems-core][base-field][flight.uid]]]",
      "aggregate": "none"
    },
    {
      "fieldId": "[-hub-][field][[[ems-core][entity-type][foqa-flights]][[ems-core][base-field][flight.exist-takeoff]]]",
      "aggregate": "none"
    }
  ],
  "filter": {
      "operator": "and",
      "args": [
          {
              "type": "filter",
              "value": {
                  "operator": "isTrue",
                  "args": [
                      {
                          "type": "field",
                          "value": "[-hub-][field][[[ems-core][entity-type][foqa-flights]][[ems-core][base-field][flight.exist-takeoff]]]"
                      }
                  ]
              }
          },
          {
              "type": "filter",
              "value": {
                  "operator": "isTrue",
                  "args": [
                      {
                          "type": "field",
                          "value": "[-hub-][field][[[ems-core][entity-type][foqa-flights]][[ems-core][base-field][flight.exist-landing]]]"
                      }
                  ]
              }
          }
      ]
  },
  "groupBy": [],
  "orderBy": [],
  "distinct": True,
  "top": 20,
  "format": "display"
}

result = client.database.get_query_results(ems_id, '[ems-core][entity-type][foqa-flights]', query)
pd = pandas.DataFrame(result.rows, columns=['Flight Record', 'Takeoff Exists'])
print(pd)
```

### Async Database query

Run the same query as above, but with paging for a large number of result rows

```python
query['top'] = 5000000

db_id = '[ems-core][entity-type][foqa-flights]'
response = client.database.start_async_query(ems_id, db_id, query)
if client.is_error(response):
    error = client.get_error_message(response)
    raise ValueError(error)

async_query_id = response.id
try:
    start_index = 0
    batch_size = 20000
    while True:
        end_index = start_index + (batch_size - 1)
        read_response = client.database.read_async_query(emsId, db_id, async_query_id, start_index, end_index)
        if client.is_error(read_response):
            break # Some kind of error occurred
        
        if len(read_response.rows) > 0:
            for row in read_response.rows:
                print(row)
        
        if not read_response.has_more_rows:
            break
        
        start_index = end_index + 1
finally:
    client.database.stop_async_query(emsId, db_id, async_query_id)
```