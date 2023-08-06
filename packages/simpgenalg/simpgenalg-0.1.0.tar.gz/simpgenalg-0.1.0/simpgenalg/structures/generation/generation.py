from .gen_rslts import allResults, runResults, genResults
from .op_app import operatorApplicator
from ..basics import basicStructure
from ...selectors.basics import basicSelector

class generationStructure(basicStructure):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.log.debug('Initializing generationStructure')


    # Runs this generation structure
    def run(self, **kargs):

        # Creating an object to contain all results gathered from all runs
        all_results = allResults(log=self.log,\
                                config=self.config,\
                                toolbox=self.toolbox)

        # Basic parameters
        n_runs = kargs.get('n_runs',kargs.get('n', 1))
        n_gens = self.config.get('n_gens',200,dtype=int,mineq=1)
        cmpr_map_dist = self.config.get('cmpr_map_dist', False, dtype=bool)
        tracking_vars = self.config.get('tracking_vars',('fit_mean','fit_stdev'))


        self.log.info(f'Starting generationStructure for {n_runs} runs')

        # Get selectors / evaluators / populations
        selector, evaluator, parents, children = self._setup_components()

        # Genetic Operators
        operator_applicator = operatorApplicator(log=self.log,\
                                                 toolbox=self.toolbox,\
                                                 config=self.config)

        # Clears those objects
        def clear():
            self.log.debug('Clearing the selector, evaluator, and populations')
            selector.clear(), evaluator.clear(), parents.clear(), children.clear()
            return

        # Iterate through number of runs
        for run in range(n_runs):
            self.log.info(f'Starting run #{run}/{n_runs}')

            # Creates object to store resutls for the current run
            run_results = runResults(log=self.log,\
                                     config=self.config,\
                                     toolbox=self.toolbox)

            # Iterate through generations
            for gen in range(n_gens+1):

                # Evaluate the parents
                evaluator.evaluate_batch(parents)

                # Check for similarity (if enabled)
                if cmpr_map_dist:
                    parents.compare_mapped_distance()

                # Select parents to reproduce
                selected = selector.select(parents)

                # Store current results
                run_results.append(pop_stats=parents.get_popstats(),\
                                   indv_attrs=parents.get_indv_attrs())
                self.log.info(run_results[-1].get_gen_strs(*tracking_vars,round=2))

                # Crete next generation (if not last generation)
                if gen != n_gens:
                    # Create new batch using selected parents and children
                    operator_applicator.apply_operators(selected,children)

                    # Swap the children and parents
                    parents, children = children, parents

            # Clear objects for restart
            clear()
        return


    def _setup_components(self):
        # Convert
        def convert(val, *args, **kargs):
            if isinstance(val, str):
                return self.toolbox[val](log=self.log,\
                                         config=self.config,\
                                         toolbox=self.toolbox)
            elif isinstance(val, (basicSelector)):
                return val(*args, log=self.log,\
                           config=self.config,\
                           toolbox=self.toolbox,\
                           **kargs)
            else:
                self.log.exception('Passed a bad value',err=ValueError)

        selector = convert(self.config.get('selector','tournament',\
                                    dtype=(basicSelector,str)))
        evaluator = convert(self.config.get('evaluator','custom',\
                                    dtype=(str)))
        parents = convert(self.config.get('population','fixed',\
                                    dtype=(str)))
        children = convert(self.config.get('population','fixed',\
                                    dtype=(str)), generate=False)

        return selector, evaluator, parents, children
