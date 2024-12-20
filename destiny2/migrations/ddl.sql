CREATE TABLE
    perks (
        id BIGINT PRIMARY KEY,
        name VARCHAR(32) NOT NULL,
        description TEXT NOT NULL,
        icon VARCHAR(32)
    );

COMMENT ON TABLE perks IS 'Perks data';

COMMENT ON COLUMN perks.id IS 'Perk hash';

CREATE TABLE
    perk_sets (id BIGINT PRIMARY KEY);

COMMENT ON TABLE perk_sets IS 'Perk sets data';

COMMENT ON COLUMN perk_sets.id IS 'Perk set hash';

CREATE TABLE
    sets_perks (
        id BIGINT REFERENCES perk_sets (id) ON DELETE CASCADE,
        perk_id BIGINT NOT NULL REFERENCES perks (id) ON DELETE CASCADE,
        PRIMARY KEY (id, perk_id)
    );

COMMENT ON TABLE sets_perks IS 'Sets perks data';

COMMENT ON COLUMN sets_perks.id IS 'Sets perk hash';

CREATE TABLE
    weapons (
        id BIGINT PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        rarity_id SMALLINT NOT NULL,
        type_id SMALLINT NOT NULL,
        archetype_id BIGINT NOT NULL REFERENCES perks (id) ON DELETE CASCADE,
        element_id SMALLINT NOT NULL,
        icon VARCHAR(32) NOT NULL,
        barrel_set_id BIGINT REFERENCES perk_sets (id) ON DELETE CASCADE,
        magazine_set_id BIGINT REFERENCES perk_sets (id) ON DELETE CASCADE,
        first_column_set_id BIGINT REFERENCES perk_sets (id) ON DELETE CASCADE,
        second_column_set_id BIGINT REFERENCES perk_sets (id) ON DELETE CASCADE
    );

COMMENT ON TABLE weapons IS 'Weapons data';

COMMENT ON COLUMN weapons.id IS 'Weapon hash';

CREATE TABLE
    armor (
        id BIGINT PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        rarity_id SMALLINT NOT NULL,
        type_id SMALLINT NOT NULL,
        icon VARCHAR(32) NOT NULL,
        class_id SMALLINT NOT NULL
    );

COMMENT ON TABLE armor IS 'Armor data';

COMMENT ON COLUMN armor.id IS 'Armor hash';

CREATE TABLE
    weapon_sources (
        id BIGINT PRIMARY KEY,
        weapon_id BIGINT NOT NULL REFERENCES weapons (id) ON DELETE CASCADE,
        name TEXT
    );

COMMENT ON TABLE weapon_sources IS 'Weapon source data';

COMMENT ON COLUMN weapon_sources.id IS 'Weapon source hash';

CREATE TABLE
    armor_sources (
        id BIGINT PRIMARY KEY,
        armor_id BIGINT NOT NULL REFERENCES armor (id) ON DELETE CASCADE,
        name TEXT
    );

COMMENT ON TABLE armor_sources IS 'Armor source data';

COMMENT ON COLUMN armor_sources.id IS 'Armor source hash';

CREATE TABLE
    IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        login TEXT NOT NULL,
        password VARCHAR(72) NOT NULL,
        role INTEGER NOT NULL
    );

COMMENT ON TABLE users IS 'Users data';

COMMENT ON COLUMN users.id IS 'User id';

CREATE TABLE
    IF NOT EXISTS god_rolls (
        id BIGSERIAL PRIMARY KEY,
        weapon_id BIGINT NOT NULL REFERENCES weapons (id) ON DELETE CASCADE,
        user_id BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        author TEXT NOT NULL,
        description TEXT NOT NULL,
        barrel_id BIGINT REFERENCES perks (id) ON DELETE CASCADE,
        magazine_id BIGINT REFERENCES perks (id) ON DELETE CASCADE,
        first_column_id BIGINT REFERENCES perks (id) ON DELETE CASCADE,
        second_column_id BIGINT REFERENCES perks (id) ON DELETE CASCADE
    );

COMMENT ON TABLE god_rolls IS 'God rolls data';

COMMENT ON COLUMN god_rolls.id IS 'Roll id';

CREATE TABLE
    IF NOT EXISTS god_rolls_prepositions (
        id BIGSERIAL PRIMARY KEY,
        weapon_id BIGINT NOT NULL REFERENCES weapons (id) ON DELETE CASCADE,
        user_id BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        author TEXT NOT NULL,
        description TEXT NOT NULL,
        barrel_id BIGINT REFERENCES perks (id) ON DELETE CASCADE,
        magazine_id BIGINT REFERENCES perks (id) ON DELETE CASCADE,
        first_column_id BIGINT REFERENCES perks (id) ON DELETE CASCADE,
        second_column_id BIGINT REFERENCES perks (id) ON DELETE CASCADE
    );

