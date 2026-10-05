"""
Food Quality Feature Extraction Pipeline
=========================================
Extracts color and spectral features from food images for inositol quantitation analysis.

Author: B.Tech Project 4 - AI-Powered Food Quality Indices
Mentor: Mr. Dipan Bandyopadhyay
"""

import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from pillow_heif import register_heif_opener
import matplotlib.pyplot as plt
from pathlib import Path

# Register HEIF opener for PIL
register_heif_opener()

# Constants
OUTPUT_SIZE = (500, 500)
DATASET_DIR = Path("dataset")
OUTPUT_DIR = Path("output")
PLOTS_DIR = Path("plots")


def load_image(image_path):
    """Load image from path, handling HEIC and other formats."""
    try:
        # Try PIL first (handles HEIC via pillow-heif)
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return np.array(img)
    except Exception as e:
        print(f"Warning: PIL failed for {image_path}: {e}")
        # Fallback to OpenCV
        img = cv2.imread(str(image_path))
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img


def preprocess_image(image, target_size=OUTPUT_SIZE):
    """Resize image to standard dimensions."""
    if image is None:
        return None
    resized = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
    return resized


def create_food_mask(image):
    """
    Create a binary mask to isolate food from white background using Otsu thresholding.
    Uses luminance-based thresholding for white background separation.
    """
    if image is None:
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Otsu's thresholding for background separation
    # Since background is white, we invert to get the food items
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
    
    return cleaned


def extract_color_features(image, mask=None):
    """
    Extract comprehensive color features from food image.
    Returns: RGB, HSV, and CIE L*a*b* color space features.
    """
    if image is None:
        return None
    
    features = {}
    
    # Apply mask if provided (isolate food only)
    if mask is not None:
        # Create 3-channel mask for color images
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        food_only = cv2.bitwise_and(image, mask_3ch)
    else:
        food_only = image.copy()
    
    # Get non-zero pixels for feature calculation
    if mask is not None:
        non_zero_mask = mask > 0
        if not np.any(non_zero_mask):
            # No food detected, use full image
            food_pixels = image.reshape(-1, 3)
        else:
            food_pixels = food_only[non_zero_mask]
    else:
        food_pixels = image.reshape(-1, 3)
    
    if len(food_pixels) == 0:
        return None
    
    # RGB features
    rgb_mean = np.mean(food_pixels, axis=0)
    rgb_std = np.std(food_pixels, axis=0)
    
    features.update({
        'r_mean': rgb_mean[0], 'r_std': rgb_std[0],
        'g_mean': rgb_mean[1], 'g_std': rgb_std[1],
        'b_mean': rgb_mean[2], 'b_std': rgb_std[2],
    })
    
    # Convert to HSV and extract features
    hsv = cv2.cvtColor(food_only.astype(np.uint8), cv2.COLOR_RGB2HSV)
    if mask is not None:
        hsv_pixels = hsv[non_zero_mask] if np.any(non_zero_mask) else hsv.reshape(-1, 3)
    else:
        hsv_pixels = hsv.reshape(-1, 3)
    
    hsv_mean = np.mean(hsv_pixels, axis=0)
    hsv_std = np.std(hsv_pixels, axis=0)
    
    # Hue is in [0, 179] range in OpenCV, normalize to [0, 360]
    features.update({
        'h_mean': (hsv_mean[0] / 179.0) * 360, 'h_std': (hsv_std[0] / 179.0) * 360,
        's_mean': hsv_mean[1], 's_std': hsv_std[1],
        'v_mean': hsv_mean[2], 'v_std': hsv_std[2],
    })
    
    # Convert to CIE L*a*b* and extract features
    lab = cv2.cvtColor(food_only.astype(np.uint8), cv2.COLOR_RGB2LAB)
    if mask is not None:
        lab_pixels = lab[non_zero_mask] if np.any(non_zero_mask) else lab.reshape(-1, 3)
    else:
        lab_pixels = lab.reshape(-1, 3)
    
    lab_mean = np.mean(lab_pixels, axis=0)
    lab_std = np.std(lab_pixels, axis=0)
    
    features.update({
        'l_mean': lab_mean[0], 'l_std': lab_std[0],
        'a_mean': lab_mean[1], 'a_std': lab_std[1],
        'b_mean': lab_mean[2], 'b_std': lab_std[2],
    })
    
    # Additional features: Color ratios and intensity metrics
    features['rgb_sum'] = np.sum(food_pixels)
    features['pixel_count'] = len(food_pixels)
    
    return features


