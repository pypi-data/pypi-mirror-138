from emerquant.factors.technical.mean_reversion import PairsTradingSerialCointegrationFactor

def rebuild_pairs_trading_serial_cointegration_factor(universe_name,
                                                      raw_OHCLV_dataframe,
                                                      resolution_in_mins,
                                                      trading_hours,
                                                      trades_only_on_weekdays,
                                                      finML_feature_engineer,
                                                      finML_optimal_entry_model,
                                                      securities_names_list,
                                                      objective,
                                                      train_split_ratio,
                                                      starting_equity,
                                                      pct_equity_invested,
                                                      market_value_pct_commissions,
                                                      bid_ask_spread_pct_slippage,
                                                      scale_equity_to_traded_securities):
    """Helper function to rebuild our PairsTradingSerialCointegrationFactor object
    """

    pairs_trading_serial_cointegration_factor = PairsTradingSerialCointegrationFactor(universe_name=universe_name,
                                                                                      raw_OHCLV_dataframe=raw_OHCLV_dataframe,
                                                                                      resolution_in_mins=resolution_in_mins,
                                                                                      trading_hours=trading_hours,
                                                                                      trades_only_on_weekdays=trades_only_on_weekdays,
                                                                                      securities_names_list=securities_names_list,
                                                                                      objective=objective,
                                                                                      train_split_ratio=train_split_ratio,
                                                                                      starting_equity=starting_equity,
                                                                                      pct_equity_invested=pct_equity_invested,
                                                                                      market_value_pct_commissions=market_value_pct_commissions,
                                                                                      bid_ask_spread_pct_slippage=bid_ask_spread_pct_slippage,
                                                                                      scale_equity_to_traded_securities=scale_equity_to_traded_securities)

    pairs_trading_serial_cointegration_factor.intialize_pairs_trading_data_structures()
    pairs_trading_serial_cointegration_factor.initialize_finML_data_structures(finML_feature_engineer=finML_feature_engineer,
                                                                               finML_optimal_entry_model=finML_optimal_entry_model)

    return pairs_trading_serial_cointegration_factor

from emerquant.connections.binance.binance_connection import BinanceConnection

def rebuild_binance_connection(binance_api_key,
                               binance_api_secret):
    """Helper function to rebuild our BinanceConnection object
    """

    binance_connection = BinanceConnection(binance_api_key,
                                           binance_api_secret)

    binance_connection.initialize_binance_client()

    return binance_connection

from emerquant.finML.optimal_entry_models import OptimalEntryClassifier

def rebuild_optimal_entry_classifier(study_name,
                                     storage_name,
                                     n_splits,
                                     n_test_splits,
                                     embargo_td,
                                     X_train_df,
                                     y_train_series,
                                     complete_datetime_index_series,
                                     train_time_of_entry_series,
                                     train_time_of_exit_series,
                                     impact_series):
    """Helper function to rebuild our BinanceConnection object
    """

    rebuild_optimal_entry_classifier = OptimalEntryClassifier(study_name,
                                                              storage_name,
                                                              n_splits,
                                                              n_test_splits,
                                                              embargo_td,
                                                              X_train_df,
                                                              y_train_series,
                                                              complete_datetime_index_series,
                                                              train_time_of_entry_series,
                                                              train_time_of_exit_series,
                                                              impact_series)

    return rebuild_optimal_entry_classifier