COMMENT ON TABLE god_rolls_prepositions IS 'God rolls prepositions data';

COMMENT ON COLUMN god_rolls_prepositions.id IS 'God roll preposition id';

CREATE VIEW
    v_weapons_page AS
SELECT
    w.id,
    w."name",
    w.rarity_id,
    w.type_id,
    p."name" AS archetype_name,
    p.icon AS archetype_icon,
    w.element_id,
    w.icon AS weapon_icon,
    ws."name" AS source
FROM
    weapons w
    LEFT JOIN weapon_sources ws on (w.id = ws.weapon_id)
    JOIN perks p ON (w.archetype_id = p.id);

COMMENT ON VIEW v_weapons_page IS 'Full data on weapons except perks';

CREATE VIEW
    v_first_column AS
SELECT DISTINCT
    p.name
FROM
    weapons w
    JOIN sets_perks sp ON (w.first_column_set_id = sp.id)
    JOIN perks p ON (sp.perk_id = p.id);

COMMENT ON VIEW v_first_column IS 'Perks of first column';

CREATE VIEW
    v_second_column AS
SELECT DISTINCT
    p.name
FROM
    weapons w
    JOIN sets_perks sp ON (w.second_column_set_id = sp.id)
    JOIN perks p ON (sp.perk_id = p.id);

COMMENT ON VIEW v_second_column IS 'Perks of second column';

CREATE VIEW
    v_armor_page AS
SELECT
    a.id,
    a."name",
    a.rarity_id,
    a.type_id,
    a.class_id,
    a.icon AS armor_icon,
    as2."name" AS source
FROM
    armor a
    LEFT JOIN armor_sources as2 on (a.id = as2.armor_id);

COMMENT ON VIEW v_armor_page IS 'Full data on armor';

CREATE
OR REPLACE FUNCTION filter_by_two_columns (first_name VARCHAR(32), second_name VARCHAR(32)) returns TABLE (
    id BIGINT,
    name VARCHAR(64),
    rarity_id SMALLINT,
    type_id SMALLINT,
    archetype_name VARCHAR(32),
    archetype_icon VARCHAR(32),
    element_id SMALLINT,
    weapon_icon VARCHAR(32),
    source TEXT
) AS '
  SELECT distinct
    w.id,
    w."name",
    w.rarity_id,
    w.type_id,
    p."name" AS archetype_name,
    p.icon AS archetype_icon,
    w.element_id,
    w.icon AS weapon_icon,
    ws."name" AS source
FROM
    weapons w
    JOIN sets_perks sp ON w.first_column_set_id = sp.id
    JOIN perks p1 ON sp.perk_id = p1.id
    JOIN sets_perks sp2 ON w.second_column_set_id = sp2.id
    JOIN perks p2 ON sp2.perk_id = p2.id
	LEFT JOIN weapon_sources ws on (w.id = ws.weapon_id)
    JOIN perks p ON (w.archetype_id = p.id)
WHERE
    p1.name = first_name
    AND p2.name = second_name;
' LANGUAGE sql;

COMMENT ON FUNCTION filter_by_two_columns IS 'Filter weapons based on provided 2 perks';

CREATE
OR REPLACE FUNCTION filter_by_first_column (perk_name VARCHAR(32)) returns TABLE (
    id BIGINT,
    name VARCHAR(64),
    rarity_id SMALLINT,
    type_id SMALLINT,
    archetype_name VARCHAR(32),
    archetype_icon VARCHAR(32),
    element_id SMALLINT,
    weapon_icon VARCHAR(32),
    source TEXT
) AS '
  SELECT distinct
    w.id,
    w."name",
    w.rarity_id,
    w.type_id,
    p."name" AS archetype_name,
    p.icon AS archetype_icon,
    w.element_id,
    w.icon AS weapon_icon,
    ws."name" AS source
FROM
    weapons w
    JOIN sets_perks sp2 ON w.first_column_set_id = sp2.id
    JOIN perks p2 ON sp2.perk_id = p2.id
	LEFT JOIN weapon_sources ws on (w.id = ws.weapon_id)
    JOIN perks p ON (w.archetype_id = p.id)
WHERE
    p2.name = perk_name;
' LANGUAGE sql;

COMMENT ON FUNCTION filter_by_first_column IS 'Filter weapons based on provided first column perk';

