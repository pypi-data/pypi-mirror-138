import unittest
import pandas as pd
import numpy as np
from autoai_ts_libs.srom.transformers.feature_engineering.timeseries.functions import *
from autoai_ts_libs.srom.transformers.feature_engineering.timeseries.function_map import MAPPING
from autoai_ts_libs.srom.transformers.feature_engineering.timeseries.functions_bivariate import *


class TestFunctions(unittest.TestCase):
    """Test various functions"""

    @classmethod
    def setUpClass(test_class):
        pass

    @classmethod
    def tearDownClass(test_class):
        pass

    def test_univariate_execution(self):
        df = pd.read_csv("./tests/data/sales.csv")
        X = df["Sales"].to_numpy()

        functions = [
            mean,
            sum_values,
            minimum,
            maximum,
            median,
            std,
            variance,
            count,
            skew,
            kurtosis,
            quantile_25,
            quantile_75,
            quantile_range,
            rate_of_change,
            sum_of_change,
            absoluate_sum_of_changes,
            trend_slop,
            abs_energy,
            mean_abs_change,
            mean_change,
            mean_second_derivative_central,
            count_above_mean,
            count_below_mean,
            corr_coefficient,
            delta_diff,
            past_value,
            fft_coefficient_real,
            fft_coefficient_abs,
            identity,
            wavelet_features,
            z_score,
            count_nan,
            geometric_mean,
            mode_abs_change,
            sum_log_values,
            normalised_count_below_mean,
            normalised_count_above_mean,
            discrete_cosine,
            svd_entropy,
            welch_spectral_entropy,
            fft_spectral_entropy,
            perm_entropy,
            katz_fd,
            petrosian_fd,
            max_langevin_fixed_point,
            fft_aggregated_kurtosis,
            fft_aggregated_skew,
            fft_aggregated_variance,
            fft_aggregated_centroid,
            partial_auto_correlation,
            augmented_dickey_fuller_used_lag,
            augmented_dickey_fuller_p_value,
            augmented_dickey_fuller_teststat,
            friedrich_coefficients,
            index_mass_quantile,
            energy_ratio_by_chunks,
            agg_auto_correlation_std,
            agg_auto_correlation_mean,
            agg_auto_correlation_median,
            agg_auto_correlation_var,
            symmetry_looking,
            ar_coefficient,
            cid_ce,
            c3,
            time_reversal_asymmetry_statistic,
            auto_covariance,
            auto_correlation,
            approximate_entropy,
            has_duplicate,
            has_duplicate_min,
            has_duplicate_max,
            variance_larger_than_standard_deviation,
            mle_uniform,
            mle_gaussian,
            coefficient_variation,
            proportion_within_std_median,
            proportion_within_std_mean,
            unique_prop,
            trimmed_mean,
            mean_abs_dev,
            proportion_values_zero,
            proportion_values_positive,
            p_left,
            piecewise_aggregate_median,
            piecewise_aggregate_mean,
            std_outlier_test,
            mean_outlier_test,
            moments,
            histogram_mode,
            bowley_skewness,
            pearson_skewness,
            improved_burstiness,
            burstiness,
            high_low_mu,
            flat_spots,
            mean_crossing_points,
            median_crossing_points,
            stability,
            lumpiness,
            fisher,
            ans_combe,
            logit,
            relative_differencing,
            differencing,
            box_cox,
            quantize,
            cumsum,
            g_skew,
            anderson_darling,
            percent_amplitude,
            percent_difference_flux_percentile,
            flux_percentile_ratio_mid80,
            flux_percentile_ratio_mid65,
            flux_percentile_ratio_mid50,
            flux_percentile_ratio_mid35,
            flux_percentile_ratio_mid20,
            pair_slope_trend,
            median_buffer_range_percentage,
            median_abs_dev,
            small_kurtosis,
            outlier_segment_count,
            autocor_length,
            mean_variance,
            rate_of_cumulative_sum,
            amplitude,
            ratio_unique_value_number_to_time_series_length,
            sum_of_reoccurring_data_points,
            sum_of_reoccurring_values,
            percentage_of_reoccurring_values_to_all_values,
            percentage_of_reoccurring_datapoints_to_all_datapoints,
            longest_strike_above_mean,
            longest_strike_below_mean,
            large_standard_deviation,
            ratio_beyond_r_sigma,
            first_location_of_minimum,
            first_location_of_maximum,
            last_location_of_minimum,
            last_location_of_maximum,
            variance,
        ]
        for func in functions:
            raised = False
            try:
                op = func(X)
            except Exception as e:
                print(e)
                raised = True
            self.assertFalse(raised, 'Exception raised')

    def test_univariate_execution_with_nan(self):
        X = np.array([1, 2, 3, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, np.nan])
        functions = [
            mean,
            sum_values,
            minimum,
            maximum,
            median,
            std,
            variance,
            count,
            skew,
            kurtosis,
            quantile_25,
            quantile_75,
            quantile_range,
            rate_of_change,
            sum_of_change,
            absoluate_sum_of_changes,
            trend_slop,
            abs_energy,
            mean_abs_change,
            mean_change,
            mean_second_derivative_central,
            count_above_mean,
            count_below_mean,
            corr_coefficient,
            delta_diff,
            past_value,
            fft_coefficient_real,
            fft_coefficient_abs,
            identity,
            wavelet_features,
            z_score,
            count_nan,
            geometric_mean,
            mode_abs_change,
            sum_log_values,
            normalised_count_below_mean,
            normalised_count_above_mean,
            discrete_cosine,
            svd_entropy,
            welch_spectral_entropy,
            fft_spectral_entropy,
            perm_entropy,
            katz_fd,
            petrosian_fd,
            max_langevin_fixed_point,
            fft_aggregated_kurtosis,
            fft_aggregated_skew,
            fft_aggregated_variance,
            fft_aggregated_centroid,
            partial_auto_correlation,
            augmented_dickey_fuller_used_lag,
            augmented_dickey_fuller_p_value,
            augmented_dickey_fuller_teststat,
            friedrich_coefficients,
            index_mass_quantile,
            energy_ratio_by_chunks,
            agg_auto_correlation_std,
            agg_auto_correlation_mean,
            agg_auto_correlation_median,
            agg_auto_correlation_var,
            symmetry_looking,
            ar_coefficient,
            cid_ce,
            c3,
            time_reversal_asymmetry_statistic,
            auto_covariance,
            auto_correlation,
            approximate_entropy,
            has_duplicate,
            has_duplicate_min,
            has_duplicate_max,
            variance_larger_than_standard_deviation,
            mle_uniform,
            mle_gaussian,
            coefficient_variation,
            proportion_within_std_median,
            proportion_within_std_mean,
            unique_prop,
            trimmed_mean,
            mean_abs_dev,
            proportion_values_zero,
            proportion_values_positive,
            p_left,
            piecewise_aggregate_median,
            piecewise_aggregate_mean,
            std_outlier_test,
            mean_outlier_test,
            moments,
            histogram_mode,
            bowley_skewness,
            pearson_skewness,
            improved_burstiness,
            burstiness,
            high_low_mu,
            flat_spots,
            mean_crossing_points,
            median_crossing_points,
            stability,
            lumpiness,
            fisher,
            ans_combe,
            logit,
            relative_differencing,
            differencing,
            box_cox,
            quantize,
            cumsum,
            g_skew,
            anderson_darling,
            percent_amplitude,
            percent_difference_flux_percentile,
            flux_percentile_ratio_mid80,
            flux_percentile_ratio_mid65,
            flux_percentile_ratio_mid50,
            flux_percentile_ratio_mid35,
            flux_percentile_ratio_mid20,
            pair_slope_trend,
            median_buffer_range_percentage,
            median_abs_dev,
            small_kurtosis,
            outlier_segment_count,
            autocor_length,
            mean_variance,
            rate_of_cumulative_sum,
            amplitude,
            ratio_unique_value_number_to_time_series_length,
            sum_of_reoccurring_data_points,
            sum_of_reoccurring_values,
            percentage_of_reoccurring_values_to_all_values,
            percentage_of_reoccurring_datapoints_to_all_datapoints,
            longest_strike_above_mean,
            longest_strike_below_mean,
            large_standard_deviation,
            ratio_beyond_r_sigma,
            first_location_of_minimum,
            first_location_of_maximum,
            last_location_of_minimum,
            last_location_of_maximum,
            variance,
        ]
        for func in functions:
            raised = False
            try:
                op = func(X)
            except Exception as e:
                print(e)
                raised = True
            self.assertFalse(raised, 'Exception raised')

    def test_univariate_execution_with_only_nan(self):
        X = np.array([np.nan])
        functions = [
            mean,
            sum_values,
            minimum,
            maximum,
            median,
            std,
            variance,
            count,
            skew,
            kurtosis,
            quantile_25,
            quantile_75,
            quantile_range,
            rate_of_change,
            sum_of_change,
            absoluate_sum_of_changes,
            trend_slop,
            abs_energy,
            mean_abs_change,
            mean_change,
            mean_second_derivative_central,
            count_above_mean,
            count_below_mean,
            corr_coefficient,
            delta_diff,
            past_value,
            fft_coefficient_real,
            fft_coefficient_abs,
            identity,
            wavelet_features,
            z_score,
            count_nan,
            geometric_mean,
            mode_abs_change,
            sum_log_values,
            normalised_count_below_mean,
            normalised_count_above_mean,
            discrete_cosine,
            svd_entropy,
            welch_spectral_entropy,
            fft_spectral_entropy,
            perm_entropy,
            katz_fd,
            petrosian_fd,
            max_langevin_fixed_point,
            fft_aggregated_kurtosis,
            fft_aggregated_skew,
            fft_aggregated_variance,
            fft_aggregated_centroid,
            #partial_auto_correlation,
            augmented_dickey_fuller_used_lag,
            augmented_dickey_fuller_p_value,
            augmented_dickey_fuller_teststat,
            friedrich_coefficients,
            index_mass_quantile,
            energy_ratio_by_chunks,
            agg_auto_correlation_std,
            agg_auto_correlation_mean,
            agg_auto_correlation_median,
            agg_auto_correlation_var,
            symmetry_looking,
            ar_coefficient,
            cid_ce,
            c3,
            time_reversal_asymmetry_statistic,
            auto_covariance,
            auto_correlation,
            approximate_entropy,
            has_duplicate,
            has_duplicate_min,
            has_duplicate_max,
            variance_larger_than_standard_deviation,
            mle_uniform,
            mle_gaussian,
            coefficient_variation,
            proportion_within_std_median,
            proportion_within_std_mean,
            unique_prop,
            trimmed_mean,
            mean_abs_dev,
            proportion_values_zero,
            proportion_values_positive,
            p_left,
            piecewise_aggregate_median,
            piecewise_aggregate_mean,
            std_outlier_test,
            mean_outlier_test,
            moments,
            histogram_mode,
            bowley_skewness,
            pearson_skewness,
            improved_burstiness,
            burstiness,
            high_low_mu,
            mean_crossing_points,
            median_crossing_points,
            stability,
            lumpiness,
            fisher,
            ans_combe,
            logit,
            relative_differencing,
            differencing,
            box_cox,
            quantize,
            cumsum,
            g_skew,
            anderson_darling,
            percent_amplitude,
            percent_difference_flux_percentile,
            flux_percentile_ratio_mid80,
            flux_percentile_ratio_mid65,
            flux_percentile_ratio_mid50,
            flux_percentile_ratio_mid35,
            flux_percentile_ratio_mid20,
            pair_slope_trend,
            median_buffer_range_percentage,
            median_abs_dev,
            small_kurtosis,
            outlier_segment_count,
            autocor_length,
            mean_variance,
            rate_of_cumulative_sum,
            amplitude,
            ratio_unique_value_number_to_time_series_length,
            sum_of_reoccurring_data_points,
            sum_of_reoccurring_values,
            percentage_of_reoccurring_values_to_all_values,
            percentage_of_reoccurring_datapoints_to_all_datapoints,
            longest_strike_above_mean,
            longest_strike_below_mean,
            large_standard_deviation,
            ratio_beyond_r_sigma,
            first_location_of_minimum,
            first_location_of_maximum,
            last_location_of_minimum,
            last_location_of_maximum,
            variance,
        ]
        for func in functions:
            raised = False
            try:
                op = func(X)
            except:
                raised = True
            self.assertFalse(raised, str(func) + 'Exception raised')

    def test_bivariate_execution(self):
        np.random.seed(0)
        X = np.random.rand(10)
        Y = np.arange(len(X))
        functions = [
            covariance,
            correlation,
            max_slope,
            linear_trend,
            eta_e,
            period_ls,
            period_prob,
            psi_cs,
            psi_eta,
            freq1_harmonics_amplitude_0,
            freq1_harmonics_amplitude_1,
            freq1_harmonics_amplitude_2,
            freq1_harmonics_amplitude_3,
            freq2_harmonics_amplitude_0,
            freq2_harmonics_amplitude_1,
            freq2_harmonics_amplitude_2,
            freq2_harmonics_amplitude_3,
            freq3_harmonics_amplitude_0,
            freq3_harmonics_amplitude_1,
            freq3_harmonics_amplitude_2,
            freq3_harmonics_amplitude_3,
            freq1_harmonics_rel_phase_0,
            freq1_harmonics_rel_phase_1,
            freq1_harmonics_rel_phase_2,
            freq1_harmonics_rel_phase_3,
            freq2_harmonics_rel_phase_0,
            freq2_harmonics_rel_phase_1,
            freq2_harmonics_rel_phase_2,
            freq2_harmonics_rel_phase_3,
            freq3_harmonics_rel_phase_0,
            freq3_harmonics_rel_phase_1,
            freq3_harmonics_rel_phase_2,
            freq3_harmonics_rel_phase_3,
            structure_function_index_21,
            structure_function_index_31,
            structure_function_index_32
        ]

        for func in functions:
            raised = False
            try:
                print(func)
                op = func(X, Y)
            except Exception as e:
                raised = True
            self.assertFalse(raised, 'Exception raised')


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True)
