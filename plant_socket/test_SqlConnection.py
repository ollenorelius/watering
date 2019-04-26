from SqlConnection import SqlConnection

def test_add_plants_and_read_them_back():
    plant_names = ["doot", "toot", "habanero", "foo", "bar"]
    sql = SqlConnection(":memory:")
    for name in plant_names:
        sql.add_plant(name)

    db_names = sql.get_plants()

    for db, gt in zip(db_names, plant_names):
        assert db["name"] == gt 


def test_add_data_points_and_read_them_back():
    plant_names = ["doot", "toot", "habanero", "foo", "bar"]
    sql = SqlConnection(":memory:")
    for name in plant_names:
        sql.add_plant(name)

    data = [("toot", 500), 
    ("toot", 510),
    ("toot", 520),
    ("toot", 530),
    ("toot", 540),
    ("doot", 400),
    ("doot", 590)]

    for data_point in data:
        sql.add_data_point(*data_point)

    db_data_toot = sql.get_data_for_plant("toot")
    db_data_doot = sql.get_data_for_plant("doot")

    gt_data_toot =  [x for x in data if x[0] == "toot"]
    gt_data_doot =  [x for x in data if x[0] == "doot"] 

    for db, gt in zip(db_data_toot, gt_data_toot):
        assert db["dryness"] == gt[1]

    for db, gt in zip(db_data_doot, gt_data_doot):
        assert db["dryness"] == gt[1]