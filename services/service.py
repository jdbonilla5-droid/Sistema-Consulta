def search_data(search, search_type, attributes, users, computers):
    resultado = []

    
    if search_type == "users":
        valid_attrs = ["nombre", "email", "user"]
    else:
        valid_attrs = ["servidor", "DNS", "SO"]

    #filtra atributos   
    if not attributes:
        attributes = valid_attrs
    else:
        attributes = [a for a in attributes if a in valid_attrs]
    search_values = search.split(";")
    resultado1 = {}

    

    for value in search_values:
        value = value.strip().lower()

        if search_type == "users":
            for u in users:
                if (
                    value in u["nombre"].lower() or
                    value in u["email"].lower() or
                    value in u["user"].lower()
                ):
                    resultado1[u["user"]] = u

        elif search_type == "computers":
            for c in computers:
                if (
                    value in c["servidor"].lower() or
                    value in c["DNS"].lower() or
                    value in c["SO"].lower()
                ):
                    resultado1[c["computers"]] = c

    for item in resultado1.values():
        filtered = {}
        for attr in attributes:
            if attr in item:
                filtered[attr] = item[attr]
        resultado.append(filtered)

    return resultado, attributes