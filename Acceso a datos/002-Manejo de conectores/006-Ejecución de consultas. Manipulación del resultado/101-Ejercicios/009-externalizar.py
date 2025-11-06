from yoursql import YourSQL

YourSQL.peticion("USE accesoadatos;")
YourSQL.peticion("SHOW TABLES;")
YourSQL.peticion("INSERT INTO clientes (id, nombre, email, activo) VALUES (1, 'Ana', 'ana@example.com', TRUE), (2, 'Luis O\\'Connor', NULL, FALSE);")
YourSQL.peticion("SELECT * FROM clientes;")

