"""
Test T07: Documentation Implementation
Tests that all required documentation files exist and are properly formatted.
"""

import os
import re
from pathlib import Path

def test_documentation_files_exist():
    """Test that all required documentation files exist."""
    docs_dir = Path("docs")
    
    # Check that docs directory exists
    assert docs_dir.exists(), "docs/ directory should exist"
    
    # Required documentation files
    required_files = [
        "README.md",
        "docs/SETUP_GUIDE.md",
        "docs/USER_GUIDE.md", 
        "docs/API_REFERENCE.md",
        "docs/DEPLOYMENT.md"
    ]
    
    for file_path in required_files:
        assert Path(file_path).exists(), f"Required file {file_path} should exist"

def test_readme_content():
    """Test that README.md has required content."""
    readme_path = Path("README.md")
    assert readme_path.exists(), "README.md should exist"
    
    content = readme_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "## 🎯 What is Koe?",
        "## 🚀 Quick Start", 
        "## 📚 Documentation",
        "## 🔧 Development"
    ]
    
    for section in required_sections:
        assert section in content, f"README.md should contain section: {section}"

def test_setup_guide_content():
    """Test that SETUP_GUIDE.md has required content."""
    setup_path = Path("docs/SETUP_GUIDE.md")
    assert setup_path.exists(), "SETUP_GUIDE.md should exist"
    
    content = setup_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "## 🎯 Overview",
        "## 📋 Prerequisites",
        "## 🚀 Installation Steps"
    ]
    
    for section in required_sections:
        assert section in content, f"SETUP_GUIDE.md should contain section: {section}"

def test_user_guide_content():
    """Test that USER_GUIDE.md has required content."""
    user_guide_path = Path("docs/USER_GUIDE.md")
    assert user_guide_path.exists(), "USER_GUIDE.md should exist"
    
    content = user_guide_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "## 🎯 Getting Started",
        "## 🔐 Account Management",
        "## 📊 Data Import"
    ]
    
    for section in required_sections:
        assert section in content, f"USER_GUIDE.md should contain section: {section}"

def test_api_reference_content():
    """Test that API_REFERENCE.md has required content."""
    api_ref_path = Path("docs/API_REFERENCE.md")
    assert api_ref_path.exists(), "API_REFERENCE.md should exist"
    
    content = api_ref_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "## 🎯 Overview",
        "## 🔐 Authentication Endpoints",
        "## 📊 CSV Upload Endpoints"
    ]
    
    for section in required_sections:
        assert section in content, f"API_REFERENCE.md should contain section: {section}"

def test_deployment_guide_content():
    """Test that DEPLOYMENT.md has required content."""
    deployment_path = Path("docs/DEPLOYMENT.md")
    assert deployment_path.exists(), "DEPLOYMENT.md should exist"
    
    content = deployment_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "## 🎯 Overview",
        "## 🏗️ Deployment Options",
        "## 🚀 Traditional VPS Deployment"
    ]
    
    for section in required_sections:
        assert section in content, f"DEPLOYMENT.md should contain section: {section}"

def test_health_check_endpoint():
    """Test that health check endpoint exists in main.py."""
    main_path = Path("app/main.py")
    assert main_path.exists(), "app/main.py should exist"
    
    content = main_path.read_text(encoding='utf-8')
    
    # Check for health check endpoint
    assert "@app.get(\"/health\")" in content, "Health check endpoint should exist in main.py"
    assert "async def health_check():" in content, "Health check function should exist"

def test_documentation_links():
    """Test that documentation files have proper internal links."""
    docs_dir = Path("docs")
    
    # Check each markdown file for broken internal links
    for md_file in docs_dir.glob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # Skip external links
            if link_url.startswith('http'):
                continue
                
            # Check if internal link file exists
            if link_url.endswith('.md'):
                link_path = docs_dir / link_url
                assert link_path.exists(), f"Broken internal link in {md_file}: {link_url}"

if __name__ == "__main__":
    # Run all tests
    test_functions = [
        test_documentation_files_exist,
        test_readme_content,
        test_setup_guide_content,
        test_user_guide_content,
        test_api_reference_content,
        test_deployment_guide_content,
        test_health_check_endpoint,
        test_documentation_links
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}: PASSED")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__}: FAILED - {e}")
        except Exception as e:
            print(f"❌ {test_func.__name__}: ERROR - {e}")
    
    print(f"\n🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All T07 documentation tests passed!")
    else:
        print("⚠️  Some tests failed. Please review the documentation.")
