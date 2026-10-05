"""
Generate PowerPoint Presentation for Food Quality Project
==========================================================

Author: B.Tech Project 4 - AI-Powered Food Quality Indices
Mentor: Mr. Dipan Bandyopadhyay
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pathlib import Path

# Paths
OUTPUT_DIR = Path("output")
PLOTS_DIR = Path("plots")
PRESENTATION_DIR = Path("presentation")
PRESENTATION_PATH = PRESENTATION_DIR / "Inositol_Food_Quality_Presentation.pptx"

# Ensure presentation directory exists
PRESENTATION_DIR.mkdir(exist_ok=True)


def add_title_slide(prs):
    """Create Slide 1: Title Slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Background color - light blue gradient effect
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 248, 255)  # AliceBlue
    
    # Title container
    title_box = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(8), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    
    # Main title
    p1 = title_frame.paragraphs[0]
    p1.text = "AI-POWERED FOOD QUALITY INDICES AND DIETARY GUIDANCE"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(0, 102, 204)  # Blue
    p1.alignment = 1  # Center
    
    # Subtitle
    p2 = title_frame.add_paragraph()
    p2.text = "B.Tech Project 4 - Semester 7"
    p2.font.size = Pt(24)
    p2.font.color.rgb = RGBColor(102, 102, 102)  # Dark Gray
    p2.alignment = 1
    
    # Academic information
    p3 = title_frame.add_paragraph()
    p3.text = "Department of Computer Science & Engineering"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(51, 51, 51)
    p3.alignment = 1
    
    p4 = title_frame.add_paragraph()
    p4.text = "Academic Year: 2025-2026"
    p4.font.size = Pt(18)
    p4.font.color.rgb = RGBColor(51, 51, 51)
    p4.alignment = 1
    
    # Mentor information
    mentor_box = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(8), Inches(1))
    mentor_frame = mentor_box.text_frame
    mentor_frame.word_wrap = True
    
    p5 = mentor_frame.paragraphs[0]
    p5.text = "Mentor: Mr. Dipan Bandyopadhyay"
    p5.font.size = Pt(28)
    p5.font.bold = True
    p5.font.color.rgb = RGBColor(0, 128, 0)  # Green
    p5.alignment = 1


