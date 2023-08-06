from .basics import basicSelector
from statistics import stdev, mean
import random

class tournamentSelector(basicSelector):

    __slots__ = ('win_rate', 'tourn_size', 'maximize', 'track_nsel', \
                 'track_sel_stats', 'nsel')

    def __init__(self, *args, **kargs):
        # Initialize basicSelector
        super().__init__(*args, **kargs)

        # Log it
        self.log.info('Initializing tournamentSelector')

        # Extract values from the config
        self.win_rate = self.config.get('win_rate', 1.0, dtype=float, maxeq=1.0, min=0)
        self.tourn_size = self.config.get('tourn_size', 10, dtype=int, mineq=2)
        self.maximize = self.config.get('maximize', True, dtype=bool)
        self.track_nsel = self.config.get('track_nsel', True, dtype=bool)
        self.track_sel_stats = self.config.get('track_sel_stats', True, \
                                                dtype=bool)
        self.nsel = self.config.get('nsel',self.config.get('pop_size',100), \
                                        dtype=int, mineq=2)


    def select(self, population, **kargs):
        # Add to log
        self.log.debug('Selecting parents')

        # Either use provided parameters or grab one from self
        win_rate = kargs.get('win_rate', self.win_rate)
        tourn_size = kargs.get('tourn_size', self.tourn_size)
        maximize = kargs.get('maximize', self.maximize)
        track_nsel = kargs.get('track_nsel', self.track_nsel)
        track_sel_stats = kargs.get('track_sel_stats', self.track_sel_stats)
        n_sel = kargs.get('nsel', self.nsel)

        # List of winners of the tournaments
        winners = []

        # If 100% win chance, we are just looking for the max/min of random
        #   sampling
        if win_rate == 1:
            if maximize:
                while len(winners) < n_sel:
                    winners.append(max(random.choices(population, k=tourn_size)))
            else:
                while len(winners) < n_sel:
                    winners.append(min(random.choices(population, k=tourn_size)))
        else: # Otherwise, we need to run through and apply the win chances
            while len(winners) < n_sel:
                # Randomly sample and then sort the individuals
                tournament = sorted(random.choices(population, k=tourn_size),\
                                reverse = maximize)
                # Per individiaul in the tournament, see if they win
                for indv in tournament:
                    if random.random() < win_rate:
                        winners.append(indv.copy(keep_ID=True))

        # If tracking number of times selected, iterate through and apply it
        #   to each individual selected
        if track_nsel:
            self.log.debug('Adding n_sel to individuals')
            for indv in winners:
                indv.incr_attr('n_sel')

        # If tracking sel stats, we will find the mean, stdev, min, and max of
        #   the selected parents' fitnesses
        if track_sel_stats:
            self.log.debug('Adding sel_stats to pop')
            selected_fits = [indv.get_fit() for indv in winners]
            population.set_popstat('sel_mean',mean(selected_fits))
            population.set_popstat('sel_stdev',stdev(selected_fits))
            population.set_popstat('sel_min',min(selected_fits))
            population.set_popstat('sel_max',max(selected_fits))

        # Return list of the winners
        return winners
