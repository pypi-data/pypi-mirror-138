#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------
         _   _   _ _____ ___ _____ ____      _    ____  _____ ____  
        / \ | | | |_   _/ _ \_   _|  _ \    / \  |  _ \| ____|  _ \ 
       / _ \| | | | | || | | || | | |_) |  / _ \ | | | |  _| | |_) |
      / ___ \ |_| | | || |_| || | |  _ <  / ___ \| |_| | |___|  _ < 
     /_/   \_\___/  |_| \___/ |_| |_| \_\/_/   \_\____/|_____|_| \_\
    
---------------------------------------------------------------------------
     A Python-Based Development Platform For Automated Trading Systems
"""

from datetime import datetime, timedelta
import sys
import os
import pyfiglet
import importlib
import numpy as np
import pandas as pd
import timeit
from scipy.optimize import brute
from ast import literal_eval
from autotrader.brokers.oanda import Oanda
# from autotrader.brokers.interactive_brokers import ib_broker
from autotrader.brokers.virtual.virtual_broker import Broker
from autotrader.lib import instrument_list, environment_manager, printout
from autotrader.lib.read_yaml import read_yaml
from autotrader import autoplot
from autotrader.autobot import AutoTraderBot
from autotrader.lib.bot_manager import ManageBot
import time

class AutoTrader():
    """
    AutoTrader: A Python-Based Development Platform For Automated Trading Systems.
    ------------------------------------------------------------------------------
    Website: https://kieran-mackle.github.io/AutoTrader/
    
    GitHub: https://github.com/kieran-mackle/AutoTrader
    
    Author: Kieran Mackle
    
    Version: 0.5.x

    Attributes
    ----------
    Note: many of the following attributes are set from the configure method of AutoTrader.
    
    feed : str 
        The data feed to be used (eg. Yahoo, Oanda).
                
    verbosity : int
        The verbosity of AutoTrader (0, 1 or 2).
    
    notify : int
        The level of email notification (0, 1 or 2).
    
    home_dir : str 
        The project home directory.
    
    use_stream : bool 
        Set to True to use price stream as data feed.
    
    detach_bot : bool 
        Set to True to spawn new thread for each bot deployed. Bots will then
        continue to trade until a termination signal is recieved from the strategy.
    
    check_data_alignment : bool
        Verify time of latest candle in data recieved against current time.
    
    allow_dancing_bears : bool
        Allow incomplete candles to be passed to strategy.
    
    account_id : str
        The brokerage account ID to use in this instance.
    
    environment : str
        The trading environment of this instance.
    
    show_plot : bool
        Automatically display plot of results.
    
    MTF_initialisation : bool
        Only download mutliple time frame data when initialising the strategy, 
        rather than every update.


    Methods
    -------
    run():
        Runs AutoTrader.
    
    configure(feed='yahoo', verbosity=1, notify=0, home_dir=None,
              use_stream=False, detach_bot=False,
              check_data_alignment=True, allow_dancing_bears=False,
              account_id=None, environment='demo', show_plot=False,
              MTF_initialisation=False):
        Configures various run settings for AutoTrader.
    
    add_strategy(strategy_filename=None, strategy_dict=None)
        Adds a strategy to AutoTrader. 
    
    plot_backtest(bot=None):
        Plots backtest results of an AutoTrader Bot.
    
    """
    
    def __init__(self):
        '''
        AutoTrader initialisation. Called when creating new AutoTrader instance.
        '''
        
        self.home_dir       = None
        self.order_summary_fp = None
        
        self.verbosity      = 1
        self.broker_verbosity = 0
        self.notify         = 0
        self.email_params   = None
        self.show_help      = None
        self.show_plot      = False
        
        # Livetrade Parameters
        self.detach_bot     = False
        self.check_data_alignment = True
        self.allow_dancing_bears = False
        self.use_stream     = False
        self.MTF_initialisation = False
        self.stream_config  = None
        
        self.broker         = None
        self.broker_utils   = None
        self.environment    = 'demo'
        self.account_id     = None
        
        self.strategies     = {}
        self._uninitiated_strat_files = []
        self._uninitiated_strat_dicts = []
        self.feed           = 'yahoo'
        self.bots_deployed  = []
        
        # Backtesting Parameters
        self.backtest_mode = False
        self.data_start = None
        self.data_end   = None
        self.data_file  = None
        self.MTF_data_files = None
        self.local_data = None
        self.local_quote_data = None
        self.auxdata = None
        self.backtest_initial_balance = None
        self.backtest_spread = None
        self.backtest_commission = None
        self.backtest_leverage = None
        self.backtest_base_currency = None
        
        # Optimisation Parameters
        self.optimisation_config = None
        self.optimise_mode = False
        self.opt_params = None
        self.bounds = None
        self.Ns = None
        
        # Scan Parameters
        self.scan_mode = False
        self.scan_index = None
        self.scan_watchlist = None
        self.scan_results = {}
        
        # Plotting
        self.max_indis_over = 3
        self.max_indis_below = 2
        self.fig_tools = "pan,wheel_zoom,box_zoom,undo,redo,reset,save,crosshair"
        self.ohlc_height = 400
        self.ohlc_width = 800
        self.top_fig_height = 150
        self.bottom_fig_height = 150
        self.jupyter_notebook = False
        self.show_cancelled = True
        self.chart_timeframe = 'default'
        
    def run(self):
        '''
        Run AutoTrader.
        '''
        
        # Define home_dir if undefined
        if self.home_dir is None:
            self.home_dir = os.getcwd()
        
        # Load uninitiated strategies
        for strat_dict in self._uninitiated_strat_dicts:
            self.add_strategy(strategy_dict=strat_dict)
        for strat_config_file in self._uninitiated_strat_files:
            self.add_strategy(strategy_filename=strat_config_file)
        
        if self.scan_watchlist is not None:
            # Scan watchlist has not overwritten strategy watchlist
            self._update_strategy_watchlist()
        
        # Print help
        if self.show_help is not None:
            printout.option_help(self.show_help)
        
        if len(self.strategies) == 0:
            print("Error: no strategy has been provided. Do so by using the" +\
                  " 'add_strategy' method of AutoTrader.")
            sys.exit(0)
            
        if sum([self.backtest_mode, self.scan_mode]) > 1:
            print("Error: backtest mode and scan mode are both set to True," +\
                  " but only one of these can run at a time.")
            print("Please check your inputs and try again.")
            sys.exit(0)
        
        if self.backtest_mode:
            if self.notify > 0:
                print("Warning: notify set to {} ".format(self.notify) + \
                      "during backtest. Setting to zero to prevent emails.")
                self.notify = 0
        
        if self.optimise_mode:
            if self.backtest_mode:
                self._run_optimise()
            else:
                print("Please set backtest parameters to run optimisation.")
        else:
            self._main()
    
    def usage(self):
        '''
        Prints usage instructions for AutoTrader.
        '''
        printout.usage()
    
    def option_help(self, option):
        '''
        Prints help for a user option of AutoTrader.
        
            Parameters:
                option (str): user option to request help for.
        '''
        printout.option_help(option)
        
    def _main(self):
        '''
        Main run file of autotrader.py. This method is called internally 
        from the "run" method.
        '''
        
        ''' -------------------------------------------------------------- '''
        '''                         Load configuration                     '''
        ''' -------------------------------------------------------------- '''
        # Construct broker config
        global_config_fp = os.path.join(self.home_dir, 'config', 'GLOBAL.yaml')
        if os.path.isfile(global_config_fp):
            global_config = read_yaml(global_config_fp)
        else:
            global_config = None
        broker_config = environment_manager.get_config(self.environment,
                                                       global_config,
                                                       self.feed)
        
        # Construct stream_config dict
        if self.use_stream:
            self.stream_config = broker_config
        
        if self.account_id is not None:
            # Overwrite default account in global config
            broker_config['ACCOUNT_ID'] = self.account_id
        
        # Append broker verbosity to broker_config
        broker_config['verbosity'] = self.broker_verbosity
        
        self._assign_broker(broker_config)
        self._configure_emailing(global_config)
        
        if self.backtest_mode:
            NAV     = []
            balance = []
            margin  = []
        
        if int(self.verbosity) > 0:
            if self.backtest_mode:
                print("Beginning new backtest.")

            elif self.scan_mode:
                print("AutoTrader - AutoScan")
                print("Time: {}\n".format(datetime.now().strftime("%A, %B %d %Y, "+
                                                                  "%H:%M:%S")))
            else:
                print("AutoTrader Livetrade")
                print("--------------------")
                print("Time: {}\n".format(datetime.now().strftime("%A, %B %d %Y, "+
                                                                  "%H:%M:%S")))
        
        ''' -------------------------------------------------------------- '''
        '''    Assign strategy to bot for each instrument in watchlist     '''
        ''' -------------------------------------------------------------- '''
        for strategy in self.strategies:
            for instrument in self.strategies[strategy]['WATCHLIST']:
                data_dict = self.local_data[instrument] if self.local_data is not None else None
                quote_data_dict = self.local_quote_data[instrument] if self.local_quote_data is not None else None
                auxdata = self.auxdata[instrument] if self.auxdata is not None else None
                bot = AutoTraderBot(instrument, self.strategies[strategy],
                                    self.broker, data_dict, quote_data_dict, 
                                    auxdata, self)
                
                if self.detach_bot is True and self.backtest_mode is False:
                    # Send bot to bot manager to monitor stream
                    print("Passing bot to bot manager...")
                    bot_name_string = "{}_{}_{}".format(strategy.replace(' ',''),
                                                        self.strategies[strategy]['INTERVAL'].split(',')[0],
                                                        instrument)
                    ManageBot(bot, self.home_dir, bot_name_string, self.use_stream)
                else:
                    self.bots_deployed.append(bot)
                    
        
        ''' -------------------------------------------------------------- '''
        '''                  Analyse price data using strategy             '''
        ''' -------------------------------------------------------------- '''
        if int(self.verbosity) > 0 and self.backtest_mode:
            # Check data lengths of each bot
            self._check_bot_data()
            
            print("\nTrading...\n")
            backtest_start_time = timeit.default_timer()
            
        if not self.detach_bot:
            start_range, end_range = self.bots_deployed[0]._get_iteration_range()
            
            for i in range(start_range, end_range):
                
                # Update each bot with latest data to generate signal
                for bot in self.bots_deployed:
                    
                    # If backtesting, update virtual broker with latest data
                    if self.backtest_mode:
                        bot._update_backtest(i)
                    
                    # Update bot
                    bot._update(i)
                    
                
                if self.backtest_mode is True:
                    NAV.append(self.broker.NAV)
                    balance.append(self.broker.portfolio_balance)
                    margin.append(self.broker.margin_available)
        
        backtest_end_time = timeit.default_timer()
        
        ''' -------------------------------------------------------------- '''
        '''                     Backtest Post-Processing                   '''
        ''' -------------------------------------------------------------- '''
        # Data iteration complete - proceed to post-processing
        if self.backtest_mode is True:
            # Create backtest summary for each bot 
            for bot in self.bots_deployed:
                bot.create_backtest_summary(balance, NAV, margin)            
            
            if int(self.verbosity) > 0:
                print(f"Backtest complete (runtime {round((backtest_end_time - backtest_start_time), 3)} s).")
                if len(self.bots_deployed) == 1:
                    bot = self.bots_deployed[0]
                    backtest_results = self.analyse_backtest(bot)
                    self.print_backtest_results(backtest_results)
                    
                else:
                    self.multibot_backtest_results = self.multibot_backtest_analysis()
                    self.print_multibot_backtest_results(self.multibot_backtest_results)
                    
                    print("Results for multiple-instrument backtests have been")
                    print("written to AutoTrader.multibot_backtest_results.")
                    print("Individual bot results can be found in the")
                    print("'bots_deployed' attribute of the AutoTrader instance.")
            
            if self.show_plot:
                if len(self.bots_deployed) == 1:
                    if len(self.bots_deployed[0].backtest_summary['trade_summary']) > 0:
                        self.plot_backtest(bot=self.bots_deployed[0])
                
                else:
                    # Backtest run with multiple bots
                    self.plot_multibot_backtest()
        
        elif self.scan_mode and self.show_plot:
            # Show plots for scanned instruments
            for bot in self.bots_deployed:
                ap = self._instantiate_autoplot(bot.data)
                ap.plot(indicators = bot.strategy.indicators, 
                        instrument = bot.instrument)
                time.sleep(0.3)

    def _clear_strategies(self):
        '''
        Removes all strategies saved in autotrader instance.
        '''
        
        self.strategies = {}
    
    def _clear_bots(self):
        '''
        Removes all deployed bots in autotrader instance.
        '''
        
        self.bots_deployed = []
    
    def plot_settings(self, max_indis_over=3, max_indis_below=2,
                      fig_tools="pan,wheel_zoom,box_zoom,undo,redo,reset,save,crosshair",
                      ohlc_height=400, ohlc_width=800, top_fig_height=150,
                      bottom_fig_height=150, jupyter_notebook=False, show_cancelled=True,
                      chart_timeframe='default'):
        ''' Configures settings for AutoPlot. '''
        
        # Assign attributes
        self.max_indis_over     = max_indis_over
        self.max_indis_below    = max_indis_below
        self.fig_tools          = fig_tools
        self.ohlc_height        = ohlc_height
        self.ohlc_width         = ohlc_width
        self.top_fig_height     = top_fig_height
        self.bottom_fig_height  = bottom_fig_height
        self.jupyter_notebook   = jupyter_notebook
        self.show_cancelled     = show_cancelled
        self.chart_timeframe    = chart_timeframe
    
    def _instantiate_autoplot(self, data):
        ''' Creates instance of AutoPlot. '''
        
        # TODO - check length of data to prevent plotting over some length...
        if self.chart_timeframe == 'default':
            ap = autoplot.AutoPlot(data)
        else:
            # Instantiate AutoPlot with requested chart timeframe
            if self.chart_timeframe in self.bots_deployed[0].MTF_data.keys():
                # Valid timeframe requested
                ap = autoplot.AutoPlot(self.bots_deployed[0].MTF_data[self.chart_timeframe])
                ap._add_backtest_price_data(data) # provide nominal timeframe data for merge operations
            else:
                warning_str = f'The chart timeframe requested ({self.chart_timeframe}) was not found ' + \
                    'in the MTF data. Please ensure that the timeframe provided matches ' + \
                    'the format provided in the strategy configuration file, or the local ' + \
                    'data provided.'
                raise Exception(warning_str)
                
        # Assign attributes
        ap.max_indis_over     = self.max_indis_over
        ap.max_indis_below    = self.max_indis_below
        ap.fig_tools          = self.fig_tools
        ap.ohlc_height        = self.ohlc_height
        ap.ohlc_width         = self.ohlc_width
        ap.top_fig_height     = self.top_fig_height
        ap.bottom_fig_height  = self.bottom_fig_height
        ap.jupyter_notebook   = self.jupyter_notebook
        ap.show_cancelled     = self.show_cancelled
        
        return ap
    
    def add_strategy(self, strategy_filename=None, 
                     strategy_dict=None):
        '''
        Adds a strategy to AutoTrader. 
        
            Parameters:
                strategy_filename (str): prefix of yaml strategy
                configuration file, located in home_dir/config.
                
                strategy_dict (dict): alternative to strategy_filename,
                the strategy dictionary can be passed directly.
        '''
        
        if self.home_dir is None:
            # Home directory has not yet been set, postpone strategy addition
            if strategy_filename is None:
                self._uninitiated_strat_dicts.append(strategy_dict)
            else:
                self._uninitiated_strat_files.append(strategy_filename)
            
        else:
            if strategy_dict is None:
                config_file_path = os.path.join(self.home_dir, 'config', strategy_filename)
                new_strategy = read_yaml(config_file_path + '.yaml')
            else:
                new_strategy = strategy_dict
            
            name = new_strategy['NAME']
            
            if name in self.strategies:
                print("Warning: duplicate strategy name deteced. Please check " + \
                      "the NAME field of your strategy configuration file and " + \
                      "make sure it is not the same as other strategies being " + \
                      "run from this instance.")
                print("Conflicting name:", name)
            
            self.strategies[name] = new_strategy
    
    
    def backtest(self, start=None, end=None, initial_balance=1000, spread=0, 
                 commission=0, leverage=1, base_currency='AUD', start_dt=None, 
                 end_dt=None):
        '''
        Configures settings for backtesting.
        
            Parameters:
                start (str): start date for backtesting, in format d/m/yyyy.
                
                end (str): end date for backtesting, in format d/m/yyyy.
                
                initial_balance (float): initial account balance in base currency 
                units.
                
                spread (float): bid/ask spread of instrument.
                
                commission (float): trading commission as percentage per trade.
                
                leverage (int): account leverage.
                
                base_currency (str): base currency of account.
                
                start_dt (datetime): datetime object corresponding to start time.
                
                end_dt (datetime): datetime object corresponding to end time.
                
            Note: 
                Start and end times must be specified as the same type. For
                example, both start and end arguments must be provided together, 
                or alternatively, start_dt and end_dt must both be provided.
        '''
        
        # Convert start and end strings to datetime objects
        if start_dt is None and end_dt is None:
            start_dt    = datetime.strptime(start + '+0000', '%d/%m/%Y%z')
            end_dt      = datetime.strptime(end + '+0000', '%d/%m/%Y%z')
        
        # Assign attributes
        self.backtest_mode = True
        self.data_start = start_dt
        self.data_end   = end_dt
        self.backtest_initial_balance = initial_balance
        self.backtest_spread = spread
        self.backtest_commission = commission
        self.backtest_leverage = leverage
        self.backtest_base_currency = base_currency
    
    
    def configure(self, feed='yahoo', verbosity=1, notify=0, home_dir=None,
                  use_stream=False, detach_bot=False,
                  check_data_alignment=True, allow_dancing_bears=False,
                  account_id=None, environment='demo', show_plot=False,
                  MTF_initialisation=False, jupyter_notebook=False):
        '''
        AutoTrader Run Configuration
        -------------------------------
        
        Configures various run settings for AutoTrader.
        
            Parameters:
                feed (str): the data feed to be used (eg. Yahoo, Oanda).
                
                verbosity (int): the verbosity of AutoTrader (0, 1 or 2).
                
                notify (int): the level of email notification (0, 1 or 2).
                
                home_dir (str): the project home directory.
                
                use_stream (bool): set to True to use price stream as data feed.
                
                detach_bot (bool): set to True to spawn new thread for each bot
                deployed.
                
                check_data_alignment (bool): verify time of latest candle in
                data recieved against current time.
                
                allow_dancing_bears (bool): allow incomplete candles to be 
                passed to strategy.
                
                account_id (str): the brokerage account ID to use in this instance.
                
                environment (str): the trading environment of this instance.
                
                show_plot (bool): automatically display plot of results.
                
                MTF_initialisation (bool): only download mutliple time frame 
                data when initialising the strategy, rather than every update.
        '''
        
        self.feed = feed
        self.verbosity = verbosity
        self.notify = notify
        self.home_dir = home_dir if home_dir is not None else os.getcwd()
        self.use_stream = use_stream
        self.detach_bot = detach_bot
        self.check_data_alignment = check_data_alignment
        self.allow_dancing_bears = allow_dancing_bears
        self.account_id = account_id
        self.environment = environment
        self.show_plot = show_plot
        self.MTF_initialisation = MTF_initialisation
        self.jupyter_notebook = jupyter_notebook
        
    def add_data(self, data_dict=None, quote_data=None, 
                 data_directory='price_data', abs_dir_path=None, auxdata=None):
        ''' 
        Add local data to run backtest on. Note that to ensure proper directory 
        configuration, this method should only be called after calling 
        autotrader.configure().
        
        Parameters:
            data_dict (dict): a dictionary containing the filenames of the datasets
                 to be used. For example:
                    data_dict = {'product1': 'filename1.csv',
                                 'product2': 'filename2.csv'}
                 
                 In the case of MTF data, the data_dict will look as follows:
                     data_dict = {'product1': {'H1': 'product1_H1.csv',
                                               'D': 'product1_D.csv'},
                                  'product2': {'H1': 'product2_H1.csv',
                                               'D': 'product2_D.csv'}
                                  }
                 
                 Note that the filenames in the dict above must be present in the 
                 data directory, as specified by the data_directory or abs_dir_path
                 parameters.
                
            quote_data (dict): a dictionary containing the quote data filenames 
                of the datasets provided in data_dict. For example:
                    quote_data = {'product1': 'product1_quote.csv',
                                  'product2': 'product2_quote.csv'}
                
                In the case of MTF data, quote data should only be provided for
                    the base timeframe (ie. the data which will be iterated on
                    when backtesting). Therefore, the quote_data dict will look
                    the same for single timeframe and MTF backtests.
            
            data_directory (str): the name of the sub-directory containing price
                data files. This directory should be located in the project
                home directory (at.home_dir).
            
            abs_dir_path: the absolute path to the data_directory. This parameter
                may be used when the datafiles are stored outside of the project
                directory.
            
            auxdata (dict): a dictionary containing raw data to supplement the 
                data passed to the strategy module. For strategies involving 
                multiple products, the keys of this dictionary must correspond
                to the products, with the auxdata in nested dictionaries or 
                otherwise. Examples include:
                    auxdata = {'product1': aux_price_data,
                               'product2': {'extra_data1': dataset1,
                                            'extra_data2': dataset2}
                               }
        '''
        # TODO - add option to specify strategy, in case multiple strategies
        # (requiring different data) are added to the instance
        
        dir_path = abs_dir_path if abs_dir_path is not None else os.path.join(self.home_dir, data_directory)
        
        # TODO - wrap the loops below into a signle for loop with dict assignment
        
        # Trading data
        if data_dict is not None:
            # Assign local data attribute
            local_data = {}
            
            # Populate local_data
            for product in data_dict:
                if type(data_dict[product]) == dict:
                    # MTF data
                    MTF_data = {}
                    for timeframe in data_dict[product]:
                        MTF_data[timeframe] = os.path.join(dir_path, data_dict[product][timeframe])
                    
                    local_data[product] = MTF_data
                else:
                    # Single timeframe data
                    local_data[product] = os.path.join(dir_path, data_dict[product])
                    
            self.local_data = local_data
        
        # Quote data
        if quote_data is not None:
            # Assign local data attribute
            local_quote_data = {}
            
            # Populate local_quote_data
            for product in quote_data:
                if type(quote_data[product]) == dict:
                    raise Exception("Only a single quote-data file should be " +\
                                    "provided per instrument traded.")
                    
                else:
                    local_quote_data[product] = os.path.join(dir_path, quote_data[product])
            
            self.local_quote_data = local_quote_data
        
        self.auxdata = auxdata
    
    def scan(self, strategy_filename=None, strategy_dict=None, scan_index=None):
        '''
        Configure AutoTrader scan. 
            
            Parameters:
                strategy_filename (str): prefix of yaml strategy
                configuration file, located in home_dir/config.
                    
                scan_index (str): index to scan.
        '''
        
        # If a strategy is provided here, add it
        if strategy_filename is not None:
            self.add_strategy(strategy_filename)
        elif strategy_dict is not None:
            self.add_strategy(strategy_dict=strategy_dict)
        
        # If scan index provided, use that. Else, use strategy watchlist
        if scan_index is not None:
            self.scan_watchlist = instrument_list.get_watchlist(scan_index,
                                                                self.feed)

        else:
            scan_index = 'Strategy watchlist'
            
        self.scan_mode = True
        self.scan_index = scan_index
        self.check_data_alignment = False
    
    def _update_strategy_watchlist(self):
        ''' Updates the watchlist of each strategy with the scan watchlist. '''
        
        for strategy in self.strategies:
            self.strategies[strategy]['WATCHLIST'] = self.scan_watchlist
    
    
    def plot_backtest(self, bot=None):
        '''
        Plots backtest results of an AutoTrader Bot.
            
            Parameters:
                bot (class): AutoTrader bot class containing backtest results.
        '''
        
        if bot is None:
            if len(self.bots_deployed) == 1:
                bot = self.bots_deployed[0]
            else:
                # Multi-bot backtest
                self.plot_multibot_backtest()
                return
            
        ap = self._instantiate_autoplot(bot.data)
        profit_df = pd.merge(bot.data, 
                             bot.backtest_summary['trade_summary']['Profit'], 
                             left_index=True, right_index=True).Profit.cumsum()
        
        ap.plot(bot.backtest_summary, cumulative_PL=profit_df)
    
    def plot_multibot_backtest(self,):
        ''' Plots the backtest results for multiple trading bots. '''
        
        cpl_dict = {}
        for bot in self.bots_deployed:
            profit_df = pd.merge(bot.data, 
                     bot.backtest_summary['trade_summary']['Profit'], 
                     left_index=True, right_index=True).Profit.cumsum()
            cpl_dict[bot.instrument] = profit_df
        
        ap = self._instantiate_autoplot(bot.data)
        ap._plot_multibot_backtest(self.multibot_backtest_results, 
                                   bot.backtest_summary['account_history']['NAV'], 
                                   cpl_dict, 
                                   bot.backtest_summary['account_history']['margin'])
        
    
    def multibot_backtest_analysis(self, bots=None):
        '''
        Analyses backtest results of multiple bots to create an overall 
        performance summary.
        
            Parameters:
                bots (list): a list of AutoTrader bots to analyse.
        '''
        
        instruments = []
        win_rate    = []
        no_trades   = []
        avg_win     = []
        max_win     = []
        avg_loss    = []
        max_loss    = []
        no_long     = []
        no_short    = []
        
        if bots is None:
            bots = self.bots_deployed
        
        for bot in bots:
            backtest_results = self.analyse_backtest(bot)
            
            instruments.append(bot.instrument)
            no_trades.append(backtest_results['no_trades'])
            if backtest_results['no_trades'] > 0:
                win_rate.append(backtest_results['all_trades']['win_rate'])
                avg_win.append(backtest_results['all_trades']['avg_win'])
                max_win.append(backtest_results['all_trades']['max_win'])
                avg_loss.append(backtest_results['all_trades']['avg_loss'])
                max_loss.append(backtest_results['all_trades']['max_loss'])
                no_long.append(backtest_results['long_trades']['no_trades'])
                no_short.append(backtest_results['short_trades']['no_trades'])
            else:
                win_rate.append(np.nan)
                avg_win.append(np.nan)
                max_win.append(np.nan)
                avg_loss.append(np.nan)
                max_loss.append(np.nan)
                no_long.append(np.nan)
                no_short.append(np.nan)
        
        multibot_backtest_results = pd.DataFrame(data={'win_rate': win_rate,
                                                       'no_trades': no_trades,
                                                       'avg_win': avg_win,
                                                       'max_win': max_win,
                                                       'avg_loss': avg_loss,
                                                       'max_loss': max_loss,
                                                       'no_long': no_long,
                                                       'no_short': no_short},
                                                 index=instruments)
        
        return multibot_backtest_results
        
    def analyse_backtest(self, bot=None):
        '''
        Analyses bot backtest results to extract key statistics.
        
            Parameters:
                bot (class): An AutoBot class instance.
        '''
        
        if bot is None:
            if len(self.bots_deployed) == 1:
                bot = self.bots_deployed[0]
            else:
                print("Reverting to multi-bot backtest.")
                return self.multibot_backtest_analysis()
                    
        backtest_summary = bot.backtest_summary
        
        trade_summary   = backtest_summary['trade_summary']
        instrument      = backtest_summary['instrument']
        account_history = backtest_summary['account_history']
        
        cpl = trade_summary.Profit.cumsum()
        
        backtest_results = {}
        
        # All trades
        no_trades = len(trade_summary)
        backtest_results['no_trades'] = no_trades
        backtest_results['start'] = account_history.index[0]
        backtest_results['end'] = account_history.index[-1]
        
        if no_trades > 0:
            backtest_results['all_trades'] = {}
            wins        = trade_summary[trade_summary.Profit > 0]
            avg_win     = np.mean(wins.Profit)
            max_win     = np.max(wins.Profit)
            loss        = trade_summary[trade_summary.Profit < 0]
            avg_loss    = abs(np.mean(loss.Profit))
            max_loss    = abs(np.min(loss.Profit))
            win_rate    = 100*len(wins)/no_trades
            longest_win_streak, longest_lose_streak  = self.broker_utils.get_streaks(trade_summary)
            avg_trade_duration = np.mean(trade_summary.Trade_duration.values)
            min_trade_duration = min(trade_summary.Trade_duration.values)
            max_trade_duration = max(trade_summary.Trade_duration.values)
            max_drawdown = min(account_history.drawdown)
            total_fees = trade_summary.Fees.sum()
            
            starting_balance = account_history.balance[0]
            ending_balance = account_history.balance[-1]
            ending_NAV = account_history.NAV[-1]
            abs_return = ending_balance - starting_balance
            pc_return = 100 * abs_return / starting_balance
            
            backtest_results['all_trades']['starting_balance'] = starting_balance
            backtest_results['all_trades']['ending_balance'] = ending_balance
            backtest_results['all_trades']['ending_NAV']    = ending_NAV
            backtest_results['all_trades']['abs_return']    = abs_return
            backtest_results['all_trades']['pc_return']     = pc_return
            backtest_results['all_trades']['avg_win']       = avg_win
            backtest_results['all_trades']['max_win']       = max_win
            backtest_results['all_trades']['avg_loss']      = avg_loss
            backtest_results['all_trades']['max_loss']      = max_loss
            backtest_results['all_trades']['win_rate']      = win_rate
            backtest_results['all_trades']['win_streak']    = longest_win_streak
            backtest_results['all_trades']['lose_streak']   = longest_lose_streak
            backtest_results['all_trades']['longest_trade'] = str(timedelta(seconds = int(max_trade_duration)))
            backtest_results['all_trades']['shortest_trade'] = str(timedelta(seconds = int(min_trade_duration)))
            backtest_results['all_trades']['avg_trade_duration'] = str(timedelta(seconds = int(avg_trade_duration)))
            backtest_results['all_trades']['net_pl']        = cpl.values[-1]
            backtest_results['all_trades']['max_drawdown']  = max_drawdown
            backtest_results['all_trades']['total_fees']    = total_fees
            
        # Cancelled and open orders
        cancelled_orders = self.broker.get_cancelled_orders(instrument)
        open_trades      = self.broker.get_open_positions(instrument)
        backtest_results['no_open'] = len(open_trades)
        backtest_results['no_cancelled'] = len(cancelled_orders)
        
        # Long trades
        long_trades     = trade_summary[trade_summary.Size > 0]
        no_long         = len(long_trades)
        backtest_results['long_trades'] = {}
        backtest_results['long_trades']['no_trades'] = no_long
        if no_long > 0:
            long_wins       = long_trades[long_trades.Profit > 0]
            avg_long_win    = np.mean(long_wins.Profit)
            max_long_win    = np.max(long_wins.Profit)
            long_loss       = long_trades[long_trades.Profit < 0]
            avg_long_loss   = abs(np.mean(long_loss.Profit))
            max_long_loss   = abs(np.min(long_loss.Profit))
            long_wr         = 100*len(long_trades[long_trades.Profit > 0])/no_long
            
            backtest_results['long_trades']['avg_long_win']     = avg_long_win
            backtest_results['long_trades']['max_long_win']     = max_long_win 
            backtest_results['long_trades']['avg_long_loss']    = avg_long_loss
            backtest_results['long_trades']['max_long_loss']    = max_long_loss
            backtest_results['long_trades']['long_wr']          = long_wr
            
        # Short trades
        short_trades    = trade_summary[trade_summary.Size < 0]
        no_short        = len(short_trades)
        backtest_results['short_trades'] = {}
        backtest_results['short_trades']['no_trades'] = no_short
        if no_short > 0:
            short_wins      = short_trades[short_trades.Profit > 0]
            avg_short_win   = np.mean(short_wins.Profit)
            max_short_win   = np.max(short_wins.Profit)
            short_loss      = short_trades[short_trades.Profit < 0]
            avg_short_loss  = abs(np.mean(short_loss.Profit))
            max_short_loss  = abs(np.min(short_loss.Profit))
            short_wr        = 100*len(short_trades[short_trades.Profit > 0])/no_short
            
            backtest_results['short_trades']['avg_short_win']   = avg_short_win
            backtest_results['short_trades']['max_short_win']   = max_short_win
            backtest_results['short_trades']['avg_short_loss']  = avg_short_loss
            backtest_results['short_trades']['max_short_loss']  = max_short_loss
            backtest_results['short_trades']['short_wr']        = short_wr
        
        return backtest_results
    
    def print_multibot_backtest_results(self, backtest_results=None):
        '''
        Prints to console the backtest results of a multi-bot backtest.
        
            Parameters:
                backtest_results (dict): dictionary containing backtest results.
        '''
        
        bot = self.bots_deployed[0]
        account_history = bot.backtest_summary['account_history']
        
        start_date = account_history.index[0]
        end_date = account_history.index[-1]
        
        starting_balance = account_history.balance[0]
        ending_balance = account_history.balance[-1]
        ending_NAV = account_history.NAV[-1]
        abs_return = ending_balance - starting_balance
        pc_return = 100 * abs_return / starting_balance
        
        print("\n---------------------------------------------------")
        print("            MultiBot Backtest Results")
        print("---------------------------------------------------")
        print("Start date:              {}".format(start_date))
        print("End date:                {}".format(end_date))
        print("Starting balance:        ${}".format(round(starting_balance, 2)))
        print("Ending balance:          ${}".format(round(ending_balance, 2)))
        print("Ending NAV:              ${}".format(round(ending_NAV, 2)))
        print("Total return:            ${} ({}%)".format(round(abs_return, 2), 
                                          round(pc_return, 1)))
        
        print("Instruments traded: ", backtest_results.index.values)
        print("Total no. trades:   ", backtest_results.no_trades.sum())
        print("Short trades:       ", backtest_results.no_short.sum(),
              "({}%)".format(round(100*backtest_results.no_short.sum()/backtest_results.no_trades.sum(),2)))
        print("Long trades:        ", backtest_results.no_long.sum(),
              "({}%)".format(round(100*backtest_results.no_long.sum()/backtest_results.no_trades.sum(),2)))
        
        print("\nInstrument win rates (%):")
        print(backtest_results[['win_rate', 'no_trades']])
        print("\nMaximum/Average Win/Loss breakdown ($):")
        print(backtest_results[["max_win", "max_loss", "avg_win", "avg_loss"]])
        print("\nAverage Reward to Risk Ratio:")
        print(round(backtest_results.avg_win / backtest_results.avg_loss,1))
        print("")
        
    
    def _assign_broker(self, broker_config):
        '''
        Configures and assigns appropriate broker for trading.
        '''
        
        if self.backtest_mode is True:
            # Backtesting; use virtual broker
            utils_module    = importlib.import_module('autotrader.brokers.virtual.utils')
            
            utils           = utils_module.Utils()
            broker          = Broker(broker_config, utils)
            
            initial_deposit = self.backtest_initial_balance
            spread          = self.backtest_spread
            leverage        = self.backtest_leverage
            commission      = self.backtest_commission
            base_currency   = self.backtest_base_currency
            
            broker.make_deposit(initial_deposit)
            broker.fee      = spread
            broker.leverage = leverage
            broker.commission = commission
            broker.spread   = spread
            broker.base_currency = base_currency
            # self.get_data.base_currency = base_currency
            
            if int(self.verbosity) > 0:
                banner = pyfiglet.figlet_format("AutoBacktest")
                print(banner)
                
        else:
            # Live/demo trading
            if self.feed.lower() == 'yahoo':
                # Assign virtual broker for Yahoo API
                utils_module    = importlib.import_module('autotrader.brokers.virtual.utils')
                utils           = utils_module.Utils()
                broker          = Broker(broker_config, utils)
                
            elif self.feed.lower() == 'oanda':
                # Oanda v20 API
                utils_module    = importlib.import_module('autotrader.brokers.{}.utils'.format(self.feed.lower()))
                utils           = utils_module.Utils()
                broker          = Oanda.Oanda(broker_config, utils)
                
            elif self.feed.lower() == 'ib':
                # Interactive Brokers API
                utils_module    = importlib.import_module('autotrader.brokers.interactive_brokers.utils')
                utils           = utils_module.Utils()
                # broker          = ib_broker.interac_broker(broker_config, utils)
        
        self.broker = broker
        self.broker_utils = utils
    
    
    def _configure_emailing(self, global_config):
        '''
        Configure email settings.
        '''
        # TODO - allow setting email in this method
        
        if int(self.notify) > 0:
            host_email      = None
            mailing_list    = None
            
            # TODO - what if no email provided?
            
            if "EMAILING" in global_config:
                # Look for host email and mailing list in strategy config, if it
                # was not picked up in strategy config
                if "MAILING_LIST" in global_config["EMAILING"] and mailing_list is None:
                    mailing_list    = global_config["EMAILING"]["MAILING_LIST"]
                if "HOST_ACCOUNT" in global_config["EMAILING"] and host_email is None:
                    host_email      = global_config["EMAILING"]["HOST_ACCOUNT"]
            
            if host_email is None:
                print("Warning: email host account not provided.")
            if mailing_list is None:
                print("Warning: no mailing list provided.")
                
            email_params = {'mailing_list': mailing_list,
                            'host_email': host_email}
            self.email_params = email_params
            
            logfiles_path = os.path.join(self.home_dir, 'logfiles')
            order_summary_fp = os.path.join(logfiles_path, 'order_history.txt')
            
            if not os.path.isdir(logfiles_path):
                os.mkdir(logfiles_path)
            
            self.order_summary_fp = order_summary_fp

    def print_backtest_results(self, backtest_results):
        ''' 
        Prints backtest results. Backtest results can be found using
        bot.backtest_summary. 
        '''
        
        # TODO - change output based on verbosity (include as input)
        
        start_date = backtest_results['start'].strftime("%b %d %Y %H:%M:%S")
        end_date = backtest_results['end'].strftime("%b %d %Y %H:%M:%S")
        
        # params      = self.strategy_params
        no_trades   = backtest_results['no_trades']
        if no_trades > 0:
            win_rate    = backtest_results['all_trades']['win_rate']
            abs_return  = backtest_results['all_trades']['abs_return']
            pc_return   = backtest_results['all_trades']['pc_return']
            max_drawdown = backtest_results['all_trades']['max_drawdown']
            max_win     = backtest_results['all_trades']['max_win']
            avg_win     = backtest_results['all_trades']['avg_win']
            max_loss    = backtest_results['all_trades']['max_loss']
            avg_loss    = backtest_results['all_trades']['avg_loss']
            longest_win_streak = backtest_results['all_trades']['win_streak']
            longest_lose_streak = backtest_results['all_trades']['lose_streak']
            total_fees = backtest_results['all_trades']['total_fees']
            starting_balance = backtest_results['all_trades']['starting_balance']
            ending_balance = backtest_results['all_trades']['ending_balance']
            ending_NAV = backtest_results['all_trades']['ending_NAV']
        
        print("\n----------------------------------------------")
        print("               Backtest Results")
        print("----------------------------------------------")
        # TODO - the below are all strategy specific. Maybe if only one strategy
        # is used (ie len(self.strategies) = 1), that can be used. Otherwise,
        # not sure. However, the granularity has to be the same ... until 
        # time indexing becomes a thing
        # print("Strategy: {}".format(self.strategy.name))
        # print("Timeframe:               {}".format(params['granularity']))
        # if params is not None and 'RR' in params:
        #     print("Risk to reward ratio:    {}".format(params['RR']))
        #     print("Profitable win rate:     {}%".format(round(100/(1+params['RR']), 1)))
        if no_trades > 0:
            print("Start date:              {}".format(start_date))
            print("End date:                {}".format(end_date))
            print("Starting balance:        ${}".format(round(starting_balance, 2)))
            print("Ending balance:          ${}".format(round(ending_balance, 2)))
            print("Ending NAV:              ${}".format(round(ending_NAV, 2)))
            print("Total return:            ${} ({}%)".format(round(abs_return, 2), 
                                              round(pc_return, 1)))
            print("Total no. trades:        {}".format(no_trades))
            print("Total fees:              ${}".format(round(total_fees, 3)))
            print("Backtest win rate:       {}%".format(round(win_rate, 1)))
            print("Maximum drawdown:        {}%".format(round(max_drawdown*100, 2)))
            print("Max win:                 ${}".format(round(max_win, 2)))
            print("Average win:             ${}".format(round(avg_win, 2)))
            print("Max loss:                -${}".format(round(max_loss, 2)))
            print("Average loss:            -${}".format(round(avg_loss, 2)))
            print("Longest win streak:      {} trades".format(longest_win_streak))
            print("Longest losing streak:   {} trades".format(longest_lose_streak))
            print("Average trade duration:  {}".format(backtest_results['all_trades']['avg_trade_duration']))
            
        else:
            print("No trades taken.")
        
        no_open = backtest_results['no_open']
        no_cancelled = backtest_results['no_cancelled']
        
        if no_open > 0:
            print("Orders still open:       {}".format(no_open))
        if no_cancelled > 0:
            print("Cancelled orders:        {}".format(no_cancelled))
        
        # Long trades
        no_long = backtest_results['long_trades']['no_trades']
        print("\n            Summary of long trades")
        print("----------------------------------------------")
        if no_long > 0:
            avg_long_win = backtest_results['long_trades']['avg_long_win']
            max_long_win = backtest_results['long_trades']['max_long_win']
            avg_long_loss = backtest_results['long_trades']['avg_long_loss']
            max_long_loss = backtest_results['long_trades']['max_long_loss']
            long_wr = backtest_results['long_trades']['long_wr']
            
            print("Number of long trades:   {}".format(no_long))
            print("Long win rate:           {}%".format(round(long_wr, 1)))
            print("Max win:                 ${}".format(round(max_long_win, 2)))
            print("Average win:             ${}".format(round(avg_long_win, 2)))
            print("Max loss:                -${}".format(round(max_long_loss, 2)))
            print("Average loss:            -${}".format(round(avg_long_loss, 2)))
        else:
            print("There were no long trades.")
          
        # Short trades
        no_short = backtest_results['short_trades']['no_trades']
        print("\n             Summary of short trades")
        print("----------------------------------------------")
        if no_short > 0:
            avg_short_win = backtest_results['short_trades']['avg_short_win']
            max_short_win = backtest_results['short_trades']['max_short_win']
            avg_short_loss = backtest_results['short_trades']['avg_short_loss']
            max_short_loss = backtest_results['short_trades']['max_short_loss']
            short_wr = backtest_results['short_trades']['short_wr']
            
            print("Number of short trades:  {}".format(no_short))
            print("short win rate:          {}%".format(round(short_wr, 1)))
            print("Max win:                 ${}".format(round(max_short_win, 2)))
            print("Average win:             ${}".format(round(avg_short_win, 2)))
            print("Max loss:                -${}".format(round(max_short_loss, 2)))
            print("Average loss:            -${}".format(round(avg_short_loss, 2)))
            
        else:
            print("There were no short trades.")

    def optimise(self, opt_params, bounds, Ns=4):
        '''
        Optimisation configuration.
        
            Parameters: 
                opt_params (list): the parameters to be optimised, as they 
                are named in the strategy configuration file.
                
                bounds (list of tuples): the bounds on each of the 
                parameters to be optimised, specified as a tuple of the form
                (lower, upper) for each parameter.
                
                Ns (int): the number of points along each dimension of the 
                optimisation grid.
        '''
        
        if type(bounds) == str:
            full_tuple = literal_eval(bounds)
            bounds = [(x[0], x[-1]) for x in full_tuple]

        if type(opt_params) == str:
            opt_params = opt_params.split(',')
        
        self.optimise_mode = True
        self.opt_params = opt_params
        self.bounds = bounds
        self.Ns = Ns
        
        
    def _run_optimise(self):
        '''
        Runs optimisation of strategy parameters.
        '''
        
        # Modify verbosity for optimisation
        verbosity = self.verbosity
        self.verbosity = 0
        self.show_plot = False
        
        self.objective      = 'profit + MDD'
        
        ''' --------------------------------------------------------------- '''
        '''                          Unpack user options                    '''
        ''' --------------------------------------------------------------- '''
        
        # Look in self.strategies for config
        if len(self.strategies) > 1:
            print("Error: please optimise one strategy at a time.")
            print("Exiting.")
            sys.exit(0)
        else:
            config_dict = self.strategies[list(self.strategies.keys())[0]]
                
        ''' --------------------------------------------------------------- '''
        '''                      Define optimisation inputs                 '''
        ''' --------------------------------------------------------------- '''
        my_args     = (config_dict, self.opt_params, self.verbosity)
        
        ''' --------------------------------------------------------------- '''
        '''                             Run Optimiser                       '''
        ''' --------------------------------------------------------------- '''
        start = timeit.default_timer()
        result = brute(func         = self._optimisation_helper_function, 
                       ranges       = self.bounds, 
                       args         = my_args, 
                       Ns           = self.Ns,
                       full_output  = True)
        stop = timeit.default_timer()
        
        ''' --------------------------------------------------------------- '''
        '''      Delete historical data file after running optimisation     '''
        ''' --------------------------------------------------------------- '''
        granularity             = config_dict["INTERVAL"]
        pair                    = config_dict["WATCHLIST"][0]
        historical_data_name    = 'hist_{0}{1}.csv'.format(granularity, pair)
        historical_quote_data_name = 'hist_{0}{1}_quote.csv'.format(granularity, pair)
        historical_data_file_path = os.path.join(self.home_dir, 
                                                 'price_data',
                                                 historical_data_name)
        historical_quote_data_file_path = os.path.join(self.home_dir, 
                                                       'price_data',
                                                       historical_quote_data_name)
        os.remove(historical_data_file_path)
        os.remove(historical_quote_data_file_path)
        
        opt_params = result[0]
        opt_value = result[1]
        
        # TODO - use the below for heatmap plotting
        # grid_points = result[2]
        # grid_values = result[3]
        
        ''' --------------------------------------------------------------- '''
        '''                           Print output                          '''
        ''' --------------------------------------------------------------- '''
        print("\nOptimisation complete.")
        print('Time to run: {}s'.format(round((stop - start), 3)))
        print("Optimal parameters:")
        print(opt_params)
        print("Objective:")
        print(opt_value)
        
        # Reset verbosity
        self.verbosity = verbosity
    
    
    def _optimisation_helper_function(self, params, config_dict, opt_params, verbosity):
        '''
        Helper function for optimising strategy parameters in AutoTrader.
        This function will parse the ordered params into the config dict.
        
        '''
        
        ''' ------------------------------------------------------------------ '''
        '''   Edit strategy parameters in config_dict using supplied params    '''
        ''' ------------------------------------------------------------------ '''
        for parameter in config_dict['PARAMETERS']:
            if parameter in opt_params:
                config_dict['PARAMETERS'][parameter] = params[opt_params.index(parameter)]
            else:
                continue
        
        ''' ------------------------------------------------------------------ '''
        '''           Run AutoTrader and evaluate objective function           '''
        ''' ------------------------------------------------------------------ '''
        self._clear_strategies()
        self._clear_bots()
        self.add_strategy(strategy_dict = config_dict)
        self._main()
        
        bot = self.bots_deployed[0]
            
        backtest_results    = self.analyse_backtest(bot)
        
        try:
            objective           = -backtest_results['all_trades']['net_pl']
        except:
            objective           = 1000
                              
        print("Parameters/objective:", params, "/", objective)
        
        return objective
    
    
    def _check_bot_data(self):
        ''' Function to compare lengths of bot data. '''
        
        data_lengths = [len(bot.data) for bot in self.bots_deployed]
        
        if min(data_lengths) != np.mean(data_lengths):
            print("\nWarning: mismatched data lengths detected. Correcting via row reduction.")
            self._normalise_bot_data()
    
    def _normalise_bot_data(self):
        ''' 
        Function to normalise the data of mutliple bots so that their
        indexes are equal, allowing backtesting.
        '''
        
        # Construct list of bot data
        data = [bot.data for bot in self.bots_deployed]
        
        for i, dat in enumerate(data):
            # Initialise common index
            comm_index = dat.index
            
            # Update common index by intersection with other data 
            for j, dat_2 in enumerate(data):
                comm_index = comm_index.intersection(dat_2.index)
            
            # Adjust bot data using common indexes
            adj_data = dat[dat.index.isin(comm_index)]
            
            # Re-assign bot data
            self.bots_deployed[i]._replace_data(adj_data)
        
    
if __name__ == '__main__':
    autotrader = AutoTrader()
    autotrader.usage()
