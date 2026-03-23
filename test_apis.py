import os
from dotenv import load_dotenv
load_dotenv()

# ── TEST 1: GROQ TEXT GENERATION ──────────────────────────────
def test_story_generation():
    print("\n" + "="*50)
    print("TEST 1: Story Generation (Groq via HuggingFace)")
    print("="*50)
    
    try:
        from services.ai_text import generate_story
        
        print("Generating story... please wait...")
        story = generate_story(
            name="Timmy",
            age=6,
            gender="Boy",
            moral="Kindness"
        )
        
        # Check all required fields exist
        assert "title" in story, "Missing title!"
        assert "pages" in story, "Missing pages!"
        assert len(story["pages"]) == 5, f"Expected 5 pages, got {len(story['pages'])}"
        assert "edu_sheet" in story, "Missing edu_sheet!"
        
        print(f"✅ Story title: {story['title']}")
        print(f"✅ Pages generated: {len(story['pages'])}")
        print(f"✅ Page 1 text: {story['pages'][0]['text'][:80]}...")
        print(f"✅ Vocab words: {story['edu_sheet']['vocab']}")
        print("✅ STORY GENERATION TEST PASSED!")
        
        return story
        
    except Exception as e:
        print(f"❌ STORY GENERATION FAILED: {str(e)}")
        return None


# ── TEST 2: IMAGE GENERATION ──────────────────────────────────
def test_image_generation():
    print("\n" + "="*50)
    print("TEST 2: Image Generation (Replicate via HuggingFace)")
    print("="*50)
    
    try:
        from services.ai_image import generate_images
        
        # Only test 1 image to save time and credits
        test_prompts = [
            "A friendly boy named Timmy sitting in a sunny garden, smiling"
        ]
        
        print("Generating 1 test image... please wait (30-60 seconds)...")
        image_urls = generate_images(test_prompts)
        
        assert len(image_urls) == 1, "Expected 1 image result"
        assert image_urls[0] is not None, "Image generation returned None!"
        assert os.path.exists(image_urls[0]), f"Image file not found: {image_urls[0]}"
        
        print(f"✅ Image saved at: {image_urls[0]}")
        print("✅ IMAGE GENERATION TEST PASSED!")
        
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
        from services.pdf_maker import create_full_pdf
        
        print("Creating PDF...")
        pdf_bytes = create_full_pdf(story, image_urls)
        
        assert pdf_bytes is not None, "PDF returned None!"
        assert len(pdf_bytes) > 0, "PDF is empty!"
        
        # Save it so you can open and check it
        with open("test_output.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF created: {len(pdf_bytes)} bytes")
        print("✅ PDF saved as test_output.pdf — open it to check!")
        print("✅ PDF GENERATION TEST PASSED!")
        
    except Exception as e:
        print(f"❌ PDF GENERATION FAILED: {str(e)}")


# ── TEST 4: MONGODB ───────────────────────────────────────────
def test_mongodb():
    print("\n" + "="*50)
    print("TEST 4: MongoDB Connection")
    print("="*50)
    
    try:
        from services.db import get_db
        
        db = get_db()
        assert db is not None, "DB returned None — check your MONGODB_URI!"
        
        # Try writing and reading a test document
        db.test.insert_one({"test": "herogen_test"})
        result = db.test.find_one({"test": "herogen_test"})
        assert result is not None, "Could not read back from MongoDB!"
        
        # Clean up test document
        db.test.delete_one({"test": "herogen_test"})
        
        print("✅ MongoDB connected successfully!")
        print("✅ Write and read test passed!")
        print("✅ MONGODB TEST PASSED!")
        
    except Exception as e:
        print(f"❌ MONGODB FAILED: {str(e)}")


# ── RUN ALL TESTS ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 HEROGEN API TESTS STARTING...")
    
    # Test 1 - Story
    story = test_story_generation()
    
    # Test 2 - Images (only if story worked)
    image_urls = None
    if story:
        image_urls = test_image_generation()
    
    # Test 3 - PDF (only if both story and images worked)
    if story and image_urls:
        test_pdf_generation(story, image_urls)
    
    # Test 4 - MongoDB (independent)
    test_mongodb()
    
    print("\n" + "="*50)
    print("ALL TESTS COMPLETE!")
    print("="*50)