# Copyright 2017 LasLabs Inc.
# Copyright 2021 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook_login_check(cr):
    """This hook will look to see if any conflicting logins exist before
    the module is installed
    :param openerp.sql_db.Cursor cr:
        Database cursor.
    """
    with cr.savepoint():
        query = """
            SELECT
                BTRIM(LOWER(login))
            FROM
                res_users
            GROUP BY
                BTRIM(LOWER(login))
            HAVING COUNT(BTRIM(LOWER(login))) > 1
        """
        cr.execute(query)
        duplicated = [user[0] for user in cr.fetchall()]
        if duplicated:
            _logger.warning(
                "Conflicting user logins exist for `%s`",
                ", ".join(dup for dup in duplicated),
            )


def post_init_hook_login_convert(cr, registry):
    """After the module is installed, set all logins to lowercase
    :param openerp.sql_db.Cursor cr:
        Database cursor.
    :param openerp.modules.registry.RegistryManager registry:
        Database registry, using v7 api.
    """
    with cr.savepoint():
        # Deactivate duplicated users which have older login_date and add them
        # _duplicate substring on their login
        query_avoid_duplicated = """
            WITH duplicated_logins AS (
                SELECT
                    BTRIM(LOWER(login)) AS login
                FROM
                    res_users
                GROUP BY
                    BTRIM(LOWER(login))
                HAVING COUNT(BTRIM(LOWER(login))) > 1
            ),
            duplicated_users AS (
                SELECT
                    id,
                    dl.login
                FROM
                    res_users AS ru
                INNER JOIN
                    duplicated_logins AS dl
                    ON BTRIM(LOWER(ru.login)) = dl.login
            ),
            login_dates AS (
                SELECT
                    create_uid,
                    MAX(create_date) AS login_date
                FROM
                    res_users_log
                GROUP BY
                    create_uid
            ),
            users_with_date AS (
                SELECT
                    du.id,
                    BTRIM(LOWER(du.login)) AS login,
                    COALESCE(ld.login_date, '2000-01-01 00:00:00') AS login_date
                FROM
                    duplicated_users AS du
                LEFT OUTER JOIN
                    login_dates AS ld
                    ON du.id = ld.create_uid
            ),
            login_min_dates AS (
                SELECT
                    login,
                    MIN(login_date) AS min_login_date
                FROM
                    users_with_date
                WHERE
                    login IN (SELECT login FROM duplicated_logins)
                GROUP BY
                    login
            ),
            deactivate_users AS (
                SELECT
                    MAX(uwd.id) AS id,
                    uwd.login
                FROM
                    users_with_date uwd
                INNER JOIN
                    login_min_dates lmd
                    ON uwd.login = lmd.login
                WHERE
                    uwd.login_date = lmd.min_login_date
                GROUP BY
                    uwd.login
            )
            UPDATE
                res_users
            SET
                active=false,
                login=concat(deactivate_users.login, '_duplicate')
            FROM
                deactivate_users
            WHERE
                res_users.id = deactivate_users.id
            ;
            """
        _logger.info("Deactivating duplicated users")
        cr.execute(query_avoid_duplicated)
        _logger.info("Lowering login of all users")
        cr.execute("UPDATE res_users SET login=BTRIM(LOWER(login))")
