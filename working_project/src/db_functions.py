from sqlalchemy import text, create_engine
from sqlalchemy.exc import (
    ProgrammingError,
    OperationalError,
    IntegrityError,
    SQLAlchemyError
)
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

def create_tables(engine) -> bool:
    """
    create_tables
    receives engine to connect to db and creates 2 tables 
    one for every day use with stricted conditions and one for recovery situations that stores everything
    :param engine: sqlalchemy engine for connection
    :return: bool
    :rtype: bool
    """


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

# this table was create to deal with unexpected problems that might arise and cannot be predicted yet
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
        with engine.connect() as conn:
            conn.execute(text(current_forecast))
            conn.execute(text(tb_raw))
            conn.commit()
        logger.info('table was created successfully')
        return True

    except OperationalError as oe:
        logger.error(f'Cannot connect to database:   {oe} ')
        return False
    except ProgrammingError as pe:

        logger.error(f'SQL syntax error:   {pe} ')
        return False

    except SQLAlchemyError as sqe:
        # catch all error
        logger.error(f'Database error:   {sqe} ')
        return False



def latest_timestamp(engine) -> datetime | None:
    """
    latest_timestamp
    this function fetchest latest added row of the db table current_forecast 
    column timestams
    
    :param engine: sqlalchemy engine
    :return: datetime object
    :rtype: object
    """


    with engine.connect() as conn:
        try:
            # queries lastest cell of the column timestamps
            result = conn.execute(text('SELECT timestamps FROM current_forecast ORDER BY timestamps DESC LIMIT 1;'))
            # returns tuple (timestamp,)
            if result:
                latest = result.fetchone()
                return latest[0]
        except ProgrammingError as pe:
            logger.error(f'SQL syntax error:   {pe} ')
        except OperationalError as oe:
            logger.error(f'Cannot connect to database:   {oe} ')