import os
import sys
from dotenv import load_dotenv
load_dotenv()

# ── TEST 1: GROQ TEXT GENERATION ──────────────────────────────
def test_story_generation():
    print("\n" + "="*50)
    print("TEST 1: Story Generation (Groq via HuggingFace)")
    print("="*50)
    
    try:
        from services.ai_text import generate_story
        
        print("Generating story... please wait (5-10 seconds)...")
        story = generate_story(
            name="Timmy",
            age=6,
            gender="Boy",
            moral="Kindness"
        )
        
        # Check all required fields
        assert "title" in story, "Missing title!"
        assert "pages" in story, "Missing pages!"
        assert len(story["pages"]) == 5, f"Expected 5 pages, got {len(story['pages'])}"
        assert "edu_sheet" in story, "Missing edu_sheet!"
        
        # Check story quality
        page1_text = story["pages"][0]["text"]
        assert len(page1_text) > 100, f"Page 1 text too short: {len(page1_text)} chars"
        
        print(f"\n✅ Story title   : {story['title']}")
        print(f"✅ Pages         : {len(story['pages'])}")
        print(f"✅ Page 1 length : {len(page1_text)} characters")
        print(f"\n--- Page 1 Preview ---")
        print(page1_text[:200] + "...")
        print(f"\n✅ Vocab words:")
        for v in story["edu_sheet"]["vocab"]:
            print(f"   - {v}")
        print(f"\n✅ Discussion questions:")
        for q in story["edu_sheet"]["discussion"]:
            print(f"   - {q}")
        print("\n✅ STORY GENERATION TEST PASSED!")
        
        return story
        
    except Exception as e:
        print(f"❌ STORY GENERATION FAILED: {str(e)}")
        return None


# ── TEST 2: IMAGE GENERATION ──────────────────────────────────
def test_image_generation(photo_path=None):
    print("\n" + "="*50)
    print("TEST 2: Image Generation (Replicate via HuggingFace)")
    print("="*50)
    
    try:
        from services.ai_image import generate_images
        
        test_prompts = [
            "A cheerful boy named Timmy sitting in a sunny garden, "
            "smiling and handing a flower to an elderly neighbor, "
            "warm afternoon light, colorful flowers around"
        ]
        
        if photo_path:
            print(f"Using face reference: {photo_path}")
        else:
            print("No face photo provided - generating without reference")
            
        print("Generating 1 test image... please wait (30-60 seconds)...")
        image_urls = generate_images(test_prompts, face_photo_path=photo_path)
        
        assert len(image_urls) == 1, "Expected 1 image result"
        assert image_urls[0] is not None, "Image generation returned None!"
        assert os.path.exists(image_urls[0]), f"Image file not found!"
        
        # Check image is valid and has content
        from PIL import Image
        img = Image.open(image_urls[0])
        assert img.size[0] > 0, "Image width is 0!"
        assert img.size[1] > 0, "Image height is 0!"
        
        print(f"\n✅ Image saved at : {image_urls[0]}")
        print(f"✅ Image size     : {img.size[0]}x{img.size[1]} pixels")
        print(f"✅ Image mode     : {img.mode}")
        print("\n✅ IMAGE GENERATION TEST PASSED!")
        print("👉 Open temp_image_1.png to check the cartoon quality!")
        
        return image_urls
        
    except Exception as e:
        print(f"❌ IMAGE GENERATION FAILED: {str(e)}")
        return None


