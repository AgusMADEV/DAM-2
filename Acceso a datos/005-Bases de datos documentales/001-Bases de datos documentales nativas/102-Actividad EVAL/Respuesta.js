use empresadam;

db.clientes.insertMany([
    {
        nombre: "Agustín",
        apellidos: "Morcillo Aguado",
        telefono: "+34 68547859",
        email: "info@agustin.es"
    },
    {
        nombre: "Elena",
        apellidos: "Botezatu",
        telefono: "+34 123654789",
        email: "info@elena.es"
    },
    {
        nombre: "Lilo",
        apellidos: "Morcillo",
        telefono: "+34 987456321",
        email: "info@lilo.es"
    },
    {
        nombre: "Dipsy",
        apellidos: "Morcillo",
        telefono: "+34 654789321",
        email: "info@dipsy.es"
    }
]);

db.clientes.find();