CREATE
OR REPLACE FUNCTION filter_by_second_column (perk_name VARCHAR(32)) returns TABLE (
    id BIGINT,
    name VARCHAR(64),
    rarity_id SMALLINT,
    type_id SMALLINT,
    archetype_name VARCHAR(32),
    archetype_icon VARCHAR(32),
    element_id SMALLINT,
    weapon_icon VARCHAR(32),
    source TEXT
) AS '
  SELECT distinct
    w.id,
    w."name",
    w.rarity_id,
    w.type_id,
    p."name" AS archetype_name,
    p.icon AS archetype_icon,
    w.element_id,
    w.icon AS weapon_icon,
    ws."name" AS source
FROM
    weapons w
    JOIN sets_perks sp2 ON w.second_column_set_id = sp2.id
    JOIN perks p2 ON sp2.perk_id = p2.id
	LEFT JOIN weapon_sources ws on (w.id = ws.weapon_id)
    JOIN perks p ON (w.archetype_id = p.id)
WHERE
    p2.name = perk_name;
' LANGUAGE sql;

COMMENT ON FUNCTION filter_by_second_column IS 'Filter weapons based on provided second column perk';

CREATE
OR REPLACE FUNCTION weapon_barrel_perks (w_id BIGINT) returns TABLE (
    barrel_id BIGINT,
    barrel_name VARCHAR(32),
    barrel_description TEXT,
    barrel_icon VARCHAR(32)
) AS '
    SELECT p.id barrel_id, p.name barrel_name, p.description barrel_description, p.icon barrel_icon
    FROM weapons w JOIN sets_perks sp ON (w.barrel_set_id = sp.id) JOIN perks p ON (sp.perk_id = p.id)
    WHERE w.id = w_id
' LANGUAGE sql;

COMMENT ON FUNCTION weapon_barrel_perks IS 'Get barrel perks for specific weapon';

CREATE
OR REPLACE FUNCTION weapon_magazine_perks (w_id BIGINT) returns TABLE (
    magazine_id BIGINT,
    magazine_name VARCHAR(32),
    magazine_description TEXT,
    magazine_icon VARCHAR(32)
) AS '
    SELECT p.id magazine_id, p.name magazine_name, p.description magazine_description, p.icon magazine_icon
    FROM weapons w JOIN sets_perks sp ON (w.magazine_set_id = sp.id) JOIN perks p ON (sp.perk_id = p.id)
    WHERE w.id = w_id
' LANGUAGE sql;

COMMENT ON FUNCTION weapon_magazine_perks IS 'Get magazine perks for specific weapon';

CREATE
OR REPLACE FUNCTION weapon_first_column_perks (w_id BIGINT) returns TABLE (
    first_column_id BIGINT,
    first_column_name VARCHAR(32),
    first_column_description TEXT,
    first_column_icon VARCHAR(32)
) AS '
    SELECT p.id first_column_id, p.name first_column_name, p.description first_column_description, p.icon first_column_icon
    FROM weapons w JOIN sets_perks sp ON (w.first_column_set_id = sp.id) JOIN perks p ON (sp.perk_id = p.id)
    WHERE w.id = w_id
' LANGUAGE sql;

COMMENT ON FUNCTION weapon_first_column_perks IS 'Get first column perks for specific weapon';

CREATE
OR REPLACE FUNCTION weapon_second_column_perks (w_id BIGINT) returns TABLE (
    second_column_id BIGINT,
    second_column_name VARCHAR(32),
    second_column_description TEXT,
    second_column_icon VARCHAR(32)
) AS '
    SELECT p.id second_column_id, p.name second_column_name, p.description second_column_description, p.icon second_column_icon
    FROM weapons w JOIN sets_perks sp ON (w.second_column_set_id = sp.id) JOIN perks p ON (sp.perk_id = p.id)
    WHERE w.id = w_id
' LANGUAGE sql;

COMMENT ON FUNCTION weapon_second_column_perks IS 'Get second column perks for specific weapon';

CREATE
OR REPLACE function user_data (l_login TEXT) RETURNS TABLE (id BIGINT, password VARCHAR(72), role INTEGER) AS '  
  SELECT id, password, role
  FROM users
  WHERE login = l_login
' LANGUAGE sql;

COMMENT ON FUNCTION user_data IS 'Get user data';

CREATE
OR REPLACE PROCEDURE register_user (l_login TEXT, l_password VARCHAR(72)) LANGUAGE SQL BEGIN ATOMIC
INSERT INTO
    users (id, login, password, role)
VALUES
    (DEFAULT, l_login, l_password, 0);

END;

COMMENT ON PROCEDURE register_user IS 'Register new user';

