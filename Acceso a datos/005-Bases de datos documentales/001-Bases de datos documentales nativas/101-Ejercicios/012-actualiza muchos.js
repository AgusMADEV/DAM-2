db.clientes.updateMany(
    {email:'info@juan.com'},
    {
        $set:
        {telefono:"11111111"}
    }
)
