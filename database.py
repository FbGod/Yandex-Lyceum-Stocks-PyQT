import sqlite3

con = sqlite3.connect("database/stocks.db")


def connect_to_deal(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""select d.id, dt.Type, dp.PlaceFull, c.CurrencyFull, d.Number, d.Tiker, d.Orderr, d.Quantity, d.Price, d.TotalCost, d.Trader, d.Commision 
    from Deal d 
    join DealType dt on (d.TypeID = dt.id) 
    inner join DealPlace dp on (d.PlaceID = dp.id) 
    inner join Currency c on (c.id = d.CurrencyID);""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO Deal(TypeID, PlaceID, CurrencyID, Number, Tiker, Orderr, Quantity, Price, TotalCost, Trader, Commision) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                       (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10]))
        con.commit()
    elif request == 'update':
        print(args)
        cursor.execute("UPDATE Deal SET TypeID=(?), PlaceID=(?), CurrencyID=(?), Number=(?), Tiker=(?), Orderr=(?), Quantity=(?), Price=(?), TotalCost=(?), Trader=(?), Commision=(?) WHERE id=(?)",
                       (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], int(args[-1])))
        con.commit()
    elif request == 'delete':
        print(args)
        cursor.execute("DELETE FROM Deal WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'dialog':
        return cursor.execute("""SELECT * FROM Deal WHERE id = ?""", (args[0],)).fetchall()


def connect_to_deal_place(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM DealPlace""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO DealPlace(PlaceFull,PlaceShort) VALUES (?,?)""", (args[0], args[1]))
        con.commit()
    elif request == 'delete':

        cursor.execute("DELETE FROM Deal WHERE PlaceID IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))

        cursor.execute("DELETE FROM DealPlace WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(update_list[0], update_list[1], old)
        cursor.execute("UPDATE DealPlace SET PlaceFull = (?), PlaceShort = (?) WHERE id = (?)", (update_list[0], update_list[1], old))
        con.commit()


def connect_to_deal_type(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM DealType""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO DealType(Type) VALUES (?)""", (args[0]))
        con.commit()
    elif request == 'delete':
        cursor.execute("DELETE FROM Deal WHERE TypeID IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))

        cursor.execute("DELETE FROM DealType WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(args)
        cursor.execute("UPDATE DealType SET Type = (?) WHERE id = (?)", (update_list[0], old))
        con.commit()


def connect_to_currency(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM Currency""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO Currency(CurrencyFull,CurrencyShort) VALUES (?,?)""", (args[0], args[1]))
        con.commit()
    elif request == 'delete':
        cursor.execute("DELETE FROM Deal WHERE CurrencyID IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))

        cursor.execute("DELETE FROM Currency WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(update_list[0], update_list[1], old)
        cursor.execute("UPDATE Currency SET CurrencyFull = (?), CurrencyShort = (?) WHERE id = (?)", (update_list[0], update_list[1], old))
        con.commit()
