def search_data(search, search_type, attributes, users, computers):
    results = []

    if search_type == "users":
        valid_attrs = ["nombre", "email", "user"]
    else:
        valid_attrs = ["nombre_servidor", "DNS", "SO"]

    if not attributes:
        attributes = valid_attrs
    else:
        attributes = [a for a in attributes if a in valid_attrs]

    search_values = search.split(";")
    results_dict = {}

    for value in search_values:
        value = value.strip().lower()

        if search_type == "users":
            for u in users:
                if (
                    value in u["nombre"].lower() or
                    value in u["email"].lower() or
                    value in u["user"].lower()
                ):
                    results_dict[u["user"]] = u

        elif search_type == "computers":
            for c in computers:
                if (
                    value in c["nombre_servidor"].lower() or
                    value in c["DNS"].lower() or
                    value in c["SO"].lower()
                ):
                    results_dict[c["nombre_servidor"]] = c

    for item in results_dict.values():
        filtered = {}
        for attr in attributes:
            if attr in item:
                filtered[attr] = item[attr]
        results.append(filtered)

    return results, attributes