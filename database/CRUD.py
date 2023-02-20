from database.models import db, Favourites


def save(user, title_id: str, title: str) -> None:
    if Favourites.select():
        for collection in Favourites.select():
            if collection.title_id == title_id:
                return
            else:
                Favourites.create(user_id=user, title_id=title_id, title=title)
    else:
        Favourites.create(user_id=user, title_id=title_id, title=title)


def retrieve_collection(user):
    res_list = list()
    for collection in Favourites.select():
        if collection.user_id == str(user):
            res_list.append({
                'title': collection.title,
                'id': collection.title_id
            })
        else:
            return None
    return res_list
