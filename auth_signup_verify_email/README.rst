.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Verify email at signup
======================

This module extends the functionality of public sign up to force users to
provide a valid email address.

To achieve this, users are not required to provide a password at
sign up: they are asked for only at first login attempt.

Installation
============

* Install `validate_email <https://pypi.python.org/pypi/validate_email>`_ with ``pip install validate_email`` or equivalent.

Configuration
=============

To configure this module, you need to:

* `Properly configure your outgoing email server(s)
  <https://www.odoo.com/es_ES/forum/help-1/question/how-to-configure-email-gateway-282#answer_290>`_.
* Go to *Settings > General Settings -> General settings*, search for the *Users* section and enable *Free sign up* in *Customer account*.

Usage
=====

To use this module, you need to:

* Log out.
* `Sign up </web/signup>`_ with a valid email.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/149/11.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/server-tools/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Icon
----

* https://openclipart.org/detail/3040/thumbtack-note-email
* https://openclipart.org/detail/202732/check-mark

Contributors
------------

* Rafael Blasco <rafaelbn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>
* Simone Orsi <simone.orsi@camptocamp.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