CREATE VIEW
    v_god_rolls AS
SELECT
    gr.id,
    gr.author,
    gr.description,
    w.name as weapon_name,
    w.icon as weapon_icon,
    p1.name as barrel_name,
    p1.icon as barrel_icon,
    p2.name as magazine_name,
    p2.icon as magazine_icon,
    p3.name as first_column_name,
    p3.icon as first_column_icon,
    p4.name as second_column_name,
    p4.icon as second_column_icon
FROM
    god_rolls gr
    JOIN weapons w on (gr.weapon_id = w.id)
    JOIN perks p1 on (gr.barrel_id = p1.id)
    JOIN perks p2 ON (gr.magazine_id = p2.id)
    JOIN perks p3 on (gr.first_column_id = p3.id)
    JOIN perks p4 on (gr.second_column_id = p4.id);

COMMENT ON VIEW v_god_rolls IS 'Full data on god rolls';

CREATE
OR REPLACE PROCEDURE submit_godroll (
    l_weapon_id BIGINT,
    l_user_id BIGINT,
    l_author TEXT,
    l_description TEXT,
    l_barrel_id BIGINT,
    l_magazine_id BIGINT,
    l_first_column_id BIGINT,
    l_second_column_id BIGINT
) LANGUAGE SQL BEGIN ATOMIC
INSERT INTO
    god_rolls_prepositions (
        id,
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
        DEFAULT,
        l_weapon_id,
        l_user_id,
        l_author,
        l_description,
        l_barrel_id,
        l_magazine_id,
        l_first_column_id,
        l_second_column_id
    );

END;

COMMENT ON PROCEDURE register_user IS 'Insert in god_rolls_prepositions new godroll preposition';

CREATE VIEW
    v_godroll_prepositions AS
SELECT
    gr.id,
    gr.author,
    gr.description,
    gr.user_id,
    w.name as weapon_name,
    w.icon as weapon_icon,
    p1.name as barrel_name,
    p1.icon as barrel_icon,
    p2.name as magazine_name,
    p2.icon as magazine_icon,
    p3.name as first_column_name,
    p3.icon as first_column_icon,
    p4.name as second_column_name,
    p4.icon as second_column_icon
FROM
    god_rolls_prepositions gr
    JOIN weapons w on (gr.weapon_id = w.id)
    JOIN perks p1 on (gr.barrel_id = p1.id)
    JOIN perks p2 ON (gr.magazine_id = p2.id)
    JOIN perks p3 on (gr.first_column_id = p3.id)
    JOIN perks p4 on (gr.second_column_id = p4.id);

COMMENT ON VIEW v_god_rolls IS 'Full data on god roll prepositions';

CREATE
OR REPLACE PROCEDURE approve_godroll (l_id BIGINT) LANGUAGE SQL BEGIN ATOMIC
INSERT INTO
    god_rolls (
        id,
        weapon_id,
        user_id,
        author,
        description,
        barrel_id,
        magazine_id,
        first_column_id,
        second_column_id
    )
SELECT
    id,
    weapon_id,
    user_id,
    author,
    description,
    barrel_id,
    magazine_id,
    first_column_id,
    second_column_id
FROM
    god_rolls_prepositions
WHERE
    id = l_id;

END;

COMMENT ON PROCEDURE register_user IS 'Approve godroll';

CREATE
OR REPLACE FUNCTION delete_approved_godroll () RETURNS trigger AS '
BEGIN
  DELETE FROM god_rolls_prepositions WHERE id = NEW.id;
  RETURN NULL;
END;
' LANGUAGE PLPGSQL;

COMMENT ON FUNCTION delete_approved_godroll IS 'Function for after_insert_god_roll trigger';

CREATE
OR REPLACE TRIGGER after_insert_god_roll AFTER INSERT ON god_rolls FOR EACH ROW EXECUTE FUNCTION delete_approved_godroll ();

COMMENT ON TRIGGER after_insert_god_roll ON god_rolls IS 'Handle deleting from god_rolls_prepositions';

CREATE
OR REPLACE PROCEDURE raise_user (l_login TEXT) LANGUAGE SQL BEGIN ATOMIC
UPDATE users
SET
    role = 1
WHERE
    login = l_login;

END;

COMMENT ON PROCEDURE raise_user IS 'Raise in role user';

CREATE
OR REPLACE PROCEDURE denote_user (l_login TEXT) LANGUAGE SQL BEGIN ATOMIC
UPDATE users
SET
    role = 0
WHERE
    login = l_login;

END;

COMMENT ON PROCEDURE denote_user IS 'Denote in role user';