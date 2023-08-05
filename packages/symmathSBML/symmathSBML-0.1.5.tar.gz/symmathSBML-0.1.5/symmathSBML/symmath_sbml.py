"""
Symbolic representation of an SBML model

Provides:
* symbolic state equations: system
   index: symbol
   value: expression for derivative
* symbolic jacobian of state equations
   index: symbol1
   column: symbol2
   value: expression d symbol1/d symbol2

Key methods:
* substatitue method provides for substituting symbols with roadrunner values
  (e.g., values of parameters in roadrunner or values of species in roadrunner)
  or user designated values.
* get provides the symbol and value information for a name (ID in libsbml)
* set changes the value information for a name (ID in libsbml)

Key properties:
* system is a Series of the system equations. The index is the variable,
  and the value is the expression.
* jacobian is a DataFrame for the Jacobian. Indexes are the variable whose
  expression is being differentiated and columns are the variables in the
  denominator of the differential
* roadrunner is the RoadRunner instance. Running simulations changes
  the values of variables that are substituted.
* namespace_dct is a dictionary with the namespace in which roadrunner
  variables are defined as symbols.
"""

"""
TO DO:
0. Update README with use case.
.1 Get Jin to change a file so she has commit history
1. Create package
"""

from symmathSBML.symmath_base import SymmathBase
from symmathSBML import msgs
from symmathSBML.persister import Persister

import collections
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sympy
import seaborn as sns
import tellurium as te


ANT = "ant"
XML = "xml"
TIME = "time"


TYPE_MODEL = "type_model"  # libsbml model
TYPE_XML = "type_xml"  # XML string
TYPE_ANTIMONY = "type_xml"  # Antimony string
TYPE_FILE = "type_file" # File reference

# filename: name of file processed
# number: index of item
# model: libsbml.Model
IteratorItem = collections.namedtuple('IteratorItem',
    'filename number model')
# nme: str name
# sym: sympy.Symbol
# rr: value in roadrunner
SymbolInfo = collections.namedtuple("SymbolInfo", "nme sym rr")