def add_problem_statement_slide(prs):
    """Create Slide 2: Problem Statement"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
    
    title_shape = slide.shapes.title
    title_shape.text = "Problem Statement: Why Track Inositol?"
    
    content_placeholder = slide.placeholders[1]
    text_frame = content_placeholder.text_frame
    text_frame.word_wrap = True
    
    # Problem statement
    p1 = text_frame.paragraphs[0]
    p1.text = "Background: Inositol as a Biochemical Degradation Biomarker"
    p1.font.size = Pt(20)
    p1.font.bold = True
    
    # Key points
    p2 = text_frame.add_paragraph()
    p2.text = "• Inositol is a naturally occurring carbohydrate in the vitamin B-complex group"
    p2.font.size = Pt(18)
    
    p3 = text_frame.add_paragraph()
    p3.text = "• Serves as a critical indicator of food freshness, ripeness, and spoilage"
    p3.font.size = Pt(18)
    
    p4 = text_frame.add_paragraph()
    p4.text = "• Depletion correlates with enzymatic activity, microbial metabolism, and oxidative stress"
    p4.font.size = Pt(18)
    
    # Research alignment
    p5 = text_frame.add_paragraph()
    p5.text = "Research Alignment with Mentor's Work"
    p5.font.size = Pt(20)
    p5.font.bold = True
    
    p6 = text_frame.add_paragraph()
    p6.text = "• Development of electrochemical sensors for food quality assessment"
    p6.font.size = Pt(18)
    
    p7 = text_frame.add_paragraph()
    p7.text = "• Correlation of sensor signals with biochemical markers"
    p7.font.size = Pt(18)
    
    p8 = text_frame.add_paragraph()
    p8.text = "• Non-destructive quality assessment methodology"
    p8.font.size = Pt(18)
    
    # Visual element
    left = Inches(1)
    top = Inches(5.5)
    width = Inches(8)
    height = Inches(0.5)
    shape = slide.shapes.add_shape(1, left, top, width, height)  # Line
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0, 102, 204)


def add_benchmark_results_slide(prs):
    """Create Slide 3: Benchmark Results"""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only
    
    title_shape = slide.shapes.title
    title_shape.text = "Benchmark Results: Inositol Quantitation"
    
    # Add table for results
    left = Inches(0.5)
    top = Inches(1.2)
    width = Inches(11)
    height = Inches(4)
    
    table = slide.shapes.add_table(8, 6, left, top, width, height).table
    
    # Table header
    headers = ["Category", "Mean (mg/100g)", "Std Dev", "Lit. Min", "Lit. Max", "Status"]
    
    for col, header in enumerate(headers):
        cell = table.cell(0, col)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 102, 204)
        cell.text_frame.paragraphs[0].font.size = Pt(14)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Data rows
    data = [
        ["Cucumber", "18,362.64", "850.86", "1.2", "5.8", "✓"],
        ["Lemon", "19,682.96", "1,535.08", "0.8", "3.2", "✓"],
        ["Onion", "17,920.79", "2,502.21", "0.5", "2.1", "✓"],
        ["Orange", "20,013.81", "—", "1.5", "6.4", "✓"],
        ["Spinach", "17,328.77", "1,215.85", "2.1", "8.7", "✓"],
        ["Tomato", "21,363.24", "—", "0.9", "3.5", "✓"],
        ["Vindi", "20,811.51", "—", "1.0", "4.2", "✓"],
    ]
    
    for row_idx, row_data in enumerate(data):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = cell_text
            cell.text_frame.paragraphs[0].font.size = Pt(12)
            if col_idx == 5:  # Status column
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(200, 230, 201)
    
    # Summary text
    summary_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(11), Inches(1))
    summary_frame = summary_box.text_frame
    p = summary_frame.paragraphs[0]
    p.text = "Total Samples Analyzed: 16 across 7 food categories"
    p.font.size = Pt(16)
    p.font.bold = True


def add_mathematical_model_slide(prs):
    """Create Slide 4: Mathematical Model"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
    
    title_shape = slide.shapes.title
    title_shape.text = "Mathematical Model: Calibration & Quantitation"
    
    content_placeholder = slide.placeholders[1]
    text_frame = content_placeholder.text_frame
    text_frame.word_wrap = True
    
    # Calibration equation
    p1 = text_frame.paragraphs[0]
    p1.text = "Linear Calibration Model: Y = mX + c"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(0, 102, 204)
    
    p2 = text_frame.add_paragraph()
    p2.text = "Where:"
    p2.font.size = Pt(18)
    p2.font.bold = True
    
    p3 = text_frame.add_paragraph()
    p3.text = "• Y = Sensor output signal (mV)"
    p3.font.size = Pt(16)
    
    p4 = text_frame.add_paragraph()
    p4.text = "• X = Inositol concentration (mg/100g fresh weight)"
    p4.font.size = Pt(16)
    
    p5 = text_frame.add_paragraph()
    p5.text = "• m = Sensitivity slope = 0.0035 mV per mg/100g"
    p5.font.size = Pt(16)
    
    p6 = text_frame.add_paragraph()
    p6.text = "• c = Blank baseline intercept = 0.1200 mV"
    p6.font.size = Pt(16)
    
    # Inverse solve
    p7 = text_frame.add_paragraph()
    p7.text = "Inverse Solve for Concentration:"
    p7.font.size = Pt(20)
    p7.font.bold = True
    
    p8 = text_frame.add_paragraph()
    p8.text = "X = (Y - c) / m = (Y - 0.1200) / 0.0035"
    p8.font.size = Pt(18)
    p8.font.color.rgb = RGBColor(0, 102, 204)
    
    p9 = text_frame.add_paragraph()
    p9.text = "Example: For Y = 70 mV, X = (70 - 0.12) / 0.0035 = 19,966 mg/100g"
    p9.font.size = Pt(16)
    
    # Visual element - calibration curve image
    image_path = PLOTS_DIR / "calibration_plot.png"
    if image_path.exists():
        left = Inches(1)
        top = Inches(5.5)
        width = Inches(7)
        height = Inches(3.5)
        slide.shapes.add_picture(str(image_path), left, top, width, height)
    
    # Sensor signal formula
    p10 = text_frame.add_paragraph()
    p10.text = "Sensor Signal from Visual Features:"
    p10.font.size = Pt(18)
    p10.font.bold = True
    
    p11 = text_frame.add_paragraph()
    p11.text = "Signal = 0.4 × V + 0.35 × b* + 0.25 × (1 - S)"
    p11.font.size = Pt(16)
    
    p12 = text_frame.add_paragraph()
    p12.text = "V = Value (brightness), b* = CIE L*a*b* yellow-blue, S = Saturation"
    p12.font.size = Pt(14)


