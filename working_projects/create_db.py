import psycopg2

# docker exec -it <container_name> psql -U <username> -d <database_name>
# docker exec -it ae795b6157f3 psql -U myuser -d mydatabase



# # myuser:mypassword@localhost:5432/mydatabase
def create_tables() -> str:
    conn1 = psycopg2.connect(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')
    conn2 = psycopg2.connect(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')
    conn1.rollback()
    conn2.rollback()

# 'pressure', 'geopheight', 'temperature', 'dewpoint', 'humidity',
#        'winddirection', 'windspeedms', 'windums', 'windvms',
#        'precipitationamount', 'totalcloudcover', 'lowcloudcover',
#        'mediumcloudcover', 'highcloudcover', 'radiationglobal',
#        'radiationglobalaccumulation', 'radiationnetsurfaceswaccumulation',
#        'radiationswaccumulation', 'visibility', 'windgust', 'timestamps'

    current_forecast = """ CREATE TABLE IF NOT EXISTS current_forecast(   
            id SERIAL PRIMARY KEY,   
            pressure DECIMAL(12, 4),   
            geopheight DECIMAL(12, 4),
            temperature DECIMAL(12, 4),
            dewpoint DECIMAL(12, 4),   
            humidity DECIMAL(12, 4),   
            winddirection DECIMAL(12, 4),   
            windspeedms DECIMAL(12, 4),   
            windums DECIMAL(12, 4),   
            windvms DECIMAL(12, 4),   
            precipitationamount DECIMAL(12, 4),   
            totalcloudcover DECIMAL(12, 4),   
            lowcloudcover DECIMAL(12, 4),   
            mediumcloudcover DECIMAL(12, 4),   
            highcloudcover DECIMAL(12, 4),   
            radiationglobal DECIMAL(12, 4),   
            radiationglobalaccumulation DECIMAL(12, 4),   
            radiationnetsurfaceswaccumulation DECIMAL(12, 4),   
            radiationswaccumulation DECIMAL(12, 4),   
            visibility DECIMAL(12, 4),   
            windgust DECIMAL(12, 4),   
            timestamps TIMESTAMP UNIQUE,   
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

    """


    tb_raw = """
            CREATE TABLE IF NOT EXISTS raw_forecast(   
            id SERIAL PRIMARY KEY,   
            pressure DECIMAL(12, 4),   
            geopheight DECIMAL(12, 4),
            temperature DECIMAL(12, 4),
            dewpoint DECIMAL(12, 4),   
            humidity DECIMAL(12, 4),   
            winddirection DECIMAL(12, 4),   
            windspeedms DECIMAL(12, 4),   
            windums DECIMAL(12, 4),   
            windvms DECIMAL(12, 4),   
            precipitationamount DECIMAL(12, 4),   
            totalcloudcover DECIMAL(12, 4),   
            lowcloudcover DECIMAL(12, 4),   
            mediumcloudcover DECIMAL(12, 4),   
            highcloudcover DECIMAL(12, 4),   
            radiationglobal DECIMAL(12, 4),   
            radiationglobalaccumulation DECIMAL(12, 4),   
            radiationnetsurfaceswaccumulation DECIMAL(12, 4),   
            radiationswaccumulation DECIMAL(12, 4),   
            visibility DECIMAL(12, 4),   
            windgust DECIMAL(12, 4),     
            timestamps TIMESTAMP,   
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

    """

    try:
        #create raw_forecast table
        cur1 = conn1.cursor()
        
        cur1.execute(query=current_forecast)
    # 

        cur2 = conn2.cursor()
        cur2.execute(query=tb_raw)

        conn1.commit()
        conn2.commit()

        cur1.close()
        cur2.close()

        conn1.close()
        conn2.close()
        return 'success'

    except psycopg2.Error as e:
        return  f'Errror in connecting to docker postgres:   {e} '
    