class SymmathSBML(SymmathBase):

    def __init__(self, model_reference, is_suppress_warnings=False):
        """
        Parameters
        ----------
        model_reference: str/roadrunner
            str: path to ant file, path to XML file, url to xml file, ant str
        is_suppress_warnings: bool
        """
        def mkAntimonyStr():
            try:
                self.roadrunner = te.loada(model_reference)
                xml_model_reference = self.roadrunner.getSBML()
                return xml_model_reference
            except:
                raise ValueError("Invalid model reference")
        ##### PUBLIC #####
        super(SymmathSBML, self).__init__(model_reference,
              is_suppress_warnings=is_suppress_warnings)
        # stoichiometry_mat - stoichiometry matrix including fixed species
        # kinetics - pd.Series of kinetics expressions
        # system - Series of the system expressions, indexed by species
        # jacobian - Dataframe of the jacobian expressions
        self.stoichiometry_mat, self.kinetics, self.system, self.jacobian =  \
              self.mkSymbolSystem()

    def copy(self):
        """
        Creates a copy of the object.
        
        Returns
        -------
        symmathSBML
        """
        new_symmath = SymmathSBML(self.antimony)
        new_symmath.model_reference = self.model_reference
        # Adjust the simulation time
        new_symmath.roadrunner.reset()
        _ = new_symmath.roadrunner.simulate(0, self.roadrunner.model.getTime())
        # Save the content of the roadrunner instance
        dct = self._getRoadrunnerDct()
        new_symmath.set(dct)
        #
        return new_symmath

    def serialize(self, path):
        """
        Serializes the current object to a file.

        Parameters
        ----------
        path: str
            Path to serialization file
        """
        persister = Persister(path)
        time = self.roadrunner.model.getTime()
        roadrunner_dct = self._getRoadrunnerDct()
        items = [self.antimony, roadrunner_dct, time]
        persister.set(items)

    @classmethod
    def deserialize(cls, path):
        """
        Creates a SymmathSBML object from a file serialization.

        Parameters
        ----------
        path: str
            Path to serialization file
        
        Returns
        -------
        SymmathSBML
        """
        persister = Persister(path)
        [antimony, roadrunner_dct, time] = persister.get()
        symmath = cls(antimony)
        symmath.roadrunner.reset()
        _ = symmath.roadrunner.simulate(0, time)
        symmath.set(roadrunner_dct)
        return symmath

    def equals(self, other):
        """
        Checks that they have the same information

        Parameters
        ----------
        other: SymmathSBML
        
        Returns
        -------
        bool
        """
        val_bool = self.antimony == other.antimony
        val_bool = val_bool and all([s1.id == s2.id for s1, s2 in
              zip(self.species, other.species)])
        val_bool = val_bool and all([s1 == s2 for s1, s2 in
              zip(self.species_names, other.species_names)])
        val_bool = val_bool and all([p1.id == p2.id for p1, p2 in
              zip(self.parameters, other.parameters)])
        val_bool = val_bool and all([p1 == p2 for p1, p2 in
              zip(self.parameter_names, other.parameter_names)])
        val_bool = val_bool and all([r1.id == r2.id for r1, r2 in
              zip(self.reactions, other.reactions)])
        val_bool = val_bool and self.system.equals(other.system)
        val_bool = val_bool and self.jacobian.equals(other.jacobian)
        # Compare roadrunner values
        val_bool = val_bool and np.isclose(
               self.roadrunner.model.getTime(), other.roadrunner.model.getTime())
        dct = self.getParameterNameDct()
        dct.update(self.getSpeciesNameDct())
        for name, value in dct.items():
            val_bool = val_bool and np.isclose(other.roadrunner[name], value)
        return val_bool

    @staticmethod
    def _convert(value, dct):
        """
        Converts a value or symbol or expression with substitution.
   
        Parameters
        ----------
        dct: dict
            key: Symbol
            value: object
        
        Returns
        -------
        expression or number
        """
        if "is_Symbol" in dir(value):
            new_value = value.subs(dct).simplify()
            if len(new_value.free_symbols) == 0:
                new_value = float(new_value)
        else:
            new_value = float(value)
        return new_value

    def _getSubstitutionDct(self, is_sub_parameters=True,
          is_sub_species=False, is_sub_others=True):
        """
        Constructs a substitution dictionary.
   
        Parameters
        ----------
        
        Returns
        -------
        dict
        """
        dct = {}
        if is_sub_parameters:
            dct.update(self.getParameterSymbolDct())
        if is_sub_species:
            dct.update(self.getSpeciesSymbolDct())
        if is_sub_others:
            dct.update(self.getOtherSymbolDct())
        return dct
     
    def getJacobian(self, is_sub_parameters=True,
          is_sub_species=False, is_sub_others=True):
        """
        Substitutes into the Jacobian as directed.
   
        Parameters
        ----------
        is_sub_parameters: bool
            substitute all parameters
        is_sub_species: bool
            substitute all species
        is_sub_others: bool
            substitute the non-species, non-parameters
        """
        dct = self._getSubstitutionDct(
              is_sub_parameters=is_sub_parameters,
              is_sub_species=is_sub_species,
              is_sub_others=is_sub_others)
        jacobian = self.jacobian.applymap(
              lambda v: sympy.simplify(self._convert(v, dct)))
        return jacobian
     
    def getSystem(self, is_sub_parameters=True,
          is_sub_species=False, is_sub_others=True):
        """
        Substitutes into the System equations.
   
        Parameters
        ----------
        is_sub_parameters: bool
            substitute all parameters
        is_sub_species: bool
            substitute all species
        is_sub_others: bool
            substitute the non-species, non-parameters
        """
        dct = self._getSubstitutionDct(
              is_sub_parameters=is_sub_parameters,
              is_sub_species=is_sub_species,
              is_sub_others=is_sub_others)
        return self.system.apply(lambda v: self._convert(v, dct))
     
    def getKinetics(self, is_sub_parameters=True,
          is_sub_species=False, is_sub_others=True):
        """
        Substitutes into the System kinetics expressions
        for each reaction.
   
        Parameters
        ----------
        is_sub_parameters: bool
            substitute all parameters
        is_sub_species: bool
            substitute all species
        is_sub_others: bool
            substitute the non-species, non-parameters
        """
        dct = self._getSubstitutionDct(
              is_sub_parameters=is_sub_parameters,
              is_sub_species=is_sub_species,
              is_sub_others=is_sub_others)
        return self.kinetics.apply(lambda v: self._convert(v, dct))

    def mkSymbolSystem(self):
        """
        Creates an ODEModel.
    
        Returns
        -------
        np.array, pd.Series, pd.Series, pd.DataFrame
            stoichiometry_mat, kinetics, system, jacobian
        """
        def evaluate(reaction):
            return eval(reaction.kinetic_law.expanded_formula, namespace_dct)
        # Create sympy expressions for kinetic laws
        reaction_epr_dct = {}
        # Add sympy symbols
        self.namespace_dct["log"] = sympy.log
        self.namespace_dct["sqrt"] = sympy.sqrt
        # Process reactions
        namespace_dct = dict(self.namespace_dct)  # Don't modify namespace
        for reaction in self.reactions:
            key = namespace_dct[reaction.id]
            for _ in range(10):  # Number of attempts to resolve names
                is_done = False
                value = None
                try:
                    value = evaluate(reaction)
                    is_done = True
                except NameError as err:
                    parts = str(err).split(" ")
                    name = parts[1].replace("'", "")
                    namespace_dct[name] = sympy.Symbol(name)
                    # Keept this in the namespace
                    self.namespace_dct[name] = namespace_dct[name]
                    msg = "Name %s undefined in reaction %s. Set to 0."  \
                          % (name, str(reaction))
                    msgs.warn(msg,
                          is_suppress_warnings=self.is_suppress_warnings)
                if is_done:
                    break
            reaction_epr_dct[key] = value
        # Express species fluxes in terms of reaction fluxes
        reaction_vec = sympy.Matrix(list(reaction_epr_dct.keys()))
        # Ensure we get all boundary species in the stoichiometrymatrix
        # FIXME: Does this include assignment rules?
        boundary_species = self.roadrunner.getBoundarySpeciesIds()
        for name in boundary_species:
            self.roadrunner.setBoundary(name, False)
        try:
            stoichiometry_mat = self.roadrunner.getFullStoichiometryMatrix()
        except Exception:
            msgs.warn("Stoichiometery matrix does not exist.",
                  is_suppress_warnings=self.is_suppress_warnings)
            stoichiometry_mat = None
        # Only rate rules
        if stoichiometry_mat is None:
            reaction_epr_dct = {}
            system_dct = {}
            self._updateSystemDctWithRules(system_dct)
        # Has reactions
        else:    
            species_reaction_vec = stoichiometry_mat * reaction_vec
            species_in_reactions = self.getSpeciesInReactions()
            rownames = list(stoichiometry_mat.rownames)
            species_in_reactions = sorted(species_in_reactions,
                  key=lambda n: rownames.index(n))
            species_reaction_dct = {self.namespace_dct[s]: 
                  e for s, e in zip(species_in_reactions, species_reaction_vec)}
            # Construct the system equations
            system_dct = {s: sympy.simplify(
                  species_reaction_dct[s].subs(reaction_epr_dct))
                for s in species_reaction_dct.keys()}
            # Handle rules
            self._updateSystemDctWithRules(system_dct)
        system = pd.Series(system_dct.values(), index=system_dct.keys())
        # Construct the Jacobian
        variables = list(system.index)
        jac_dct = {v: [] for v in variables}
        for var1 in variables:
            epr = system.loc[var1]
            for var2 in variables:
                jac_dct[var2].append(sympy.diff(epr, var2))
        jacobian = pd.DataFrame(jac_dct, index=variables)
        #
        kinetics = pd.Series(reaction_epr_dct, dtype=object)
        return stoichiometry_mat, kinetics, system, jacobian

    def _updateSystemDctWithRules(self, system_dct):
        """
        Updates the system dictionary (and self.namespace_dct) as a result
        of assignment rules and rate rules.

        Parameters
        ----------
        system_dct: dict
            key: symbol
            value: expression
        """
        for num in range(self.model.getNumRules()):
            rule = self.model.getRule(num)
            formula_str = rule.getFormula()
            try:
                expression = eval(formula_str, self.namespace_dct)
            except Exception as excp:
                import pdb; pdb.set_trace()
            variable = rule.getVariable()
            self.species_names.append(variable)
            if not variable in self.namespace_dct.keys():
                self.namespace_dct[variable] = sympy.Symbol(variable)
            symbol = self.namespace_dct[variable]
            if "Rate" in str(type(rule)):
                system_dct[symbol] = expression
            elif "Assignment" in str(type(rule)):
                self.namespace_dct[variable] = expression
            else:
                raise RuntimeError("Unknown rule type")

    def setTime(self, time):
        """
        Sets the time for the simulation by running the simulation to that time.

        Parameters
        ----------
        time: float
        """
        self.roadrunner.reset()
        self.roadrunner.simulate(0, time)

    def calculateJacobianSensitivity(self, is_normalized=True):
        """
        Calculates the sensitivity of the species (state) variable w.r.t. all
        other species by summing derivatives and evaluating at the current
        value of the state vector.

        Parameters
        ----------
        is_normalized: bool
            divide by the value
        
        Returns
        -------
        DataFrame
            columns: species column in Jacobian
            index: species used in derivative denominator
            values: sympy expression
        """
        # Initializations
        symbols = list(self.jacobian.index)
        dct = {s: [] for s in symbols}
        # Construct substitution dictionary
        subs_dct = self.getParameterSymbolDct()
        subs_dct.update(self.getSpeciesSymbolDct())
        # Take derivatives
        for s1 in symbols: # Row
            s1_arr = np.array(self.jacobian[s1])
            row_epr = s1_arr.dot(self.getSpeciesArray())
            row_value = row_epr.subs(subs_dct)
            if row_value == 0:
                row_value = 10e5
            for s2 in symbols:  # Columns
                deriv = sympy.diff(row_epr, s2).subs(subs_dct)
                if is_normalized:
                    deriv = deriv/row_value
                if deriv.is_number:
                    deriv = float(deriv)
                dct[s1].append(deriv)
        # Return the result
        df = pd.DataFrame(dct, index=symbols, columns=symbols)
        return df
            
    def getSpeciesArray(self):
        return np.array([self.get(s).rr for s in self.species_names])

    def plotJacobianSensitivityHeatmap(self, title="", is_plot=True,
          vmin=None, vmax=None):
        """
        Plots a heatmap of the derivative of each row in the Jacobain
        multiplied by the current value of the state vector.

        Parameters
        ----------
        title: str
        """
        df = self.calculateJacobianSensitivity()
        max_val = max([np.abs(v) for v in df.values.flatten()])
        if vmin is None:
            vmin = -max_val
        if vmax is None:
            vmax = max_val
        columns = list(df.columns)
        columns.reverse()
        df_new = df.iloc[::-1]
        sns.heatmap(df_new, cmap="seismic", vmin=vmin, vmax=vmax)
        plt.xlabel("State Evaluated")
        plt.ylabel("Derivative w.r.t. State")
        plt.title(title)
        if is_plot:
            plt.show()

    def addNamespace(self, dct):
        """
        Adds the symbol namespace to the dictionary.

        Parameters
        ----------
        dct: dict       
        """
        dct.update(self.namespace_dct)

    def removeNamespace(self, dct):
        """
        Removes the symbol namespace to the dictionary.

        Parameters
        ----------
        dct: dict       
        """
        for key in self.namespace_dct:
            if key in dct.keys():
                del dct[key]

    def getSpeciesInReactions(self):
        """
        Get names of all species that appear as reactants or products.
        
        Returns
        -------
        list-str
        """
        names = []
        for reaction in self.reactions:
            names.extend([str(s.getSpecies()) for s in reaction.reactants])
            names.extend([str(s.getSpecies()) for s in reaction.products])
        names = list(set(names))
        names.sort()
        return names
