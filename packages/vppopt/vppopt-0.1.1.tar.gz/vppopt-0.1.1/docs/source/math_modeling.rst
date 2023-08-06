================================
Mathematical modeling with pyomo
================================

More info about using pyomo could be found `here <https://pyomo.readthedocs.io/en/stable/pyomo_overview/overview_components.html>`_

Overview of Modeling Components and Processes
---------------------------------------------

Pyomo (Python Optimization Modeling Objects) supports an object-oriented design for the definition of optimization models. The basic steps of a simple modeling process are:

- Create model and declare components
- Instantiate the model
- Apply solver
- Interrogate solver results

A Pyomo model consists of a collection of modeling components that define different aspects of the model. Pyomo includes the **modeling components** that are commonly supported by mordern AMLs:

- index set
- symbolic parameters
- decision variables
- objectives
- and constraints

These modeling components are defined in Pyomo through the following Python classes:

Set
^^^

Set data that is used to define a model instance

Parameter
^^^^^^^^

Parameter data that is used to define a model instance

Variable
^^^^^^^^

Decision variables in a model

Objective
^^^^^^^^^

Expression that are minimized or maximized in a model

Constraint
^^^^^^^^^^

Constraint expressions that impose restriction on variable values in a model

Simple models
-------------

A simple concrete Pyomo model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

min :math:`2x_1 + 3x_2`

s.t.
    :math:`3x_1 + 4x_2 \le 1`

    :math:`x_1,\ x_2 \ge 0`


This can be implemented as a concrete model as follows:

.. code-block:: python
    
    import pyomo.environ as pyo
    # model declaration
    model = pyo.ConcreteModel()
    # variable declaration
    model.x = pyo.Var([1,2],domain=pyo.NonNegativeReals)
    # model objective expression
    model.OBJ = pyo.Objective(expr = 2*model.x[1]+3*model.x[2])
    # model constraint
    model.Constraint1 = pyo.Constraint(expr = 3*model.x[1]+4*model.x[2]>=1)
    

A simple abstract Pyomo model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

min :math:`\Sigma_j^n(c_j \cdot x_j)`

s.t.

    :math:`\Sigma_j^n(a_{ij}x_j \ge b_i)\ \ \ i= 1...m`

    :math:`x_j \ge 0\ \ \ j = 1...n`

.. code-block:: python
    
    import pyomo.environ as pyo
    model = pyo.AbstractModel()
    
    model.m = pyo.Param(within=pyo.NonNegativeIntegers)
    model.n = pyo.Param(within=pyo.NonNegativeIntegers)
    
    model.I = pyo.RangeSet(1,model.m)
    model.J = pyo.RangeSet(1,model.n)

    model.a = pyo.Param(model.I,model.J)
    model.b = pyo.Param(model.I)
    model.c = pyo.Param(model.J)

    # declaration of decision variables
    model.x = pyo.Var(model.J, domain = pyo.NonNegativeReals)
    
    def obj_expression(m):
        return pyo.summation(m.c,m.x)
    
    model.OBJ = pyo.Objective(rule=obj_expression)

    def ax_constraint_rule(m,i):
        # return the expression for the constraint for i
        return sum(m.a[i,j]*m.x[j] for j in m.J)>=m.b[i]
    
    model.AbxConstraint = pyo.Constraint(model.I,rule=ax_constraint_rule)


In order to use this model, data must be given for the values of the parameters.

Notions
-------

`Shadow price & reduced cost (of a linear programming model) <https://www.or-as.be/blog/tsbd_sp>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A shadow price value is associated with each constraint of the model. It is the instantaneous change in the objective value of the optimal soltion obtained by changing the right hand side constraint by one unit
- A reduced cost value is associated with each variable of the model. it is the amount by which an objective function parameter would have to improve before it would be possible for a corresponding variable to assume a positive value in the optimal solution
- It should be intuitively clear that the reduced cost is equal to the shadow price of the non-negativity constraint of the variable


Model 1.

minimise    :math:`cost\ (C) = 10 x_1 + 7 x_2.`

s.t.
    :math:`x_1 + x_2 \ge 10`
    
    :math:`x_1 \ge 0`

    :math:`x_2 \ge 0`

The optimal solution is equal to :math:`x_1 = 0` and :math:`x_2 = 10` with an objective of 70. 
Indeed, x\ :sub:`1` is too expensive compared to x\ :sub:`2`, and therefore x\ :sub:`1` = 0. Therefore, 
the cost should be reduced from 10 to 7 (or lower, so by minimum a value of 3) to make the 
production of x1 attractive, hence, the value of 3 for the reduced cost.

Now let’s go back to the statement: “The reduced cost of a decision variable 
(i.e. value 3 for variable x1) is equal to the shadow price of the non-negativity 
constraint of the variable (i.e. x1 >= 0)”

The shadow price for the constraint :math:`x_1 \ge 0` can be defined as follows: 
If you increase the right hand side of that constraint (currently 0) by one unit 
(i.e. the constraint changes to :math:`x_1 \ge 1`), what is the impact on the objective. 
Hence, the model changes into (notice the small difference):

Model 2.

minimise :math:`cost\ (C) = 10 x_1 + 7 x_2.`

s.t.

    :math:`x_1 + x_2 \ge 10`
    
    :math:`x_1 \ge 1`

    :math:`x_2 \ge 0`

The optimal solution is now equal to x\ :sub:`1` = 1 and x\ :sub:`2` = 9 with an objective of 73. 
This is exactly 3 more than the previous solution, and hence, the shadow price 
of the constraint :math:`x1 \ge 0` in model 1 is equal to 3. This value 3 is equal to 
the reduced cost of x\ :sub:`1` in model 1, which illustrates third statement.

Equivalent Periodical Cost
^^^^^^^^^^^^^^^^^^^^^^^^^^

epc (equivalent periodical cost) for the period of one year --> equivalent annual cost. 
According wikipedia, in finance the epc is the cost per year of owning and operating an 
asset over its entire lifespan. It is calculated by dividing the NPV of a project by the 
present value of annuity factor

Weighted Average Cost of Capital
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

wacc (Weighted Average Cost of Capital) is a calculation of a firm's cost of capital in 
which each category of capital is proportionaly weighted. All sources of capital, including 
common stock, preferred stock, bonds, and any other long-term debt, are included in a WACC calculation

:math:`WACC = ({E \over V}\cdot Re)+\left[{D \over V}\cdot R_d \cdot (1-T_c)\right]`

where

- E: Market value of the firm's equity
- D: Market value of the firm's debt
- V: E+D
- Re: Cost of equity
- Rd: Cost of debt
- Tc: Corporate tax rate

Variable Cost
^^^^^^^^^^^^^

A variable cost is a corporate expense that changes in proportion to how much a company produces or sells.

Miscellaneous
-------------

- `Pyomo and JuMP – Modeling environments for the 21st century <http://egon.cheme.cmu.edu/ewo/docs/EWO_Seminar_03_10_2017.pdf>`_
- Practical guidelines for solving difficult mixed integer linear programs