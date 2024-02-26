import psycopg2
from config import host,user,password,db_name
import pandas as pd
from datetime import date



dt=date.today().strftime('%d-%m-%y')

def execute_query_all_pats():
    try:
        conn = psycopg2.connect (
            host=host,
            user=user,
            password=password,
            dbname=db_name,
            port =5432 
        )

        with conn.cursor():
                 sql_query= pd.read_sql("""
                                        SELECT m.num ||'-'|| m.YEAR AS №ИБ,
                                        mm.dept_get_name(h.dept_id) AS Отделение,
                                        to_char(h.input_dt, 'DD.MM.YYYY HH24:MI:SS')  AS Дата_поступления,
                                        to_char(h.hosp_dt, 'DD.MM.YYYY HH24:MI:SS') AS Дата_госпитализации,
                                        to_char(h.hosp_dt - h.input_dt, 'HH24:MI:SS') AS Время,
                                        mm.emp_get_fio_by_id (h.doctor_emp_id) AS Врач

                                        FROM mm.mdoc m 
                                        JOIN mm.hospdoc h ON h.mdoc_id = m.id 


                                        WHERE h.hosp_dt BETWEEN current_date - INTERVAL '1 day, -6 hours' AND current_date - INTERVAL '-6 hours'
                                        AND h.dept_id NOT IN ('7f35c044-8375-4057-8d04-bba5573b4f85')
                                        ORDER BY Отделение ASC
                                        """,conn)
                 writer = pd.ExcelWriter(f'/opt/emg_bot/emgg/Поступившие пациенты за сутки_{dt}.xlsx')
                 df = pd.DataFrame(sql_query)
                 df.to_excel(writer,index=False, sheet_name="Sheet1") 
                 for column in df:
                    column_length = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)
                 writer.close()
    finally:
            if conn:
                conn.close ()
                print ("[INFO] PG CONN CLOSED")