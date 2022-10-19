

class Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, suppliers):
        self.conn.execute("""
                  INSERT or REPLACE INTO suppliers ( id, name ) VALUES (?, ?)
              """, [suppliers.id, suppliers.name])

    def find_id_by_name(self, name):
        c = self.conn.cursor()
        c.execute(""" 
                SELECT id FROM suppliers WHERE name = ? 
                """, [name])

        return c.fetchone()

    def find_name_by_id(self, id):
        c = self.conn.cursor()
        c.execute(""" 
                SELECT name FROM suppliers WHERE id = ? 
                """, [id])

        return c.fetchone()[0]


class Hats:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, hats):
        self.conn.execute("""
        INSERT or REPLACE INTO hats ( id, topping, supplier, quantity ) VALUES (?, ?, ?, ?)
        """, [hats.id, hats.topping, hats.supplier, hats.quantity])

    def insert_from_repo(self, id, topping, supplier, quantity):
        self.conn.execute("""
                          INSERT or REPLACE INTO hats ( id, topping, supplier, quantity) VALUES (?, ?, ?, ?)
                      """, [id, topping, supplier, quantity])

    def delete(self, id):
        self.conn.execute("""
                DELETE FROM hats WHERE id = ?
         """, [id])

    def get_quantity_by_id(self, id):
        c = self.conn.cursor()
        c.execute(""" 
                SELECT quantity FROM hats WHERE id = ? 
                """, [id])

        return c.fetchone()[0]

    def get_lowest_id_by_topping(self, topping):
        c = self.conn.cursor()
        c.execute(""" 
                SELECT id FROM hats WHERE topping = ? ORDER BY supplier
                """, [topping])
        to_return = c.fetchone()[0]
        return to_return

    def update_quantity(self, id):
        c = self.conn.cursor()
        c.execute("""UPDATE hats SET quantity = quantity - 1 where id = (?) """, [id])

    def find_supplier_by_id(self, id):
        c = self.conn.cursor()
        c.execute(""" 
        SELECT supplier FROM hats WHERE id = ? 
        """, [id])
        return c.fetchone()[0]


class Orders:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, id, location, hat):
        self.conn.execute("""
                  INSERT or REPLACE INTO orders (id, location, hat) VALUES (?, ?, ?)
              """, [id, location, hat])