def process_food_category(category_dir):
    """Process all images in a food category directory."""
    category_name = category_dir.name
    print(f"Processing category: {category_name}")
    
    all_features = []
    
    # Process all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.bmp', '.tiff']
    
    for image_path in category_dir.iterdir():
        if image_path.suffix.lower() not in image_extensions:
            continue
        
        print(f"  Processing: {image_path.name}")
        
        try:
            # Load image
            image = load_image(image_path)
            if image is None:
                print(f"    Warning: Could not load {image_path}")
                continue
            
            # Preprocess
            preprocessed = preprocess_image(image)
            
            # Create mask
            mask = create_food_mask(preprocessed)
            if mask is None:
                print(f"    Warning: Could not create mask for {image_path}")
                continue
            
            # Extract features
            features = extract_color_features(preprocessed, mask)
            if features is None:
                print(f"    Warning: Could not extract features for {image_path}")
                continue
            
            # Add metadata
            features['category'] = category_name
            features['filename'] = image_path.name
            features['file_path'] = str(image_path)
            
            all_features.append(features)
            
        except Exception as e:
            print(f"    Error processing {image_path}: {e}")
            continue
    
    return all_features


def visualize_sample_images(dataset_dir, output_dir):
    """Create sample visualization of processing pipeline."""
    sample_count = 0
    max_samples = 5
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for category_dir in dataset_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        for image_path in category_dir.iterdir():
            if not image_path.is_file():
                continue
            
            try:
                image = load_image(image_path)
                if image is None:
                    continue
                
                preprocessed = preprocess_image(image)
                mask = create_food_mask(preprocessed)
                
                # Apply mask
                mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
                masked = cv2.bitwise_and(preprocessed, mask_3ch)
                
                # Plot
                idx = sample_count % 6
                
                axes[idx].imshow(preprocessed)
                axes[idx].set_title(f'{category_dir.name}\n(Original)')
                axes[idx].axis('off')
                
                if sample_count < 6:
                    axes[idx + 3].imshow(masked)
                    axes[idx + 3].set_title(f'{category_dir.name}\n(Food Isolated)')
                    axes[idx + 3].axis('off')
                
                sample_count += 1
                
                if sample_count >= max_samples * 6:
                    break
                    
            except:
                continue
        
        if sample_count >= max_samples * 6:
            break
    
    plt.tight_layout()
    plt.savefig(output_dir / 'processing_samples.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Sample visualization saved to: {output_dir / 'processing_samples.png'}")


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("FOOD QUALITY FEATURE EXTRACTION PIPELINE")
    print("=" * 60)
    
    # Ensure output directories exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)
    
    # Process all food categories
    all_data = []
    
    for category_dir in sorted(DATASET_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        
        category_data = process_food_category(category_dir)
        all_data.extend(category_data)
    
    # Create DataFrame
    if not all_data:
        print("No data extracted! Check dataset directory.")
        return
    
    df = pd.DataFrame(all_data)
    
    # Save features to CSV
    output_csv = OUTPUT_DIR / 'extracted_features.csv'
    df.to_csv(output_csv, index=False)
    print(f"\nFeatures saved to: {output_csv}")
    print(f"Total samples processed: {len(df)}")
    print(f"Categories: {df['category'].unique().tolist()}")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("FEATURE SUMMARY BY CATEGORY")
    print("=" * 60)
    
    for category in df['category'].unique():
        cat_df = df[df['category'] == category]
        print(f"\n{category.upper()}:")
        print(f"  Samples: {len(cat_df)}")
        print(f"  Mean RGB: [{cat_df['r_mean'].mean():.1f}, {cat_df['g_mean'].mean():.1f}, {cat_df['b_mean'].mean():.1f}]")
        print(f"  Mean HSV: [{cat_df['h_mean'].mean():.1f}°, {cat_df['s_mean'].mean():.1f}, {cat_df['v_mean'].mean():.1f}]")
        print(f"  Mean L*a*b*: [{cat_df['l_mean'].mean():.1f}, {cat_df['a_mean'].mean():.1f}, {cat_df['b_mean'].mean():.1f}]")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    
    # Color feature distributions
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # RGB mean plot
    colors_rgb = ['red', 'green', 'blue']
    for i, (ax, channel) in enumerate(zip(axes[0], ['r_mean', 'g_mean', 'b_mean'])):
        for category in df['category'].unique():
            cat_df = df[df['category'] == category]
            ax.bar(category, cat_df[channel].mean(), color=colors_rgb[i], alpha=0.7, label=category)
        ax.set_ylabel(f'{channel.upper()} Mean')
        ax.set_title(f'Mean {channel.upper()} by Category')
        ax.tick_params(axis='x', rotation=45)
    
    # HSV mean plot
    for i, (ax, channel) in enumerate(zip(axes[1], ['h_mean', 's_mean', 'v_mean'])):
        for category in df['category'].unique():
            cat_df = df[df['category'] == category]
            ax.bar(category, cat_df[channel].mean(), color='orange', alpha=0.7, label=category)
        ax.set_ylabel(f'{channel.upper()} Mean')
        ax.set_title(f'Mean {channel.upper()} by Category')
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'color_features.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Color features plot saved to: {PLOTS_DIR / 'color_features.png'}")
    
    # Create sample visualizations
    visualize_sample_images(DATASET_DIR, PLOTS_DIR)
    
    print("\n" + "=" * 60)
    print("FEATURE EXTRACTION COMPLETE")
    print("=" * 60)
    
    return df


if __name__ == "__main__":
    main()