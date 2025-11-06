db.clientes.updateOne(
    {nombre:'Jose Vicente'},
    {
        $set:
        {email:"info@jocarsa.com"}
    }
)
