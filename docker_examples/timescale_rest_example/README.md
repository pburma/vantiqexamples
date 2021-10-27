### Provide a Timescale database for Vantiq to read-write into

This example will load a Vantiq edge node and a timeseries database called Timescale. Timescale is based on Postgres and supports many Postgres extensions. This example also loads Postgrest which adds a Rest API for Timescale.

Doc links:
[Postgrest with Timescale](https://postgrest.org/en/v5.2/integrations/timescaledb.html#load-sample-data)
[Postgrest Docker](https://hub.docker.com/u/postgrest)
[Timescale Docker](https://hub.docker.com/r/timescale/timescaledb)

The postgres interface supports many operations like select, insert, update, ect. But the Timescale aggregates are not supported such as select avg(column). In order to access the aggregate queries Views, Functions, Stored Procedures will have to be setup on the Timescale side of things which can then be accessed via Rest.

Here is an example view:
```
create mydata_view AS
SELECT time_bucket('15 minutes', time) AS fifteen_min,
    sensorid, COUNT(*),
    MAX(speed) AS max_speed,
    MAX(alt) AS max_alt
  FROM mydata
  WHERE time > NOW() - INTERVAL '3 hours'
  GROUP BY fifteen_min, sensorid
  ORDER BY fifteen_min DESC, max_speed DESC;
```
The view name max_vtcdata can then be accessed directory at the URL http://<ipaddress>:<port>/max_vtcdata but note that function and stored procedures might appear under different paths such as /rpc/funciton-name.

When creating new tables make sure to convert the psql table to a Timescale hypertable, when using the timescale docker image it seems to happen automatically.

I used [pgAdmin](https://www.pgadmin.org/) to setup my tables and views in Timescale.

To use with Vantiq setup a source that points to the root of the postgrest server. If doing an edge only connection then http://vantiq_edge_timescale:3000 is the URL to default too based on this sample docker-compose.yml. Change the server hostname to whatever you call the service in that file.

A Select is a GET and a Insert is a POST to the tablename in the URL of the postgrest interface. Here is an example of each where the source name is "timescale"
* Returns a VIEW: ```SELECT FROM SOURCE timescale WITH path = "/avg_speed_daily"```
* Inserts into mydata table: ```SELECT FROM SOURCE timescale WITH path = "/mydata", method="POST", body=data```

Data is an object that contains the new row being added. It would also be possible to use a PUBLISH instead of a SELECT but I find its easier to use the SELECT statement and just change the default method to POST.

This example is bare minimum to get up and running and provides no security or authentication for the postgrest endpoints.


