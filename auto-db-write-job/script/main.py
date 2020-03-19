import os
import requests
import openpyxl as px
import psycopg2
import uuid
from bs4 import BeautifulSoup
import settings as env
from servant import FileDownLoader, XlsDateToIsoConverter, OnsetDateProvider, IsRelationConverter


def db_connect():
    return psycopg2.connect(env.AWJ_DB_CONNECT_SETUP)


def main():
    if os.path.isfile(env.FILE_NAME):
        os.remove(env.FILE_NAME)

    res = requests.get("https://web.pref.hyogo.lg.jp/kk03/corona_kanjyajyokyo.html")

    soup = BeautifulSoup(res.content, "html.parser")
    xls_link = soup.select("#tmp_contents a.icon_excel")

    fdl = FileDownLoader.Summon("https://web.pref.hyogo.lg.jp" + xls_link[0]["href"], env.FILE_NAME)
    fdl.service()

    wb = px.load_workbook(env.FILE_NAME)
    sheet = wb["公表"]

    with db_connect() as conn:
        with conn.cursor() as db:

            for irow in range(5, sheet.max_row - 1):

                infected_people_id = uuid.uuid4()
                infected_people_no = sheet.cell(row=irow, column=2).value

                xdic = XlsDateToIsoConverter.Summon(sheet.cell(row=irow, column=3).value)
                odp = OnsetDateProvider.Summon(sheet.cell(row=irow, column=9).value)

                db.execute("SELECT EXISTS (SELECT * FROM infected_peoples WHERE no = %s);", (infected_people_no,))
                (is_exist_infected_people,) = db.fetchone()

                if not is_exist_infected_people:
                    db.execute("""
                        INSERT
                        INTO infected_peoples (
                            id,
                            no,
                            confirmed_date,
                            age_group,
                            sex,
                            jurisdiction,
                            residence,
                            occupation,
                            onset_date,
                            travel_history,
                            remarks
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        str(infected_people_id),
                        infected_people_no,
                        xdic.service(),
                        sheet.cell(row=irow, column=4).value,
                        sheet.cell(row=irow, column=5).value,
                        sheet.cell(row=irow, column=6).value,
                        sheet.cell(row=irow, column=7).value,
                        sheet.cell(row=irow, column=8).value,
                        odp.service(),
                        sheet.cell(row=irow, column=10).value,
                        sheet.cell(row=irow, column=11).value
                    ))

                    infected_place_no = 0
                    for icol in range(12, sheet.max_column - 1):
                        if sheet.cell(row=4, column=icol).value is None:
                            continue
                        infected_place_id = uuid.uuid4()
                        infected_place_no += 1
                        irc = IsRelationConverter.Summon(sheet.cell(row=irow, column=icol).value)
                        db.execute("""
                            INSERT
                            INTO infected_places (
                                id,
                                no,
                                infected_people_id,
                                name,
                                is_relation
                            )
                            VALUES (%s, %s, %s, %s, %s);
                        """, (
                            str(infected_place_id),
                            infected_place_no,
                            str(infected_people_id),
                            sheet.cell(row=4, column=icol).value.replace("\n", ""),
                            irc.service()
                        ))
                else:

                    db.execute("""
                        UPDATE infected_peoples
                        SET confirmed_date = %s,
                        age_group = %s,
                        sex = %s,
                        jurisdiction = %s,
                        residence = %s,
                        occupation = %s,
                        onset_date = %s,
                        travel_history = %s,
                        remarks = %s
                        WHERE no = %s;
                    """, (
                        xdic.service(),
                        sheet.cell(row=irow, column=4).value,
                        sheet.cell(row=irow, column=5).value,
                        sheet.cell(row=irow, column=6).value,
                        sheet.cell(row=irow, column=7).value,
                        sheet.cell(row=irow, column=8).value,
                        odp.service(),
                        sheet.cell(row=irow, column=10).value,
                        sheet.cell(row=irow, column=11).value,
                        infected_people_no
                    ))

                    db.execute("SELECT id FROM infected_peoples WHERE no = %s;", (infected_people_no,))
                    (infected_people_id,) = db.fetchone()

                    infected_place_no = 0
                    for icol in range(12, sheet.max_column):
                        if sheet.cell(row=4, column=icol).value is None:
                            continue
                        infected_place_no += 1
                        irc = IsRelationConverter.Summon(sheet.cell(row=irow, column=icol).value)
                        db.execute("""
                            UPDATE infected_places
                            SET is_relation = %s, name = %s
                            WHERE no = %s AND infected_people_id = %s;
                        """, (
                            irc.service(),
                            sheet.cell(row=4, column=icol).value.replace("\n", ""),
                            infected_place_no,
                            infected_people_id
                        ))


if __name__ == '__main__':
    main()