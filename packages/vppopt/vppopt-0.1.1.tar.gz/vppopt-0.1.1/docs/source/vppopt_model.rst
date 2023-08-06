~~~~~~~~
VPPOPT model
~~~~~~~~

Mathematical model and its corresponding numerical objects of a simple energy system
-----------------------------------------------------

Electrolyser
^^^^^^^^^^^^

The electrolyser of energy system could be represented by a :oemof.solph:`Transformer` with one `input` (electricity flow) and one `ouput` (hydrogen flow). For each time step, theirs operations and constraints are described as follow:

:math:`P(i)^{H2}_{El} = \eta^{H2}_{El} \cdot P(i)^{elec}_{El}`

:math:`P(i)^{elec}_{El}\le K_{El}`

Where

- :math:`P(i)^{elec}_{EL}` and :math:`P(i)^{H2}_{EL}` are respectively the **electricity consumption** and the **H2 production** of the electrolysis unit, both expressed in kW
- :math:`\eta_{EL}` is the conversion ratio between electricity and H2 and :math:`K_{EL}` is the installed capacity of the electrolyser that sets
an upper value to the electricity input of the unit

.. note:: As the electrolysis occurs, water is consummed and O2 is produced. For the large fleets of electrolysis plants, the water consumption can become very large and water treatment considerations might arise since the electrolysis process requires deionised water. On the other hand, the O2 is a valuable molecule that can, as an example, be used in oxy-combustion systems.

Fuel cell combined heat-and-power
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The fuel cell CHP of energy system could be represented by a :oemof.solph:`Transformer` with one `input` (hydrogen flow) and two `ouputs` (electricity and heat flows). For each time step, theirs operations and constraints are described as follow:

:math:`P(i)^{elec}_{FC} = \eta^{elec}_{FC} \cdot P(i)^{H2}_{FC}`

:math:`P(i)^{heat}_{FC}= \eta^{heat}_{FC} \cdot P(i)^{H2}_{FC} = \lambda_{FC} \cdot P(i)^{elec}_{FC}`

:math:`P(i)^{elec}_{FC} \le K_{FC}`

Where:

- :math:`\eta_{FC}^{elec}` and :math:`\eta_{FC}^{heat}` are the electric and thermal efficiencies of the fuel cell system
- :math:`P(i)^{H2}_{FC}` is the hydrogen power required as input for the i\ :sup:`th` time step.
- The electric power entered as input is constrained by the maximum power capacity induced by the size of the fleet K\ :sub:`FC`.

.. note:: With :oemof-soph:`Transformer` class a constant efficiency will be used. The :oemof.solph:`OffsetTranformer` or
    :oemof.solph:`PiecewiseLinearTransformer` class (still experimental but should work) could be considered for variable
    efficiencies but will create a MIP problem instead of LP one.


Energy storage
^^^^^^^^^^^^^^

The energy storage technology could be modeled by :oemof.solph:`GenericStorage`

For each energy carrier, it is common to model the dynamics of its associated storage unit by updating the SOC at each tiem step by considering

- self discharge of the battery :math:`\delta_s^e`
- charging and discharging efficiencies

:math:`SOC(i)_s^e = (1-\delta^e_s) \cdot SOC(i-1)^e_s+\eta^e_c \cdot P(i)^e_c-\eta^e_d \cdot P(i)_d`

:math:`SOC(i)^e_s \le K^e_s`

:math:`P(i)_c^{elec} \le K_{bat}`

:math:`P(i)_d^{elec} \le K_{bat}`

:math:`k^{elec}_s = R_{bat} \cdot K_{bat}`

Where

- :math:`K_{bat}` is the installed power capacity of the battery
- :math:`R_{bat}` is the ratio evaluating the inter-dependencie of the energy and power components of a battery, e.g. R_bat = 4

:math:`SOC(i,last)^e_s = SOC(i,first)_s^e`

.. note:: When there more than one storage technologies, it is possible that a storage can
    be charged and discharged simultaneously even though it does not make sense. 
    An Additional constraint could be added (make problem become an MILP) to prevent
    to flows from being active at the same time. Alternatively, this could be avoided 
    using variable cost

Costs
-----

Investment costs
^^^^^^^^^^^^^^^^

The total CAPEX of the Multi-Energy System:

:math:`CAPEX_{tot} = \Sigma (capex_g \cdot K_g) + \Sigma(capex_s \cdot \kappa_s)`

Where:

- K\ :sub:`g` is the installed power capacity of the technology unit g
- :math:`\kappa_s` is the installed energy capacity of the storage unit s
- capex\ :sub:`g`, capex\ :sub:`s` are the specific investment cost of the technology g and storage s respectively

Operating costs
^^^^^^^^^^^^^^^

The operating costs could be divided in five constributions

:math:`OPEX_{tot} = \Sigma(opex_g) + \Sigma(opex_s) + C_{fuel} + C_{CO2} + C_{NS}^{elec}`

where

- opex\ :sub:`g` is the individual OPEX of each technology unit
- opex\ :sub:`s` is the individual OPEX of each storage unit
- C\ :sub:`fuel` is the fuel costs
- C\ :sub:`CO2` is the CO2 emissions costs
- :math:`C_{NS}^{elec}` is the electricity not served costs

The fixed operation and maintenance costs (FOM) and the variable operation 
maintenace costs (VOM) specific to each technology

:math:`opex_g = FOM_g \cdot K_g + VOM_g \cdot \Sigma P(i)_g^e`
:math:`opex_s = FOM_s \cdot \kappa_s + VOM_g \cdot \Sigma \left( P(i)_c^e + P(i)_d^e \right)`


Cost in oemof.solph
^^^^^^^^^^^^^^^^^^^

- The equivalent periodical costs (ep_costs) are related to the installed capacity represented by the investment variable. Therefore you can use it for all costs related to the installed capacity:

  - capital_costs
  - fixed_operational_costs
  - ...

- The variable cost: For (variable) operational costs (OPEX) you should use the `variable_costs` attribute because these costs are related to the flow variable (usage of the device).

Reference
---------

https://forum.openmod.org/t/is-it-possible-to-consider-opex-additionally-to-capex-which-is-necessary-for-the-optimization-with-the-investment-mode/878

https://forum.openmod.org/t/investment-variation-investment-during-year/2677

https://forum.openmod.org/t/result-export-in-excel/1308/2