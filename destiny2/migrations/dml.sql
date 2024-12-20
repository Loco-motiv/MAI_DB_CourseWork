--few suggestions and approved god rolls
INSERT INTO
    users (login, password, role)
VALUES
    (
        'admin',
        '$2b$12$9detj2AxPbeQQBvRqmxf0uIzULVZnSZ7k4cTaLc0nmKcUA1VNX97e',
        2
    ),
    (
        'moder',
        '$2b$12$1FTi//DNXw0M/m49fYQVV.DzUoIaKc6JDF/GZHzQd2K29klyAAyne',
        1
    ),
    (
        'user',
        '$2b$12$SDzC2rshyxMSa6v84oSEcO/MQyK8mrScNqMjWndeOOprCFvQKxVZi',
        0
    );

-- INSERT INTO
--     god_rolls (
--         weapon_id,
--         user_id,
--         author,
--         description,
--         barrel_id,
--         magazine_id,
--         first_column_id,
--         second_column_id
--     )
-- VALUES
--     (
--         882778888,
--         2,
--         'LocoMelon',
--         'Hype',
--         1467527085,
--         3142289711,
--         191144788,
--         64866129
--     );
INSERT INTO
    god_rolls_prepositions (
        weapon_id,
        user_id,
        author,
        description,
        barrel_id,
        magazine_id,
        first_column_id,
        second_column_id
    )
VALUES
    (
        882778888,
        1,
        'YabLoco',
        'Hype',
        1467527085,
        3142289711,
        191144788,
        64866129
    );