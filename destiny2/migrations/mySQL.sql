-- weapons
SELECT
    json->>"hash" as id,
    json->"displayProperties"->>"name" as name,
    json->"inventory"->>"tierType" as rarity_id,
    json->>"itemSubType" AS type_id,
    json->"sockets"->"socketEntries"->0->>"singleInitialItemHash" as archetype_id,
    json->>"defaultDamageType" as element_id,
    SUBSTRING(json->"displayProperties"->>"icon", 32, 32) as icon,
    case
        when json->"sockets"->"socketEntries"->1->>"plugSources" in (2, 6, 0) then COALESCE(
            json->"sockets"->"socketEntries"->1->>"randomizedPlugSetHash",
            json->"sockets"->"socketEntries"->1->>"reusablePlugSetHash"
        )
        else NULL
    end as barrel_set_id,
    case
        when json->"sockets"->"socketEntries"->2->>"plugSources" in (2, 6, 0) then COALESCE(
            json->"sockets"->"socketEntries"->2->>"randomizedPlugSetHash",
            json->"sockets"->"socketEntries"->2->>"reusablePlugSetHash"
        )
        else NULL
    end as magazine_set_id,
    case
        when json->"sockets"->"socketEntries"->3->>"plugSources" in (2, 6, 0) then COALESCE(
            json->"sockets"->"socketEntries"->3->>"randomizedPlugSetHash",
            json->"sockets"->"socketEntries"->3->>"reusablePlugSetHash"
        )
        else NULL
    end as first_column_set_id,
    case
        when json->"sockets"->"socketEntries"->4->>"plugSources" in (2, 6, 0) then COALESCE(
            json->"sockets"->"socketEntries"->4->>"randomizedPlugSetHash",
            json->"sockets"->"socketEntries"->4->>"reusablePlugSetHash"
        )
        else NULL
    end as second_column_set_id
FROM
    DestinyInventoryItemDefinition
where
    json->>"defaultDamageType" <> 0;

-- armor
SELECT
    json->>"hash" as id,
    json->"displayProperties"->>"name" as name,
    json->"inventory"->>"tierType" as rarity_id,
    json->>"itemSubType" AS type_id,
    SUBSTRING(json->"displayProperties"->>"icon", 32, 32) as icon,
    json->>"classType" AS class_id
FROM
    DestinyInventoryItemDefinition
where
    json->>"itemType" = 2;

-- perk sets
SELECT
    DestinyPlugSetDefinition.json->>"hash" as id
FROM
    DestinyPlugSetDefinition
WHERE
    DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->1->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->1->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->1->>"reusablePlugSetHash"
                )
                else NULL
            end as barrel_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    )
    or DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->2->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->2->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->2->>"reusablePlugSetHash"
                )
                else NULL
            end as magazine_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    )
    or DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->3->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->3->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->3->>"reusablePlugSetHash"
                )
                else NULL
            end as first_column_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    )
    or DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->4->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->4->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->4->>"reusablePlugSetHash"
                )
                else NULL
            end as second_column_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    );

-- sets perks
SELECT DISTINCT
    DestinyPlugSetDefinition.json->>"hash" as id,
    perk.value->>"plugItemHash" as perk_id
FROM
    DestinyPlugSetDefinition,
    json_each (
        DestinyPlugSetDefinition.json,
        '$."reusablePlugItems"'
    ) AS perk
WHERE
    DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->1->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->1->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->1->>"reusablePlugSetHash"
                )
                else NULL
            end as barrel_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    )
    or DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->2->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->2->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->2->>"reusablePlugSetHash"
                )
                else NULL
            end as magazine_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    )
    or DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->3->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->3->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->3->>"reusablePlugSetHash"
                )
                else NULL
            end as first_column_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    )
    or DestinyPlugSetDefinition.json->>"hash" in (
        SELECT DISTINCT
            case
                when json->"sockets"->"socketEntries"->4->>"plugSources" in (2, 6, 0) then COALESCE(
                    json->"sockets"->"socketEntries"->4->>"randomizedPlugSetHash",
                    json->"sockets"->"socketEntries"->4->>"reusablePlugSetHash"
                )
                else NULL
            end as second_column_set_id
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"defaultDamageType" <> 0
    );

-- perks
SELECT
    json->>"hash" as id,
    json->"displayProperties"->>"name" as name,
    json->"displayProperties"->>"description" as description,
    SUBSTRING(json->"displayProperties"->>"icon", 32, 32) as icon
FROM
    DestinyInventoryItemDefinition