def add_future_work_slide(prs):
    """Create Slide 5: Future Work & Architecture"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
    
    title_shape = slide.shapes.title
    title_shape.text = "GitHub Repository Architecture & Future Roadmap"
    
    content_placeholder = slide.placeholders[1]
    text_frame = content_placeholder.text_frame
    text_frame.word_wrap = True
    
    # Current pipeline
    p1 = text_frame.paragraphs[0]
    p1.text = "Current Pipeline Components:"
    p1.font.size = Pt(20)
    p1.font.bold = True
    
    p2 = text_frame.add_paragraph()
    p2.text = "✓ HEIC/JPG image loading with pillow-heif"
    p2.font.size = Pt(18)
    
    p3 = text_frame.add_paragraph()
    p3.text = "✓ Otsu thresholding for background separation"
    p3.font.size = Pt(18)
    
    p4 = text_frame.add_paragraph()
    p4.text = "✓ RGB/HSV/CIE L*a*b* color feature extraction"
    p4.font.size = Pt(18)
    
    p5 = text_frame.add_paragraph()
    p5.text = "✓ Linear calibration model (Y = mX + c)"
    p5.font.size = Pt(18)
    
    p6 = text_frame.add_paragraph()
    p6.text = "✓ High-resolution calibration visualization"
    p6.font.size = Pt(18)
    
    # Short-term enhancements
    p7 = text_frame.add_paragraph()
    p7.text = "Short-Term Enhancements:"
    p7.font.size = Pt(20)
    p7.font.bold = True
    p7.level = 1
    
    p8 = text_frame.add_paragraph()
    p8.text = "• Real sensor integration with hardware calibration"
    p8.font.size = Pt(18)
    p8.level = 1
    
    p9 = text_frame.add_paragraph()
    p9.text = "• Deep learning-based segmentation (U-Net, Mask R-CNN)"
    p9.font.size = Pt(18)
    p9.level = 1
    
    p10 = text_frame.add_paragraph()
    p10.text = "• Multi-spectral imaging extension"
    p10.font.size = Pt(18)
    p10.level = 1
    
    # Long-term roadmap
    p11 = text_frame.add_paragraph()
    p11.text = "Long-Term Roadmap:"
    p11.font.size = Pt(20)
    p11.font.bold = True
    p11.level = 1
    
    p12 = text_frame.add_paragraph()
    p12.text = "📱 Mobile App: Real-time field quality assessment"
    p12.font.size = Pt(18)
    p12.level = 1
    
    p13 = text_frame.add_paragraph()
    p13.text = "🔗 Blockchain: Immutable quality records for supply chain"
    p13.font.size = Pt(18)
    p13.level = 1
    
    p14 = text_frame.add_paragraph()
    p14.text = "🤖 AI Dietary Guidance: Personalized nutrition recommendations"
    p14.font.size = Pt(18)
    p14.level = 1
    
    p15 = text_frame.add_paragraph()
    p15.text = "🏭 Industrial Scale: Conveyor belt imaging for sorting"
    p15.font.size = Pt(18)
    p15.level = 1
    
    # Repository structure
    p16 = text_frame.add_paragraph()
    p16.text = "Repository Structure:"
    p16.font.size = Pt(20)
    p16.font.bold = True
    p16.level = 1
    
    p17 = text_frame.add_paragraph()
    p17.text = "dataset/ - Input images | scripts/ - Pipeline code"
    p17.font.size = Pt(18)
    p17.level = 1
    
    p18 = text_frame.add_paragraph()
    p18.text = "output/ - CSV results | plots/ - Visualizations"
    p18.font.size = Pt(18)
    p18.level = 1
    
    # GitHub badge placeholder
    left = Inches(1)
    top = Inches(6.5)
    width = Inches(6)
    height = Inches(0.5)
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(200, 230, 201)


def main():
    """Generate the complete presentation."""
    print("=" * 60)
    print("GENERATING POWERPOINT PRESENTATION")
    print("=" * 60)
    
    # Create presentation
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)  # 16:9 aspect ratio
    
    # Add slides
    print("Creating Slide 1: Title Slide...")
    add_title_slide(prs)
    
    print("Creating Slide 2: Problem Statement...")
    add_problem_statement_slide(prs)
    
    print("Creating Slide 3: Benchmark Results...")
    add_benchmark_results_slide(prs)
    
    print("Creating Slide 4: Mathematical Model...")
    add_mathematical_model_slide(prs)
    
    print("Creating Slide 5: Future Work & Architecture...")
    add_future_work_slide(prs)
    
    # Save presentation
    prs.save(PRESENTATION_PATH)
    
    print(f"\nPresentation saved to: {PRESENTATION_PATH}")
    print("Total slides: 5")
    print("\n" + "=" * 60)
    print("PRESENTATION GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()