# ── TEST 3: PDF GENERATION ────────────────────────────────────
def test_pdf_generation(story, image_urls):
    print("\n" + "="*50)
    print("TEST 3: PDF Generation")
    print("="*50)
    
    try:
        from services.pdf_maker import (
            create_full_pdf,
            create_coloring_pdf,
            create_edu_pdf
        )

        # Add child info to story_data for PDF cover
        story["child_name"] = "Timmy"
        story["moral"] = "Kindness"

        # ── Full PDF ──
        print("Creating full storybook PDF...")
        pdf_bytes = create_full_pdf(story, image_urls)
        assert len(pdf_bytes) > 0, "Full PDF is empty!"
        with open("test_full_storybook.pdf", "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ Full PDF      : test_full_storybook.pdf ({len(pdf_bytes):,} bytes)")

        # ── Coloring PDF ──
        print("Creating coloring pages PDF...")
        coloring_bytes = create_coloring_pdf(image_urls)
        assert len(coloring_bytes) > 0, "Coloring PDF is empty!"
        with open("test_coloring.pdf", "wb") as f:
            f.write(coloring_bytes)
        print(f"✅ Coloring PDF  : test_coloring.pdf ({len(coloring_bytes):,} bytes)")

        # ── Edu Sheet PDF ──
        print("Creating teacher edu sheet PDF...")
        edu_bytes = create_edu_pdf(story)
        assert len(edu_bytes) > 0, "Edu PDF is empty!"
        with open("test_edu_sheet.pdf", "wb") as f:
            f.write(edu_bytes)
        print(f"✅ Edu Sheet PDF : test_edu_sheet.pdf ({len(edu_bytes):,} bytes)")

        print("\n✅ PDF GENERATION TEST PASSED!")
        print("👉 Open the PDF files to check the quality!")
        
    except Exception as e:
        print(f"❌ PDF GENERATION FAILED: {str(e)}")


# ── TEST 4: MONGODB ───────────────────────────────────────────
def test_mongodb(story=None, image_urls=None):
    print("\n" + "="*50)
    print("TEST 4: MongoDB Connection + Story Save")
    print("="*50)
    
    try:
        from services.db import get_db, save_story, get_user_stories
        
        # Test connection
        db = get_db()
        assert db is not None, "DB returned None!"
        print("✅ MongoDB connected!")

        # Test write and read
        db.test.insert_one({"test": "herogen_test"})
        result = db.test.find_one({"test": "herogen_test"})
        assert result is not None, "Could not read back from MongoDB!"
        db.test.delete_one({"test": "herogen_test"})
        print("✅ Write and read test passed!")

        # Test saving a real story if available
        if story and image_urls:
            story_id = save_story(
                user_id="test_user",
                child_name="Timmy",
                age=6,
                moral="Kindness",
                story_data=story,
                image_urls=image_urls
            )
            assert story_id is not None, "Story save returned None!"
            print(f"✅ Story saved with ID: {story_id}")

            # Test retrieving stories
            stories = get_user_stories("test_user")
            assert len(stories) > 0, "No stories found after saving!"
            print(f"✅ Retrieved {len(stories)} story/stories for test_user")

        print("\n✅ MONGODB TEST PASSED!")
        
    except Exception as e:
        print(f"❌ MONGODB FAILED: {str(e)}")


# ── RUN ALL TESTS ─────────────────────────────────────────────
if __name__ == "__main__":
    
    # Get photo path from command line argument if provided
    # Usage: python test_apis.py photo.jpg
    photo_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if photo_path and not os.path.exists(photo_path):
        print(f"⚠️ Photo not found: {photo_path}")
        photo_path = None

    print("\n🚀 HEROGEN API TESTS STARTING...")
    if photo_path:
        print(f"📸 Using face photo: {photo_path}")
    else:
        print("📸 No face photo — running without face reference")
    
    # Test 1 - Story generation
    story = test_story_generation()
    
    # Test 2 - Image generation
    image_urls = None
    if story:
        image_urls = test_image_generation(photo_path)
    
    # Test 3 - PDF generation
    if story and image_urls:
        test_pdf_generation(story, image_urls)
    
    # Test 4 - MongoDB
    test_mongodb(story, image_urls)
    
    print("\n" + "="*50)
    print("ALL TESTS COMPLETE!")
    print("="*50)
    print("\n📁 Check these output files:")
    print("   - temp_image_1.png        (cartoon illustration)")
    print("   - test_full_storybook.pdf (complete storybook)")
    print("   - test_coloring.pdf       (coloring pages)")
    print("   - test_edu_sheet.pdf      (teacher guide)")