================
Excel Input File
================

Initializing (empty) Excel Input Template
-----------------------------------------

An Excel file (being served as a template) containing different (empty) 
sheets, e.g. INFO, buses, commodity_sources, demand, etc., will be created 
by the following sub-command

.. code-block:: bash

    vppopt init -pdir <project directory path>

by default an Excel file name ``vppopt.xls`` will be created in 
``<project directory path>``. Other Excel file names could be initialized 
using argument ``--scenario`` or ``-s`` as follow:

.. code-block:: bash

    vppopt init -pdir <project directory path> -s <scenario name>

Completing Excel Input File
---------------------------

buses
^^^^^

This Excel sheet containing metadata for creating buses of energy system

.. code-block:: python

    """
    label (required): str, 
        unique label of buses, e.g. ``bel``, ``bheat``
    active (required): boolean, 
        blank or 0 --> False, this value decide if the bus will be active (i.e. being created) or not
    excess (optional): boolean,
        blank or 0 --> False, otherwise --> True
        This value decide if excess energy is allowable or not and will have impact on sizing energy system component
        True --> allowable, False --> not allowable
        If the excess energy will be allowable, an oemof Sink object will be created for quantifying it.
    shortage (optional): boolean,
        blank or 0 --> False, otherwise --> True
        This value dicide if the power shortage is allowable or not and will have impact on sizing energy system component
        True --> allowable, False --> not allowable
        If True, an oemof Source object will be created for quantifying the shortage flow
    excess costs (optional): float,
        variable_costs of not-used excess energy (positive value) or income (negative value) from reinjection to grid 
        will be multiplied with excess flow for calculating the total cost/incomme from excess energy
    shortage costs (optional): float, 
        variable_costs (positive value) of power shortage will be multiplied with power shortage flow for calculating its 
        total cost 
    """

.. image:: _files/buses_sheet.jpg
    :align: center

From the image above
- Three buses labled ``bel``, ``bh2`` and ``bheat`` will be created
- The excess electricity is allowable with a variable_costs of 0.0002 (e.g. €/kWh)

commodity_sources
^^^^^^^^^^^^^^^^^

This Excel sheet containing metadata for creating commodity sources of energy system, e.g. grid electricity, natural gas, etc.

.. code-block:: python

    """
    label (required): str, 
        unique label of commodity sources, e.g. ``grid_elec``
    active (required): boolean,
        blank or 0 --> False, this value decide if the bus will be active (i.e. being created) or not
    to (required): str,
        bus name (must be found from buses sheet) that is connected from a commodity source
    variable costs: float,
        variable_costs that will be multiplied with commodity source flow for the total cost
    """

.. image:: _files/commodity_sources_sheet.jpg
    :align: center

demand
^^^^^^

.. code-block:: python

    """
    label (required): str, 
        unique label of demand sink, e.g. ``container_workspace``
    active (required): boolean,
        blank or 0 --> False, this value decide if the bus will be active (i.e. being created) or not
    from (required): str,
        bus name (must be found from buses sheet) that is connected to a demand sink
    nominal value: float,
        nominal_value that will be multiplied with commodity source flow for the total cost
    """

.. image:: _files/demand_sheet.jpg
    :align: center

renewables
^^^^^^^^^^

.. image:: _files/renewables_sheet.jpg
    :align: center

storages
^^^^^^^^

.. image:: _files/storages_sheet.jpg
    :align: center

transformers
^^^^^^^^^^^^

.. image:: _files/transformer_sheet.jpg
    :align: center

transformers_chp
^^^^^^^^^^^^^^^^

.. image:: _files/transformer_chp_sheet.jpg
    :align: center

time_series
^^^^^^^^^^^

.. image:: _files/ts_sheet.jpg
    :align: center