where
    json->"hash" in (
        SELECT DISTINCT
            perk.value->"plugItemHash" as perk_id
        FROM
            DestinyPlugSetDefinition,
            json_each (
                DestinyPlugSetDefinition.json,
                '$."reusablePlugItems"'
            ) AS perk
        WHERE
            DestinyPlugSetDefinition.json->"hash" in (
                SELECT DISTINCT
                    case
                        when json->"sockets"->"socketEntries"->0->>"plugSources" in (2, 6) then COALESCE(
                            json->"sockets"->"socketEntries"->0->"randomizedPlugSetHash",
                            json->"sockets"->"socketEntries"->0->"reusablePlugSetHash"
                        )
                        else NULL
                    end as frame_id
                FROM
                    DestinyInventoryItemDefinition
                where
                    json->>"defaultDamageType" <> 0
            )
            or DestinyPlugSetDefinition.json->"hash" in (
                SELECT DISTINCT
                    case
                        when json->"sockets"->"socketEntries"->1->>"plugSources" in (2, 6, 0) then COALESCE(
                            json->"sockets"->"socketEntries"->1->"randomizedPlugSetHash",
                            json->"sockets"->"socketEntries"->1->"reusablePlugSetHash"
                        )
                        else NULL
                    end as barrel_set_id
                FROM
                    DestinyInventoryItemDefinition
                where
                    json->>"defaultDamageType" <> 0
            )
            or DestinyPlugSetDefinition.json->"hash" in (
                SELECT DISTINCT
                    case
                        when json->"sockets"->"socketEntries"->2->>"plugSources" in (2, 6, 0) then COALESCE(
                            json->"sockets"->"socketEntries"->2->"randomizedPlugSetHash",
                            json->"sockets"->"socketEntries"->2->"reusablePlugSetHash"
                        )
                        else NULL
                    end as magazine_set_id
                FROM
                    DestinyInventoryItemDefinition
                where
                    json->>"defaultDamageType" <> 0
            )
            or DestinyPlugSetDefinition.json->"hash" in (
                SELECT DISTINCT
                    case
                        when json->"sockets"->"socketEntries"->3->>"plugSources" in (2, 6, 0) then COALESCE(
                            json->"sockets"->"socketEntries"->3->"randomizedPlugSetHash",
                            json->"sockets"->"socketEntries"->3->"reusablePlugSetHash"
                        )
                        else NULL
                    end as first_column_set_id
                FROM
                    DestinyInventoryItemDefinition
                where
                    json->>"defaultDamageType" <> 0
            )
            or DestinyPlugSetDefinition.json->"hash" in (
                SELECT DISTINCT
                    case
                        when json->"sockets"->"socketEntries"->4->>"plugSources" in (2, 6, 0) then COALESCE(
                            json->"sockets"->"socketEntries"->4->"randomizedPlugSetHash",
                            json->"sockets"->"socketEntries"->4->"reusablePlugSetHash"
                        )
                        else NULL
                    end as second_column_set_id
                FROM
                    DestinyInventoryItemDefinition
                where
                    json->>"defaultDamageType" <> 0
            )
    );

-- weapon_sources
SELECT
    json->>"hash" AS id,
    json->>"itemHash" AS weapon_id,
    CASE
        WHEN json->>"sourceString" = '' THEN json->"displayProperties"->>"description"
        ELSE CASE
            WHEN json->>"sourceString" LIKE 'Source:%' THEN SUBSTRING(json->>"sourceString", 9)
            ELSE json->>"sourceString"
        END
    END AS name
FROM
    DestinyCollectibleDefinition
WHERE
    item_id IN (
        SELECT
            DestinyInventoryItemDefinition.json->>"hash"
        FROM
            DestinyInventoryItemDefinition
        WHERE
            DestinyInventoryItemDefinition.json->>"defaultDamageType" <> 0
    );

-- armor_sources
SELECT
    json->>"hash" AS id,
    json->>"itemHash" AS armor_id,
    CASE
        WHEN json->>"sourceString" = '' THEN json->"displayProperties"->>"description"
        ELSE CASE
            WHEN json->>"sourceString" LIKE 'Source:%' THEN SUBSTRING(json->>"sourceString", 9)
            ELSE json->>"sourceString"
        END
    END AS name
FROM
    DestinyCollectibleDefinition
WHERE
    armor_id IN (
        SELECT
            DestinyInventoryItemDefinition.json->>"hash"
        FROM
            DestinyInventoryItemDefinition
        where
            json->>"itemType" = 2
    )