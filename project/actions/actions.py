# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import datetime
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3

conn = sqlite3.connect('sub.db')
print("Data base \"sub.db\" connected successfully")
cursor = conn.cursor()
cursor.execute("create table if not exists Subs("
               "subID INTEGER primary key AUTOINCREMENT,"
               "user TEXT not null,"
               "start TEXT not null,"
               "length INTERGER not null)")
print("Table created successfully")
conn.commit()
conn.close()


class add_plan(Action):

    def name(self) -> Text:
        return "add_plan"

    def run(self, dispatcher, tracker, domain):
        print("successfully plan")
        plan = tracker.get_slot("sub_plan")
        name = tracker.get_slot("user_name")
        print(plan)
        print(name)
        con = sqlite3.connect('sub.db')
        print("sub database successfully set")
        if plan == "monthly_plan":
            dispatcher.utter_message(template="utter_monthly_plan")
            sql_insert_subscription(name, plan)
        elif plan == "annual_plan":
            dispatcher.utter_message(template="utter_annual_plan")
            sql_insert_subscription(name, plan)
        elif plan == "free_plan":
            dispatcher.utter_message(template="utter_free_plan")
            sql_insert_subscription(name, plan)
        return []


class sub_enquiry(Action):

    def name(self) -> Text:
        return "sub_enquiry"

    def run(self, dispatcher, tracker, domain):
        number = tracker.get_slot("sub_number")
        icursor = sql_query(number)
        result = icursor.fetchall()



def sql_insert_subscription(name, plan):
    con = sqlite3.connect("sub.db")

    current_time = datetime.datetime().now()
    length = 0
    if plan == "monthly_plan":
        length = 30
    elif plan == "annual_plan":
        length = 360
    elif plan == "free_plan":
        length = 14

    print("insert connection success")
    insert_string = "insert into Subs (user, start, length)" \
                    "values (, " + name + ", " + current_time + ", " + length + ")"
    icursor = con.cursor()


def sql_query(number):
    con = sqlite3.connect("sub.db")
    icursor = con.execute("select * from Subs where subID = \'" + number + "\'")

    for row in icursor:
        print(f'ID: {row[0]}  |  Name: {row[1]}  |  starting Time: {row[2]}  |  length: {row[3]}')
    return icursor

# class AddSubPlans(Action):
#     def name(self) -> Text:
#         return ""

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
