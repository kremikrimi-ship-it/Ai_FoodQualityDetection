"""
Inositol Quantitation Calculation Pipeline
===========================================
Calculates inositol concentrations from optical sensor measurements
using calibration curve Y = mX + c.

Author: B.Tech Project 4 - AI-Powered Food Quality Indices
Mentor: Mr. Dipan Bandyopadhyay
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Constants - Calibration parameters from mentor's sensor model
SENSITIVITY_SLOPE = 0.0035  # mV per mg/100g (slope)
BLANK_INTERCEPT = 0.1200     # mV (blank baseline offset)

# Literature reference ranges for inositol in fresh produce (mg/100g)
LITERATURE_RANGES = {
    'cucumber': {'min': 1.2, 'max': 5.8, 'mean': 3.5},
    'lemon': {'min': 0.8, 'max': 3.2, 'mean': 2.0},
    'onion': {'min': 0.5, 'max': 2.1, 'mean': 1.3},
    'orange': {'min': 1.5, 'max': 6.4, 'mean': 4.0},
    'spinach': {'min': 2.1, 'max': 8.7, 'mean': 5.4},
    'tomato': {'min': 0.9, 'max': 3.5, 'mean': 2.2},
    'vindi': {'min': 1.0, 'max': 4.2, 'mean': 2.6}  # Bottle gourd
}

OUTPUT_DIR = Path("output")
PLOTS_DIR = Path("plots")


def calculate_inositol(sensor_signal_mV):
    """
    Calculate inositol concentration from sensor signal.
    
    Calibration model: Y = m * X + c
    Where:
        Y = Sensor output signal (mV)
        m = 0.0035 (sensitivity slope)
        c = 0.1200 (blank baseline intercept)
        X = Inositol concentration (mg/100g)
    
    Inverse solve for X:
        X = (Y - c) / m
    
    Args:
        sensor_signal_mV: Measured sensor signal in millivolts
    
    Returns:
        Inositol concentration in mg/100g fresh weight
    """
    if sensor_signal_mV <= BLANK_INTERCEPT:
        return 0.0  # Below detection threshold
    
    inositol_mg_per_100g = (sensor_signal_mV - BLANK_INTERCEPT) / SENSITIVITY_SLOPE
    return max(0.0, inositol_mg_per_100g)


def compute_sensor_signal_from_features(features_df):
    """
    Compute simulated sensor signal from extracted color features.
    
    This uses a weighted combination of color metrics that correlate
    with inositol concentration in fresh produce.
    
    Signal model: Signal = w1*V + w2*b* + w3*(1-S) + w4*std
    Where V is Value (HSV), b* is yellow-blue (CIE), S is Saturation
    """
    signals = []
    
    for _, row in features_df.iterrows():
        # Compute combined signal from multiple color metrics
        # Higher inositol correlates with:
        # - Higher Value (brightness) inHSV
        # - Higher b* (yellow component) in CIE Lab
        # - Lower Saturation (more muted colors)
        
        signal_v = row['v_mean'] / 255.0 * 100  # Normalize to 0-100 range
        signal_b = (row['b_mean'] + 128) / 256.0 * 100  # Normalize CIE b* range
        signal_s = (255 - row['s_mean']) / 255.0 * 100  # Inverted saturation
        
        # Weighted combination (empirical weights)
        weighted_signal = (
            0.4 * signal_v +
            0.35 * signal_b +
            0.25 * signal_s
        )
        
        # Add small noise for variation (simulates real sensor variability)
        noise = np.random.normal(0, 0.5)
        final_signal = weighted_signal + noise
        
        signals.append(final_signal)
    
    return signals


def generate_calibration_plot(df, output_path):
    """
    Generate high-resolution calibration curve plot.
    
    Plots the linear regression line Y = mX + c against the actual
    food sample data points.
    """
    # Prepare data
    sensor_signals = df['sensor_signal_mV'].values
    inositol_values = df['inositol_mg_per_100g'].values
    
    # Generate regression line points
    x_range = np.linspace(0, max(inositol_values) * 1.1, 100)
    y_range = SENSITIVITY_SLOPE * x_range + BLANK_INTERCEPT
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot calibration line
    ax.plot(x_range, y_range, 'b-', linewidth=2, 
            label=f'Calibration Curve: Y = {SENSITIVITY_SLOPE}X + {BLANK_INTERCEPT}')
    
    # Plot food sample points with category colors
    categories = df['category'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
    
    for i, category in enumerate(categories):
        cat_df = df[df['category'] == category]
        ax.scatter(cat_df['inositol_mg_per_100g'], cat_df['sensor_signal_mV'],
                  color=colors[i], s=150, alpha=0.7, edgecolors='darkred',
                  linewidth=1.5, label=category.capitalize())
    
    # Add literature ranges as shaded bands
    for _, row in df.iterrows():
        category = row['category']
        if category in LITERATURE_RANGES:
            lit_range = LITERATURE_RANGES[category]
            y_min = SENSITIVITY_SLOPE * lit_range['min'] + BLANK_INTERCEPT
            y_max = SENSITIVITY_SLOPE * lit_range['max'] + BLANK_INTERCEPT
            ax.axhspan(y_min, y_max, alpha=0.1, color=colors[
                np.where(categories == category)[0][0]])
    
    # Formatting
    ax.set_xlabel('Inositol Concentration (mg / 100g fresh weight)', fontsize=12)
    ax.set_ylabel('Sensor Signal (mV)', fontsize=12)
    ax.set_title('Inositol Calibration Curve for Fresh Produce\n' +
                f'Sensor Model: Y = {SENSITIVITY_SLOPE}X + {BLANK_INTERCEPT}', 
                fontsize=14, fontweight='bold')
    
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0), fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Add R² annotation
    correlation = np.corrcoef(inositol_values, sensor_signals)[0, 1]
    ax.text(0.05, 0.95, f'Correlation: {correlation:.4f}', 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Calibration plot saved to: {output_path}")
    return fig


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("INOSITOL QUANTITATION CALCULATION PIPELINE")
    print("=" * 60)
    
    # Ensure output directories exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)
    
    # Load extracted features
    features_path = OUTPUT_DIR / 'extracted_features.csv'
    
    if not features_path.exists():
        print(f"Error: Features file not found at {features_path}")
        print("Please run extract_features.py first.")
        return None
    
    df_features = pd.read_csv(features_path)
    print(f"Loaded {len(df_features)} samples from {features_path}")
    
    # Compute sensor signals from color features
    print("\nComputing sensor signals from color features...")
    sensor_signals = compute_sensor_signal_from_features(df_features)
    df_features['sensor_signal_mV'] = sensor_signals
    
    # Calculate inositol concentrations
    print("Calculating inositol concentrations...")
    df_features['inositol_mg_per_100g'] = df_features['sensor_signal_mV'].apply(
        calculate_inositol
    )
    
    # Add literature comparison
    def get_literature_info(category):
        if category in LITERATURE_RANGES:
            lit = LITERATURE_RANGES[category]
            return pd.Series([lit['min'], lit['max'], lit['mean'], 
                            lit['min'] <= df_features['inositol_mg_per_100g'].mean() <= lit['max']],
                          index=['lit_min', 'lit_max', 'lit_mean', 'within_lit_range'])
        return pd.Series([np.nan, np.nan, np.nan, False],
                        index=['lit_min', 'lit_max', 'lit_mean', 'within_lit_range'])
    
    df_features['lit_min'] = df_features['category'].apply(
        lambda x: LITERATURE_RANGES.get(x, {}).get('min', np.nan)
    )
    df_features['lit_max'] = df_features['category'].apply(
        lambda x: LITERATURE_RANGES.get(x, {}).get('max', np.nan)
    )
    
    # Generate final output table
    output_columns = [
        'category', 'filename', 'sensor_signal_mV', 'inositol_mg_per_100g',
        'lit_min', 'lit_max', 'r_mean', 'g_mean', 'b_mean',
        'h_mean', 's_mean', 'v_mean', 'l_mean', 'a_mean', 'b_mean'
    ]
    
    df_final = df_features[output_columns].copy()
    df_final.columns = [
        'Category', 'Filename', 'Sensor_Signal_mV', 'Inositol_mg_per_100g',
        'Literature_Min', 'Literature_Max', 'R_Mean', 'G_Mean', 'B_Mean',
        'Hue_Mean', 'Saturation_Mean', 'Value_Mean', 'L_Mean', 'a_Mean', 'b_Mean'
    ]
    
    # Save final CSV
    output_csv = OUTPUT_DIR / 'final_inositol_quantitation.csv'
    df_final.to_csv(output_csv, index=False)
    print(f"\nFinal results saved to: {output_csv}")
    
    # Generate calibration plot
    calibration_plot_path = PLOTS_DIR / 'calibration_plot.png'
    generate_calibration_plot(df_features, calibration_plot_path)
    
    # Print summary table
    print("\n" + "=" * 60)
    print("INOSITOL QUANTITATION RESULTS")
    print("=" * 60)
    
    summary_df = df_final.groupby('Category').agg({
        'Inositol_mg_per_100g': ['mean', 'std', 'min', 'max'],
        'Sensor_Signal_mV': ['mean', 'std']
    }).round(3)
    
    print("\nSummary by Category:")
    print(summary_df.to_string())
    
    # Overall statistics
    print("\n" + "-" * 60)
    print("OVERALL STATISTICS")
    print("-" * 60)
    print(f"Total Samples: {len(df_final)}")
    print(f"Mean Inositol: {df_final['Inositol_mg_per_100g'].mean():.3f} mg/100g")
    print(f"Std Deviation: {df_final['Inositol_mg_per_100g'].std():.3f} mg/100g")
    print(f"Min Inositol: {df_final['Inositol_mg_per_100g'].min():.3f} mg/100g")
    print(f"Max Inositol: {df_final['Inositol_mg_per_100g'].max():.3f} mg/100g")
    
    # Detailed sample table
    print("\n" + "-" * 60)
    print("DETAILED SAMPLE RESULTS")
    print("-" * 60)
    print(df_final.to_string(index=False))
    
    # Calibration model info
    print("\n" + "=" * 60)
    print("CALIBRATION MODEL")
    print("=" * 60)
    print(f"Linear Equation: Y = mX + c")
    print(f"  Slope (m):  {SENSITIVITY_SLOPE:.6f} mV per mg/100g")
    print(f"  Intercept (c): {BLANK_INTERCEPT:.6f} mV (blank baseline)")
    print(f"\nInverse solve for concentration:")
    print(f"  X = (Y - c) / m")
    print(f"  X = (Sensor_Signal - 0.1200) / 0.0035")
    
    print("\n" + "=" * 60)
    print("INOSITOL QUANTITATION COMPLETE")
    print("=" * 60)
    
    return df_final


if __name__ == "__main__":
    main()