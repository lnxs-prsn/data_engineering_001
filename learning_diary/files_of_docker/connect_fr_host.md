psql -h localhost -p 5432 -U myuser -d mydatabase

docker exec -it my-postgres psql -U myuser -d mydatabase

conn from apps 
postgresql://myuser:mypassword@localhost:5432/mydatabase
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
